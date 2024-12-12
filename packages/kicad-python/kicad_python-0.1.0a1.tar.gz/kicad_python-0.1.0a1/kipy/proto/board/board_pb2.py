"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ..common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ..board import board_types_pb2 as board_dot_board__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11board/board.proto\x12\x0bkiapi.board\x1a\x1dcommon/types/base_types.proto\x1a\x17board/board_types.proto" \n\x0bBoardFinish\x12\x11\n\ttype_name\x18\x01 \x01(\t".\n\x15BoardImpedanceControl\x12\x15\n\ris_controlled\x18\x01 \x01(\x08"\x14\n\x12BoardEdgeConnector",\n\x0cCastellation\x12\x1c\n\x14has_castellated_pads\x18\x01 \x01(\x08"\'\n\x0bEdgePlating\x12\x18\n\x10has_edge_plating\x18\x01 \x01(\x08"\xa3\x01\n\x11BoardEdgeSettings\x122\n\tconnector\x18\x01 \x01(\x0b2\x1f.kiapi.board.BoardEdgeConnector\x12/\n\x0ccastellation\x18\x02 \x01(\x0b2\x19.kiapi.board.Castellation\x12)\n\x07plating\x18\x03 \x01(\x0b2\x18.kiapi.board.EdgePlating"\x19\n\x17BoardStackupCopperLayer"\xc3\x01\n\x11BoardStackupLayer\x12/\n\tthickness\x18\x01 \x01(\x0b2\x1c.kiapi.common.types.Distance\x12,\n\x05layer\x18\x02 \x01(\x0e2\x1d.kiapi.board.types.BoardLayer\x12\x0f\n\x07enabled\x18\x03 \x01(\x08\x126\n\x06copper\x18\x04 \x01(\x0b2$.kiapi.board.BoardStackupCopperLayerH\x00B\x06\n\x04item"\xcd\x01\n\x0cBoardStackup\x12(\n\x06finish\x18\x01 \x01(\x0b2\x18.kiapi.board.BoardFinish\x125\n\timpedance\x18\x02 \x01(\x0b2".kiapi.board.BoardImpedanceControl\x12,\n\x04edge\x18\x03 \x01(\x0b2\x1e.kiapi.board.BoardEdgeSettings\x12.\n\x06layers\x18\x04 \x03(\x0b2\x1e.kiapi.board.BoardStackupLayer"\xb1\x01\n\x1aBoardLayerGraphicsDefaults\x12+\n\x05layer\x18\x01 \x01(\x0e2\x1c.kiapi.board.BoardLayerClass\x120\n\x04text\x18\x02 \x01(\x0b2".kiapi.common.types.TextAttributes\x124\n\x0eline_thickness\x18\x03 \x01(\x0b2\x1c.kiapi.common.types.Distance"K\n\x10GraphicsDefaults\x127\n\x06layers\x18\x01 \x03(\x0b2\'.kiapi.board.BoardLayerGraphicsDefaults"I\n\rBoardSettings\x128\n\x11graphics_defaults\x18\x01 \x01(\x0b2\x1d.kiapi.board.GraphicsDefaults"\x12\n\x10BoardDesignRules*\x8c\x01\n\x0fBoardLayerClass\x12\x0f\n\x0bBLC_UNKNOWN\x10\x00\x12\x12\n\x0eBLC_SILKSCREEN\x10\x01\x12\x0e\n\nBLC_COPPER\x10\x02\x12\r\n\tBLC_EDGES\x10\x03\x12\x11\n\rBLC_COURTYARD\x10\x04\x12\x13\n\x0fBLC_FABRICATION\x10\x05\x12\r\n\tBLC_OTHER\x10\x06b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'board.board_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_BOARDLAYERCLASS']._serialized_start = 1233
    _globals['_BOARDLAYERCLASS']._serialized_end = 1373
    _globals['_BOARDFINISH']._serialized_start = 90
    _globals['_BOARDFINISH']._serialized_end = 122
    _globals['_BOARDIMPEDANCECONTROL']._serialized_start = 124
    _globals['_BOARDIMPEDANCECONTROL']._serialized_end = 170
    _globals['_BOARDEDGECONNECTOR']._serialized_start = 172
    _globals['_BOARDEDGECONNECTOR']._serialized_end = 192
    _globals['_CASTELLATION']._serialized_start = 194
    _globals['_CASTELLATION']._serialized_end = 238
    _globals['_EDGEPLATING']._serialized_start = 240
    _globals['_EDGEPLATING']._serialized_end = 279
    _globals['_BOARDEDGESETTINGS']._serialized_start = 282
    _globals['_BOARDEDGESETTINGS']._serialized_end = 445
    _globals['_BOARDSTACKUPCOPPERLAYER']._serialized_start = 447
    _globals['_BOARDSTACKUPCOPPERLAYER']._serialized_end = 472
    _globals['_BOARDSTACKUPLAYER']._serialized_start = 475
    _globals['_BOARDSTACKUPLAYER']._serialized_end = 670
    _globals['_BOARDSTACKUP']._serialized_start = 673
    _globals['_BOARDSTACKUP']._serialized_end = 878
    _globals['_BOARDLAYERGRAPHICSDEFAULTS']._serialized_start = 881
    _globals['_BOARDLAYERGRAPHICSDEFAULTS']._serialized_end = 1058
    _globals['_GRAPHICSDEFAULTS']._serialized_start = 1060
    _globals['_GRAPHICSDEFAULTS']._serialized_end = 1135
    _globals['_BOARDSETTINGS']._serialized_start = 1137
    _globals['_BOARDSETTINGS']._serialized_end = 1210
    _globals['_BOARDDESIGNRULES']._serialized_start = 1212
    _globals['_BOARDDESIGNRULES']._serialized_end = 1230