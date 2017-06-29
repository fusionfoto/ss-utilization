import argparse
import logging
import sys
from datetime import datetime, timedelta

from swiftstackapi import api, output
from swiftstackapi.api import DTF_ISO8601


def timestamp(stamp):
    """
    returns datetime object for given ISO 8601 timestamp string

    :param stamp: timestamp in
    :return: datetime object for time stamp (timezone naive, but adjusted to UTC)
    """
    dt = datetime.strptime(stamp[0:19], DTF_ISO8601)

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


def parse_args(args):
    # TODO version flag?
    parser = argparse.ArgumentParser()
    required_parser = parser.add_argument_group('required arguments')
    required_parser.add_argument(
        "-m",
        "--controller",
        help="Hostname of controller",
        type=str,
        dest="controller_host",
        required=True
    )
    required_parser.add_argument(
        "-c",
        "--cluster",
        help="ID of cluster on controller",
        type=int,
        dest="cluster_id",
        required=True
    )
    required_parser.add_argument(
        "-u",
        "--user",
        help="SwiftStack API User",
        type=str,
        dest="ssapi_user",
        required=True
    )
    required_parser.add_argument(
        "-k",
        "--key",
        help="SwiftStack API Key",
        type=str,
        dest="ssapi_key",
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
        help="Storage Policy in cluster",
        type=int,
        dest="storage_policy",
        required=True
    )
    required_parser.add_argument(
        "-o",
        "--output",
        help="file to output utilization data",
        type=str,
        dest="output_file",
        required=True
    )
    parsed = parser.parse_args(args)
    return parsed


def setup_logging():
    log_level = logging.DEBUG
    log_format = "%(asctime)s [%(name)s] " \
                 "%(levelname)s: %(message)s"
    logging.basicConfig(level=log_level, format=log_format)


def main(args=None):
    if not args:
        args = sys.argv[1:]

    config = parse_args(args)

    setup_logging()

    logging.info("Starting SS-Utilization o-matic...")
    logging.debug("Got configuration:")
    for item in config.__dict__:
        logging.debug("%s: %s " % (item, config.__dict__[item]))

    try:
        ssapiclient = api.SwiftStackAPIClient(controller=config.controller_host,
                                              apiuser=config.ssapi_user,
                                              apikey=config.ssapi_key)

        util_accts = ssapiclient.get_accounts(cluster=config.cluster_id,
                                              start_time=config.start_datetime,
                                              end_time=config.end_datetime,
                                              policy=config.storage_policy)
        util_output = {}
        for account in util_accts:
            util_output[account] = ssapiclient.get_acct_util(
                cluster=config.cluster_id,
                account=account,
                start_time=config.start_datetime,
                end_time=config.end_datetime,
                policy=config.storage_policy)

        with open(config.output_file, 'wb') as f:
            writer = output.CsvUtilizationWriter(util_output, f)
            writer.write_csv()

    except:
        raise
