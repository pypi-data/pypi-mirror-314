"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ...common.types import project_settings_pb2 as common_dot_types_dot_project__settings__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&common/commands/project_commands.proto\x12\x15kiapi.common.commands\x1a\x1dcommon/types/base_types.proto\x1a#common/types/project_settings.proto"\x0f\n\rGetNetClasses"I\n\x12NetClassesResponse\x123\n\x0bnet_classes\x18\x01 \x03(\x0b2\x1e.kiapi.common.project.NetClass"\\\n\x13ExpandTextVariables\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\x0c\n\x04text\x18\x02 \x03(\t"+\n\x1bExpandTextVariablesResponse\x12\x0c\n\x04text\x18\x01 \x03(\tb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.commands.project_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_GETNETCLASSES']._serialized_start = 133
    _globals['_GETNETCLASSES']._serialized_end = 148
    _globals['_NETCLASSESRESPONSE']._serialized_start = 150
    _globals['_NETCLASSESRESPONSE']._serialized_end = 223
    _globals['_EXPANDTEXTVARIABLES']._serialized_start = 225
    _globals['_EXPANDTEXTVARIABLES']._serialized_end = 317
    _globals['_EXPANDTEXTVARIABLESRESPONSE']._serialized_start = 319
    _globals['_EXPANDTEXTVARIABLESRESPONSE']._serialized_end = 362