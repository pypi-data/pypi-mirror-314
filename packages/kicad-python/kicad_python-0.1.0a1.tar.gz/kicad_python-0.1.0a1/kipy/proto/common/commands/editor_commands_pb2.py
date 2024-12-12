"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ...common.types import base_types_pb2 as common_dot_types_dot_base__types__pb2
from ...common.types import enums_pb2 as common_dot_types_dot_enums__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%common/commands/editor_commands.proto\x12\x15kiapi.common.commands\x1a\x19google/protobuf/any.proto\x1a\x1dcommon/types/base_types.proto\x1a\x18common/types/enums.proto"=\n\rRefreshEditor\x12,\n\x05frame\x18\x01 \x01(\x0e2\x1d.kiapi.common.types.FrameType"B\n\x10GetOpenDocuments\x12.\n\x04type\x18\x01 \x01(\x0e2 .kiapi.common.types.DocumentType"T\n\x18GetOpenDocumentsResponse\x128\n\tdocuments\x18\x01 \x03(\x0b2%.kiapi.common.types.DocumentSpecifier"\x1b\n\tRunAction\x12\x0e\n\x06action\x18\x01 \x01(\t"K\n\x11RunActionResponse\x126\n\x06status\x18\x01 \x01(\x0e2&.kiapi.common.commands.RunActionStatus"\r\n\x0bBeginCommit";\n\x13BeginCommitResponse\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID"w\n\tEndCommit\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x123\n\x06action\x18\x02 \x01(\x0e2#.kiapi.common.commands.CommitAction\x12\x0f\n\x07message\x18\x03 \x01(\t"\x13\n\x11EndCommitResponse"\x8f\x01\n\x0bCreateItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12#\n\x05items\x18\x02 \x03(\x0b2\x14.google.protobuf.Any\x12+\n\tcontainer\x18\x03 \x01(\x0b2\x18.kiapi.common.types.KIID"X\n\nItemStatus\x123\n\x04code\x18\x01 \x01(\x0e2%.kiapi.common.commands.ItemStatusCode\x12\x15\n\rerror_message\x18\x02 \x01(\t"k\n\x12ItemCreationResult\x121\n\x06status\x18\x01 \x01(\x0b2!.kiapi.common.commands.ItemStatus\x12"\n\x04item\x18\x02 \x01(\x0b2\x14.google.protobuf.Any"\xbe\x01\n\x13CreateItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12@\n\rcreated_items\x18\x03 \x03(\x0b2).kiapi.common.commands.ItemCreationResult"n\n\x08GetItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x122\n\x05types\x18\x02 \x03(\x0e2#.kiapi.common.types.KiCadObjectType"\x9e\x01\n\x10GetItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12#\n\x05items\x18\x03 \x03(\x0b2\x14.google.protobuf.Any"b\n\x0bUpdateItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12#\n\x05items\x18\x02 \x03(\x0b2\x14.google.protobuf.Any"i\n\x10ItemUpdateResult\x121\n\x06status\x18\x01 \x01(\x0b2!.kiapi.common.commands.ItemStatus\x12"\n\x04item\x18\x02 \x01(\x0b2\x14.google.protobuf.Any"\xbc\x01\n\x13UpdateItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12>\n\rupdated_items\x18\x03 \x03(\x0b2\'.kiapi.common.commands.ItemUpdateResult"i\n\x0bDeleteItems\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12*\n\x08item_ids\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIID"u\n\x12ItemDeletionResult\x12$\n\x02id\x18\x01 \x01(\x0b2\x18.kiapi.common.types.KIID\x129\n\x06status\x18\x02 \x01(\x0e2).kiapi.common.commands.ItemDeletionStatus"\xbe\x01\n\x13DeleteItemsResponse\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x125\n\x06status\x18\x02 \x01(\x0e2%.kiapi.common.types.ItemRequestStatus\x12@\n\rdeleted_items\x18\x03 \x03(\x0b2).kiapi.common.commands.ItemDeletionResult"\x9f\x01\n\x0eGetBoundingBox\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12\'\n\x05items\x18\x02 \x03(\x0b2\x18.kiapi.common.types.KIID\x124\n\x04mode\x18\x03 \x01(\x0e2&.kiapi.common.commands.BoundingBoxMode"j\n\x16GetBoundingBoxResponse\x12\'\n\x05items\x18\x01 \x03(\x0b2\x18.kiapi.common.types.KIID\x12\'\n\x05boxes\x18\x02 \x03(\x0b2\x18.kiapi.common.types.Box2"\xa1\x01\n\x07HitTest\x12.\n\x06header\x18\x01 \x01(\x0b2\x1e.kiapi.common.types.ItemHeader\x12$\n\x02id\x18\x02 \x01(\x0b2\x18.kiapi.common.types.KIID\x12-\n\x08position\x18\x03 \x01(\x0b2\x1b.kiapi.common.types.Vector2\x12\x11\n\ttolerance\x18\x04 \x01(\x05"G\n\x0fHitTestResponse\x124\n\x06result\x18\x01 \x01(\x0e2$.kiapi.common.commands.HitTestResult"L\n\x11GetTitleBlockInfo\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"O\n\x14SaveDocumentToString\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier"b\n\x15SavedDocumentResponse\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\x10\n\x08contents\x18\x02 \x01(\t"\x17\n\x15SaveSelectionToString"Q\n\x16SavedSelectionResponse\x12%\n\x03ids\x18\x01 \x03(\x0b2\x18.kiapi.common.types.KIID\x12\x10\n\x08contents\x18\x02 \x01(\t"j\n\x1dParseAndCreateItemsFromString\x127\n\x08document\x18\x01 \x01(\x0b2%.kiapi.common.types.DocumentSpecifier\x12\x10\n\x08contents\x18\x02 \x01(\t*W\n\x0fRunActionStatus\x12\x0f\n\x0bRAS_UNKNOWN\x10\x00\x12\n\n\x06RAS_OK\x10\x01\x12\x0f\n\x0bRAS_INVALID\x10\x02\x12\x16\n\x12RAS_FRAME_NOT_OPEN\x10\x03*=\n\x0cCommitAction\x12\x0f\n\x0bCMA_UNKNOWN\x10\x00\x12\x0e\n\nCMA_COMMIT\x10\x01\x12\x0c\n\x08CMA_DROP\x10\x02*\x93\x01\n\x0eItemStatusCode\x12\x0f\n\x0bISC_UNKNOWN\x10\x00\x12\n\n\x06ISC_OK\x10\x01\x12\x14\n\x10ISC_INVALID_TYPE\x10\x02\x12\x10\n\x0cISC_EXISTING\x10\x03\x12\x13\n\x0fISC_NONEXISTENT\x10\x04\x12\x11\n\rISC_IMMUTABLE\x10\x05\x12\x14\n\x10ISC_INVALID_DATA\x10\x07*Y\n\x12ItemDeletionStatus\x12\x0f\n\x0bIDS_UNKNOWN\x10\x00\x12\n\n\x06IDS_OK\x10\x01\x12\x13\n\x0fIDS_NONEXISTENT\x10\x02\x12\x11\n\rIDS_IMMUTABLE\x10\x03*R\n\x0fBoundingBoxMode\x12\x0f\n\x0bBBM_UNKNOWN\x10\x00\x12\x11\n\rBBM_ITEM_ONLY\x10\x01\x12\x1b\n\x17BBM_ITEM_AND_CHILD_TEXT\x10\x02*=\n\rHitTestResult\x12\x0f\n\x0bHTR_UNKNOWN\x10\x00\x12\x0e\n\nHTR_NO_HIT\x10\x01\x12\x0b\n\x07HTR_HIT\x10\x02b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.commands.editor_commands_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_RUNACTIONSTATUS']._serialized_start = 3299
    _globals['_RUNACTIONSTATUS']._serialized_end = 3386
    _globals['_COMMITACTION']._serialized_start = 3388
    _globals['_COMMITACTION']._serialized_end = 3449
    _globals['_ITEMSTATUSCODE']._serialized_start = 3452
    _globals['_ITEMSTATUSCODE']._serialized_end = 3599
    _globals['_ITEMDELETIONSTATUS']._serialized_start = 3601
    _globals['_ITEMDELETIONSTATUS']._serialized_end = 3690
    _globals['_BOUNDINGBOXMODE']._serialized_start = 3692
    _globals['_BOUNDINGBOXMODE']._serialized_end = 3774
    _globals['_HITTESTRESULT']._serialized_start = 3776
    _globals['_HITTESTRESULT']._serialized_end = 3837
    _globals['_REFRESHEDITOR']._serialized_start = 148
    _globals['_REFRESHEDITOR']._serialized_end = 209
    _globals['_GETOPENDOCUMENTS']._serialized_start = 211
    _globals['_GETOPENDOCUMENTS']._serialized_end = 277
    _globals['_GETOPENDOCUMENTSRESPONSE']._serialized_start = 279
    _globals['_GETOPENDOCUMENTSRESPONSE']._serialized_end = 363
    _globals['_RUNACTION']._serialized_start = 365
    _globals['_RUNACTION']._serialized_end = 392
    _globals['_RUNACTIONRESPONSE']._serialized_start = 394
    _globals['_RUNACTIONRESPONSE']._serialized_end = 469
    _globals['_BEGINCOMMIT']._serialized_start = 471
    _globals['_BEGINCOMMIT']._serialized_end = 484
    _globals['_BEGINCOMMITRESPONSE']._serialized_start = 486
    _globals['_BEGINCOMMITRESPONSE']._serialized_end = 545
    _globals['_ENDCOMMIT']._serialized_start = 547
    _globals['_ENDCOMMIT']._serialized_end = 666
    _globals['_ENDCOMMITRESPONSE']._serialized_start = 668
    _globals['_ENDCOMMITRESPONSE']._serialized_end = 687
    _globals['_CREATEITEMS']._serialized_start = 690
    _globals['_CREATEITEMS']._serialized_end = 833
    _globals['_ITEMSTATUS']._serialized_start = 835
    _globals['_ITEMSTATUS']._serialized_end = 923
    _globals['_ITEMCREATIONRESULT']._serialized_start = 925
    _globals['_ITEMCREATIONRESULT']._serialized_end = 1032
    _globals['_CREATEITEMSRESPONSE']._serialized_start = 1035
    _globals['_CREATEITEMSRESPONSE']._serialized_end = 1225
    _globals['_GETITEMS']._serialized_start = 1227
    _globals['_GETITEMS']._serialized_end = 1337
    _globals['_GETITEMSRESPONSE']._serialized_start = 1340
    _globals['_GETITEMSRESPONSE']._serialized_end = 1498
    _globals['_UPDATEITEMS']._serialized_start = 1500
    _globals['_UPDATEITEMS']._serialized_end = 1598
    _globals['_ITEMUPDATERESULT']._serialized_start = 1600
    _globals['_ITEMUPDATERESULT']._serialized_end = 1705
    _globals['_UPDATEITEMSRESPONSE']._serialized_start = 1708
    _globals['_UPDATEITEMSRESPONSE']._serialized_end = 1896
    _globals['_DELETEITEMS']._serialized_start = 1898
    _globals['_DELETEITEMS']._serialized_end = 2003
    _globals['_ITEMDELETIONRESULT']._serialized_start = 2005
    _globals['_ITEMDELETIONRESULT']._serialized_end = 2122
    _globals['_DELETEITEMSRESPONSE']._serialized_start = 2125
    _globals['_DELETEITEMSRESPONSE']._serialized_end = 2315
    _globals['_GETBOUNDINGBOX']._serialized_start = 2318
    _globals['_GETBOUNDINGBOX']._serialized_end = 2477
    _globals['_GETBOUNDINGBOXRESPONSE']._serialized_start = 2479
    _globals['_GETBOUNDINGBOXRESPONSE']._serialized_end = 2585
    _globals['_HITTEST']._serialized_start = 2588
    _globals['_HITTEST']._serialized_end = 2749
    _globals['_HITTESTRESPONSE']._serialized_start = 2751
    _globals['_HITTESTRESPONSE']._serialized_end = 2822
    _globals['_GETTITLEBLOCKINFO']._serialized_start = 2824
    _globals['_GETTITLEBLOCKINFO']._serialized_end = 2900
    _globals['_SAVEDOCUMENTTOSTRING']._serialized_start = 2902
    _globals['_SAVEDOCUMENTTOSTRING']._serialized_end = 2981
    _globals['_SAVEDDOCUMENTRESPONSE']._serialized_start = 2983
    _globals['_SAVEDDOCUMENTRESPONSE']._serialized_end = 3081
    _globals['_SAVESELECTIONTOSTRING']._serialized_start = 3083
    _globals['_SAVESELECTIONTOSTRING']._serialized_end = 3106
    _globals['_SAVEDSELECTIONRESPONSE']._serialized_start = 3108
    _globals['_SAVEDSELECTIONRESPONSE']._serialized_end = 3189
    _globals['_PARSEANDCREATEITEMSFROMSTRING']._serialized_start = 3191
    _globals['_PARSEANDCREATEITEMSFROMSTRING']._serialized_end = 3297