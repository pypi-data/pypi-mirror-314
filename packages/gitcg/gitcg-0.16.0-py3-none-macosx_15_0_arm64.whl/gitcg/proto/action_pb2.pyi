import enums_pb2 as _enums_pb2
import preview_pb2 as _preview_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(_message.Message):
    __slots__ = ("switch_active", "play_card", "use_skill", "elemental_tuning", "declare_end", "preview", "required_cost")
    SWITCH_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    PLAY_CARD_FIELD_NUMBER: _ClassVar[int]
    USE_SKILL_FIELD_NUMBER: _ClassVar[int]
    ELEMENTAL_TUNING_FIELD_NUMBER: _ClassVar[int]
    DECLARE_END_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_COST_FIELD_NUMBER: _ClassVar[int]
    switch_active: SwitchActiveAction
    play_card: PlayCardAction
    use_skill: UseSkillAction
    elemental_tuning: ElementalTuningAction
    declare_end: DeclareEndAction
    preview: _containers.RepeatedCompositeFieldContainer[_preview_pb2.PreviewData]
    required_cost: _containers.RepeatedCompositeFieldContainer[_enums_pb2.DiceRequirement]
    def __init__(self, switch_active: _Optional[_Union[SwitchActiveAction, _Mapping]] = ..., play_card: _Optional[_Union[PlayCardAction, _Mapping]] = ..., use_skill: _Optional[_Union[UseSkillAction, _Mapping]] = ..., elemental_tuning: _Optional[_Union[ElementalTuningAction, _Mapping]] = ..., declare_end: _Optional[_Union[DeclareEndAction, _Mapping]] = ..., preview: _Optional[_Iterable[_Union[_preview_pb2.PreviewData, _Mapping]]] = ..., required_cost: _Optional[_Iterable[_Union[_enums_pb2.DiceRequirement, _Mapping]]] = ...) -> None: ...

class SwitchActiveAction(_message.Message):
    __slots__ = ("character_id",)
    CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    character_id: int
    def __init__(self, character_id: _Optional[int] = ...) -> None: ...

class PlayCardAction(_message.Message):
    __slots__ = ("card_id", "target_ids")
    CARD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_IDS_FIELD_NUMBER: _ClassVar[int]
    card_id: int
    target_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, card_id: _Optional[int] = ..., target_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class UseSkillAction(_message.Message):
    __slots__ = ("skill_id", "target_ids")
    SKILL_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_IDS_FIELD_NUMBER: _ClassVar[int]
    skill_id: int
    target_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, skill_id: _Optional[int] = ..., target_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class ElementalTuningAction(_message.Message):
    __slots__ = ("removed_card_id", "target_dice")
    REMOVED_CARD_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_DICE_FIELD_NUMBER: _ClassVar[int]
    removed_card_id: int
    target_dice: _enums_pb2.DiceType
    def __init__(self, removed_card_id: _Optional[int] = ..., target_dice: _Optional[_Union[_enums_pb2.DiceType, str]] = ...) -> None: ...

class DeclareEndAction(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
