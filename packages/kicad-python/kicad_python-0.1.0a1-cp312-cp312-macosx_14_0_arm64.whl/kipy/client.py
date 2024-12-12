# This program source code file is part of KiCad, a free EDA CAD application.
#
# Copyright (C) 2024 KiCad Developers
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import pynng
from typing import TypeVar

from google.protobuf.message import Message

from kipy.errors import ApiError, ConnectionError
from kipy.proto.common import ApiRequest, ApiResponse, ApiStatusCode

class KiCadClient:
    def __init__(self, socket_path: str, client_name: str, kicad_token: str, timeout_ms: int):
        self._socket_path = socket_path
        self._client_name = client_name
        self._kicad_token = kicad_token
        self._timeout_ms = timeout_ms
        self._connected = False

    def _connect(self):
        if self._connected:
            self._conn.close()

        try:
            self._conn = pynng.Req0(dial=self._socket_path, block_on_dial=True,
                                    send_timeout=self._timeout_ms, recv_timeout=self._timeout_ms)
            self._connected = True
        except pynng.exceptions.NNGException as e:
            self._connected = False
            raise ConnectionError(f"Failed to connect to KiCad: {e}") from None

    @property
    def connected(self):
        return self._connected

    R = TypeVar('R', bound=Message)

    def send(self, command: Message, response_type: type[R]) -> R:
        if not self._connected:
            self._connect()

        envelope = ApiRequest()
        envelope.message.Pack(command)
        envelope.header.kicad_token = self._kicad_token
        envelope.header.client_name = self._client_name

        try:
            self._conn.send(envelope.SerializeToString())
        except pynng.exceptions.NNGException as e:
            raise ConnectionError(f"Failed to send command to KiCad: {e}") from None

        try:
            reply_data = self._conn.recv_msg()
        except pynng.exceptions.NNGException as e:
            raise ConnectionError(f"Error receiving reply from KiCad: {e}") from None

        reply = ApiResponse()
        reply.ParseFromString(reply_data.bytes)

        if reply.status.status == ApiStatusCode.AS_OK:
            response = response_type()

            if not reply.message.Unpack(response):
                raise ApiError(
                    f"Failed to unpack {response_type.__name__} from the response to {type(command).__name__}"
                )

            if self._kicad_token == "":
                self._kicad_token = reply.header.kicad_token

            return response
        else:
            raise ApiError(f"KiCad returned error: {reply.status.error_message}",
                           raw_message=reply.status.error_message, code=reply.status.status)
