import enums_pb2 as _enums_pb2
import action_pb2 as _action_pb2
import preview_pb2 as _preview_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RerollDiceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SwitchHandsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ChooseActiveRequest(_message.Message):
    __slots__ = ("candidate_ids",)
    CANDIDATE_IDS_FIELD_NUMBER: _ClassVar[int]
    candidate_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, candidate_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class ActionRequest(_message.Message):
    __slots__ = ("action",)
    ACTION_FIELD_NUMBER: _ClassVar[int]
    action: _containers.RepeatedCompositeFieldContainer[_action_pb2.Action]
    def __init__(self, action: _Optional[_Iterable[_Union[_action_pb2.Action, _Mapping]]] = ...) -> None: ...

class SelectCardRequest(_message.Message):
    __slots__ = ("candidate_definition_ids",)
    CANDIDATE_DEFINITION_IDS_FIELD_NUMBER: _ClassVar[int]
    candidate_definition_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, candidate_definition_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = ("reroll_dice", "switch_hands", "choose_active", "action", "select_card")
    REROLL_DICE_FIELD_NUMBER: _ClassVar[int]
    SWITCH_HANDS_FIELD_NUMBER: _ClassVar[int]
    CHOOSE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SELECT_CARD_FIELD_NUMBER: _ClassVar[int]
    reroll_dice: RerollDiceRequest
    switch_hands: SwitchHandsRequest
    choose_active: ChooseActiveRequest
    action: ActionRequest
    select_card: SelectCardRequest
    def __init__(self, reroll_dice: _Optional[_Union[RerollDiceRequest, _Mapping]] = ..., switch_hands: _Optional[_Union[SwitchHandsRequest, _Mapping]] = ..., choose_active: _Optional[_Union[ChooseActiveRequest, _Mapping]] = ..., action: _Optional[_Union[ActionRequest, _Mapping]] = ..., select_card: _Optional[_Union[SelectCardRequest, _Mapping]] = ...) -> None: ...

class RerollDiceResponse(_message.Message):
    __slots__ = ("dice_to_reroll",)
    DICE_TO_REROLL_FIELD_NUMBER: _ClassVar[int]
    dice_to_reroll: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, dice_to_reroll: _Optional[_Iterable[int]] = ...) -> None: ...

class SwitchHandsResponse(_message.Message):
    __slots__ = ("removed_hand_ids",)
    REMOVED_HAND_IDS_FIELD_NUMBER: _ClassVar[int]
    removed_hand_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, removed_hand_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class ChooseActiveResponse(_message.Message):
    __slots__ = ("active_character_id",)
    ACTIVE_CHARACTER_ID_FIELD_NUMBER: _ClassVar[int]
    active_character_id: int
    def __init__(self, active_character_id: _Optional[int] = ...) -> None: ...

class ActionResponse(_message.Message):
    __slots__ = ("chosen_action_index", "used_dice")
    CHOSEN_ACTION_INDEX_FIELD_NUMBER: _ClassVar[int]
    USED_DICE_FIELD_NUMBER: _ClassVar[int]
    chosen_action_index: int
    used_dice: _containers.RepeatedScalarFieldContainer[_enums_pb2.DiceType]
    def __init__(self, chosen_action_index: _Optional[int] = ..., used_dice: _Optional[_Iterable[_Union[_enums_pb2.DiceType, str]]] = ...) -> None: ...

class SelectCardResponse(_message.Message):
    __slots__ = ("selected_definition_id",)
    SELECTED_DEFINITION_ID_FIELD_NUMBER: _ClassVar[int]
    selected_definition_id: int
    def __init__(self, selected_definition_id: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("reroll_dice", "switch_hands", "choose_active", "action", "select_card")
    REROLL_DICE_FIELD_NUMBER: _ClassVar[int]
    SWITCH_HANDS_FIELD_NUMBER: _ClassVar[int]
    CHOOSE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SELECT_CARD_FIELD_NUMBER: _ClassVar[int]
    reroll_dice: RerollDiceResponse
    switch_hands: SwitchHandsResponse
    choose_active: ChooseActiveResponse
    action: ActionResponse
    select_card: SelectCardResponse
    def __init__(self, reroll_dice: _Optional[_Union[RerollDiceResponse, _Mapping]] = ..., switch_hands: _Optional[_Union[SwitchHandsResponse, _Mapping]] = ..., choose_active: _Optional[_Union[ChooseActiveResponse, _Mapping]] = ..., action: _Optional[_Union[ActionResponse, _Mapping]] = ..., select_card: _Optional[_Union[SelectCardResponse, _Mapping]] = ...) -> None: ...
