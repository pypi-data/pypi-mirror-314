import re
import string
from dataclasses import dataclass
from typing import Optional
from enum import IntEnum

__all__ = [
    "Rarity",
    "SkinMetadatum",
    "StickerMetadatum",
    "ItemMetadatum",
    "SkinContainerEntry",
    "ItemContainerEntry",
    "ContainerEntry",
    "GenericContainer",
    "SkinCase",
    "SouvenirPackage",
    "StickerCapsule",
    "Container",
    "remove_skin_name_formatting",
]


class Rarity(IntEnum):
    Common = 0
    Uncommon = 1
    Rare = 2
    Mythical = 3
    Legendary = 4
    Ancient = 5
    Contraband = 6

    def get_name_for_skin(self) -> str:
        """
        Get the rarity string if the item is a skin
        """
        return [
            "Consumer Grade",
            "Industrial Grade",
            "Mil-Spec",
            "Restricted",
            "Classified",
            "Covert",
            "Contraband",
        ][self.value]

    def get_name_for_regular_item(self) -> str:
        """
        Get the rarity string if the item is a regular item
        """
        return [
            "Base Grade",
            "Industrial Grade",
            "High Grade",
            "Remarkable",
            "Exotic",
            "Extraordinary",
            "Contraband",
        ][self.value]


@dataclass
class SkinMetadatum:
    formatted_name: str
    rarity: Rarity
    price: int
    image_url: str
    description: Optional[str]
    min_float: float
    max_float: float


@dataclass
class StickerMetadatum:
    formatted_name: str
    rarity: Rarity
    price: int
    image_url: str


type ItemMetadatum = SkinMetadatum | StickerMetadatum


@dataclass
class SkinContainerEntry:
    unformatted_name: str
    min_float: float
    max_float: float


@dataclass
class ItemContainerEntry:
    unformatted_name: str


type ContainerEntry = SkinContainerEntry | ItemContainerEntry


@dataclass
class GenericContainer[T: ContainerEntry]:
    formatted_name: str
    price: int
    image_url: str
    requires_key: bool
    contains: dict[Rarity, list[T]]
    contains_rare: list[T]


@dataclass
class SkinCase(GenericContainer[SkinContainerEntry]):
    pass


@dataclass
class SouvenirPackage(GenericContainer[SkinContainerEntry]):
    pass


@dataclass
class StickerCapsule(GenericContainer[ItemContainerEntry]):
    pass


type Container = SkinCase | SouvenirPackage | StickerCapsule

_SPECIAL_CHARS_REGEX = re.compile(r"[™★♥\s]")


def remove_skin_name_formatting(skin_name: str) -> str:
    """
    Removes formatting from skin names:
    - Converts to lowercase
    - Removes punctuation, whitespace and special characters
    """
    skin_name = _SPECIAL_CHARS_REGEX.sub("", skin_name.lower())
    return skin_name.translate(str.maketrans("", "", string.punctuation))
