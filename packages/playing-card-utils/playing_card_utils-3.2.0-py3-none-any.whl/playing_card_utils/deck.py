"""Class deck"""

from random import shuffle, randint
from typing import Iterator, Iterable, List, Dict
from .card import Card
from .suites import Suite
from .card_type import CardType
from .exceptions import CardError, NotEnoughCardsError

SPADES = Suite(code="S")
HEARTS = Suite(code="H")
CLUBS = Suite(code="C")
DIAMONDS = Suite(code="D")

ACE = CardType(code="A")
TWO = CardType(code="2")
THREE = CardType(code="3")
FOUR = CardType(code="4")
FIVE = CardType(code="5")
SIX = CardType(code="6")
SEVEN = CardType(code="7")
EIGHT = CardType(code="8")
NINE = CardType(code="9")
TEN = CardType(code="T")
JACK = CardType(code="J")
QUEEN = CardType(code="Q")
KING = CardType(code="K")


# Initialize cards list
CARDS_LIST = [
    Card(suite=SPADES, card_type=ACE),
    Card(suite=SPADES, card_type=TWO),
    Card(suite=SPADES, card_type=THREE),
    Card(suite=SPADES, card_type=FOUR),
    Card(suite=SPADES, card_type=FIVE),
    Card(suite=SPADES, card_type=SIX),
    Card(suite=SPADES, card_type=SEVEN),
    Card(suite=SPADES, card_type=EIGHT),
    Card(suite=SPADES, card_type=NINE),
    Card(suite=SPADES, card_type=TEN),
    Card(suite=SPADES, card_type=JACK),
    Card(suite=SPADES, card_type=QUEEN),
    Card(suite=SPADES, card_type=KING),

    Card(suite=HEARTS, card_type=ACE),
    Card(suite=HEARTS, card_type=TWO),
    Card(suite=HEARTS, card_type=THREE),
    Card(suite=HEARTS, card_type=FOUR),
    Card(suite=HEARTS, card_type=FIVE),
    Card(suite=HEARTS, card_type=SIX),
    Card(suite=HEARTS, card_type=SEVEN),
    Card(suite=HEARTS, card_type=EIGHT),
    Card(suite=HEARTS, card_type=NINE),
    Card(suite=HEARTS, card_type=TEN),
    Card(suite=HEARTS, card_type=JACK),
    Card(suite=HEARTS, card_type=QUEEN),
    Card(suite=HEARTS, card_type=KING),

    Card(suite=CLUBS, card_type=ACE),
    Card(suite=CLUBS, card_type=TWO),
    Card(suite=CLUBS, card_type=THREE),
    Card(suite=CLUBS, card_type=FOUR),
    Card(suite=CLUBS, card_type=FIVE),
    Card(suite=CLUBS, card_type=SIX),
    Card(suite=CLUBS, card_type=SEVEN),
    Card(suite=CLUBS, card_type=EIGHT),
    Card(suite=CLUBS, card_type=NINE),
    Card(suite=CLUBS, card_type=TEN),
    Card(suite=CLUBS, card_type=JACK),
    Card(suite=CLUBS, card_type=QUEEN),
    Card(suite=CLUBS, card_type=KING),

    Card(suite=DIAMONDS, card_type=ACE),
    Card(suite=DIAMONDS, card_type=TWO),
    Card(suite=DIAMONDS, card_type=THREE),
    Card(suite=DIAMONDS, card_type=FOUR),
    Card(suite=DIAMONDS, card_type=FIVE),
    Card(suite=DIAMONDS, card_type=SIX),
    Card(suite=DIAMONDS, card_type=SEVEN),
    Card(suite=DIAMONDS, card_type=EIGHT),
    Card(suite=DIAMONDS, card_type=NINE),
    Card(suite=DIAMONDS, card_type=TEN),
    Card(suite=DIAMONDS, card_type=JACK),
    Card(suite=DIAMONDS, card_type=QUEEN),
    Card(suite=DIAMONDS, card_type=KING),
]


class Deck:
    """A class representing a deck of playing cards.

    The `Deck` class represents a standard deck of 52 playing cards,
    consisting of four suits (spades, hearts, clubs, and diamonds)
    and 13 ranks (Ace, 2 through 10, Jack, Queen, and King).

    Attributes:
        cards (list[Card]): A list of `Card` objects representing the cards in the deck.

    Methods:
        __init__(): Initializes a new instance of the `Deck` class.

        shuffle(): Shuffles the cards in the deck.

        __init_cards__(): Initializes the list of cards in the deck.

        add_card(card: Card, duplicate_allowed: bool = False): Adds a card to the deck,
        optionally allowing duplicates.

        remove_card(card: Card): Removes a card from the deck.

        remove_cards(cards: Iterable[Card]): Removes multiple cards from the deck.

        draw_card(card: Card): Draws a specific card from the deck.

        draw_random_cards(number_of_cards: int): Draws a specified number of
        random cards from the deck.

        card_exists(card: Card): Checks if a specific card is in the deck.

        missing_cards(): Returns a list of cards that are missing from the deck.
        __len__(): Returns the number of cards in the deck.
        __iter__(): Returns an iterator for the deck.
        __str__(): Returns a string representation of the deck.
    """
    def __init__(self) -> None:
        self.cards: list[Card] = CARDS_LIST.copy()

    def reset(self) -> None:
        """Resets the deck"""
        self.cards = CARDS_LIST.copy()

    def count(self) -> int:
        """
        Counts the number of cards in the deck.

        This function returns the length of the `cards` list in the `Deck`
        object.

        Parameters:
            self (Deck): The `Deck` object that contains the `cards` list.

        Returns:
            int: The number of cards in the deck.
        """
        return len(self.cards)

    def shuffle(self) -> None:
        """
        Shuffles the deck of cards.

        This function shuffles the `cards` list in the `Deck` object by iterating
        over a range of numbers from 1 to a random number between 3 and 10. In
        each iteration, the `shuffle` function from the `random` module is
        called to shuffle the `cards` list.

        Parameters:
            self (Deck): The `Deck` object that contains the `cards` list.

        Returns:
            None
        """
        for _ in range(1, randint(3, 10)):
            shuffle(self.cards)

    def draw_card(self, card: Card) -> Card | None:
        """
        Removes a specific card from the deck if it exists.

        Parameters:
            self (Deck): The `Deck` object that contains the `cards` list.
            card (Card): The card object to remove from the deck.

        Returns:
            Card | None: The removed card if found, None otherwise.

        Raises:
            CardError: If the specified card is not in the deck.
        """
        if card in self.cards:
            self.cards.remove(card)
            return card
        raise CardError(f"Card {card} not in deck")

    def draw_random_card(self, shuffle_deck: bool = True) -> Card | None:
        """
        Draws a random card from the deck.

        Parameters:
            self (Deck): The `Deck` object that contains the `cards` list.
            shuffle_deck (bool, optional): Whether to shuffle the deck
            before drawing. Defaults to True.

        Returns:
            Card | None: The drawn card if found, None otherwise.

        Raises:
            NotEnoughCardsError: If there are not enough cards in the deck
            to satisfy the draw request.
        """
        if shuffle_deck:
            self.shuffle()
        if len(self.cards) > 0:
            return self.cards.pop(0)
        raise NotEnoughCardsError("Not enough cards in deck")

    def draw_random_cards(
        self, number_of_cards: int = 1, shuffle_deck: bool = True
    ) -> list[Card]:
        """
        Draws a specified number of random cards from the deck.

        Args:
            number_of_cards (int, optional): The number of cards to draw. Defaults to 1.
            shuffle_deck (bool, optional): Whether to shuffle the deck
            before drawing. Defaults to True.

        Returns:
            list[Card]: A list of the drawn cards.

        Raises:
            NotEnoughCardsError: If there are not enough cards in the deck
            to satisfy the draw request.
        """
        cards = []
        if shuffle_deck:
            self.shuffle()
        if len(self.cards) >= number_of_cards:
            for _ in range(number_of_cards):
                cards.append(self.cards.pop(0))
            return cards
        raise NotEnoughCardsError("Not enough cards in deck")

    def add_card(self, card: Card, duplicate_allowed: bool = False) -> None:
        """
        Adds a card to the deck.

        Args:
            self: The deck object.
            card (Card): The card object to add to the deck.
            duplicate_allowed (bool, optional): Whether adding duplicate
            cards is allowed. Defaults to False.

        Returns:
            None
        """
        if not duplicate_allowed and card in self.cards:
            raise CardError(f"Card {card} already in deck")
        self.cards.append(card)

    def add_cards(self, cards: Iterable[Card], duplicate_allowed: bool = False) -> None:
        """
        Adds multiple cards to the deck.

        Args:
            self: The deck object.
            cards (Iterable[Card]): An iterable of card objects to add to the deck.
            duplicate_allowed (bool, optional): Whether adding duplicate
            cards is allowed. Defaults to False.

        Returns:
            None
        """
        for card in cards:
            if not duplicate_allowed and card in self.cards:
                raise CardError(f"Card {card} already in deck")
            self.cards.append(card)

    def add_card_at_index(
        self,
        card: Card,
        index: int,
        duplicate_allowed: bool = False
    ) -> None:
        """Adds a card to the deck at the specified index.

        Args:
            card (Card): The card to add to the deck.
            index (int): The position in the deck to insert the card.
            duplicate_allowed (bool, optional): Whether duplicate cards are allowed.
                Defaults to False.

        Raises:
            IndexError: If the index is out of range.
            CardError: If duplicate cards are not allowed and the card is already in the deck.

        Returns:
            None
        """
        if index < 0 or index > len(self.cards):
            raise IndexError("Index out of range")
        if not duplicate_allowed and card in self.cards:
            raise CardError(f"Card {card} already in deck")
        self.cards.insert(index, card)

    def count_by_suite(self, suite: Suite) -> int:
        """Counts the number of cards in the given suite.

        Args:
            suite (Suite): The suite to count cards for.

        Returns:
            int: The number of cards in the given suite.
        """
        return len([card for card in self.cards if card.suite == suite])

    def count_by_card_type(self, card_type: CardType) -> int:
        """Counts the number of cards of the given card type.
        Args:
            card_type (CardType): The type of card to count.

        Returns:
            int: The number of cards of the given card type.
        """
        return len(
            [card for card in self.cards if card.card_type == card_type]
        )

    def count_by_card(self, card: Card) -> int:
        """
        Counts the number of cards in the deck that are equal to the specified card.

        Args:
            self: The deck object.
            card (Card): The card to count in the deck.

        Returns:
            int: The number of cards in the deck that are equal to the specified card.
        """
        return len([c for c in self.cards if c == card])

    def card_exists(self, card: Card) -> bool:
        """
        Checks if a card exists in the deck.

        Args:
            self: The deck object.
            card (Card): The card to check in the deck.

        Returns:
            bool: True if the card exists in the deck, False otherwise.
        """
        return card in self.cards

    def remove_card(self, card: Card) -> None:
        """
        Removes a card from the deck.

        Args:
            self: The deck object.
            card (Card): The card to remove from the deck.

        Returns:
            None
        """
        if card not in self.cards:
            raise CardError(f"Card {card} not in deck")
        self.cards.remove(card)

    def remove_cards(self, cards: Iterable[Card]) -> None:
        """
        Removes multiple cards from the deck.

        Args:
            self: The deck object.
            cards (Iterable[Card]): The cards to remove from the deck.

        Returns:
            None
        """
        for card in cards:
            if card not in self.cards:
                raise CardError(f"Card {card} not in deck")
            self.cards.remove(card)

    def draw_card_at_index(self, index: int) -> Card:
        """
        Draws a card at a given index in the deck.

        Args:
            self: The deck object.
            index (int): The index of the card to draw.

        Returns:
            Card: The card that was drawn.
        """
        if index < 0 or index >= len(self.cards):
            raise IndexError(f"Index {index} out of range")
        card = self.cards[index]
        self.cards.pop(index)
        return card

    def deal_multi_players(
        self,
        number_of_players: int,
        number_of_cards: int,
        shuffle_deck: bool = True
    ) -> Dict[int, List[Card]]:
        """
        Deal a specified number of cards to multiple players from the deck.

        Args:
            number_of_players (int): The number of players to deal cards to.
            number_of_cards (int): The number of cards to deal to each player.
            shuffle_deck (bool, optional): Whether to shuffle the deck before
            dealing. Defaults to True.

        Returns:
            Dict: A dictionary where the keys are player indices (0 to number_of_players - 1)
                and the values are lists of cards dealt to each player.

        Raises:
            ValueError: If the number of players is less than 1.
            NotEnoughCardsError: If the deck does not have enough cards to deal the required number.

        Example:
            >>> deck = Deck()
            >>> deck.deal_multi_players(number_of_players=4, number_of_cards=5)
            {0: [Card('Hearts', '2'), Card('Clubs', '3'), ...],
            1: [Card('Spades', '4'), Card('Diamonds', '5'), ...],
            2: [Card('Hearts', '6'), Card('Clubs', '7'), ...],
            3: [Card('Spades', '8'), Card('Diamonds', '9'), ...]}
        """
        cards: Dict[int, List[Card]] = {}
        if number_of_players < 1:
            raise ValueError(
                "Number of players cannot be < 1"
            )
        cards_required = number_of_players * number_of_cards
        if cards_required > len(self.cards):
            raise NotEnoughCardsError(
                "The deck does not have the required number of cards"
            )
        if shuffle_deck:
            self.shuffle()
        for player_index in range(number_of_players):
            cards[player_index] = self.draw_random_cards(
                number_of_cards=number_of_cards,
                shuffle_deck=shuffle_deck
            )
        return cards

    def remove_card_at_index(self, index: int) -> None:
        """
        Removes a card at a given index in the deck.

        Args:
            self: The deck object.
            index (int): The index of the card to remove.

        Returns:
            None
        """
        if index < 0 or index >= len(self.cards):
            raise IndexError(f"Index {index} out of range")
        self.cards.pop(index)

    def remove_suite(self, suite: Suite) -> None:
        """
        Removes all cards in the given suite from the deck.

        Args:
            self: The deck object.
            suite (Suite): The suite to remove cards from.

        Returns:
            None
        """
        self.remove_cards([card for card in self.cards if card.suite == suite])

    def remove_card_type(self, card_type: CardType) -> None:
        """
        Removes all cards of the given card type from the deck.

        Args:
            self: The deck object.
            card_type (CardType): The card type to remove cards from.

        Returns:
            None
        """
        self.remove_cards(
            [card for card in self.cards if card.card_type == card_type]
        )

    def missing_cards(self) -> List[Card]:
        """
        Returns a list of cards that are missing from the deck.

        This function iterates over the `CARDS_LIST` and checks if each
        card is present in the `cards` attribute of the current instance.
        If a card is not found in the `cards` attribute, it is added to the `missing_cards` list.

        Returns:
            List[Card]: A list of cards that are missing from the deck.
        """
        mc: List[Card] = []
        for card in CARDS_LIST:
            if not self.card_exists(card):
                mc.append(card)
        return mc

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f"{self.cards}"

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)
