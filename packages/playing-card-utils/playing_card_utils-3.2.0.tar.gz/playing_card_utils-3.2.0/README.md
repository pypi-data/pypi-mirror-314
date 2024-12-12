# playing-card-utils

## Introduction
The comprehensive Python library for all your playing card needs! Whether you’re a game developer, a hobbyist, or just someone who loves card games, pyCard is your go-to solution for creating and managing a wide variety of card games.

### Suite

Suites -> [♠, ♥, ♣, ♦]

- Symbol

```python
import playing_card_utils as pc

print("Spade:", pc.SPADES)
print("Heart:", pc.HEARTS)
print("Club:", pc.CLUBS)
print("Diamond:", pc.DIAMONDS)

"""
Spade: ♠
Heart: ♥
Club: ♣
Diamond: ♦
"""
```

- Name
```python
import playing_card_utils as pc

print("1:", pc.SPADES.name)
print("2:", pc.HEARTS.name)
print("3:", pc.CLUBS.name)
print("4:", pc.DIAMONDS.name)

"""
1: Spades
2: Hearts
3: Clubs
4: Diamonds
"""
```

----
### Card Type

Card Types -> [A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K]

- Names
```python
import playing_card_utils as pc

for card_type in pc.CARD_TYPES:
    print(card_type.name)

"""
Ace
Two
Three
Four
Five
Six
Seven
Eight
Nine
Ten
Jack
Queen
King
"""

```

- Weight
```python
import playing_card_utils as pc

for card_type in pc.CARD_TYPES:
    print(f"{card_type.name} -> {card_type.weight}")

"""
Ace -> 14
Two -> 2
Three -> 3
Four -> 4
Five -> 5
Six -> 6
Seven -> 7
Eight -> 8
Nine -> 9
Ten -> 10
Jack -> 11
Queen -> 12
King -> 13
"""
```
----
### Card

Create instance of the card.

- Using the class

```python
import playing_card_utils as pc

ace_of_spades = pc.Card(
    suite=pc.SUITES.SPADES,
    card_type=pc.CARD_TYPES.ACE
)

print(ace_of_spades)
# Output >>> A♠
```

- Direct

```python
import playing_card_utils as pc

ace_of_spades = pc.ACE_SPADES
print("Card:", ace_of_spades)
# Output >>> Card: A♠
```

#### Card properties & attributes

- Name
```python
import playing_card_utils as pc

# Card Name
print("Name:", pc.ACE_SPADES.name)
# Output >>> Name: Ace of Spades
```

- Card Suite
```python
import playing_card_utils as pc

print("Suite:", pc.ACE_SPADES.suite)
# Output >>> Suite: ♠
```

- Card Type
```python
import playing_card_utils as pc

print("Card Type:", pc.ACE_SPADES.card_type)
# Output >>> Card Type: A
```
----
### Deck

The class provides the following functions and attributes

- [add_card_at_index](#add-card-at-given-index)
- [add_cards](#add-card-in-the-deck)
- [card_exists](#card-exists-in-the-deck)
- [cards](#cards-in-deck)
- [count](#count)
- [count_by_card](#count-by-card)
- [count_by_card_type](#count-by-card-type)
- [count_by_suite](#count-by-suite)
- [draw_card](#draw-card)
- [draw_card_at_index](#draw-card-at-index)
- [draw_random_card](#draw-random-card)
- [draw_random_cards](#draw-random-cards)
- [deal_multi_players](#deal-multi-players)
- [missing_cards](#missing-cards)
- [remove_card](#remove-card)
- [remove_card_at_index](#remove-card-at-index)
- [remove_card_type](#remove-cards-by-type)
- [remove_cards](#remove-cards)
- [remove_suite](#remove-cards-by-suite)
- [reset](#reset-the-deck)
- [shuffle](#shuffle)

#### Initialization
```python
from playing_card_utils.deck import Deck

deck = Deck()
```

#### Cards in Deck

List storing all the cards in the deck

```python
from playing_card_utils.deck import Deck

deck = Deck()
print(deck.cards)

# [A♠, 2♠, 3♠, 4♠, 5♠, 6♠, 7♠, 8♠, 9♠, T♠, J♠, Q♠, K♠, A♥, 2♥, 3♥, 4♥, 5♥, 6♥, 7♥, 8♥, 9♥, T♥, J♥, Q♥, K♥, A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, 8♣, 9♣, T♣, J♣, Q♣, K♣, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, 8♦, 9♦, T♦, J♦, Q♦, K♦]

```

#### Count

The number of cards in the deck can be counted in two ways
1. `len(deck)`
2. `deck.count()`

#### Shuffle
```python
from playing_card_utils.deck import Deck

deck = Deck()
deck.shuffle()
print(deck.cards)

# [3♦, A♦, 8♥, 5♠, 6♣, 6♦, 5♥, T♣, 8♣, 7♥, 4♠, 2♦, Q♥, K♥, 8♦, 6♠, A♠, A♣, T♥, K♦, 7♦, 9♠, 3♥, 5♦, J♣, 2♥, 4♦, 9♦, 3♠, A♥, K♠, 9♥, 2♣, K♣, 2♠, J♥, J♦, Q♠, 4♥, 3♣, T♦, 5♣, 7♠, 6♥, 8♠, T♠, Q♣, 9♣, 4♣, J♠, 7♣, Q♦]

```

#### Card exists in the deck

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Check if the deck contains the Ace of Spades
print("Ace of Spades exists:", deck.card_exists(card=pc.ACE_SPADES))

# Remove the Ace of Spades from the deck
deck.remove_card(card=pc.ACE_SPADES)

# Check if the deck contains the Ace of Spades after removal
print("Ace of Spades exists:", deck.card_exists(card=pc.ACE_SPADES))

# Ace of Spades exists: True
# Ace of Spades removed: False

```

#### Count number of cards in the deck
```python
from playing_card_utils.deck import Deck

deck = Deck()
print("Number of cards in the deck:", deck.count())

# Number of cards in the deck: 52

```

#### Empty the deck
```python
from playing_card_utils.deck import Deck

deck = Deck()
deck.cards = []
print("Number of cards in the deck:", deck.count())

# Number of cards in the deck: 0

```

#### Reset the deck
```python
from playing_card_utils.deck import Deck

deck = Deck()

deck.shuffle()
print("After shuffle:", deck)

deck.reset()
print("After reset:", deck)

# After shuffle: [Q♥, T♦, 8♣, Q♠, 4♥, 2♥, 5♥, 9♥, 8♠, 6♦, A♦, T♥, Q♦, 4♦, A♣, J♦, K♥, 2♣, 9♦, 6♠, 8♥, 3♥, 5♣, 9♠, 6♣, K♠, A♠, 3♦, 7♥, 4♠, Q♣, K♦, T♠, J♠, 2♦, 3♠, A♥, 7♣, 7♠, 6♥, T♣, K♣, 5♠, J♣, J♥, 4♣, 2♠, 3♣, 8♦, 9♣, 5♦, 7♦]

# After reset: [A♠, 2♠, 3♠, 4♠, 5♠, 6♠, 7♠, 8♠, 9♠, T♠, J♠, Q♠, K♠, A♥, 2♥, 3♥, 4♥, 5♥, 6♥, 7♥, 8♥, 9♥, T♥, J♥, Q♥, K♥, A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, 8♣, 9♣, T♣, J♣, Q♣, K♣, A♦, 2♦, 3♦, 4♦, 5♦, 6♦, 7♦, 8♦, 9♦, T♦, J♦, Q♦, K♦]

```

#### Count by suite
```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()
spades_count = deck.count_by_suite(pc.SPADES)
print("Spades in the deck:", spades_count)

# Spades in the deck: 13

```

#### Draw Card

Draws a given card from the deck if it exists. If not exists then raises `CardError` exception.

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

card = deck.draw_card(card=pc.ACE_SPADES)
print(card)

# A♠

```

#### Draw Card at Index

Draws card at given index if the index exists.
If the index does not exist then raises `IndexError`

```python
from playing_card_utils.deck import Deck

deck = Deck()

print("Card at index 33:", deck.cards[33])
card = deck.draw_card_at_index(index=33)
print("Drawn card", card)

# Card at index 33: 8♣
# Drawn card 8♣

```

#### Draw Random Card

Draws a random card from the deck. If the deck is empty, then raises `NotEnoughCardsError`

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

random_card = deck.draw_random_card()
print("Random Card:", random_card)
print("Cards in the deck:", len(deck))

# Random Card: K♦
# Cards in the deck: 51
```

#### Draw Random Cards

Draws given number of cards from the deck.
If the number is greater than the number of cards in the deck, then `NotEnoughCardsError` exception is raised

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

random_cards = deck.draw_random_cards(number_of_cards=2)
print("Random Cards:", random_cards)
print("Cards in the deck:", len(deck))

# Random Cards: [Q♣, 3♠]
# Cards in the deck: 50
```

#### Deal Multi Players

Deals cards to multiple players

```python
from playing_card_utils.deck import Deck

deck = Deck()

player_cards_0 = deck.deal_multi_players(
    number_of_players=4,
    number_of_cards=2
)

deck.reset()

player_cards_1 = deck.deal_multi_players(
    number_of_players=4,
    number_of_cards=2,
    shuffle_deck=False
)

print("player_cards_0:", player_cards_0)
print("player_cards_1:", player_cards_1)

# player_cards_0: {0: [2♥, 7♦], 1: [9♦, J♣], 2: [T♣, 2♣], 3: [J♠, J♦]}
# player_cards_1: {0: [A♠, 2♠], 1: [3♠, 4♠], 2: [5♠, 6♠], 3: [7♠, 8♠]}

```

#### Missing Cards

Returns the list of cards which are missing in the deck

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
deck.remove_cards([
    pc.JACK_SPADES,
    pc.JACK_HEARTS
])

print(deck.missing_cards())

# [J♠, J♥]

```

#### Count by card type
```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()
aces_count = deck.count_by_card_type(pc.ACE)
print("Spades in the deck:", aces_count)

# Aces in the deck: 4
```

#### Count by card
```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

print("Ace of Spades in deck:", deck.count_by_card(card=pc.ACE_SPADES))

# Ace of Spades in deck: 1
```

#### Add card in the deck

By default, the `duplicate_allowed` is set to `False`

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()
deck.add_card(card=pc.ACE_SPADES, duplicate_allowed=True)

ace_count = deck.count_by_card_type(pc.ACE)
print("Aces in the deck:", ace_count)

spades_count = deck.count_by_suite(pc.SPADES)
print("Spades in the deck:", spades_count)

# Aces in the deck: 5
# Spades in the deck: 14

```

If we try to run the same code with `duplicate_allowed = False` then `CardError` exception will be raised.


#### Add multiple cards

Adds multiple cards at once.

`duplicate_allowed` is also applicable to this function. The default is `False`

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Emptying the deck
deck.cards = []

# Cards to be added
cards = [pc.ACE_SPADES, pc.KING_SPADES, pc.QUEEN_SPADES, pc.JACK_SPADES]

deck.add_cards(cards=cards)
print(deck)

# [A♠, K♠, Q♠, J♠]

```

#### Add card at given index

Adds card at given index.

`duplicate_allowed` is also applicable to this function. The default is `False`

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

deck.cards = [
    pc.ACE_SPADES, pc.QUEEN_SPADES
]

print("Cards before adding:", deck)
deck.add_card_at_index(card=pc.KING_SPADES, index=1)
print("Cards after adding:", deck)

# Cards before adding: [A♠, Q♠]
# Cards after adding: [A♠, K♠, Q♠]

```

#### Remove Card

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

deck.remove_card(pc.ACE_SPADES)

print("Cards in the deck:", len(deck))

# Cards in the deck: 51

```

#### Remove Card at Index

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
card_at_index_14 = deck.cards[14]
deck.remove_card_at_index(14)

print("Card at index 14:", card_at_index_14)
print(deck.missing_cards())

# Card at index 14: 2♥
# [2♥]

```

#### Remove Cards

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards = [pc.JACK_SPADES, pc.JACK_HEARTS]
deck.remove_cards(cards=cards)
print(deck.missing_cards())

# [J♠, J♥]

```

#### Remove cards by suite

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

deck.remove_suite(pc.SPADES)

print("Cards in the deck:", len(deck))

# Cards in the deck: 39

```

##### Remove Cards by Type

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

deck.remove_card_type(card_type=pc.SIX)

print("Cards in the deck:", len(deck))

# Cards in the deck: 48

```

### General Functions

- [sort_cards](#sort-cards)
- [same_suite](#same-suite)
- [is_in_sequence](#is-in-sequence)
- [count_by_suite](#count-by-suite)
- [count_by_card_type](#count-by-card-type)
- [count_by_card](#count-by-card)

#### Sort Cards

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards = [
    pc.ACE_CLUBS,
    pc.NINE_DIAMONDS,
    pc.TWO_HEARTS,
    pc.FOUR_CLUBS
]
cards = pc.sort_cards(cards=cards)
print(cards)

# [2♥, 4♣, 9♦, A♣]

```

#### Same Suite

Checks whether the cards in the given list are of same suite

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards_a = [
    pc.ACE_CLUBS,
    pc.NINE_DIAMONDS,
    pc.TWO_HEARTS,
    pc.FOUR_CLUBS
]
print("Are cards in `cards_a` of same suite?", pc.same_suite(cards_a))

cards_b = [
    pc.QUEEN_CLUBS,
    pc.KING_CLUBS,
    pc.ACE_CLUBS,
]
print("Are cards in `cards_b` of same suite?", pc.same_suite(cards_b))

# Are cards in `cards_a` of same suite? False
# Are cards in `cards_b` of same suite? True

```

#### Is in Sequence

Checks whether the cards in the given list are in sequence

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards_a = [
    pc.ACE_CLUBS,
    pc.NINE_DIAMONDS,
    pc.TWO_HEARTS,
    pc.FOUR_CLUBS
]
print("Are cards in `cards_a` in sequence?", pc.is_in_sequence(cards_a))

cards_b = [
    pc.QUEEN_CLUBS,
    pc.KING_CLUBS,
    pc.ACE_CLUBS,
]
print("Are cards in `cards_b` in sequence?", pc.is_in_sequence(cards_b))

cards_c = [
    pc.THREE_CLUBS,
    pc.TWO_CLUBS,
    pc.ACE_CLUBS,
]
print("Are cards in `cards_c` in sequence?", pc.is_in_sequence(cards_c))

# Are cards in `cards_a` in sequence? False
# Are cards in `cards_b` in sequence? True
# Are cards in `cards_c` in sequence? True

```

#### Count by Suite

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards_a = [
    pc.ACE_CLUBS,
    pc.NINE_DIAMONDS,
    pc.TWO_HEARTS,
    pc.FOUR_CLUBS
]
clubs_in_cards_a = pc.count_by_suite(suite=pc.CLUBS, cards=cards_a)
print("Number of clubs in cards_a:", clubs_in_cards_a)

# Number of clubs in cards_a: 2

```

#### Count by Card Type

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards_a = [
    pc.ACE_CLUBS,
    pc.NINE_DIAMONDS,
    pc.TWO_HEARTS,
    pc.FOUR_CLUBS,
    pc.ACE_HEARTS
]
aces_in_cards_a = pc.count_by_card_type(card_type=pc.ACE, cards=cards_a)
print("Number of aces in cards_a:", aces_in_cards_a)

# Number of aces in cards_a: 2

```

#### Count by Card

```python
import playing_card_utils as pc
from playing_card_utils.deck import Deck

deck = Deck()

# Removing Jack of Spades and Jack of Hearts
cards_a = [
    pc.ACE_CLUBS,
    pc.ACE_HEARTS,
    pc.ACE_HEARTS,
    pc.FOUR_CLUBS,
    pc.ACE_HEARTS
]
ace_of_hearts_in_cards_a = pc.count_by_card(cards=cards_a, card=pc.ACE_HEARTS)
print("Number of ace of hearts in cards_a:", ace_of_hearts_in_cards_a)

# Number of ace of hearts in cards_a: 3

```