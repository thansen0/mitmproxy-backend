# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/image_classification.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!protos/image_classification.proto\"Y\n\x07NLImage\x12\r\n\x05\x63olor\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\r\n\x05width\x18\x03 \x01(\x05\x12\x0e\n\x06height\x18\x04 \x01(\x05\x12\x12\n\nimg_format\x18\x05 \x01(\t\"\'\n\x0cImageMessage\x12\x17\n\x05image\x18\x01 \x01(\x0b\x32\x08.NLImage\"^\n\rImageResponse\x12\x10\n\x08\x64rawings\x18\x01 \x01(\x02\x12\x0e\n\x06hentai\x18\x02 \x01(\x02\x12\x0f\n\x07neutral\x18\x03 \x01(\x02\x12\x0c\n\x04porn\x18\x04 \x01(\x02\x12\x0c\n\x04sexy\x18\x05 \x01(\x02\x32G\n\rClassifyImage\x12\x36\n\x13StartClassification\x12\r.ImageMessage\x1a\x0e.ImageResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.image_classification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_NLIMAGE']._serialized_start=37
  _globals['_NLIMAGE']._serialized_end=126
  _globals['_IMAGEMESSAGE']._serialized_start=128
  _globals['_IMAGEMESSAGE']._serialized_end=167
  _globals['_IMAGERESPONSE']._serialized_start=169
  _globals['_IMAGERESPONSE']._serialized_end=263
  _globals['_CLASSIFYIMAGE']._serialized_start=265
  _globals['_CLASSIFYIMAGE']._serialized_end=336
# @@protoc_insertion_point(module_scope)
