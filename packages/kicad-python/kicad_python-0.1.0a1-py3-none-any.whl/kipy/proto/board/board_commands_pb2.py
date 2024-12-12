"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ..common.types import enums_pb2 as common_dot_types_dot_enums__pb2
from ..board import board_pb2 as board_dot_board__pb2
from ..board import board_types_pb2 as board_dot_board__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aboard/board_commands.proto\x12\x14kiapi.board.commands\x1a\x1dcommon/types/base_types.proto\x1a\x18common/types/enums.proto\x1a\x11board/board.proto\x1a\x17board/board_types.proto"G\n\x0fGetBoardStackup\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"B\n\x14BoardStackupResponse\x12*\n\x07stackup\x18\x01 \x01(\x0b2\x19.kiapi.board.BoardStackup"v\n\x12UpdateBoardStackup\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12*\n\x07stackup\x18\x02 \x01(\x0b2\x19.kiapi.board.BoardStackup"K\n\x13GetGraphicsDefaults\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"K\n\x18GraphicsDefaultsResponse\x12/\n\x08defaults\x18\x01 \x01(\x0b2\x1d.kiapi.board.GraphicsDefaults"X\n\x07GetNets\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\x17\n\x0fnetclass_filter\x18\x02 \x03(\t"4\n\x0cNetsResponse\x12$\n\x04nets\x18\x01 \x03(\x0b2\x16.kiapi.board.types.Net"\xa2\x01\n\rGetItemsByNet\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x122\n\x05types\x18\x02 \x03(\x0e2#.kiapi.common.types.KiCadObjectType\x12-\n\tnet_codes\x18\x03 \x03(\x0b2\x1a.kiapi.board.types.NetCode"\x8d\x01\n\x12GetItemsByNetClass\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x122\n\x05types\x18\x02 \x03(\x0e2#.kiapi.common.types.KiCadObjectType\x12\x13\n\x0bnet_classes\x18\x03 \x03(\t"l\n\x0bRefillZones\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\'\n\x05zones\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIID"\xa2\x01\n\x14GetPadShapeAsPolygon\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12&\n\x04pads\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIID\x12,\n\x05layer\x18\x03 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer"{\n\x19PadShapeAsPolygonResponse\x12&\n\x04pads\x18\x01 \x03(\x0b2\x18.kiapi.common.types.KIID\x126\n\x08polygons\x18\x02 \x03(\x0b2$.kiapi.common.types.PolygonWithHoles"H\n\x10GetVisibleLayers\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"B\n\x12BoardLayerResponse\x12,\n\x05layer\x18\x01 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer"<\n\x0bBoardLayers\x12-\n\x06layers\x18\x01 \x03(\x0e2\x1d.kiapi.board.types.BoardLayer"w\n\x10SetVisibleLayers\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12-\n\x06layers\x18\x02 \x03(\x0e2\x1d.kiapi.board.types.BoardLayer"F\n\x0eGetActiveLayer\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"t\n\x0eSetActiveLayer\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12,\n\x05layer\x18\x02 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer"u\n\x14InteractiveMoveItems\x124\n\x05board\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\'\n\x05items\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIIDb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'board.board_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETBOARDSTACKUP']._serialized_start = 153
    _globals['_GETBOARDSTACKUP']._serialized_end = 224
    _globals['_BOARDSTACKUPRESPONSE']._serialized_start = 226
    _globals['_BOARDSTACKUPRESPONSE']._serialized_end = 292
    _globals['_UPDATEBOARDSTACKUP']._serialized_start = 294
    _globals['_UPDATEBOARDSTACKUP']._serialized_end = 412
    _globals['_GETGRAPHICSDEFAULTS']._serialized_start = 414
    _globals['_GETGRAPHICSDEFAULTS']._serialized_end = 489
    _globals['_GRAPHICSDEFAULTSRESPONSE']._serialized_start = 491
    _globals['_GRAPHICSDEFAULTSRESPONSE']._serialized_end = 566
    _globals['_GETNETS']._serialized_start = 568
    _globals['_GETNETS']._serialized_end = 656
    _globals['_NETSRESPONSE']._serialized_start = 658
    _globals['_NETSRESPONSE']._serialized_end = 710
    _globals['_GETITEMSBYNET']._serialized_start = 713
    _globals['_GETITEMSBYNET']._serialized_end = 875
    _globals['_GETITEMSBYNETCLASS']._serialized_start = 878
    _globals['_GETITEMSBYNETCLASS']._serialized_end = 1019
    _globals['_REFILLZONES']._serialized_start = 1021
    _globals['_REFILLZONES']._serialized_end = 1129
    _globals['_GETPADSHAPEASPOLYGON']._serialized_start = 1132
    _globals['_GETPADSHAPEASPOLYGON']._serialized_end = 1294
    _globals['_PADSHAPEASPOLYGONRESPONSE']._serialized_start = 1296
    _globals['_PADSHAPEASPOLYGONRESPONSE']._serialized_end = 1419
    _globals['_GETVISIBLELAYERS']._serialized_start = 1421
    _globals['_GETVISIBLELAYERS']._serialized_end = 1493
    _globals['_BOARDLAYERRESPONSE']._serialized_start = 1495
    _globals['_BOARDLAYERRESPONSE']._serialized_end = 1561
    _globals['_BOARDLAYERS']._serialized_start = 1563
    _globals['_BOARDLAYERS']._serialized_end = 1623
    _globals['_SETVISIBLELAYERS']._serialized_start = 1625
    _globals['_SETVISIBLELAYERS']._serialized_end = 1744
    _globals['_GETACTIVELAYER']._serialized_start = 1746
    _globals['_GETACTIVELAYER']._serialized_end = 1816
    _globals['_SETACTIVELAYER']._serialized_start = 1818
    _globals['_SETACTIVELAYER']._serialized_end = 1934
    _globals['_INTERACTIVEMOVEITEMS']._serialized_start = 1936
    _globals['_INTERACTIVEMOVEITEMS']._serialized_end = 2053