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

from abc import ABC, abstractmethod

from google.protobuf.message import Message
from kipy.proto.common.types.base_types_pb2 import KIID

class Wrapper(ABC):
    def __init__(self, proto: Message):
        pass

    @property
    def proto(self):
        return self.__dict__['_proto']
    
class Item(Wrapper):
    @property
    @abstractmethod
    def id(self) -> KIID:
        return KIID()
