#
# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
#
import requests
import json

from etpproto.connection import ETPConnection

from hdf5extractor.etp.websocket_manager import WebSocketManager


def print_capabilities(serv_uri: str):
    server_caps_list_txt = requests.get(
        "http://"
        + serv_uri
        + ".well-known/etp-server-capabilities?GetVersions=true"
    ).text
    print(
        f"Server versions : {server_caps_list_txt} and this client version is {ETPConnection.SUB_PROTOCOL}"
    )

    print("======> SERVER CAPS :")
    server_caps_txt = requests.get(
        "http://"
        + serv_uri
        + ".well-known/etp-server-capabilities?GetVersion="
        + ETPConnection.SUB_PROTOCOL
    ).text
    print(json.dumps(json.loads(server_caps_txt), sort_keys=True, indent=4))
    print("<====== SERVER CAPS\n")


async def client_get_xml(
    serv_uri: str = None,
    serv_get_token_uri: str = None,
    username: str = None,
    password: str = None,
    token: str = None,
    uris: list = [],
    print_caps: bool = False,
):
    if not serv_uri.endswith("/"):
        serv_uri += "/"

    if print_caps:
        print_capabilities(serv_uri)

    wsm = WebSocketManager(
        "ws://" + serv_uri, username=username, password=password, token=token
    )

    return ["coucou"]
