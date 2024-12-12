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

from time import sleep
from typing import List, Dict, Union, Iterable, Optional, Sequence, cast, overload
from google.protobuf.empty_pb2 import Empty

from kipy.board_types import (
    ArcTrack,
    BoardItem,
    BoardText,
    BoardTextBox,
    Dimension,
    FootprintInstance,
    Net,
    Pad,
    BoardShape,
    Track,
    Via,
    Zone,
    to_concrete_board_shape,
    to_concrete_dimension,
    unwrap
)
from kipy.client import ApiError, KiCadClient
from kipy.common_types import Commit, TitleBlockInfo, TextAttributes
from kipy.geometry import Box2, PolygonWithHoles, Vector2
from kipy.project import Project
from kipy.proto.board import board_types_pb2
from kipy.proto.common.commands import editor_commands_pb2, project_commands_pb2
from kipy.proto.common.envelope_pb2 import ApiStatusCode
from kipy.util import pack_any
from kipy.wrapper import Item, Wrapper

from kipy.proto.common.commands import Ping
from kipy.proto.common.types import DocumentSpecifier, KIID, KiCadObjectType, base_types_pb2
from kipy.proto.common.commands.editor_commands_pb2 import (
    BeginCommit, BeginCommitResponse, CommitAction,
    EndCommit, EndCommitResponse,
    CreateItems, CreateItemsResponse,
    UpdateItems, UpdateItemsResponse,
    GetItems, GetItemsResponse,
    DeleteItems, DeleteItemsResponse,
    HitTest, HitTestResponse, HitTestResult
)
from kipy.proto.board import board_pb2
from kipy.proto.board import board_commands_pb2

# Re-exported protobuf enum types
from kipy.proto.board.board_pb2 import (    # noqa
    BoardLayerClass
)
from kipy.proto.board.board_types_pb2 import ( #noqa
    BoardLayer
)

class BoardLayerGraphicsDefaults(Wrapper):
    """Wraps a kiapi.board.types.BoardLayerGraphicsDefaults object"""
    def __init__(self, proto: Optional[board_pb2.BoardLayerGraphicsDefaults] = None):
        self._proto = board_pb2.BoardLayerGraphicsDefaults()

        if proto is not None:
            self._proto.CopyFrom(proto)

    @property
    def text(self) -> TextAttributes:
        return TextAttributes(self._proto.text)

class Board:
    def __init__(self, kicad: KiCadClient, document: DocumentSpecifier):
        self._kicad = kicad
        self._doc = document

    @property
    def client(self) -> KiCadClient:
        return self._kicad

    @property
    def document(self) -> DocumentSpecifier:
        return self._doc

    def project(self) -> Project:
        return Project(self._kicad, self._doc)

    @property
    def name(self) -> str:
        """Returns the file name of the board"""
        return self._doc.board_filename

    def save(self):
        pass

    def save_as(self, filename: str):
        pass

    def begin_commit(self) -> Commit:
        command = BeginCommit()
        return Commit(self._kicad.send(command, BeginCommitResponse).id)

    def push_commit(self, commit: Commit, message: str = ""):
        command = EndCommit()
        command.id.CopyFrom(commit.id)
        command.action = CommitAction.CMA_COMMIT
        command.message = message
        self._kicad.send(command, EndCommitResponse)

    def drop_commit(self, commit: Commit):
        command = EndCommit()
        command.id.CopyFrom(commit.id)
        command.action = CommitAction.CMA_DROP
        self._kicad.send(command, EndCommitResponse)

    def create_items(self, items: Union[Wrapper, Iterable[Wrapper]]) -> List[Wrapper]:
        command = CreateItems()
        command.header.document.CopyFrom(self._doc)

        if isinstance(items, Wrapper):
            command.items.append(pack_any(items.proto))
        else:
            command.items.extend([pack_any(i.proto) for i in items])

        return [
            unwrap(result.item)
            for result in self._kicad.send(command, CreateItemsResponse).created_items
        ]

    def get_items(
        self, types: Union[KiCadObjectType.ValueType, Sequence[KiCadObjectType.ValueType]]
    ) -> Sequence[Wrapper]:
        """Retrieves items from the board, optionally filtering to a single or set of types"""
        command = GetItems()
        command.header.document.CopyFrom(self._doc)

        if isinstance(types, int):
            command.types.append(types)
        else:
            command.types.extend(types)

        return [unwrap(item) for item in self._kicad.send(command, GetItemsResponse).items]

    def get_tracks(self) -> Sequence[Union[Track, ArcTrack]]:
        return [
            cast(Track, item) if isinstance(item, Track) else cast(ArcTrack, item)
            for item in self.get_items(
                types=[KiCadObjectType.KOT_PCB_TRACE, KiCadObjectType.KOT_PCB_ARC]
            )
        ]

    def get_vias(self) -> Sequence[Via]:
        return [cast(Via, item) for item in self.get_items(types=[KiCadObjectType.KOT_PCB_VIA])]

    def get_pads(self) -> Sequence[Pad]:
        return [cast(Pad, item) for item in self.get_items(types=[KiCadObjectType.KOT_PCB_PAD])]

    def get_footprints(self) -> Sequence[FootprintInstance]:
        return [
            cast(FootprintInstance, item)
            for item in self.get_items(types=[KiCadObjectType.KOT_PCB_FOOTPRINT])
        ]

    def get_shapes(self) -> Sequence[BoardShape]:
        """Retrieves all graphic shapes (not including tracks or text) on the board"""
        return [
            item
            for item in (
                to_concrete_board_shape(cast(BoardShape, item))
                for item in self.get_items(types=[KiCadObjectType.KOT_PCB_SHAPE])
            )
            if item is not None
        ]

    def get_dimensions(self) -> Sequence[Dimension]:
        """Retrieves all dimension objects on the board"""
        return [
            item
            for item in (
                to_concrete_dimension(cast(Dimension, item))
                for item in self.get_items(types=[KiCadObjectType.KOT_PCB_DIMENSION])
            )
            if item is not None
        ]

    def get_text(self) -> Sequence[Union[BoardText, BoardTextBox]]:
        return [
            cast(BoardText, item) if isinstance(item, BoardText) else cast(BoardTextBox, item)
            for item in self.get_items(
                types=[KiCadObjectType.KOT_PCB_TEXT, KiCadObjectType.KOT_PCB_TEXTBOX]
            )
        ]

    def get_zones(self) -> Sequence[Zone]:
        return [cast(Zone, item) for item in self.get_items(types=[KiCadObjectType.KOT_PCB_ZONE])]

    def get_as_string(self) -> str:
        command = editor_commands_pb2.SaveDocumentToString()
        command.document.CopyFrom(self._doc)
        return self._kicad.send(command, editor_commands_pb2.SavedDocumentResponse).contents

    def get_selection_as_string(self) -> str:
        command = editor_commands_pb2.SaveSelectionToString()
        return self._kicad.send(command, editor_commands_pb2.SavedSelectionResponse).contents

    def update_items(self, items: Union[BoardItem, Sequence[BoardItem]]):
        command = UpdateItems()
        command.header.document.CopyFrom(self._doc)

        if isinstance(items, BoardItem):
            command.items.append(pack_any(items.proto))
        else:
            command.items.extend([pack_any(i.proto) for i in items])

        if len(command.items) == 0:
            return

        return [
            unwrap(result.item)
            for result in self._kicad.send(command, UpdateItemsResponse).updated_items
        ]

    def remove_items(self, items: Union[BoardItem, Sequence[BoardItem]]):
        command = DeleteItems()
        command.header.document.CopyFrom(self._doc)

        if isinstance(items, BoardItem):
            command.item_ids.append(items.id)
        else:
            command.item_ids.extend([item.id for item in items])

        if len(command.item_ids) == 0:
            return

        self._kicad.send(command, DeleteItemsResponse)

    def get_nets(
        self, netclass_filter: Optional[Union[str, Sequence[str]]] = None
    ) -> Sequence[Net]:
        command = board_commands_pb2.GetNets()
        command.board.CopyFrom(self._doc)

        if isinstance(netclass_filter, str):
            command.netclass_filter.append(netclass_filter)
        elif netclass_filter is not None:
            command.netclass_filter.extend(netclass_filter)

        return [
            Net(net)
            for net in self._kicad.send(command, board_commands_pb2.NetsResponse).nets
        ]

    def get_selection(self) -> Sequence[Wrapper]:
        return []

    def add_to_selection(self, items):
        pass

    def remove_from_selection(self, items):
        pass

    def clear_selection(self):
        pass

    def get_stackup(self) -> board_pb2.BoardStackup:
        command = board_commands_pb2.GetBoardStackup()
        command.board.CopyFrom(self._doc)
        return self._kicad.send(command, board_commands_pb2.BoardStackupResponse).stackup

    def get_graphics_defaults(self) -> Dict[int, BoardLayerGraphicsDefaults]:
        cmd = board_commands_pb2.GetGraphicsDefaults()
        cmd.board.CopyFrom(self._doc)
        reply = self._kicad.send(cmd, board_commands_pb2.GraphicsDefaultsResponse)
        return {
            board_pb2.BoardLayerClass.BLC_SILKSCREEN:  BoardLayerGraphicsDefaults(reply.defaults.layers[0]),
            board_pb2.BoardLayerClass.BLC_COPPER:      BoardLayerGraphicsDefaults(reply.defaults.layers[1]),
            board_pb2.BoardLayerClass.BLC_EDGES:       BoardLayerGraphicsDefaults(reply.defaults.layers[2]),
            board_pb2.BoardLayerClass.BLC_COURTYARD:   BoardLayerGraphicsDefaults(reply.defaults.layers[3]),
            board_pb2.BoardLayerClass.BLC_FABRICATION: BoardLayerGraphicsDefaults(reply.defaults.layers[4]),
            board_pb2.BoardLayerClass.BLC_OTHER:       BoardLayerGraphicsDefaults(reply.defaults.layers[5])
        }

    def get_title_block_info(self) -> TitleBlockInfo:
        cmd = editor_commands_pb2.GetTitleBlockInfo()
        cmd.document.CopyFrom(self._doc)
        return TitleBlockInfo(self._kicad.send(cmd, base_types_pb2.TitleBlockInfo))

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

    @overload
    def get_item_bounding_box(
        self, items: BoardItem, include_text: bool = False
    ) -> Optional[Box2]: ...

    @overload
    def get_item_bounding_box(
        self, items: Sequence[BoardItem], include_text: bool = False
    ) -> List[Optional[Box2]]: ...

    def get_item_bounding_box(
        self,
        items: Union[BoardItem, Sequence[BoardItem]],
        include_text: bool = False
    ) -> Union[Optional[Box2], List[Optional[Box2]]]:
        """Gets the KiCad-calculated bounding box for an item or items, returning None if the item
        does not exist or has no bounding box"""
        cmd = editor_commands_pb2.GetBoundingBox()
        cmd.header.document.CopyFrom(self._doc)
        cmd.mode = (
            editor_commands_pb2.BoundingBoxMode.BBM_ITEM_AND_CHILD_TEXT
            if include_text
            else editor_commands_pb2.BoundingBoxMode.BBM_ITEM_ONLY
        )

        if isinstance(items, BoardItem):
            cmd.items.append(items.id)
        else:
            cmd.items.extend([i.id for i in items])

        response = self._kicad.send(cmd, editor_commands_pb2.GetBoundingBoxResponse)

        if isinstance(items, BoardItem):
            return Box2.from_proto(response.boxes[0]) if len(response.boxes) == 1 else None

        item_to_bbox = {item: bbox for item, bbox in zip(response.items, response.boxes)}
        return [
            Box2.from_proto(box)
            for box in (item_to_bbox.get(item.id, None) for item in items)
            if box is not None
        ]

    @overload
    def get_pad_shapes_as_polygons(
        self, pads: Pad, layer: BoardLayer.ValueType = BoardLayer.BL_F_Cu
    ) -> Optional[PolygonWithHoles]: ...

    @overload
    def get_pad_shapes_as_polygons(
        self, pads: Sequence[Pad], layer: BoardLayer.ValueType = BoardLayer.BL_F_Cu
    ) -> List[Optional[PolygonWithHoles]]: ...

    def get_pad_shapes_as_polygons(
        self, pads: Union[Pad, Sequence[Pad]], layer: BoardLayer.ValueType = BoardLayer.BL_F_Cu
    ) -> Union[Optional[PolygonWithHoles], List[Optional[PolygonWithHoles]]]:
        cmd = board_commands_pb2.GetPadShapeAsPolygon()
        cmd.board.CopyFrom(self._doc)
        cmd.layer = layer

        if isinstance(pads, Pad):
            cmd.pads.append(pads.id)
        else:
            cmd.pads.extend([pad.id for pad in pads])

        response = self._kicad.send(cmd, board_commands_pb2.PadShapeAsPolygonResponse)

        if isinstance(pads, Pad):
            return PolygonWithHoles(response.polygons[0]) if len(response.polygons) == 1 else None

        pad_to_polygon = {pad: polygon for pad, polygon in zip(response.pads, response.polygons)}
        return [
            PolygonWithHoles(p)
            for p in (pad_to_polygon.get(pad.id, None) for pad in pads)
            if p is not None
        ]

    def interactive_move(self, items: Union[KIID, Iterable[KIID]]):
        cmd = board_commands_pb2.InteractiveMoveItems()
        cmd.board.CopyFrom(self._doc)

        if isinstance(items, KIID):
            cmd.items.append(items)
        else:
            cmd.items.extend(items)

        self._kicad.send(cmd, Empty)

    def refill_zones(self, block=True, max_poll_seconds: float = 30.0,
                     poll_interval_seconds: float = 0.5):
        cmd = board_commands_pb2.RefillZones()
        cmd.board.CopyFrom(self._doc)
        self._kicad.send(cmd, Empty)

        if not block:
            return

        # Zone fill is a blocking operation that can block the entire event loop.
        # To hide this from API users somewhat, do an initial busy loop here
        sleeps = 0

        while sleeps < max_poll_seconds:
            sleep(poll_interval_seconds)
            try:
                self._kicad.send(Ping(), Empty)
            except IOError:
                # transport-layer timeout
                continue
            except ApiError as e:
                if e.code == ApiStatusCode.AS_BUSY:
                    continue
                else:
                    raise e
            break

    def hit_test(self, item: Item, position: Vector2, tolerance: int = 0) -> bool:
        cmd = HitTest()
        cmd.header.document.CopyFrom(self._doc)
        cmd.id.CopyFrom(item.id)
        cmd.position.CopyFrom(position.proto)
        cmd.tolerance = tolerance
        return self._kicad.send(cmd, HitTestResponse).result == HitTestResult.HTR_HIT

    def get_visible_layers(self) -> Sequence[board_types_pb2.BoardLayer.ValueType]:
        cmd = board_commands_pb2.GetVisibleLayers()
        cmd.board.CopyFrom(self._doc)
        response = self._kicad.send(cmd, board_commands_pb2.BoardLayers)
        return response.layers

    def set_visible_layers(self, layers: Sequence[board_types_pb2.BoardLayer.ValueType]):
        cmd = board_commands_pb2.SetVisibleLayers()
        cmd.board.CopyFrom(self._doc)
        cmd.layers.extend(layers)
        self._kicad.send(cmd, Empty)

    def get_active_layer(self) -> board_types_pb2.BoardLayer.ValueType:
        cmd = board_commands_pb2.GetActiveLayer()
        cmd.board.CopyFrom(self._doc)
        response = self._kicad.send(cmd, board_commands_pb2.BoardLayerResponse)
        return response.layer

    def set_active_layer(self, layer: board_types_pb2.BoardLayer.ValueType):
        cmd = board_commands_pb2.SetActiveLayer()
        cmd.board.CopyFrom(self._doc)
        cmd.layer = layer
        self._kicad.send(cmd, Empty)
