import enums_pb2 as _enums_pb2
import mutation_pb2 as _mutation_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EquipmentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EQUIPMENT_OTHER: _ClassVar[EquipmentType]
    EQUIPMENT_WEAPON: _ClassVar[EquipmentType]
    EQUIPMENT_ARTIFACT: _ClassVar[EquipmentType]
    EQUIPMENT_TECHNIQUE: _ClassVar[EquipmentType]
EQUIPMENT_OTHER: EquipmentType
EQUIPMENT_WEAPON: EquipmentType
EQUIPMENT_ARTIFACT: EquipmentType
EQUIPMENT_TECHNIQUE: EquipmentType

class Notification(_message.Message):
    __slots__ = ("state", "mutation")
    STATE_FIELD_NUMBER: _ClassVar[int]
    MUTATION_FIELD_NUMBER: _ClassVar[int]
    state: State
    mutation: _containers.RepeatedCompositeFieldContainer[_mutation_pb2.ExposedMutation]
    def __init__(self, state: _Optional[_Union[State, _Mapping]] = ..., mutation: _Optional[_Iterable[_Union[_mutation_pb2.ExposedMutation, _Mapping]]] = ...) -> None: ...

class State(_message.Message):
    __slots__ = ("phase", "round_number", "current_turn", "winner", "player")
    PHASE_FIELD_NUMBER: _ClassVar[int]
    ROUND_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TURN_FIELD_NUMBER: _ClassVar[int]
    WINNER_FIELD_NUMBER: _ClassVar[int]
    PLAYER_FIELD_NUMBER: _ClassVar[int]
    phase: _mutation_pb2.PhaseType
    round_number: int
    current_turn: int
    winner: int
    player: _containers.RepeatedCompositeFieldContainer[PlayerState]
    def __init__(self, phase: _Optional[_Union[_mutation_pb2.PhaseType, str]] = ..., round_number: _Optional[int] = ..., current_turn: _Optional[int] = ..., winner: _Optional[int] = ..., player: _Optional[_Iterable[_Union[PlayerState, _Mapping]]] = ...) -> None: ...

class PlayerState(_message.Message):
    __slots__ = ("active_character_id", "character", "combat_status", "summon", "support", "dice", "pile_card", "hand_card", "declared_end", "legend_used", "initiative_skill")
    ACTIVE_CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    COMBAT_STATUS_FIELD_NUMBER: _ClassVar[int]
    SUMMON_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_FIELD_NUMBER: _ClassVar[int]
    DICE_FIELD_NUMBER: _ClassVar[int]
    PILE_CARD_FIELD_NUMBER: _ClassVar[int]
    HAND_CARD_FIELD_NUMBER: _ClassVar[int]
    DECLARED_END_FIELD_NUMBER: _ClassVar[int]
    LEGEND_USED_FIELD_NUMBER: _ClassVar[int]
    INITIATIVE_SKILL_FIELD_NUMBER: _ClassVar[int]
    active_character_id: int
    character: _containers.RepeatedCompositeFieldContainer[CharacterState]
    combat_status: _containers.RepeatedCompositeFieldContainer[EntityState]
    summon: _containers.RepeatedCompositeFieldContainer[EntityState]
    support: _containers.RepeatedCompositeFieldContainer[EntityState]
    dice: _containers.RepeatedScalarFieldContainer[_enums_pb2.DiceType]
    pile_card: _containers.RepeatedCompositeFieldContainer[CardState]
    hand_card: _containers.RepeatedCompositeFieldContainer[CardState]
    declared_end: bool
    legend_used: bool
    initiative_skill: _containers.RepeatedCompositeFieldContainer[SkillInfo]
    def __init__(self, active_character_id: _Optional[int] = ..., character: _Optional[_Iterable[_Union[CharacterState, _Mapping]]] = ..., combat_status: _Optional[_Iterable[_Union[EntityState, _Mapping]]] = ..., summon: _Optional[_Iterable[_Union[EntityState, _Mapping]]] = ..., support: _Optional[_Iterable[_Union[EntityState, _Mapping]]] = ..., dice: _Optional[_Iterable[_Union[_enums_pb2.DiceType, str]]] = ..., pile_card: _Optional[_Iterable[_Union[CardState, _Mapping]]] = ..., hand_card: _Optional[_Iterable[_Union[CardState, _Mapping]]] = ..., declared_end: bool = ..., legend_used: bool = ..., initiative_skill: _Optional[_Iterable[_Union[SkillInfo, _Mapping]]] = ...) -> None: ...

class CharacterState(_message.Message):
    __slots__ = ("id", "definition_id", "entity", "defeated", "health", "max_health", "energy", "max_energy", "aura")
    ID_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    DEFEATED_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    MAX_HEALTH_FIELD_NUMBER: _ClassVar[int]
    ENERGY_FIELD_NUMBER: _ClassVar[int]
    MAX_ENERGY_FIELD_NUMBER: _ClassVar[int]
    AURA_FIELD_NUMBER: _ClassVar[int]
    id: int
    definition_id: int
    entity: _containers.RepeatedCompositeFieldContainer[EntityState]
    defeated: bool
    health: int
    max_health: int
    energy: int
    max_energy: int
    aura: _enums_pb2.AuraType
    def __init__(self, id: _Optional[int] = ..., definition_id: _Optional[int] = ..., entity: _Optional[_Iterable[_Union[EntityState, _Mapping]]] = ..., defeated: bool = ..., health: _Optional[int] = ..., max_health: _Optional[int] = ..., energy: _Optional[int] = ..., max_energy: _Optional[int] = ..., aura: _Optional[_Union[_enums_pb2.AuraType, str]] = ...) -> None: ...

class EntityState(_message.Message):
    __slots__ = ("id", "definition_id", "description_dictionary", "variable_name", "variable_value", "hint_text", "hint_icon", "has_usage_per_round", "equipment")
    class DescriptionDictionaryEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    HINT_TEXT_FIELD_NUMBER: _ClassVar[int]
    HINT_ICON_FIELD_NUMBER: _ClassVar[int]
    HAS_USAGE_PER_ROUND_FIELD_NUMBER: _ClassVar[int]
    EQUIPMENT_FIELD_NUMBER: _ClassVar[int]
    id: int
    definition_id: int
    description_dictionary: _containers.ScalarMap[str, str]
    variable_name: str
    variable_value: int
    hint_text: str
    hint_icon: int
    has_usage_per_round: bool
    equipment: EquipmentType
    def __init__(self, id: _Optional[int] = ..., definition_id: _Optional[int] = ..., description_dictionary: _Optional[_Mapping[str, str]] = ..., variable_name: _Optional[str] = ..., variable_value: _Optional[int] = ..., hint_text: _Optional[str] = ..., hint_icon: _Optional[int] = ..., has_usage_per_round: bool = ..., equipment: _Optional[_Union[EquipmentType, str]] = ...) -> None: ...

class CardState(_message.Message):
    __slots__ = ("id", "definition_id", "description_dictionary", "definition_cost")
    class DescriptionDictionaryEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_COST_FIELD_NUMBER: _ClassVar[int]
    id: int
    definition_id: int
    description_dictionary: _containers.ScalarMap[str, str]
    definition_cost: _containers.RepeatedCompositeFieldContainer[_enums_pb2.DiceRequirement]
    def __init__(self, id: _Optional[int] = ..., definition_id: _Optional[int] = ..., description_dictionary: _Optional[_Mapping[str, str]] = ..., definition_cost: _Optional[_Iterable[_Union[_enums_pb2.DiceRequirement, _Mapping]]] = ...) -> None: ...

class SkillInfo(_message.Message):
    __slots__ = ("definition_id", "definition_cost")
    DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_COST_FIELD_NUMBER: _ClassVar[int]
    definition_id: int
    definition_cost: _containers.RepeatedCompositeFieldContainer[_enums_pb2.DiceRequirement]
    def __init__(self, definition_id: _Optional[int] = ..., definition_cost: _Optional[_Iterable[_Union[_enums_pb2.DiceRequirement, _Mapping]]] = ...) -> None: ...
