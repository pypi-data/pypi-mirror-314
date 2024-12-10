#
# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
#
import argparse
import pprint

import os
import asyncio
from hdf5extractor.etp.utils import client_get_xml, print_capabilities


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        required=True,
        type=str,
        help="[Required] ETP server host (e.g. rdms.mycompagny.com:8080/etp)",
    )
    parser.add_argument(
        "--username",
        "-u",
        type=str,
        help="[Required] Username for the connexion",
    )
    parser.add_argument(
        "--password",
        "-p",
        type=str,
        help="[Required] Password for the connexion",
    )
    parser.add_argument(
        "--token",
        "-t",
        type=str,
        help="[Required] Token for the connexion",
    )
    parser.add_argument(
        "--uris",
        "-i",
        nargs="+",
        type=str,
        help="[Required] Password for the connexion",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="extracted",
        type=str,
        help="H5 output folder",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force the overwrite the output files if allready exists",
    )
    parser.add_argument(
        "--show-capabilities",
        action="store_true",
        help="The client print the recieved server capabilities",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    result = asyncio.run(
        client_get_xml(
            serv_uri=args.host,
            serv_get_token_uri=None,
            username=args.username,
            password=args.password,
            token=args.token,
            uris=args.uris,
            print_caps=args.show_capabilities,
        )
    )
    print(f"Result {result}")
    try:
        os.makedirs(args.output)
    except OSError:
        pass
