"""Card type module"""

from dataclasses import dataclass
from typing import Any

# Initialize card type codes
CARD_TYPE_CODES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]

# Initialize card type names
code_to_name = {
    "A": "Ace",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
    "T": "Ten",
    "J": "Jack",
    "Q": "Queen",
    "K": "King",
}

# Initialize card type weights
code_to_weight = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

code_to_alphaweight = {
    "2": "A",
    "3": "B",
    "4": "C",
    "5": "D",
    "6": "E",
    "7": "F",
    "8": "G",
    "9": "H",
    "T": "I",
    "J": "J",
    "Q": "K",
    "K": "L",
    "A": "M"
}

# Initialize rank order
rank_order = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


@dataclass
class CardType:
    """
    Represents a type of card.

    Attributes:
        code (str): The code representing the type of the card.

    Methods:
        __post_init__(self): Validates the card type code.
    """
    code: str  # A 2 3 4 5 6 7 8 9 T J Q K

    def __post_init__(self) -> None:
        """
        Validates the card type code.

        This method is called automatically after the CardType object is created.
        It checks if the `code` attribute of the CardType object is present
        in the `CARD_TYPE_CODES` list.
        If the `code` is not present in the list, it raises a `ValueError`
        with a message indicating the invalid card type code.

        Parameters:
            self (CardType): The CardType object.

        Returns:
            None: This method does not return anything.

        Raises:
            ValueError: If the `code` attribute of the CardType object is
                        not present in the `CARD_TYPE_CODES` list.
        """
        if self.code not in CARD_TYPE_CODES:
            raise ValueError(f"Invalid card type code {self.code}")

    @property
    def name(self) -> str:
        """Get name of the card type"""
        return code_to_name[self.code]

    @property
    def weight(self) -> int:
        """Get weight of the card type"""
        return code_to_weight[self.code]

    @property
    def alphaweight(self) -> str:
        """Get alphaweight of the card type"""
        return code_to_alphaweight[self.code]

    def __str__(self) -> str:
        return self.code

    def __repr__(self) -> str:
        return self.code

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, CardType):
            return self.code == other.code
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, CardType):
            return code_to_weight[self.code] < code_to_weight[other.code]
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, CardType):
            return code_to_weight[self.code] <= code_to_weight[other.code]
        return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, CardType):
            return code_to_weight[self.code] > code_to_weight[other.code]
        return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, CardType):
            return code_to_weight[self.code] >= code_to_weight[other.code]
        return NotImplemented
