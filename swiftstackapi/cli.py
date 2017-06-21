import argparse
import sys
from datetime import datetime, timedelta

import logging

from swiftstackapi import api

DTF_ISO8601 = "%Y-%m-%dT%H:%M:%S"


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--controller",
        help="Hostname of controller",
        type=str,
        dest="controller_host"
    )
    parser.add_argument(
        "-c",
        "--cluster",
        help="ID of cluster on controller",
        type=int,
        dest="cluster_id"
    )
    parser.add_argument(
        "-u",
        "--user",
        help="SwiftStack API User",
        type=str,
        dest="ssapi_user"
    )
    parser.add_argument(
        "-k",
        "--key",
        help="SwiftStack API Key",
        type=str,
        dest="ssapi_key"
    )
    parser.add_argument(
        "-s",
        "--start",
        help="Start timestamp for utilization in the format "
             "yyyy-mm-ddThh:mm:ss[+/-NNNN] (where NNNN is the timezone offset); "
             "e.g.: 2013-08-29T19:24:44-0700",
        type=timestamp,
        dest="start_datetime"
    )
    parser.add_argument(
        "-e",
        "--end",
        help="End timestamp for utilization in the format "
             "yyyy-mm-ddThh:mm:ss[+/-NNNN] (where NNNN is the timezone offset); "
             "e.g.: 2013-08-29T19:24:44-0700",
        type=timestamp,
        dest="end_datetime"
    )
    parser.add_argument(
        "-p",
        "--policy",
        help="Storage Policy in cluster",
        type=str,
        dest="storage_policy"
    )
    parsed = parser.parse_args(args)
    return parsed


def setup_logging():
    log_level = logging.DEBUG
    log_format = "%(asctime)s [%(threadName)s.%(name)s] " \
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
    except:
        raise






