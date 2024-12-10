#
# Copyright (c) 2022-2023 Geosiris.
# SPDX-License-Identifier: Apache-2.0
#
import sys
import websocket
import asyncio

try:
    import thread
except ImportError:
    import _thread as thread

import time
from datetime import datetime

from base64 import b64encode

from etpproto.connection import ETPConnection, ConnectionType
from etpproto.client_info import ClientInfo
from etpproto.messages import Message

import hdf5extractor.etp.server_protocols

from hdf5extractor.etp.requester import request_session

import pprint


def basic_auth_header(username, password):
    assert ":" not in username
    user_pass = f"{username}:{password}"
    basic_credentials = b64encode(user_pass.encode()).decode()
    print("Credentials : 'Basic " + basic_credentials + "'")
    return "authorization: Basic " + basic_credentials


async def wait_for_response(
    conn: ETPConnection, websocket_manager, msg_id: int, timeout: int = 5
):
    delta_t = 0.01
    begining = datetime.now()
    while (datetime.now() - begining).seconds < timeout:
        if msg_id in websocket_manager.recieved_msg_dict and (
            isinstance(websocket_manager.recieved_msg_dict[msg_id], Message)
            or (
                isinstance(websocket_manager.recieved_msg_dict[msg_id], list)
                and websocket_manager.recieved_msg_dict[msg_id][
                    -1
                ].is_final_msg()
            )
        ):
            return websocket_manager.recieved_msg_dict[msg_id]
        await asyncio.sleep(delta_t)
    return None


class WebSocketManager:
    def __init__(
        self,
        uri: str,
        username: str = None,
        password: str = None,
        token: str = None,
    ):
        self.recieved_msg_dict = {}
        if token:
            print("auth bearer : \n" + "authorization: Bearer " + token)
            self.ws = websocket.WebSocketApp(
                uri,
                subprotocols=[ETPConnection.SUB_PROTOCOL],
                header=["authorization: Bearer " + token],
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )
        elif username and password:
            self.ws = websocket.WebSocketApp(
                uri,
                subprotocols=[ETPConnection.SUB_PROTOCOL],
                header=[basic_auth_header(username, password)],
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )
        else:
            self.ws = websocket.WebSocketApp(
                uri,
                subprotocols=[ETPConnection.SUB_PROTOCOL],
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )

        self.etp_connection = ETPConnection(
            connection_type=ConnectionType.CLIENT,
            client_info=ClientInfo(
                ip=uri,
                endpoint_capabilities={
                    "MaxWebSocketFramePayloadSize": 40000,
                    "MaxWebSocketMessagePayloadSize": 40000,
                },
            ),
        )
        self.recieved = {}

        def run(*args):

            self.ws.run_forever()
            # print("thread terminating...")
            self.etp_connection.is_connected = False

        thread.start_new_thread(run, ())

    def is_connected(self):
        # print(self.etp_connection)
        return self.etp_connection.is_connected

    def on_message(self, ws, message):
        print("ON_MSG : ")
        # print("ON_MSG : ", message)

        async def handle_msg(
            conn: ETPConnection, websocket_manager, msg: bytes
        ):
            try:
                # print("##> before recieved " )
                recieved = Message.decode_binary_message(
                    message,
                    dict_map_pro_to_class=ETPConnection.generic_transition_table,
                )
                print("\n##> recieved header : ", recieved.header, "\n\n")
                # if (
                #     recieved.header.protocol == 0
                #     or type(recieved.body) != bytes
                # ):
                # print("ERR : ", recieved.body)
                print("##> body type : ", type(recieved.body))
                # print("##> body content : ", recieved.body)

                # msg = await conn.decode_partial_message(recieved)

                # print("##> msg " )
                if msg:
                    async for b_msg in conn.handle_bytes_generator(msg):
                        # print(b_msg)
                        # print("##> bmsg " )
                        if (
                            b_msg.headers.correlation_id
                            not in websocket_manager.recieved_msg_dict[
                                b_msg.headers.correlation_id
                            ]
                        ):
                            websocket_manager.recieved_msg_dict[
                                b_msg.headers.correlation_id
                            ] = [0]
                        websocket_manager.recieved_msg_dict[
                            b_msg.headers.correlation_id
                        ].append(b_msg)
                    # print("MSG : " + str(type(msg.body)))

                # async for b_msg in conn.handle_bytes_generator(msg):
                #     # print(b_msg)
                #     pass
                # # print("MSG : " + str(type(msg.body)))
            except Exception as e:
                print(e)

        asyncio.run(handle_msg(self.etp_connection, self, message))

    def on_error(self, ws, error):
        print("ON_ERR")
        try:
            print(error)
        except Exception as e:
            print(e)

    def on_close(self, ws, a, b):
        # print("ON_CLOSE")
        try:
            print("### closed ###", a, "\n", b)
            print("Bye bye")
            sys.stdout.flush()
            self.etp_connection.is_connected = False
            sys.exit(1)
        except Exception as e:
            print(e)

    def on_open(self, ws):
        # print("OPENING")
        try:
            answer = asyncio.run(self.send_and_wait(request_session(), 4.0))
            print("CONNECTED : ", answer)

        except Exception as e:
            print(e)

    async def send_and_wait(self, req, timeout: int = 5):
        print("SENDING " + str(req))
        msg_id = -1
        async for (
            msg_id,
            msg_to_send,
        ) in self.etp_connection.send_msg_and_error_generator(
            Message.get_object_message(etp_object=req), None
        ):
            self.ws.send(msg_to_send, websocket.ABNF.OPCODE_BINARY)
            # print("Msg sent... ", msg_to_send)
        # return wait_for_response(conn=self.etp_connection, msg_id = msg_id, timeout=timeout)
        result = await wait_for_response(
            conn=self.etp_connection,
            websocket_manager=self,
            msg_id=msg_id,
            timeout=timeout,
        )
        # print("Answer : \n", result)
        print("Answer recieved")
        return result

    async def send_no_wait(self, req, timeout: int = 5):
        print("SENDING NW" + str(req))
        msg_id_list = []
        msg_id = -1
        async for (
            msg_id,
            msg_to_send,
        ) in self.etp_connection.send_msg_and_error_generator(
            Message.get_object_message(etp_object=req), None
        ):
            self.ws.send(msg_to_send, websocket.ABNF.OPCODE_BINARY)
            msg_id_list.append(msg_id)

        return msg_id_list
