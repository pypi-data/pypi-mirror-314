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

def from_mm(value_mm: float) -> int:
    """
    KiCad uses several internal unit systems, but for the IPC API, all distance units are defined as
    64-bit nanometers
    :param value_mm: a quantity in millimeters
    :return: the quantity in KiCad API units
    """
    return int(value_mm * 1_000_000)

def to_mm(value_nm: int) -> float:
    """
    Converts a KiCad API length/distance value (in nanometers) to millimeters
    """
    return float(value_nm) / 1_000_000