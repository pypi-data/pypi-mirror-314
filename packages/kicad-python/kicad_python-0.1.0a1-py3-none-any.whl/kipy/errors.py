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

from kipy.proto.common import ApiStatusCode

class ConnectionError(Exception):
    """Raised when a connection to KiCad cannot be established"""
    pass

class ApiError(Exception):
    def __init__(self, message: str, raw_message: str = "",
                 code: ApiStatusCode.ValueType = ApiStatusCode.AS_BAD_REQUEST):
         super().__init__(message)
         self._raw_message = raw_message
         self._code = code

    @property
    def code(self) -> ApiStatusCode.ValueType:
        return self._code

    @property
    def raw_message(self) -> str:
        return self.raw_message
