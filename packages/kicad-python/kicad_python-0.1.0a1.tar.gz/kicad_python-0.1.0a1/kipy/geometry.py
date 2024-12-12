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

from __future__ import annotations

from typing import Optional, Union
import math
from kipy.proto.common import types
from kipy.wrapper import Wrapper

class Vector2(Wrapper):
    """Wraps a kiapi.common.types.Vector2, aka VECTOR2I"""
    def __init__(self, proto: Optional[types.Vector2] = None):
        self._proto = types.Vector2()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    @classmethod
    def from_xy(cls, x_nm: int, y_nm: int):
        """Initialize Vector2 with x and y values in nanometers"""
        proto = types.Vector2()
        proto.x_nm = x_nm
        proto.y_nm = y_nm
        return cls(proto)

    @property
    def x(self) -> int:
        return self._proto.x_nm

    @x.setter
    def x(self, val: int):
        self._proto.x_nm = val

    @property
    def y(self) -> int:
        return self._proto.y_nm

    @y.setter
    def y(self, val: int):
        self._proto.y_nm = val

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __add__(self, other: Vector2) -> Vector2:
        r = Vector2(self._proto)
        r.x += other.x
        r.y += other.y
        return r

    def __sub__(self, other: Vector2) -> Vector2:
        r = Vector2(self._proto)
        r.x -= other.x
        r.y -= other.y
        return r

    def __neg__(self) -> Vector2:
        r = Vector2(self._proto)
        r.x = -r.x
        r.y = -r.y
        return r

    def __mul__(self, scalar: float) -> Vector2:
        r = Vector2(self._proto)
        r.x = int(r.x * scalar)
        r.y = int(r.y * scalar)
        return r

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

class Vector3D(Wrapper):
    """Wraps a kiapi.common.types.Vector3D"""
    def __init__(self, proto: Optional[types.Vector3D] = None):
        self._proto = types.Vector3D()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    @classmethod
    def from_xyz(cls, x_nm: float, y_nm: float, z_nm: float):
        """Initialize Vector3D with x, y, and z values in nanometers"""
        proto = types.Vector3D()
        proto.x_nm = x_nm
        proto.y_nm = y_nm
        proto.z_nm = z_nm
        return cls(proto)

    @property
    def x(self) -> float:
        return self._proto.x_nm

    @x.setter
    def x(self, val: float):
        self._proto.x_nm = val

    @property
    def y(self) -> float:
        return self._proto.y_nm

    @y.setter
    def y(self, val: float):
        self._proto.y_nm = val

    @property
    def z(self) -> float:
        return self._proto.z_nm

    @z.setter
    def z(self, val: float):
        self._proto.z_nm = val

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        if isinstance(other, Vector3D):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return NotImplemented

    def __add__(self, other: Vector3D) -> Vector3D:
        r = Vector3D(self._proto)
        r.x += other.x
        r.y += other.y
        r.z += other.z
        return r

    def __sub__(self, other: Vector3D) -> Vector3D:
        r = Vector3D(self._proto)
        r.x -= other.x
        r.y -= other.y
        r.z -= other.z
        return r

    def __neg__(self) -> Vector3D:
        r = Vector3D(self._proto)
        r.x = -r.x
        r.y = -r.y
        r.z = -r.z
        return r

    def __mul__(self, scalar: float) -> Vector3D:
        r = Vector3D(self._proto)
        r.x = r.x * scalar
        r.y = r.y * scalar
        r.z = r.z * scalar
        return r

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

class Box2:
    def __init__(
        self,
        pos_proto: Optional[types.Vector2] = None,
        size_proto: Optional[types.Vector2] = None,
    ):
        self._pos_proto = types.Vector2()
        self._size_proto = types.Vector2()

        if pos_proto is not None:
            self._pos_proto.CopyFrom(pos_proto)

        if size_proto is not None:
            self._size_proto.CopyFrom(size_proto)

    @classmethod
    def from_xywh(cls, x_nm: int, y_nm: int, w_nm: int, h_nm: int):
        pos = Vector2.from_xy(x_nm, y_nm)
        size = Vector2.from_xy(w_nm, h_nm)
        return cls(pos._proto, size._proto)

    @classmethod
    def from_pos_size(cls, pos: Vector2, size: Vector2):
        return cls(pos._proto, size._proto)

    @classmethod
    def from_proto( cls, other: types.Box2):
        return cls(other.position, other.size)

    @property
    def pos(self) -> Vector2:
        return Vector2(self._pos_proto)

    @property
    def size(self) -> Vector2:
        return Vector2(self._size_proto)

    def move(self, delta: Vector2):
        self._pos_proto.x_nm += delta.x
        self._pos_proto.y_nm += delta.y

    def merge(self, other: Union[Vector2, Box2]):
        if isinstance(other, Vector2):
            min_x = min(self.pos.x, other.x)
            min_y = min(self.pos.y, other.y)
            max_x = max(self.pos.x + self.size.x, other.x)
            max_y = max(self.pos.y + self.size.y, other.y)
        else:
            min_x = min(self.pos.x, other.pos.x)
            min_y = min(self.pos.y, other.pos.y)
            max_x = max(self.pos.x + self.size.x, other.pos.x + other.size.x)
            max_y = max(self.pos.y + self.size.y, other.pos.y + other.size.y)

        self._pos_proto.x_nm = min_x
        self._pos_proto.y_nm = min_y
        self._size_proto.x_nm = max_x - min_x
        self._size_proto.y_nm = max_y - min_y

    def inflate(self, amount: int):
        new_width = self.size.x + amount
        new_height = self.size.y + amount
        self._pos_proto.x_nm -= (new_width - self.size.x) // 2
        self._pos_proto.y_nm -= (new_height - self.size.y) // 2
        self._size_proto.x_nm = new_width
        self._size_proto.y_nm = new_height

class Angle(Wrapper):
    def __init__(self, proto: Optional[types.Angle] = None):
        self._proto = types.Angle()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"Angle({self.degrees})"

    @classmethod
    def from_degrees(cls, degrees: float):
        """Initialize Angle with a value in degrees"""
        proto = types.Angle()
        proto.value_degrees = degrees
        return cls(proto)

    @property
    def degrees(self) -> float:
        return self._proto.value_degrees

    @degrees.setter
    def degrees(self, val: float):
        self._proto.value_degrees = val

    def __eq__(self, other):
        if isinstance(other, Angle):
            return self.degrees == other.degrees
        return NotImplemented

    def __add__(self, other: Angle) -> Angle:
        return Angle.from_degrees(self.degrees + other.degrees)

    def __sub__(self, other: Angle) -> Angle:
        return Angle.from_degrees(self.degrees - other.degrees)

    def __neg__(self) -> Angle:
        return Angle.from_degrees(-self.degrees)

    def __mul__(self, scalar: float) -> Angle:
        return Angle.from_degrees(self.degrees * scalar)

    def to_radians(self) -> float:
        return math.radians(self.degrees)

class ArcStartMidEnd(Wrapper):
    def __init__(
        self,
        proto: Optional[types.ArcStartMidEnd] = None,
        proto_ref: Optional[types.ArcStartMidEnd] = None,
    ):
        self._proto = proto_ref if proto_ref is not None else types.ArcStartMidEnd()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"ArcStartMidEnd(start={self.start}, mid={self.mid}, end={self.end})"

    @property
    def start(self) -> Vector2:
        return Vector2(self._proto.start)

    @start.setter
    def start(self, val: Vector2):
        self._proto.start.CopyFrom(val._proto)

    @property
    def mid(self) -> Vector2:
        return Vector2(self._proto.mid)

    @mid.setter
    def mid(self, val: Vector2):
        self._proto.mid.CopyFrom(val._proto)

    @property
    def end(self) -> Vector2:
        return Vector2(self._proto.end)

    @end.setter
    def end(self, val: Vector2):
        self._proto.end.CopyFrom(val._proto)

    def center(self) -> Optional[Vector2]:
        """
        Calculates the center of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The center of the arc, or None if the arc is degenerate
        """
        # TODO we may want to add an API call to get KiCad to calculate this for us,
        # for situations where matching KiCad's behavior exactly is important
        return arc_center(self.start, self.mid, self.end)

    def radius(self) -> float:
        """
        Calculates the radius of the arc.  Uses a different algorithm than KiCad so may have
        slightly different results.  The KiCad API preserves the start, middle, and end points of
        the arc, so any other properties such as the center point and angles must be calculated

        :return: The radius of the arc, or 0 if the arc is degenerate
        """
        # TODO we may want to add an API call to get KiCad to calculate this for us,
        # for situations where matching KiCad's behavior exactly is important
        return arc_radius(self.start, self.mid, self.end)

    def start_angle(self) -> Optional[float]:
        return arc_start_angle(self.start, self.mid, self.end)

    def end_angle(self) -> Optional[float]:
        return arc_end_angle(self.start, self.mid, self.end)

    def bounding_box(self) -> Box2:
        """Returns the bounding box of the arc -- not calculated by KiCad; may differ from KiCad's"""
        box = Box2()
        box.merge(self.start)
        box.merge(self.end)
        box.merge(self.mid)
        return box

class PolyLineNode(Wrapper):
    def __init__(
        self,
        proto: Optional[types.PolyLineNode] = None,
        proto_ref: Optional[types.PolyLineNode] = None,
    ):
        self._proto = proto_ref if proto_ref is not None else types.PolyLineNode()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        if self.has_point:
            return f"PolyLineNode(point={self.point})"
        elif self.has_arc:
            return f"PolyLineNode(arc={self.arc})"
        return "PolyLineNode()"

    @property
    def has_point(self) -> bool:
        return self._proto.HasField("point")

    @property
    def point(self) -> Vector2:
        return Vector2(self._proto.point)

    @point.setter
    def point(self, val: Vector2):
        self._proto.point.CopyFrom(val._proto)

    @property
    def has_arc(self) -> bool:
        return self._proto.HasField("arc")

    @property
    def arc(self) -> ArcStartMidEnd:
        return ArcStartMidEnd(self._proto.arc)

    @arc.setter
    def arc(self, val: ArcStartMidEnd):
        self._proto.arc.CopyFrom(val._proto)

class PolyLine(Wrapper):
    def __init__(
        self,
        proto: Optional[types.PolyLine] = None,
        proto_ref: Optional[types.PolyLine] = None,
    ):
        self._proto = proto_ref if proto_ref is not None else types.PolyLine()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"PolyLine(nodes={self.nodes}, closed={self.closed})"

    @property
    def nodes(self) -> list[PolyLineNode]:
        return [PolyLineNode(proto_ref=node) for node in self._proto.nodes]

    @property
    def closed(self) -> bool:
        return self._proto.closed

    @closed.setter
    def closed(self, val: bool):
        self._proto.closed = val

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index: int) -> PolyLineNode:
        return self.nodes[index]

    def __setitem__(self, index: int, value: PolyLineNode):
        self._proto.nodes[index].CopyFrom(value._proto)

    def append(self, node: PolyLineNode):
        self._proto.nodes.append(node._proto)

    def insert(self, index: int, node: PolyLineNode):
        self._proto.nodes.insert(index, node._proto)

    def remove(self, node: PolyLineNode):
        self._proto.nodes.remove(node._proto)

    def clear(self):
        self._proto.ClearField("nodes")

class PolygonWithHoles(Wrapper):
    def __init__(
        self,
        proto: Optional[types.PolygonWithHoles] = None,
        proto_ref: Optional[types.PolygonWithHoles] = None,
    ):
        self._proto = proto_ref if proto_ref is not None else types.PolygonWithHoles()

        if proto is not None:
            self._proto.CopyFrom(proto)

    def __repr__(self):
        return f"PolygonWithHoles(outline={self.outline}, holes={self.holes})"

    @property
    def outline(self) -> PolyLine:
        return PolyLine(proto_ref=self._proto.outline)

    @property
    def holes(self) -> list[PolyLine]:
        return [PolyLine(proto_ref=hole) for hole in self._proto.holes]

    def add_hole(self, hole: PolyLine):
        self._proto.holes.append(hole._proto)

    def remove_hole(self, hole: PolyLine):
        self._proto.holes.remove(hole._proto)

    def bounding_box(self) -> Box2:
        if not self.outline.nodes:
            return Box2()

        min_x = int('inf')
        min_y = int('inf')
        max_x = int('-inf')
        max_y = int('-inf')

        for node in self.outline:
            if node.has_point:
                min_x = min(min_x, node.point.x)
                min_y = min(min_y, node.point.y)
                max_x = max(max_x, node.point.x)
                max_y = max(max_y, node.point.y)
            elif node.has_arc:
                box = node.arc.bounding_box()
                min_x = min(min_x, box.pos.x)
                min_y = min(min_y, box.pos.y)
                max_x = max(max_x, box.pos.x + box.size.x)
                max_y = max(max_y, box.pos.y + box.size.y)

        return Box2.from_pos_size(
            Vector2.from_xy(min_x, min_y), Vector2.from_xy(max_x - min_x, max_y - min_y)
        )

    def move(self, delta: Vector2):
        for node in self.outline:
            if node.has_point:
                node.point += delta
            elif node.has_arc:
                node.arc.start += delta
                node.arc.mid += delta
                node.arc.end += delta

        for hole in self.holes:
            for node in hole:
                if node.has_point:
                    node.point += delta
                elif node.has_arc:
                    node.arc.start += delta
                    node.arc.mid += delta
                    node.arc.end += delta

def arc_center(start: Vector2, mid: Vector2, end: Vector2) -> Optional[Vector2]:
    """
    Calculates the center of the arc.  Uses a different algorithm than KiCad so may have
    slightly different results.  The KiCad API preserves the start, middle, and end points of
    the arc, so any other properties such as the center point and angles must be calculated

    :return: The center of the arc, or None if the arc is degenerate
    """
    # TODO we may want to add an API call to get KiCad to calculate this for us,
    # for situations where matching KiCad's behavior exactly is important
    if start == end:
        return (start + mid) * 0.5

    def perpendicular_bisector(p1: Vector2, p2: Vector2):
        mid_point = (p1 + p2) * 0.5
        direction = p2 - p1
        perpendicular_direction = Vector2.from_xy(-direction.y, direction.x)
        return mid_point, perpendicular_direction

    mid1, dir1 = perpendicular_bisector(start, mid)
    mid2, dir2 = perpendicular_bisector(mid, end)

    det = dir1.x * dir2.y - dir1.y * dir2.x

    if det == 0:
        return None

    # Intersect the two perpendicular bisectors to find the center
    t = (mid2.x - mid1.x) * dir2.y - (mid2.y - mid1.y) * dir2.x / det
    center = mid1 + dir1 * t

    return center

def arc_radius(start: Vector2, mid: Vector2, end: Vector2) -> float:
    """
    Calculates the radius of the arc.  Uses a different algorithm than KiCad so may have
    slightly different results.  The KiCad API preserves the start, middle, and end points of
    the arc, so any other properties such as the center point and angles must be calculated

    :return: The radius of the arc, or 0 if the arc is degenerate
    """
    # TODO we may want to add an API call to get KiCad to calculate this for us,
    # for situations where matching KiCad's behavior exactly is important
    center = arc_center(start, mid, end)
    if center is None:
        return 0

    return (start - center).length()

def arc_start_angle(start: Vector2, mid: Vector2, end: Vector2) -> Optional[float]:
    center = arc_center(start, mid, end)
    if center is None:
        return None

    return (start - center).angle()

def arc_end_angle(start: Vector2, mid: Vector2, end: Vector2) -> Optional[float]:
    center = arc_center(start, mid, end)
    if center is None:
        return None

    angle = (end - center).angle()

    start_angle = arc_start_angle(start, mid, end)
    assert(start_angle is not None)

    if angle == start_angle:
        angle += 2 * math.pi

    while angle < start_angle:
        angle += 2 * math.pi

    return angle
