import mutation_pb2 as _mutation_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PreviewData(_message.Message):
    __slots__ = ("switch_active", "create_entity", "remove_entity", "modify_entity_var", "transform_definition", "elemental_reaction")
    SWITCH_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    CREATE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    REMOVE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    MODIFY_ENTITY_VAR_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    ELEMENTAL_REACTION_FIELD_NUMBER: _ClassVar[int]
    switch_active: _mutation_pb2.SwitchActiveEM
    create_entity: _mutation_pb2.CreateEntityEM
    remove_entity: _mutation_pb2.RemoveEntityEM
    modify_entity_var: _mutation_pb2.ModifyEntityVarEM
    transform_definition: _mutation_pb2.TransformDefinitionEM
    elemental_reaction: _mutation_pb2.ElementalReactionEM
    def __init__(self, switch_active: _Optional[_Union[_mutation_pb2.SwitchActiveEM, _Mapping]] = ..., create_entity: _Optional[_Union[_mutation_pb2.CreateEntityEM, _Mapping]] = ..., remove_entity: _Optional[_Union[_mutation_pb2.RemoveEntityEM, _Mapping]] = ..., modify_entity_var: _Optional[_Union[_mutation_pb2.ModifyEntityVarEM, _Mapping]] = ..., transform_definition: _Optional[_Union[_mutation_pb2.TransformDefinitionEM, _Mapping]] = ..., elemental_reaction: _Optional[_Union[_mutation_pb2.ElementalReactionEM, _Mapping]] = ...) -> None: ...
