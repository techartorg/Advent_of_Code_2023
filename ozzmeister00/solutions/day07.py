"""--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship.
 (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends
  back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding 
a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's
 looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks
 covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island
  that is directly above Island Island, making it hard to even get there. Normally, they use big 
  machines to move the rocks and filter the sand, but the machines have broken down because Desert
   Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks 
if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. 
Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength 
of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
 The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are 
each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label,
 and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different 
label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than
 any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the 
first card in each hand. If these cards are different, the hand with the stronger first card 
is considered stronger. If the first card in each hand have the same label, however, then 
move on to considering the second card in each hand. If they differ, the hand with the higher
 second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first
 card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger
  because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input).
 For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount.
 Each hand wins an amount equal to its bid multiplied by its rank, where
  the weakest hand gets rank 1, the second-weakest hand gets rank 2,
   and so on up to the strongest hand. Because there are five hands
    in this example, the strongest hand will have rank 5 and its bid
     will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type,
 so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same
 label, but the second card of KK677 is stronger (K vs T), so KTJJT gets
  rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card,
 so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by
 adding up the result of multiplying each hand's bid with its rank
  (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings 
  in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?

248113761

--- Part Two ---

To make things a little more interesting, the Elf introduces one additional 
rule. Now, J cards are jokers - wildcards that can act like whatever 
card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker 
even than 2. The other cards stay in the same order: 
A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of 
determining hand type; for example, QJJQ2 is now considered four of a 
kind. However, for the purpose of breaking ties between two hands of
 the same type, J is always treated as J, not the card it's pretending to
  be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, 
so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3
, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

248294409? Too high.
246341542? Still too high after making sure that if J is the most card in hand, we can resolve that to a different card
"""

import collections

import solver.runner
import solver.solver

PARTONE_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
PARTTWO_RANKS = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']


class Card(str):
    CARD_RANKS = PARTONE_RANKS

    def __new__(cls, *args, **kwargs):
        cardID = '2'
        if len(args):
            if isinstance(args[0], str):
                if args[0] not in Card.CARD_RANKS:
                    raise ValueError(f"Input card ID {args[0]} not a valid card. Must be: {Card.CARD_RANKS}")
                cardID = args[0]
            elif isinstance(args[0], int):
                if args[0] >= len(Card.CARD_RANKS):
                    raise ValueError(f"Input card index {args[0]} not a valid card. Must be less than {len(Card.CARD_RANKS)}")
                
                cardID = Card.CARD_RANKS[args[0]]

        return super().__new__(cls, cardID)

    @property
    def rank(self):
        """
        Get the rank of this card within the list of cards

        :returns int:
        """
        return Card.CARD_RANKS.index(self)

    def __hash__(self):
        return super(Card, self).__hash__()

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank

        return super(Card, self).__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Card):
            return self.rank < other.rank

        return super(Card, self).__lt__(other)

    def __gt__(self, other):
        if isinstance(other, Card):
            return self.rank > other.rank

        return super(Card, self).__gt__(other)

    def __le__(self, other):
        if isinstance(other, Card):
            return self.rank <= other.rank

        return super(Card, self).__le__(other)

    def __ge__(self, other):
        if isinstance(other, Card):
            return self.rank >= other.rank

        return super(Card, self).__ge__(other)

    
class HandRanking(object):
    RANK = -1
    NAME = 'INVALID'

    def __init__(self, cards, jokersWild=False):
        """
        :param list[Card] cards: the list of cards from the Hand
        :param bool jokersWild: if true, will treat Jokers as wild and rank as the best possible hand
        """
        # safety check
        if not isinstance(cards[0], Card):
            cards = [Card(i) for i in cards]

        self.cards = cards
        self.jokersWild = jokersWild

    def __str__(self):
        return self.NAME

    def __eq__(self, other):
        if isinstance(other, HandRanking):
            rankComparison = self.RANK == other.RANK
            if rankComparison:
                allEqual = [card == other.cards[i] for i, card in enumerate(self.cards)]
                return all(allEqual)
            
            return rankComparison

        return TypeError(f"Comparison between type {type(other)} and HandRanking not supported.")

    def __lt__(self, other):
        if isinstance(other, HandRanking):
            if self.RANK == other.RANK:
                for i, card in enumerate(self.cards):
                    # if the two cards aren't the same, compare them
                    if card != other.cards[i]:
                        return  card < other.cards[i]
                        
                return False
            
            return self.RANK < other.RANK

        return TypeError(f"Comparison between type {type(other)} and HandRanking not supported.")

    def __gt__(self, other):
        if isinstance(other, HandRanking):
            if self.RANK == other.RANK:
                for i, card in enumerate(self.cards):
                    # if the two cards aren't the same, compare them
                    if card != other.cards[i]:
                        return  card > other.cards[i]
                        
                return False
            
            return self.RANK > other.RANK

        return TypeError(f"Comparison between type {type(other)} and HandRanking not supported.")

    def __le__(self, other):
        if isinstance(other, HandRanking):
            if self.RANK == other.RANK:
                for i, card in enumerate(self.cards):
                    # if the two cards aren't the same, compare them
                    if card != other.cards[i]:
                        return  card <= other.cards[i]
                        
                return False
            
            return self.RANK <= other.RANK

        return TypeError(f"Comparison between type {type(other)} and HandRanking not supported.")

    def __ge__(self, other):
        if isinstance(other, HandRanking):
            if self.RANK == other.RANK:
                for i, card in enumerate(self.cards):
                    # if the two cards aren't the same, compare them
                    if card != other.cards[i]:
                        return  card >= other.cards[i]
                        
                return False
            
            return self.RANK >= other.RANK

        return TypeError(f"Comparison between type {type(other)} and HandRanking not supported.")

    @staticmethod
    def handHasRank(cards):
        """
        Determine if the input set of cards matches this Ranking

        :param list[Card] cards:

        :returns bool:
        """
        raise NotImplementedError("You must implement this function for this rank")


class OfAKind(HandRanking):
    """
    Base class for all the hand rankings that look for multiples of 
    the same card. 

    Set KIND_COUNTS to an array of the values you're looking for
    so a Five Of a Kind would be KIND_COUNTS = [5]
    and two pair would be KIND_COUNTS = [2, 2]

    The counts in the hand must match the KIND_COUNTS exactly
    for a hand to achieve this rank
    """
    KIND_COUNTS =[]

    def __init__(self, *args, **kwargs):
        super(OfAKind, self).__init__(*args, **kwargs)

        self.counts = collections.defaultdict(int)
        for c in self.cards:
            self.counts[c] += 1

        kindCounts = [i for i in self.KIND_COUNTS]
        self.matchedCounts = 0

        if self.jokersWild and 'J' in self.counts:
            most = max(self.counts, key=self.counts.get)

            # if Js are the most of all the cards in the hand
            if most == 'J':
                # then treat the "Most" we want to add to as the highest ranked card in the hand
                most = list(sorted(self.counts.keys()))[-1]

            # if the actual highest card in the hand isn't J, then add J's count to that
            # and remove J from the list of counts
            if most != 'J':
                self.counts[most] += self.counts['J']
                del self.counts['J']

        values = list(self.counts.values())

        # search the kindCounts we're looking for, but only make a count valid once
        # this way a two pair (2, 2) doesn't look like a full house (2, 3)
        while kindCounts:
            testCount = kindCounts.pop()
            if testCount in values:
                index = values.index(testCount)
                del values[index] # nuke the found value from the list of found values so we can prevent duplicates
                self.matchedCounts += 1

    def handHasRank(self):
        return self.matchedCounts == len(self.KIND_COUNTS)


class FiveOfAKind(OfAKind):
    RANK = 6
    KIND_COUNTS = [5]
    NAME = 'FiveOfAKind'


class FourOfAKind(OfAKind):
    RANK = 5
    KIND_COUNTS = [4]
    NAME = 'FourOfAKind'


class FullHouse(OfAKind):
    RANK = 4
    KIND_COUNTS = [2, 3]
    NAME = 'FullHouse'


class ThreeOfAKind(OfAKind):
    RANK = 3
    KIND_COUNTS = [3]
    NAME = 'ThreeOfKind'


class TwoPair(OfAKind):
    RANK = 2
    KIND_COUNTS = [2, 2]
    NAME = 'TwoPair'


class Pair(OfAKind):
    RANK = 1
    KIND_COUNTS = [2]
    NAME = 'Pair'


class HighCard(HandRanking):
    RANK = 0
    NAME = 'HighCard'


class Hand(object):
    """
    Given an input string of a given hand of the form "CARDS BID" eg. "32T3K 765"
    Determine what kind of hand this is so you can determine its strength,
    which will let you compute the value of of this hand
    """
    RANKINGS = [Pair, TwoPair, ThreeOfAKind, FullHouse, FourOfAKind, FiveOfAKind]

    def __init__(self, handString, jokersWild=False):
        """
        :param str handString: the string for this hand
        :param bool jokersWild: if true, will treat Js as wild, and pass that information on to the hand rankings
        """
        tokens = handString.split(' ')
        self.cards = [Card(i) for i in tokens[0]]
        self.bid = int(tokens[-1])

        # first, assume we have a high card
        self.ranking = HighCard(self.cards, jokersWild=jokersWild)

        # then, test all of the rankings in order from low to high
        # to see which rank this hand has
        for ranking in self.RANKINGS:
            # if we have the rank
            if ranking(self.cards, jokersWild=jokersWild).handHasRank():
                # and the test ranking is is higher than the hand's current rank
                testRanking = ranking(self.cards)
                if testRanking > self.ranking:
                    self.ranking = testRanking

    def toString(self):
        handString = ''.join([h for h in self.cards])
        handString += f' {self.bid}'
        return handString

    def __str__(self):
        handString = self.toString().split(' ')
        return f"{self.ranking}: {handString[0]} Bid: {handString[-1]}"

    def __repr__(self):
        return f"Hand('{self.toString()}')"

    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.ranking == other.ranking

        return TypeError(f"Comparison between type {type(other)} and Hand not supported.")

    def __lt__(self, other):
        if isinstance(other, Hand):
            return self.ranking < other.ranking

        return TypeError(f"Comparison between type {type(other)} and Hand not supported.")

    def __gt__(self, other):
        if isinstance(other, Hand):
            return self.ranking > other.ranking

        return TypeError(f"Comparison between type {type(other)} and Hand not supported.")     

    def __le__(self, other):
        if isinstance(other, Hand):
            return self.ranking <= other.ranking

        return TypeError(f"Comparison between type {type(other)} and Hand not supported.")

    def __ge__(self, other):
        if isinstance(other, Hand):
            return self.ranking >= other.ranking

        return TypeError(f"Comparison between type {type(other)} and Hand not supported.")


class Solver(solver.solver.ProblemSolver):
    def __init__(self, rawData=None):
        super(Solver, self).__init__(7, rawData=rawData)

    def ProcessInput(self):
        """

        :param str data: the raw input data

        :return str data: since most of the processing happens in the Hand class
        just pass the string through, so we can re-instantiate the hand in Part 2
        with different settings
        """
        return self.rawData

    def SolvePartOne(self):
        """
        Rank all the input hands, and get their winnings based on their ranks

        :return int: the total winnings for all of these hands
        """
        # instatiate the hands here based on them being in part 2
        hands = [Hand(i) for i in self.rawData.splitlines() if i.strip()]

        result = 0

        hands.sort()

        for i, hand in enumerate(hands):
            result += (hand.bid * (i + 1))

        return result

    def SolvePartTwo(self):
        """
        Swap behavior over to Part Two, where Js are wild and 

        :returns int: the total winnings from these hands
        """
        # change out the card rankings
        Card.CARD_RANKS = PARTTWO_RANKS

        # instatiate the hands here based on them being in part 2
        hands = [Hand(i, jokersWild=True) for i in self.rawData.splitlines() if i.strip()]

        result = 0

        hands.sort()

        for i, hand in enumerate(hands):
            result += (hand.bid * (i + 1))

        return result        


if __name__ == '__main__':
    daySolver = Solver()
    if solver.runner.RunTests(daySolver.day):
        daySolver.Run()
