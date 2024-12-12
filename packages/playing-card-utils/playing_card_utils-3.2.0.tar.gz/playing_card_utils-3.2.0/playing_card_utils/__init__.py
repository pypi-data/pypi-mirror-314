"""
Initialize pycards module
"""
from typing import (
    Iterable,
    List
)
from .suites import Suite
from .card_type import CardType
from .card import Card
from .deck import CARDS_LIST

# Initialize suites
SUITES = [SPADES, HEARTS, CLUBS, DIAMONDS] = [
    Suite(code="S"), Suite(code="H"), Suite(code="C"), Suite(code="D")
]

# Initialize card types
CARD_TYPES = [
    ACE, TWO, THREE, FOUR, FIVE, SIX,
    SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING
    ] = [
        CardType(code="A"), CardType(code="2"), CardType(code="3"),
        CardType(code="4"), CardType(code="5"), CardType(code="6"),
        CardType(code="7"), CardType(code="8"), CardType(code="9"),
        CardType(code="T"), CardType(code="J"), CardType(code="Q"),
        CardType(code="K")
    ]

# Initialize cards
CARDS = [
    ACE_SPADES,
    TWO_SPADES,
    THREE_SPADES,
    FOUR_SPADES,
    FIVE_SPADES,
    SIX_SPADES,
    SEVEN_SPADES,
    EIGHT_SPADES,
    NINE_SPADES,
    TEN_SPADES,
    JACK_SPADES,
    QUEEN_SPADES,
    KING_SPADES,

    ACE_HEARTS,
    TWO_HEARTS,
    THREE_HEARTS,
    FOUR_HEARTS,
    FIVE_HEARTS,
    SIX_HEARTS,
    SEVEN_HEARTS,
    EIGHT_HEARTS,
    NINE_HEARTS,
    TEN_HEARTS,
    JACK_HEARTS,
    QUEEN_HEARTS,
    KING_HEARTS,

    ACE_CLUBS,
    TWO_CLUBS,
    THREE_CLUBS,
    FOUR_CLUBS,
    FIVE_CLUBS,
    SIX_CLUBS,
    SEVEN_CLUBS,
    EIGHT_CLUBS,
    NINE_CLUBS,
    TEN_CLUBS,
    JACK_CLUBS,
    QUEEN_CLUBS,
    KING_CLUBS,

    ACE_DIAMONDS,
    TWO_DIAMONDS,
    THREE_DIAMONDS,
    FOUR_DIAMONDS,
    FIVE_DIAMONDS,
    SIX_DIAMONDS,
    SEVEN_DIAMONDS,
    EIGHT_DIAMONDS,
    NINE_DIAMONDS,
    TEN_DIAMONDS,
    JACK_DIAMONDS,
    QUEEN_DIAMONDS,
    KING_DIAMONDS
] = CARDS_LIST


def sort_cards(cards: Iterable[Card], reverse: bool = False) -> List[Card]:
    """
    Sorts a list of cards in ascending or descending order based on the weight of their card types.

    Args:
        cards (Iterable[Card]): The list of cards to be sorted.
        reverse (bool, optional): If True, sorts the cards in descending order. Defaults to False.

    Returns:
        List[Card]: The sorted list of cards.
    """
    return sorted(cards, key=lambda card: card, reverse=reverse)


def same_suite(cards: Iterable[Card]) -> bool:
    """
    Check if all the cards in the given iterable have the same suite code.

    Parameters:
        cards (Iterable[Card]): An iterable of Card objects.

    Returns:
        bool: True if all the cards have the same suite code, False otherwise.
    """
    return len(set(map(lambda card: card.suite.code, cards))) == 1


def is_in_sequence(cards: List[Card]) -> bool:
    """
    Check if all the cards in the given list are in a sequential order.
    Parameters:
        cards (List[Card]): A list of Card objects to check for sequence.
    Returns:
        bool: True if the cards are in a sequence, False otherwise.
    """
    if len(cards) < 2:
        return True

    sorted_cards = sort_cards(cards=cards)

    # Check normal sequence
    for i in range(1, len(sorted_cards)):
        if sorted_cards[i].card_type.weight - sorted_cards[i - 1].card_type.weight != 1:
            break
    else:
        return True

    # Check special case for Ace as 1
    if sorted_cards[0].card_type.code == '2' and sorted_cards[-1].card_type.code == 'A':
        for i in range(1, len(sorted_cards) - 1):
            if sorted_cards[i].card_type.weight - sorted_cards[i - 1].card_type.weight != 1:
                return False
        return True

    return False


def count_by_suite(cards: Iterable[Card], suite: Suite) -> int:
    """
    Count the number of cards in the given iterable that belong to the specified suite.

    Args:
        cards (Iterable[Card]): An iterable of Card objects.
        suite (Suite): The Suite object representing the suite to count cards for.

    Returns:
        int: The number of cards in the iterable that belong to the specified suite.
    """
    return len([card for card in cards if card.suite == suite])


def count_by_card_type(cards: Iterable[Card], card_type: CardType) -> int:
    """
    Count the number of cards in the given iterable that belong to the specified card type.

    Args:
        cards (Iterable[Card]): An iterable of Card objects.
        card_type (CardType): The CardType object representing the card type to count cards for.

    Returns:
        int: The number of cards in the iterable that belong to the specified card type.
    """
    return len([card for card in cards if card.card_type == card_type])


def count_by_card(cards: Iterable[Card], card: Card) -> int:
    """
    Count the number of cards in the given iterable that are equal to the specified card.

    Args:
        cards (Iterable[Card]): An iterable of Card objects.
        card (Card): The Card object to count in the iterable.

    Returns:
        int: The number of cards in the iterable that are equal to the specified card.
    """
    return len([c for c in cards if c == card])
