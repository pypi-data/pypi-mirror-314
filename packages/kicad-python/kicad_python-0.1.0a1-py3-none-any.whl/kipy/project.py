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

from typing import List, Union, overload

from kipy.client import KiCadClient
from kipy.project_types import NetClass
from kipy.proto.common.types import DocumentSpecifier
from kipy.proto.common.commands import project_commands_pb2


class Project:
    def __init__(self, kicad: KiCadClient, document: DocumentSpecifier):
        self._kicad = kicad
        self._doc = document

    @property
    def document(self) -> DocumentSpecifier:
        return self._doc

    @property
    def name(self) -> str:
        """Returns the name of the project"""
        return self._doc.project.name

    @property
    def path(self) -> str:
        return self._doc.project.path

    def get_net_classes(self) -> List[NetClass]:
        command = project_commands_pb2.GetNetClasses()
        response = self._kicad.send(command, project_commands_pb2.NetClassesResponse)
        return [NetClass(p) for p in response.net_classes]

    @overload
    def expand_text_variables(self, text: str) -> str:
        ...

    @overload
    def expand_text_variables(self, text: List[str]) -> List[str]:
        ...

    def expand_text_variables(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        command = project_commands_pb2.ExpandTextVariables()
        command.document.CopyFrom(self._doc)
        if isinstance(text, list):
            command.text.extend(text)
        else:
            command.text.append(text)
        response = self._kicad.send(command, project_commands_pb2.ExpandTextVariablesResponse)
        return (
            [text for text in response.text]
            if isinstance(text, list)
            else response.text[0]
            if len(response.text) > 0
            else ""
        )
