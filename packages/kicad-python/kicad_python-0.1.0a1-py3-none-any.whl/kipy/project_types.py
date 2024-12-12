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

from kipy.proto.common.types import project_settings_pb2
from kipy.wrapper import Wrapper


class NetClass(Wrapper):
    def __init__(self, proto: project_settings_pb2.NetClass = project_settings_pb2.NetClass()):
        self._proto = proto

    @property
    def name(self) -> str:
        return self._proto.name
