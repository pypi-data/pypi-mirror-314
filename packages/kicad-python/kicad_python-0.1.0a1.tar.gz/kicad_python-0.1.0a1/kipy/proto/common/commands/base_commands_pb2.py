"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#common/commands/base_commands.proto\x12\x15kiapi.common.commands\x1a\x1dcommon/types/base_types.proto"\x0c\n\nGetVersion"G\n\x12GetVersionResponse\x121\n\x07version\x18\x01 \x01(\x0b2 .kiapi.common.types.KiCadVersion"\x06\n\x04Ping"8\n\x0eGetTextExtents\x12&\n\x04text\x18\x01 \x01(\x0b2\x18.kiapi.common.types.Text"r\n\rTextOrTextBox\x12(\n\x04text\x18\x01 \x01(\x0b2\x18.kiapi.common.types.TextH\x00\x12.\n\x07textbox\x18\x02 \x01(\x0b2\x1b.kiapi.common.types.TextBoxH\x00B\x07\n\x05inner"E\n\x0fGetTextAsShapes\x122\n\x04text\x18\x01 \x03(\x0b2$.kiapi.common.commands.TextOrTextBox"w\n\x0eTextWithShapes\x122\n\x04text\x18\x01 \x01(\x0b2$.kiapi.common.commands.TextOrTextBox\x121\n\x06shapes\x18\x02 \x01(\x0b2!.kiapi.common.types.CompoundShape"Z\n\x17GetTextAsShapesResponse\x12?\n\x10text_with_shapes\x18\x01 \x03(\x0b2%.kiapi.common.commands.TextWithShapesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.commands.base_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETVERSION']._serialized_start = 93
    _globals['_GETVERSION']._serialized_end = 105
    _globals['_GETVERSIONRESPONSE']._serialized_start = 107
    _globals['_GETVERSIONRESPONSE']._serialized_end = 178
    _globals['_PING']._serialized_start = 180
    _globals['_PING']._serialized_end = 186
    _globals['_GETTEXTEXTENTS']._serialized_start = 188
    _globals['_GETTEXTEXTENTS']._serialized_end = 244
    _globals['_TEXTORTEXTBOX']._serialized_start = 246
    _globals['_TEXTORTEXTBOX']._serialized_end = 360
    _globals['_GETTEXTASSHAPES']._serialized_start = 362
    _globals['_GETTEXTASSHAPES']._serialized_end = 431
    _globals['_TEXTWITHSHAPES']._serialized_start = 433
    _globals['_TEXTWITHSHAPES']._serialized_end = 552
    _globals['_GETTEXTASSHAPESRESPONSE']._serialized_start = 554
    _globals['_GETTEXTASSHAPESRESPONSE']._serialized_end = 644