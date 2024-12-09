from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiceRequirementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DICE_REQ_VOID: _ClassVar[DiceRequirementType]
    DICE_REQ_CRYO: _ClassVar[DiceRequirementType]
    DICE_REQ_HYDRO: _ClassVar[DiceRequirementType]
    DICE_REQ_PYRO: _ClassVar[DiceRequirementType]
    DICE_REQ_ELECTRO: _ClassVar[DiceRequirementType]
    DICE_REQ_ANEMO: _ClassVar[DiceRequirementType]
    DICE_REQ_GEO: _ClassVar[DiceRequirementType]
    DICE_REQ_DENDRO: _ClassVar[DiceRequirementType]
    DICE_REQ_ALIGNED: _ClassVar[DiceRequirementType]
    DICE_REQ_ENERGY: _ClassVar[DiceRequirementType]
    DICE_REQ_LEGEND: _ClassVar[DiceRequirementType]

class DiceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DICE_UNSPECIFIED: _ClassVar[DiceType]
    DICE_CRYO: _ClassVar[DiceType]
    DICE_HYDRO: _ClassVar[DiceType]
    DICE_PYRO: _ClassVar[DiceType]
    DICE_ELECTRO: _ClassVar[DiceType]
    DICE_ANEMO: _ClassVar[DiceType]
    DICE_GEO: _ClassVar[DiceType]
    DICE_DENDRO: _ClassVar[DiceType]
    DICE_OMNI: _ClassVar[DiceType]

class DamageType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DMG_PHYSICAL: _ClassVar[DamageType]
    DMG_CRYO: _ClassVar[DamageType]
    DMG_HYDRO: _ClassVar[DamageType]
    DMG_PYRO: _ClassVar[DamageType]
    DMG_ELECTRO: _ClassVar[DamageType]
    DMG_ANEMO: _ClassVar[DamageType]
    DMG_GEO: _ClassVar[DamageType]
    DMG_DENDRO: _ClassVar[DamageType]
    DMG_PIERCING: _ClassVar[DamageType]
    DMG_HEAL: _ClassVar[DamageType]

class AuraType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AURA_NONE: _ClassVar[AuraType]
    AURA_CRYO: _ClassVar[AuraType]
    AURA_HYDRO: _ClassVar[AuraType]
    AURA_PYRO: _ClassVar[AuraType]
    AURA_ELECTRO: _ClassVar[AuraType]
    AURA_DENDRO: _ClassVar[AuraType]
    AURA_CRYO_DENDRO: _ClassVar[AuraType]

class ReactionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REACTION_UNSPECIFIED: _ClassVar[ReactionType]
    REACTION_MELT: _ClassVar[ReactionType]
    REACTION_VAPORIZE: _ClassVar[ReactionType]
    REACTION_OVERLOADED: _ClassVar[ReactionType]
    REACTION_SUPERCONDUCT: _ClassVar[ReactionType]
    REACTION_ELECTRO_CHARGED: _ClassVar[ReactionType]
    REACTION_FROZEN: _ClassVar[ReactionType]
    REACTION_SWIRL_CRYO: _ClassVar[ReactionType]
    REACTION_SWIRL_HYDRO: _ClassVar[ReactionType]
    REACTION_SWIRL_PYRO: _ClassVar[ReactionType]
    REACTION_SWIRL_ELECTRO: _ClassVar[ReactionType]
    REACTION_CRYSTALLIZE_CRYO: _ClassVar[ReactionType]
    REACTION_CRYSTALLIZE_HYDRO: _ClassVar[ReactionType]
    REACTION_CRYSTALLIZE_PYRO: _ClassVar[ReactionType]
    REACTION_CRYSTALLIZE_ELECTRO: _ClassVar[ReactionType]
    REACTION_BURNING: _ClassVar[ReactionType]
    REACTION_BLOOM: _ClassVar[ReactionType]
    REACTION_QUICKEN: _ClassVar[ReactionType]
DICE_REQ_VOID: DiceRequirementType
DICE_REQ_CRYO: DiceRequirementType
DICE_REQ_HYDRO: DiceRequirementType
DICE_REQ_PYRO: DiceRequirementType
DICE_REQ_ELECTRO: DiceRequirementType
DICE_REQ_ANEMO: DiceRequirementType
DICE_REQ_GEO: DiceRequirementType
DICE_REQ_DENDRO: DiceRequirementType
DICE_REQ_ALIGNED: DiceRequirementType
DICE_REQ_ENERGY: DiceRequirementType
DICE_REQ_LEGEND: DiceRequirementType
DICE_UNSPECIFIED: DiceType
DICE_CRYO: DiceType
DICE_HYDRO: DiceType
DICE_PYRO: DiceType
DICE_ELECTRO: DiceType
DICE_ANEMO: DiceType
DICE_GEO: DiceType
DICE_DENDRO: DiceType
DICE_OMNI: DiceType
DMG_PHYSICAL: DamageType
DMG_CRYO: DamageType
DMG_HYDRO: DamageType
DMG_PYRO: DamageType
DMG_ELECTRO: DamageType
DMG_ANEMO: DamageType
DMG_GEO: DamageType
DMG_DENDRO: DamageType
DMG_PIERCING: DamageType
DMG_HEAL: DamageType
AURA_NONE: AuraType
AURA_CRYO: AuraType
AURA_HYDRO: AuraType
AURA_PYRO: AuraType
AURA_ELECTRO: AuraType
AURA_DENDRO: AuraType
AURA_CRYO_DENDRO: AuraType
REACTION_UNSPECIFIED: ReactionType
REACTION_MELT: ReactionType
REACTION_VAPORIZE: ReactionType
REACTION_OVERLOADED: ReactionType
REACTION_SUPERCONDUCT: ReactionType
REACTION_ELECTRO_CHARGED: ReactionType
REACTION_FROZEN: ReactionType
REACTION_SWIRL_CRYO: ReactionType
REACTION_SWIRL_HYDRO: ReactionType
REACTION_SWIRL_PYRO: ReactionType
REACTION_SWIRL_ELECTRO: ReactionType
REACTION_CRYSTALLIZE_CRYO: ReactionType
REACTION_CRYSTALLIZE_HYDRO: ReactionType
REACTION_CRYSTALLIZE_PYRO: ReactionType
REACTION_CRYSTALLIZE_ELECTRO: ReactionType
REACTION_BURNING: ReactionType
REACTION_BLOOM: ReactionType
REACTION_QUICKEN: ReactionType

class DiceRequirement(_message.Message):
    __slots__ = ("type", "count")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    type: DiceRequirementType
    count: int
    def __init__(self, type: _Optional[_Union[DiceRequirementType, str]] = ..., count: _Optional[int] = ...) -> None: ...
