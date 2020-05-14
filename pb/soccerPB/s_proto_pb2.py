# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: s_proto.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='s_proto.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\rs_proto.proto\"_\n\x0eServerInfoResS\x12\x0b\n\x03ret\x18\x01 \x01(\x11\x12\x1f\n\tdate_jdbc\x18\x02 \x03(\x0b\x32\x0c.JdbcInfoPBS\x12\x1f\n\tgame_jdbc\x18\x03 \x03(\x0b\x32\x0c.JdbcInfoPBS\"5\n\x0bJdbcInfoPBS\x12\x11\n\tserver_id\x18\x01 \x01(\t\x12\x13\n\x0bserver_name\x18\x02 \x01(\t\"R\n\x12\x44\x61taComparisonResS\x12\x0b\n\x03ret\x18\x01 \x01(\x11\x12 \n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x12.DataComparisonPBS\x12\r\n\x05\x65xtra\x18\x03 \x01(\t\"5\n\x11\x44\x61taComparisonPBS\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x03(\t\"y\n\x12\x44\x61taComparisonReqS\x12\x11\n\tserver_id\x18\x01 \x01(\t\x12\x13\n\x0bsource_mark\x18\x02 \x01(\t\x12\x12\n\nquery_type\x18\x03 \x01(\x11\x12\'\n\x0bquery_param\x18\x04 \x03(\x0b\x32\x12.DataComparisonKey\"L\n\x11\x44\x61taComparisonKey\x12\x12\n\ntable_name\x18\x01 \x01(\t\x12\x10\n\x08\x63ol_name\x18\x02 \x01(\t\x12\x11\n\tcol_value\x18\x03 \x03(\tb\x06proto3'
)




_SERVERINFORESS = _descriptor.Descriptor(
  name='ServerInfoResS',
  full_name='ServerInfoResS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ret', full_name='ServerInfoResS.ret', index=0,
      number=1, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='date_jdbc', full_name='ServerInfoResS.date_jdbc', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='game_jdbc', full_name='ServerInfoResS.game_jdbc', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=112,
)


_JDBCINFOPBS = _descriptor.Descriptor(
  name='JdbcInfoPBS',
  full_name='JdbcInfoPBS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='server_id', full_name='JdbcInfoPBS.server_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='server_name', full_name='JdbcInfoPBS.server_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=114,
  serialized_end=167,
)


_DATACOMPARISONRESS = _descriptor.Descriptor(
  name='DataComparisonResS',
  full_name='DataComparisonResS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ret', full_name='DataComparisonResS.ret', index=0,
      number=1, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='DataComparisonResS.data', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extra', full_name='DataComparisonResS.extra', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=251,
)


_DATACOMPARISONPBS = _descriptor.Descriptor(
  name='DataComparisonPBS',
  full_name='DataComparisonPBS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='DataComparisonPBS.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='DataComparisonPBS.data', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=253,
  serialized_end=306,
)


_DATACOMPARISONREQS = _descriptor.Descriptor(
  name='DataComparisonReqS',
  full_name='DataComparisonReqS',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='server_id', full_name='DataComparisonReqS.server_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source_mark', full_name='DataComparisonReqS.source_mark', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query_type', full_name='DataComparisonReqS.query_type', index=2,
      number=3, type=17, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='query_param', full_name='DataComparisonReqS.query_param', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=308,
  serialized_end=429,
)


_DATACOMPARISONKEY = _descriptor.Descriptor(
  name='DataComparisonKey',
  full_name='DataComparisonKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='table_name', full_name='DataComparisonKey.table_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='col_name', full_name='DataComparisonKey.col_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='col_value', full_name='DataComparisonKey.col_value', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=431,
  serialized_end=507,
)

_SERVERINFORESS.fields_by_name['date_jdbc'].message_type = _JDBCINFOPBS
_SERVERINFORESS.fields_by_name['game_jdbc'].message_type = _JDBCINFOPBS
_DATACOMPARISONRESS.fields_by_name['data'].message_type = _DATACOMPARISONPBS
_DATACOMPARISONREQS.fields_by_name['query_param'].message_type = _DATACOMPARISONKEY
DESCRIPTOR.message_types_by_name['ServerInfoResS'] = _SERVERINFORESS
DESCRIPTOR.message_types_by_name['JdbcInfoPBS'] = _JDBCINFOPBS
DESCRIPTOR.message_types_by_name['DataComparisonResS'] = _DATACOMPARISONRESS
DESCRIPTOR.message_types_by_name['DataComparisonPBS'] = _DATACOMPARISONPBS
DESCRIPTOR.message_types_by_name['DataComparisonReqS'] = _DATACOMPARISONREQS
DESCRIPTOR.message_types_by_name['DataComparisonKey'] = _DATACOMPARISONKEY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServerInfoResS = _reflection.GeneratedProtocolMessageType('ServerInfoResS', (_message.Message,), {
  'DESCRIPTOR' : _SERVERINFORESS,
  '__module__' : 's_proto_pb2'
  # @@protoc_insertion_point(class_scope:ServerInfoResS)
  })
_sym_db.RegisterMessage(ServerInfoResS)

JdbcInfoPBS = _reflection.GeneratedProtocolMessageType('JdbcInfoPBS', (_message.Message,), {
  'DESCRIPTOR' : _JDBCINFOPBS,
  '__module__' : 's_proto_pb2'
  # @@protoc_insertion_point(class_scope:JdbcInfoPBS)
  })
_sym_db.RegisterMessage(JdbcInfoPBS)

DataComparisonResS = _reflection.GeneratedProtocolMessageType('DataComparisonResS', (_message.Message,), {
  'DESCRIPTOR' : _DATACOMPARISONRESS,
  '__module__' : 's_proto_pb2'
  # @@protoc_insertion_point(class_scope:DataComparisonResS)
  })
_sym_db.RegisterMessage(DataComparisonResS)

DataComparisonPBS = _reflection.GeneratedProtocolMessageType('DataComparisonPBS', (_message.Message,), {
  'DESCRIPTOR' : _DATACOMPARISONPBS,
  '__module__' : 's_proto_pb2'
  # @@protoc_insertion_point(class_scope:DataComparisonPBS)
  })
_sym_db.RegisterMessage(DataComparisonPBS)

DataComparisonReqS = _reflection.GeneratedProtocolMessageType('DataComparisonReqS', (_message.Message,), {
  'DESCRIPTOR' : _DATACOMPARISONREQS,
  '__module__' : 's_proto_pb2'
  # @@protoc_insertion_point(class_scope:DataComparisonReqS)
  })
_sym_db.RegisterMessage(DataComparisonReqS)

DataComparisonKey = _reflection.GeneratedProtocolMessageType('DataComparisonKey', (_message.Message,), {
  'DESCRIPTOR' : _DATACOMPARISONKEY,
  '__module__' : 's_proto_pb2'
  # @@protoc_insertion_point(class_scope:DataComparisonKey)
  })
_sym_db.RegisterMessage(DataComparisonKey)


# @@protoc_insertion_point(module_scope)
