import torch
from settings import arg
from settings import constants


class CardToString():
    """ Convert between string and numeric representations of cards.
        2c, 2d, 2h, 2s, 3c, 3d, 3h, 3s ... Ac, Ad, Ah, As
    """
    def __init__(self):
        self.suit_table = list('cdhs')
        self.rank_table = [str(i) for i in range(2, 10)] + list('TJQKA')
        self.card_to_string_table = {}
        self.string_to_card_table = {}
        for card in range(constants.card_count):
            rank = self.rank_table[card // constants.suit_count]
            suit = self.suit_table[card % constants.suit_count]
            card_string = rank + suit
            self.card_to_string_table[card] = card_string
            self.string_to_card_table[card_string] = card

    def card_to_string(self, card):
        return self.card_to_string_table[card]

    def string_to_card(self, card_string):
        return self.string_to_card_table[card_string]

    def cards_to_string(self, cards):
        cards_string = ""
        for card in cards:
            cards_string += self.card_to_string(card.item())
        return cards_string

    def string_to_cards(self, cards_string):
        cards = torch.zeros([len(cards_string) // 2], dtype=arg.int_dtype).to(arg.device)
        for i in range(0, len(cards_string), 2):
            card_string = cards_string[i] + cards_string[i + 1]
            cards[i // 2] = self.string_to_card(card_string)
        return cards


card_to_string = CardToString()
