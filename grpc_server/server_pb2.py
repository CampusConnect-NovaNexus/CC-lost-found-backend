# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: grpc_server/server.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'grpc_server/server.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18grpc_server/server.proto\"\'\n\x14GenerateTokenRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"\x0e\n\x0c\x45mptyRequest\"\x90\x01\n\x04Item\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\ritem_category\x18\x02 \x01(\t\x12\x18\n\x10item_description\x18\x03 \x01(\t\x12\x17\n\nitem_image\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x12\n\nitem_title\x18\x05 \x01(\t\x12\x0f\n\x07user_id\x18\x06 \x01(\tB\r\n\x0b_item_image\"\x1d\n\x05Items\x12\x14\n\x05items\x18\x01 \x03(\x0b\x32\x05.Item\"$\n\x0esucessResponse\x12\x12\n\nisSuceeded\x18\x01 \x01(\x08\"\x91\x01\n\x11\x43reateItemRequest\x12\x15\n\ritem_category\x18\x01 \x01(\t\x12\x18\n\x10item_description\x18\x02 \x01(\t\x12\x17\n\nitem_image\x18\x03 \x01(\tH\x00\x88\x01\x01\x12\x12\n\nitem_title\x18\x04 \x01(\t\x12\x0f\n\x07user_id\x18\x05 \x01(\tB\r\n\x0b_item_image\"\x8c\x01\n\x11UpdateItemRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x15\n\ritem_category\x18\x02 \x01(\t\x12\x18\n\x10item_description\x18\x03 \x01(\t\x12\x17\n\nitem_image\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x12\n\nitem_title\x18\x05 \x01(\tB\r\n\x0b_item_image\"\x1f\n\x11\x44\x65leteItemRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x1e\n\x0fMulItemsRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\" \n\x12GetItemByIdRequest\x12\n\n\x02id\x18\x01 \x01(\t2\xa5\x02\n\x0bItemService\x12$\n\x0bGetAllItems\x12\r.EmptyRequest\x1a\x06.Items\x12,\n\x10GetMultipleItems\x12\x10.MulItemsRequest\x1a\x06.Items\x12\x31\n\nCreateItem\x12\x12.CreateItemRequest\x1a\x0f.sucessResponse\x12\x31\n\nUpdateItem\x12\x12.UpdateItemRequest\x1a\x0f.sucessResponse\x12\x31\n\nDeleteItem\x12\x12.DeleteItemRequest\x1a\x0f.sucessResponse\x12)\n\x0bGetItemById\x12\x13.GetItemByIdRequest\x1a\x05.Itemb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'grpc_server.server_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GENERATETOKENREQUEST']._serialized_start=28
  _globals['_GENERATETOKENREQUEST']._serialized_end=67
  _globals['_EMPTYREQUEST']._serialized_start=69
  _globals['_EMPTYREQUEST']._serialized_end=83
  _globals['_ITEM']._serialized_start=86
  _globals['_ITEM']._serialized_end=230
  _globals['_ITEMS']._serialized_start=232
  _globals['_ITEMS']._serialized_end=261
  _globals['_SUCESSRESPONSE']._serialized_start=263
  _globals['_SUCESSRESPONSE']._serialized_end=299
  _globals['_CREATEITEMREQUEST']._serialized_start=302
  _globals['_CREATEITEMREQUEST']._serialized_end=447
  _globals['_UPDATEITEMREQUEST']._serialized_start=450
  _globals['_UPDATEITEMREQUEST']._serialized_end=590
  _globals['_DELETEITEMREQUEST']._serialized_start=592
  _globals['_DELETEITEMREQUEST']._serialized_end=623
  _globals['_MULITEMSREQUEST']._serialized_start=625
  _globals['_MULITEMSREQUEST']._serialized_end=655
  _globals['_GETITEMBYIDREQUEST']._serialized_start=657
  _globals['_GETITEMBYIDREQUEST']._serialized_end=689
  _globals['_ITEMSERVICE']._serialized_start=692
  _globals['_ITEMSERVICE']._serialized_end=985
# @@protoc_insertion_point(module_scope)
