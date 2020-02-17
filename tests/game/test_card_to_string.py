import context
import unittest
import torch
from game.card_to_string import card_to_string
from settings.arguments import arg


class TestCardToString(unittest.TestCase):

    def test_card_to_string(self):
        card = 0
        string = card_to_string.card_to_string(card)
        self.assertEqual(string, '2c')

        card = 51
        string = card_to_string.card_to_string(card)
        self.assertEqual(string, 'As')

        card = 12
        string = card_to_string.card_to_string(card)
        self.assertEqual(string, '5c')

    def test_string_to_card(self):
        string = '2c'
        card = card_to_string.string_to_card(string)
        self.assertEqual(card, 0)

        string = 'As'
        card = card_to_string.string_to_card(string)
        self.assertEqual(card, 51)

        string = '5c'
        card = card_to_string.string_to_card(string)
        self.assertEqual(card, 12)

    def test_cards_to_string(self):
        cards = arg.IntTensor([0, 12, 51]).to(arg.device)
        string = card_to_string.cards_to_string(cards)
        self.assertEqual(string, '2c5cAs')

    def test_string_to_cards(self):
        string = '2c5cAs'
        cards = card_to_string.string_to_cards(string)
        real_cards = arg.IntTensor([0, 12, 51]).to(arg.device)
        torch.testing.assert_allclose(cards, real_cards)

        string = ''
        cards = card_to_string.string_to_cards(string)
        real_cards = arg.IntTensor([]).to(arg.device)
        torch.testing.assert_allclose(cards, real_cards)


if __name__ == "__main__":
    unittest.main()
