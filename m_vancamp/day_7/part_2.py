import dataclasses
import numbers


Cards = list(reversed([
    'A',
    'K',
    'Q',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
    'J'
]))


@dataclasses.dataclass
class Hand:
    Cards: str
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
        if self.max_strength != other.max_strength:
            return self.max_strength > other.max_strength
        return self.beats_high_card_by_first_index(other)

    def beats_high_card_by_first_index(self, other):
        for idx in range(len(self.Cards)):
            a, b = self.Cards[idx], other.Cards[idx]
            if a == b:
                continue
            return Cards.index(a) > Cards.index(b)
        return False

    def count_by_kind(self, cards):
        counts = list()

        for card in list(set(cards)):
            counts.append(cards.count(card))

        return counts

    def max_of_a_kind(self, cards):
        return max(self.count_by_kind(cards))

    @property
    def max_strength(self):
        strength = 0

        for permutation in Cards:
            if permutation == 'J':
                continue

            s = self.strength(self.Cards.replace('J', permutation))
            if s > strength:
                strength = s

        return strength

    def strength(self, cards):
        if self.max_of_a_kind(cards) == 6:
            return 6

        # -- five of a kind
        if self.max_of_a_kind(cards) == 5:
            return 6

        # -- four of a kind
        if self.max_of_a_kind(cards) == 4:
            return 5

        # -- full house
        if self.count_by_kind(cards).count(2) == 1 and self.count_by_kind(cards).count(3) == 1:
            return 4

        # -- three of a kind but not full house
        if self.max_of_a_kind(cards) == 3:
            return 3

        # -- two pair
        if self.count_by_kind(cards).count(2) == 2:
            return 2

        # -- one pair
        if self.max_of_a_kind(cards) == 2:
            return 1

        # -- high card
        if self.max_of_a_kind(cards) == 1:
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
        print(hand.Cards, rank, Hand.Rankings[hand.max_strength], hand.max_strength)
        result += winnings

    print(result)
