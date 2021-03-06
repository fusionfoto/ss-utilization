# Copyright 2018 SwiftStack, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import logging
import os
import sys
from datetime import datetime, timedelta

import StringIO

from swiftstackapi import api, output, version


OUTPUT_FIELD_MAP = {
    'a': 'account',
    's': 'start',
    'e': 'end',
    'p': 'policy',
    'c': 'container_count',
    'o': 'object_count',
    'b': 'bytes_used'
}

OUTPUT_FIELD_HELPTXT = "output format columns to include: \n" + "".join(
    ['{0}: {1},\n'.format(k, v) for k,v in OUTPUT_FIELD_MAP.iteritems()]
)


def timestamp(stamp):
    """
    returns datetime object for given ISO 8601 timestamp string

    :param stamp: timestamp in
    :return: datetime object for time stamp (timezone naive, but adjusted to UTC)
    """
    dt = datetime.strptime(stamp[0:19], api.DTF_ISO8601)

    if len(stamp) > 24:
        raise ValueError("Malformed timezone offset")
    elif len(stamp) > 19:
        # process additional tzoffset
        if stamp[19] == '+':
            dt += timedelta(hours=int(stamp[20:22]), minutes=int(stamp[23:]))
        elif stamp[19] == '-':
            dt -= timedelta(hours=int(stamp[20:22]), minutes=int(stamp[23:]))
        else:
            # not valid tzoffset
            raise ValueError("Not valid timezone offset")

    return dt


# from https://stackoverflow.com/questions/10551117/setting-options-from-environment-variables-when-using-argparse
# see also https://docs.python.org/2.7/library/argparse.html#argparse.Action
class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required,
                                         **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_args(args):
    parser = argparse.ArgumentParser()
    required_parser = parser.add_argument_group('required arguments')
    required_parser.add_argument(
        "-m",
        "--controller",
        help="Hostname of controller (or env[SSAPI_CONTROLLER])",
        type=str,
        dest="controller_host",
        envvar='SSAPI_CONTROLLER',
        action=EnvDefault,
        required=True
    )
    required_parser.add_argument(
        "-c",
        "--cluster",
        help="ID of cluster on controller (or env[SSAPI_CLUSTER])",
        type=int,
        dest="cluster_id",
        envvar='SSAPI_CLUSTER',
        action=EnvDefault,
        required=True
    )
    required_parser.add_argument(
        "-u",
        "--user",
        help="SwiftStack API User (or env[SSAPI_USER])",
        type=str,
        dest="ssapi_user",
        envvar='SSAPI_USER',
        action=EnvDefault,
        required=True
    )
    required_parser.add_argument(
        "-k",
        "--key",
        help="SwiftStack API Key (or env[SSAPI_KEY])",
        type=str,
        dest="ssapi_key",
        envvar='SSAPI_KEY',
        action=EnvDefault,
        required=True
    )
    required_parser.add_argument(
        "-s",
        "--start",
        help="Start timestamp for utilization in the format "
             "yyyy-mm-ddThh:mm:ss[+/-NNNN] (where NNNN is the timezone offset); "
             "e.g.: 2013-08-29T19:24:44-0700",
        type=timestamp,
        dest="start_datetime",
        required=True
    )
    required_parser.add_argument(
        "-e",
        "--end",
        help="End timestamp for utilization in the format "
             "yyyy-mm-ddThh:mm:ss[+/-NNNN] (where NNNN is the timezone offset); "
             "e.g.: 2013-08-29T19:24:44-0700",
        type=timestamp,
        dest="end_datetime",
        required=True
    )
    required_parser.add_argument(
        "-p",
        "--policy",
        help="Storage policies in cluster (can specify multiple, e.g. '-p 1 2')",
        type=int,
        nargs='+',
        dest="storage_policy",
        required=True
    )
    parser.add_argument("-o", "--output", help="file to output utilization data; "
                                               "if not specified, output will be printed",
                        type=str, dest="output_file", default=None)
    parser.add_argument("-f", "--fields", help=OUTPUT_FIELD_HELPTXT,
                        nargs="+", choices=OUTPUT_FIELD_MAP.keys(),
                        dest="output_fields")
    parser.add_argument('--raw', help="output raw hourly utilization hours; don't summarize",
                        action='store_true',
                        dest="raw_output")
    parser.add_argument('--accountonly', help="output account only, not utilization hours; not summarize",
                        action='store_true',
                        dest="account_output")
    parser.add_argument('--cert', help="path to controller SSL cert (e.g. if self-signed)",
                        type=str, dest="controller_cert_path", default=None)
    parser.add_argument('-V', '--version', help='print version and exit',
                        action='version',
                        version='%(prog)s ' + version.version)
    parser.add_argument('-v', '--verbose', help='verbose log messages',
                        action='count')
    parser.add_argument('-q', '--quiet', help='disable all logging (overrides verbose)',
                        action='store_true')
    parsed = parser.parse_args(args)
    return parsed


def setup_logging(name=None, level=logging.INFO):
    log_level = level
    log_format = "%(asctime)s [%(name)s] " \
                 "%(levelname)s: %(message)s"
    logging.basicConfig(level=log_level, format=log_format)

    if not name:
        logger = logging.getLogger(__name__)
    else:
        logger = logging.getLogger(name)
    return logger


def map_fields(output_fields):
    mapped = []
    for field_key in output_fields:
        mapped.append(OUTPUT_FIELD_MAP[field_key])
    return mapped


def main(args=None):
    if not args:
        args = sys.argv[1:]

    config = parse_args(args)

    if config.verbose:
        if config.verbose > 1:
            # no lower logging level, but lets handle it anyway and just set it to DEBUG
            logger = setup_logging(os.path.basename(sys.argv[0]), logging.DEBUG)
        else:
            logger = setup_logging(os.path.basename(sys.argv[0]), logging.DEBUG)
    else:
        logger = setup_logging(os.path.basename(sys.argv[0]), logging.INFO)

    if config.quiet:
        logging.disable(logging.CRITICAL)

    logger.info("Starting SS-Utilization o-matic...")
    logger.debug("Got configuration:")
    for item in config.__dict__:
        logger.debug("%s: %s " % (item, config.__dict__[item]))

    capture_fields = None
    if config.output_fields:
        capture_fields = map_fields(config.output_fields)

    try:
        ssapiclient = api.SwiftStackAPIClient(controller=config.controller_host,
                                              apiuser=config.ssapi_user,
                                              apikey=config.ssapi_key,
                                              controller_cert=config.controller_cert_path)
        # TODO: all this logic needs to be in some unit-testable function!!
        util_output = {}
        for p in config.storage_policy:
            util_accts = ssapiclient.get_accounts(cluster=config.cluster_id,
                                                  start_time=config.start_datetime,
                                                  end_time=config.end_datetime,
                                                  policy=p)
            logger.info("Got %d accounts in utilization period for policy %s" %
                        (len(util_accts), p))

            if len(util_accts) > 0:
                if config.account_output is False:
                    for account in util_accts:
                        if account not in util_output:
                            util_output[account] = {}
                        records = ssapiclient.get_acct_util(cluster=config.cluster_id,
                                                            account=account,
                                                            start_time=config.start_datetime,
                                                            end_time=config.end_datetime,
                                                            policy=p)
                        util_output[account][p] = records
                        logger.info("Got %d records for account %s in policy %s" % (len(records),
                                                                                    account,
                                                                                    p))
            else:
                logger.warn("No accounts found in utilization period for policy %s" % p)

        if util_output:
            if config.output_file:
                with open(config.output_file, 'wb') as f:
                    if config.account_output:
                        capture_fields = ['account']
                        writer = output.CsvUtilizationWriter(util_accts, f, output_fields=capture_fields)
                        writer.write_accountonly_csv()
                    else:
                        writer = output.CsvUtilizationWriter(util_output, f, output_fields=capture_fields)
                        if config.raw_output:
                            writer.write_raw_csv()
                        else:
                            writer.write_summary_csv()
                    logger.info("Wrote %s" % config.output_file)
            else:
                fake_csvfile = StringIO.StringIO()
                if config.account_output:
                    capture_fields = ['account']
                    writer = output.CsvUtilizationWriter(util_accts, fake_csvfile,
                                                         output_fields=capture_fields)
                    writer.write_accountonly_csv()
                else:
                    writer = output.CsvUtilizationWriter(util_output, fake_csvfile,
                                                         output_fields=capture_fields)
                    if config.raw_output:
                        writer.write_raw_csv()
                    else:
                        writer.write_summary_csv()
                print fake_csvfile.getvalue()
                fake_csvfile.close()
        else:
            logger.error("No utilization data found in specified time range!")

    except:
        raise

    logger.info("Utilization Run Complete")
