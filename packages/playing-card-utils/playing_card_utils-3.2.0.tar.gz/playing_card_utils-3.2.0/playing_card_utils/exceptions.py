"""Exceptions related to the pycards package"""


class CardError(Exception):
    """Base class for card exceptions"""


class NotEnoughCardsError(Exception):
    """Not enough cards in deck error"""
