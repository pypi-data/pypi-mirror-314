"""Suites"""

from dataclasses import dataclass
from typing import Any

SUITE_CODES = ["S", "H", "C", "D"]


@dataclass
class Suite:
    """Represents a suite of cards in a standard deck.

    Attributes:
        code (str): The code representing the suite, e.g., 'S' for Spades.

    Raises:
        ValueError: If an invalid suite code is provided.

    Example:
        Creating a Suite object:
        suite = Suite(code="S")
    """

    code: str

    def __post_init__(self) -> None:
        """
        Initializes the object after its creation.

        This method is called automatically after the object is created.
        It checks if the provided code is a valid suite code.
        If the code is not in the list of valid suite codes,
        it raises a ValueError with the message "Invalid suite code: {self.code}".

        Parameters:
            None

        Returns:
            None
        """
        if self.code not in SUITE_CODES:
            raise ValueError(f"Invalid suite code: {self.code}")

    @property
    def name(self) -> str:
        """Get name of the suite"""
        suite_names = {
            "S": "Spades",
            "H": "Hearts",
            "C": "Clubs",
            "D": "Diamonds"
        }
        return suite_names[self.code]

    @property
    def symbol(self) -> str:
        """Get symbol of the suite"""
        suite_symbols = {
            "S": "♠",
            "H": "♥",
            "C": "♣",
            "D": "♦"
        }
        return suite_symbols[self.code]

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return self.symbol

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Suite):
            return self.code == other.code
        return NotImplemented
