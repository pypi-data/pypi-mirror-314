import enums_pb2 as _enums_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PhaseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PHASE_INIT_HANDS: _ClassVar[PhaseType]
    PHASE_INIT_ACTIVES: _ClassVar[PhaseType]
    PHASE_ROLL: _ClassVar[PhaseType]
    PHASE_ACTION: _ClassVar[PhaseType]
    PHASE_END: _ClassVar[PhaseType]
    PHASE_GAME_END: _ClassVar[PhaseType]

class CardArea(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CARD_AREA_HAND: _ClassVar[CardArea]
    CARD_AREA_PILE: _ClassVar[CardArea]

class RemoveCardReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REMOVE_CARD_REASON_UNSPECIFIED: _ClassVar[RemoveCardReason]
    REMOVE_CARD_REASON_PLAY: _ClassVar[RemoveCardReason]
    REMOVE_CARD_REASON_ELEMENTAL_TUNING: _ClassVar[RemoveCardReason]
    REMOVE_CARD_REASON_HANDS_OVERFLOW: _ClassVar[RemoveCardReason]
    REMOVE_CARD_REASON_DISPOSED: _ClassVar[RemoveCardReason]
    REMOVE_CARD_REASON_DISABLED: _ClassVar[RemoveCardReason]
    REMOVE_CARD_REASON_ON_DRAW_TRIGGERED: _ClassVar[RemoveCardReason]

class CreateEntityArea(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENTITY_AREA_UNSPECIFIED: _ClassVar[CreateEntityArea]
    ENTITY_AREA_CHARACTER: _ClassVar[CreateEntityArea]
    ENTITY_AREA_COMBAT_STATUS: _ClassVar[CreateEntityArea]
    ENTITY_AREA_SUMMON: _ClassVar[CreateEntityArea]
    ENTITY_AREA_SUPPORT: _ClassVar[CreateEntityArea]

class ActionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_UNSPECIFIED: _ClassVar[ActionType]
    ACTION_USE_SKILL: _ClassVar[ActionType]
    ACTION_PLAY_CARD: _ClassVar[ActionType]
    ACTION_SWITCH_ACTIVE: _ClassVar[ActionType]
    ACTION_ELEMENTAL_TUNING: _ClassVar[ActionType]
    ACTION_DECLARE_END: _ClassVar[ActionType]

class PlayerStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PLAYER_STATUS_UNSPECIFIED: _ClassVar[PlayerStatus]
    PLAYER_STATUS_CHOOSING_ACTIVE: _ClassVar[PlayerStatus]
    PLAYER_STATUS_SWITCHING_HANDS: _ClassVar[PlayerStatus]
    PLAYER_STATUS_REROLLING: _ClassVar[PlayerStatus]
    PLAYER_STATUS_ACTING: _ClassVar[PlayerStatus]
    PLAYER_STATUS_SELECTING_CARDS: _ClassVar[PlayerStatus]
PHASE_INIT_HANDS: PhaseType
PHASE_INIT_ACTIVES: PhaseType
PHASE_ROLL: PhaseType
PHASE_ACTION: PhaseType
PHASE_END: PhaseType
PHASE_GAME_END: PhaseType
CARD_AREA_HAND: CardArea
CARD_AREA_PILE: CardArea
REMOVE_CARD_REASON_UNSPECIFIED: RemoveCardReason
REMOVE_CARD_REASON_PLAY: RemoveCardReason
REMOVE_CARD_REASON_ELEMENTAL_TUNING: RemoveCardReason
REMOVE_CARD_REASON_HANDS_OVERFLOW: RemoveCardReason
REMOVE_CARD_REASON_DISPOSED: RemoveCardReason
REMOVE_CARD_REASON_DISABLED: RemoveCardReason
REMOVE_CARD_REASON_ON_DRAW_TRIGGERED: RemoveCardReason
ENTITY_AREA_UNSPECIFIED: CreateEntityArea
ENTITY_AREA_CHARACTER: CreateEntityArea
ENTITY_AREA_COMBAT_STATUS: CreateEntityArea
ENTITY_AREA_SUMMON: CreateEntityArea
ENTITY_AREA_SUPPORT: CreateEntityArea
ACTION_UNSPECIFIED: ActionType
ACTION_USE_SKILL: ActionType
ACTION_PLAY_CARD: ActionType
ACTION_SWITCH_ACTIVE: ActionType
ACTION_ELEMENTAL_TUNING: ActionType
ACTION_DECLARE_END: ActionType
PLAYER_STATUS_UNSPECIFIED: PlayerStatus
PLAYER_STATUS_CHOOSING_ACTIVE: PlayerStatus
PLAYER_STATUS_SWITCHING_HANDS: PlayerStatus
PLAYER_STATUS_REROLLING: PlayerStatus
PLAYER_STATUS_ACTING: PlayerStatus
PLAYER_STATUS_SELECTING_CARDS: PlayerStatus

class ExposedMutation(_message.Message):
    __slots__ = ("change_phase", "step_round", "switch_turn", "set_winner", "transfer_card", "switch_active", "remove_card", "create_card", "create_character", "create_entity", "remove_entity", "modify_entity_var", "transform_definition", "reset_dice", "damage", "elemental_reaction", "action_done", "triggered", "player_status_change")
    CHANGE_PHASE_FIELD_NUMBER: _ClassVar[int]
    STEP_ROUND_FIELD_NUMBER: _ClassVar[int]
    SWITCH_TURN_FIELD_NUMBER: _ClassVar[int]
    SET_WINNER_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_CARD_FIELD_NUMBER: _ClassVar[int]
    SWITCH_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    REMOVE_CARD_FIELD_NUMBER: _ClassVar[int]
    CREATE_CARD_FIELD_NUMBER: _ClassVar[int]
    CREATE_CHARACTER_FIELD_NUMBER: _ClassVar[int]
    CREATE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    REMOVE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    MODIFY_ENTITY_VAR_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    RESET_DICE_FIELD_NUMBER: _ClassVar[int]
    DAMAGE_FIELD_NUMBER: _ClassVar[int]
    ELEMENTAL_REACTION_FIELD_NUMBER: _ClassVar[int]
    ACTION_DONE_FIELD_NUMBER: _ClassVar[int]
    TRIGGERED_FIELD_NUMBER: _ClassVar[int]
    PLAYER_STATUS_CHANGE_FIELD_NUMBER: _ClassVar[int]
    change_phase: ChangePhaseEM
    step_round: StepRoundEM
    switch_turn: SwitchTurnEM
    set_winner: SetWinnerEM
    transfer_card: TransferCardEM
    switch_active: SwitchActiveEM
    remove_card: RemoveCardEM
    create_card: CreateCardEM
    create_character: CreateCharacterEM
    create_entity: CreateEntityEM
    remove_entity: RemoveEntityEM
    modify_entity_var: ModifyEntityVarEM
    transform_definition: TransformDefinitionEM
    reset_dice: ResetDiceEM
    damage: DamageEM
    elemental_reaction: ElementalReactionEM
    action_done: ActionDoneEM
    triggered: TriggeredEM
    player_status_change: PlayerStatusChangeEM
    def __init__(self, change_phase: _Optional[_Union[ChangePhaseEM, _Mapping]] = ..., step_round: _Optional[_Union[StepRoundEM, _Mapping]] = ..., switch_turn: _Optional[_Union[SwitchTurnEM, _Mapping]] = ..., set_winner: _Optional[_Union[SetWinnerEM, _Mapping]] = ..., transfer_card: _Optional[_Union[TransferCardEM, _Mapping]] = ..., switch_active: _Optional[_Union[SwitchActiveEM, _Mapping]] = ..., remove_card: _Optional[_Union[RemoveCardEM, _Mapping]] = ..., create_card: _Optional[_Union[CreateCardEM, _Mapping]] = ..., create_character: _Optional[_Union[CreateCharacterEM, _Mapping]] = ..., create_entity: _Optional[_Union[CreateEntityEM, _Mapping]] = ..., remove_entity: _Optional[_Union[RemoveEntityEM, _Mapping]] = ..., modify_entity_var: _Optional[_Union[ModifyEntityVarEM, _Mapping]] = ..., transform_definition: _Optional[_Union[TransformDefinitionEM, _Mapping]] = ..., reset_dice: _Optional[_Union[ResetDiceEM, _Mapping]] = ..., damage: _Optional[_Union[DamageEM, _Mapping]] = ..., elemental_reaction: _Optional[_Union[ElementalReactionEM, _Mapping]] = ..., action_done: _Optional[_Union[ActionDoneEM, _Mapping]] = ..., triggered: _Optional[_Union[TriggeredEM, _Mapping]] = ..., player_status_change: _Optional[_Union[PlayerStatusChangeEM, _Mapping]] = ...) -> None: ...

class ChangePhaseEM(_message.Message):
    __slots__ = ("new_phase",)
    NEW_PHASE_FIELD_NUMBER: _ClassVar[int]
    new_phase: PhaseType
    def __init__(self, new_phase: _Optional[_Union[PhaseType, str]] = ...) -> None: ...

class StepRoundEM(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SwitchTurnEM(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SetWinnerEM(_message.Message):
    __slots__ = ("winner",)
    WINNER_FIELD_NUMBER: _ClassVar[int]
    winner: int
    def __init__(self, winner: _Optional[int] = ...) -> None: ...

class TransferCardEM(_message.Message):
    __slots__ = ("who", "card_id", "card_definition_id", "to", "transfer_to_opp")
    WHO_FIELD_NUMBER: _ClassVar[int]
    CARD_ID_FIELD_NUMBER: _ClassVar[int]
    CARD_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_TO_OPP_FIELD_NUMBER: _ClassVar[int]
    who: int
    card_id: int
    card_definition_id: int
    to: CardArea
    transfer_to_opp: bool
    def __init__(self, who: _Optional[int] = ..., card_id: _Optional[int] = ..., card_definition_id: _Optional[int] = ..., to: _Optional[_Union[CardArea, str]] = ..., transfer_to_opp: bool = ..., **kwargs) -> None: ...

class SwitchActiveEM(_message.Message):
    __slots__ = ("who", "character_id", "character_definition_id", "via_skill_id")
    WHO_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    VIA_SKILL_ID_FIELD_NUMBER: _ClassVar[int]
    who: int
    character_id: int
    character_definition_id: int
    via_skill_id: int
    def __init__(self, who: _Optional[int] = ..., character_id: _Optional[int] = ..., character_definition_id: _Optional[int] = ..., via_skill_id: _Optional[int] = ...) -> None: ...

class RemoveCardEM(_message.Message):
    __slots__ = ("who", "card_id", "card_definition_id", "reason")
    WHO_FIELD_NUMBER: _ClassVar[int]
    CARD_ID_FIELD_NUMBER: _ClassVar[int]
    CARD_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    who: int
    card_id: int
    card_definition_id: int
    reason: RemoveCardReason
    def __init__(self, who: _Optional[int] = ..., card_id: _Optional[int] = ..., card_definition_id: _Optional[int] = ..., reason: _Optional[_Union[RemoveCardReason, str]] = ..., **kwargs) -> None: ...

class CreateCardEM(_message.Message):
    __slots__ = ("who", "card_id", "card_definition_id", "to")
    WHO_FIELD_NUMBER: _ClassVar[int]
    CARD_ID_FIELD_NUMBER: _ClassVar[int]
    CARD_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    who: int
    card_id: int
    card_definition_id: int
    to: CardArea
    def __init__(self, who: _Optional[int] = ..., card_id: _Optional[int] = ..., card_definition_id: _Optional[int] = ..., to: _Optional[_Union[CardArea, str]] = ...) -> None: ...

class CreateCharacterEM(_message.Message):
    __slots__ = ("who", "character_id", "character_definition_id")
    WHO_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    who: int
    character_id: int
    character_definition_id: int
    def __init__(self, who: _Optional[int] = ..., character_id: _Optional[int] = ..., character_definition_id: _Optional[int] = ...) -> None: ...

class CreateEntityEM(_message.Message):
    __slots__ = ("who", "entity_id", "entity_definition_id", "where")
    WHO_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    WHERE_FIELD_NUMBER: _ClassVar[int]
    who: int
    entity_id: int
    entity_definition_id: int
    where: CreateEntityArea
    def __init__(self, who: _Optional[int] = ..., entity_id: _Optional[int] = ..., entity_definition_id: _Optional[int] = ..., where: _Optional[_Union[CreateEntityArea, str]] = ...) -> None: ...

class RemoveEntityEM(_message.Message):
    __slots__ = ("entity_id", "entity_definition_id")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    entity_definition_id: int
    def __init__(self, entity_id: _Optional[int] = ..., entity_definition_id: _Optional[int] = ...) -> None: ...

class ModifyEntityVarEM(_message.Message):
    __slots__ = ("entity_id", "entity_definition_id", "variable_name", "variable_value")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    entity_definition_id: int
    variable_name: str
    variable_value: int
    def __init__(self, entity_id: _Optional[int] = ..., entity_definition_id: _Optional[int] = ..., variable_name: _Optional[str] = ..., variable_value: _Optional[int] = ...) -> None: ...

class TransformDefinitionEM(_message.Message):
    __slots__ = ("entity_id", "new_entity_definition_id")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_ENTITY_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    new_entity_definition_id: int
    def __init__(self, entity_id: _Optional[int] = ..., new_entity_definition_id: _Optional[int] = ...) -> None: ...

class ResetDiceEM(_message.Message):
    __slots__ = ("who", "dice")
    WHO_FIELD_NUMBER: _ClassVar[int]
    DICE_FIELD_NUMBER: _ClassVar[int]
    who: int
    dice: _containers.RepeatedScalarFieldContainer[_enums_pb2.DiceType]
    def __init__(self, who: _Optional[int] = ..., dice: _Optional[_Iterable[_Union[_enums_pb2.DiceType, str]]] = ...) -> None: ...

class DamageEM(_message.Message):
    __slots__ = ("type", "value", "target_id", "target_definition_id", "source_id", "source_definition_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    type: _enums_pb2.DamageType
    value: int
    target_id: int
    target_definition_id: int
    source_id: int
    source_definition_id: int
    def __init__(self, type: _Optional[_Union[_enums_pb2.DamageType, str]] = ..., value: _Optional[int] = ..., target_id: _Optional[int] = ..., target_definition_id: _Optional[int] = ..., source_id: _Optional[int] = ..., source_definition_id: _Optional[int] = ...) -> None: ...

class ElementalReactionEM(_message.Message):
    __slots__ = ("type", "character_id", "character_definition_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    type: _enums_pb2.ReactionType
    character_id: int
    character_definition_id: int
    def __init__(self, type: _Optional[_Union[_enums_pb2.ReactionType, str]] = ..., character_id: _Optional[int] = ..., character_definition_id: _Optional[int] = ...) -> None: ...

class ActionDoneEM(_message.Message):
    __slots__ = ("who", "action_type", "character_or_card_id", "skill_or_card_definition_id", "character_definition_id")
    WHO_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_OR_CARD_ID_FIELD_NUMBER: _ClassVar[int]
    SKILL_OR_CARD_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    who: int
    action_type: ActionType
    character_or_card_id: int
    skill_or_card_definition_id: int
    character_definition_id: int
    def __init__(self, who: _Optional[int] = ..., action_type: _Optional[_Union[ActionType, str]] = ..., character_or_card_id: _Optional[int] = ..., skill_or_card_definition_id: _Optional[int] = ..., character_definition_id: _Optional[int] = ...) -> None: ...

class TriggeredEM(_message.Message):
    __slots__ = ("entity_id", "entity_definition_id")
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    entity_id: int
    entity_definition_id: int
    def __init__(self, entity_id: _Optional[int] = ..., entity_definition_id: _Optional[int] = ...) -> None: ...

class PlayerStatusChangeEM(_message.Message):
    __slots__ = ("who", "status")
    WHO_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    who: int
    status: PlayerStatus
    def __init__(self, who: _Optional[int] = ..., status: _Optional[_Union[PlayerStatus, str]] = ...) -> None: ...
