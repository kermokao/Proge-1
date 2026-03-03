"""Simple Poker implementation."""

from collections import Counter


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Hand:
    suits = ["diamonds", "clubs", "hearts", "spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = []

    def _value_rank(self, value):
        return self.values.index(value)

    def can_add_card(self, card: Card) -> bool:
        if len(self.cards) >= 5:
            return False
        if card.value not in self.values or card.suit not in self.suits:
            return False
        for c in self.cards:
            if c.value == card.value and c.suit == card.suit:
                return False
        return True

    def add_card(self, card: Card):
        if self.can_add_card(card):
            self.cards.append(card)

    def can_remove_card(self, card: Card):
        return any(c.value == card.value and c.suit == card.suit for c in self.cards)

    def remove_card(self, card: Card):
        if self.can_remove_card(card):
            self.cards = [c for c in self.cards if not (c.value == card.value and c.suit == card.suit)]

    def get_cards(self):
        return self.cards

    def is_straight(self):
        if len(self.cards) != 5:
            return False
        sorted_cards = sorted(self.cards, key=lambda c: self._value_rank(c.value))
        for i in range(4):
            if self._value_rank(sorted_cards[i + 1].value) != \
               self._value_rank(sorted_cards[i].value) + 1:
                return False
        return True

    def is_flush(self):
        if len(self.cards) != 5:
            return False
        first_suit = self.cards[0].suit
        return all(card.suit == first_suit for card in self.cards)

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()

    def is_full_house(self):
        if len(self.cards) != 5:
            return False
        counter = Counter(card.value for card in self.cards)
        return sorted(counter.values()) == [2, 3]

    def is_four_of_a_kind(self):
        if len(self.cards) != 5:
            return False
        counter = Counter(card.value for card in self.cards)
        return 4 in counter.values()

    def is_three_of_a_kind(self):
        if len(self.cards) != 5:
            return False
        counter = Counter(card.value for card in self.cards)
        return 3 in counter.values() and not self.is_full_house()

    def is_pair(self):
        if len(self.cards) != 5:
            return False
        counter = Counter(card.value for card in self.cards)
        return list(counter.values()).count(2) == 1

    def get_hand_type(self):
        if len(self.cards) < 5:
            return None
        if self.is_straight_flush():
            return "straight flush"
        if self.is_flush():
            return "flush"
        if self.is_straight():
            return "straight"
        if self.is_full_house():
            return "full house"
        if self.is_four_of_a_kind():
            return "four of a kind"
        if self.is_three_of_a_kind():
            return "three of a kind"
        if self.is_pair():
            return "pair"
        return "high card"

    def __repr__(self):
        cards_str = ", ".join(str(card) for card in self.cards)
        hand_type = self.get_hand_type()
        if hand_type is None:
            return f"I'm holding {cards_str}"
        return f"I got a {hand_type} with cards: {cards_str}"


if __name__ == "__main__":
    hand = Hand()
    cards = [Card("2", "diamonds"), Card("4", "spades"), Card("5", "clubs"), Card("3", "diamonds"), Card("6", "hearts")]
    [hand.add_card(card) for card in cards]
    assert hand.get_hand_type() == "straight"

    hand = Hand()
    cards = [Card("10", "diamonds"), Card("2", "diamonds"), Card("A", "diamonds"), Card("6", "diamonds"),
             Card("9", "diamonds")]
    [hand.add_card(card) for card in cards]
    assert hand.get_hand_type() == "flush"

    hand = Hand()
    cards = [Card("A", "hearts"), Card("A", "clubs"), Card("A", "spades"), Card("A", "diamonds"),
             Card("9", "diamonds")]
    [hand.add_card(card) for card in cards]
    assert hand.get_hand_type() == "four of a kind"
