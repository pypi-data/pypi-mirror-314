"""Card Class"""

from dataclasses import dataclass
from typing import Any
from .suites import Suite
from .card_type import CardType


@dataclass
class Card:
    """Card"""
    suite: Suite
    card_type: CardType

    @property
    def name(self) -> str:
        """Get name of the card"""
        return f"{self.card_type.name} of {self.suite.name}"

    def __str__(self) -> str:
        """Card string representation"""
        return f"{self.card_type.code}{self.suite.symbol}"

    def __repr__(self) -> str:
        """Card representation"""
        return f"{self.card_type.code}{self.suite.symbol}"

    def __eq__(self, other: Any) -> bool:
        """Card equality"""
        if isinstance(other, Card):
            return all(
                [
                    self.card_type.code == other.card_type.code,
                    self.suite.code == other.suite.code
                ]
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.card_type.code, self.suite.code))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight < other.card_type.weight
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight <= other.card_type.weight
        return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight > other.card_type.weight
        return False

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight >= other.card_type.weight
        return False
