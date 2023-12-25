import dataclasses
import numbers


Cards = list(reversed([
    'A',
    'K',
    'Q',
    'J',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2'
]))


@dataclasses.dataclass
class Hand:
    Cards: list = None
    Bid: int = 0

    Rankings = list(reversed(
        [
            'Five of a kind',
            'Four of a kind',
            'Full house',
            'Three of a kind',
            'Two Pair',
            'One Pair',
            'High Card'
        ]
    ))

    def __gt__(self, other):
        if self.strength != other.strength:
            return self.strength > other.strength
        return self.beats_high_card_by_first_index(other)

    def beats_high_card_by_first_index(self, other):
        for idx in range(len(self.Cards)):
            a, b = self.Cards[idx], other.Cards[idx]
            if a == b:
                continue
            return Cards.index(a) > Cards.index(b)
        return False

    @property
    def card_set(self):
        return list(set(self.Cards))

    @property
    def count_by_kind(self):
        return sorted(list([self.Cards.count(card) for card in self.card_set]))

    @property
    def max_of_a_kind(self):
        return max(self.count_by_kind)

    @property
    def strength(self):
        # -- five of a kind
        if self.max_of_a_kind == 5:
            return 6

        # -- four of a kind
        if self.max_of_a_kind == 4:
            return 5

        # -- full house
        if self.count_by_kind.count(2) == 1 and self.count_by_kind.count(3) == 1:
            return 4

        # -- three of a kind but not full house
        if self.max_of_a_kind == 3:
            return 3

        # -- two pair
        if self.count_by_kind.count(2) == 2:
            return 2

        # -- one pair
        if self.count_by_kind.count(2) == 1:
            return 1

        # -- high card
        if self.max_of_a_kind == 1:
            return 0


def load_data(is_test=False):
    with open('input.txt' if not is_test else 'test_input.txt') as fp:
        lines = list([line.strip() for line in fp.readlines()])

    hands = list()

    for line in lines:
        cards, bid = line.split(' ')
        hands.append(Hand(cards, int(bid)))

    return hands


if __name__ == '__main__':
    card_data = sorted(load_data(False))

    result = 0
    for i in range(len(card_data)):
        hand = card_data[i]
        # -- rank is 1-based.
        rank = i + 1
        winnings = rank * hand.Bid
        print(hand.Cards, rank, hand.strength, hand.card_set, hand.count_by_kind)
        result += winnings

    print(result)
