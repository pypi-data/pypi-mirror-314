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

import os
import platform
import random
import string
from tempfile import gettempdir
from typing import Sequence, Union
from google.protobuf.empty_pb2 import Empty

from kipy.board import Board
from kipy.client import KiCadClient, ApiError
from kipy.common_types import Text, TextBox, CompoundShape
from kipy.geometry import Box2
from kipy.project import Project
from kipy.proto.common import commands
from kipy.proto.common.types import base_types_pb2, DocumentType, DocumentSpecifier
from kipy.proto.common.commands import base_commands_pb2


def default_socket_path() -> str:
    path = os.environ.get('KICAD_API_SOCKET')
    if path is not None:
        return path
    return f'ipc://{gettempdir()}\\kicad\\api.sock' if platform.system() == 'Windows' else 'ipc:///tmp/kicad/api.sock'

def random_client_name() -> str:
    return 'anonymous-'+''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def default_kicad_token() -> str:
    token = os.environ.get('KICAD_API_TOKEN')
    if token is not None:
        return token
    return ""

class KiCad:
    def __init__(self, socket_path: str=default_socket_path(),
                 client_name: str=random_client_name(),
                 kicad_token: str=default_kicad_token(),
                 timeout_ms: int=2000):
        """Creates a connection to a running KiCad instance

        :param socket_path: The path to the IPC API socket (leave default to read from the
            KICAD_API_SOCKET environment variable, which will be set automatically by KiCad when
            launching API plugins, or to use the default platform-dependent socket path if the
            environment variable is not set).
        :param client_name: A unique name identifying this plugin instance.  Leave default to
            generate a random client name.
        :param kicad_token: A token that can be provided to the client to uniquely identify a
            KiCad instance.  Leave default to read from the KICAD_API_TOKEN environment variable.
        :param timeout_ms: The maximum time to wait for a response from KiCad, in milliseconds
        """
        self._client = KiCadClient(socket_path, client_name, kicad_token, timeout_ms)

    @staticmethod
    def from_client(client: KiCadClient):
        """Creates a KiCad object from an existing KiCad client"""
        k = KiCad.__new__(KiCad)
        k._client = client
        return k

    def get_version(self):
        """Returns the KiCad version as a string, including any package-specific info"""
        response = self._client.send(commands.GetVersion(), commands.GetVersionResponse)
        return response.version.full_version

    def ping(self):
        self._client.send(commands.Ping(), Empty)

    def run_action(self, action: str):
        """Runs a KiCad tool action, if it is available

        WARNING: This is an unstable API and is not intended for use other
        than by API developers. KiCad does not guarantee the stability of
        action names, and running actions may have unintended side effects.
        :param action: the name of a KiCad TOOL_ACTION
        :return: a value from the KIAPI.COMMON.COMMANDS.RUN_ACTION_STATUS enum
        """
        return self._client.send(commands.RunAction(), commands.RunActionResponse)

    def get_open_documents(self, doc_type: DocumentType.ValueType) -> Sequence[DocumentSpecifier]:
        """Retrieves a list of open documents matching the given type"""
        command = commands.GetOpenDocuments()
        command.type = doc_type
        response = self._client.send(command, commands.GetOpenDocumentsResponse)
        return response.documents

    def get_project(self, document: DocumentSpecifier) -> Project:
        """Returns a Project object for the given document"""
        return Project(self._client, document)

    def get_board(self) -> Board:
        """Retrieves a reference to the PCB open in KiCad, if one exists"""
        docs = self.get_open_documents(DocumentType.DOCTYPE_PCB)
        if len(docs) == 0:
            raise ApiError("Expected to be able to retrieve at least one board")
        return Board(self._client, docs[0])

    # Utility functions

    def get_text_extents(self, text: Text) -> Box2:
        cmd = base_commands_pb2.GetTextExtents()
        cmd.text.CopyFrom(text.proto)
        reply = self._client.send(cmd, base_types_pb2.Box2)
        return Box2.from_proto(reply)

    def get_text_as_shapes(
        self, texts: Union[Text, TextBox, Sequence[Union[Text, TextBox]]]
    ) -> list[CompoundShape]:
        if isinstance(texts, Text) or isinstance(texts, TextBox):
            texts = [texts]

        cmd = base_commands_pb2.GetTextAsShapes()
        for t in texts:
            inner = base_commands_pb2.TextOrTextBox()
            if isinstance(t, Text):
                inner.text.CopyFrom(t.proto)
            else:
                inner.textbox.CopyFrom(t.proto)
            cmd.text.append(inner)

        reply = self._client.send(cmd, base_commands_pb2.GetTextAsShapesResponse)

        return [CompoundShape(entry.shapes) for entry in reply.text_with_shapes]
