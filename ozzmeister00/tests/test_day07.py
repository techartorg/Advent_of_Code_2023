from unittest import TestCase

import solutions.day07

class Test(TestCase):
    def test_card(self):
        # test instantiation from string
        card = solutions.day07.Card('A')

        # test instantiation from int
        card = solutions.day07.Card(0)

        # test bad instantiations
        defaultCard = solutions.day07.Card()
        self.assertEqual('2', defaultCard)

        self.assertRaises(ValueError, solutions.day07.Card, 'B')
        self.assertRaises(ValueError, solutions.day07.Card, 100)

        # make sure the ranks work
        ace = solutions.day07.Card('A')
        otherAce = solutions.day07.Card('A')
        two = solutions.day07.Card('2')

        self.assertEqual(two.rank, 0)
        self.assertEqual(ace.rank, 12)

        # test comparisons
        self.assertEqual(ace, otherAce)
        self.assertNotEqual(ace, two)
        self.assertTrue(ace > two)
        self.assertTrue(ace >= otherAce)
        self.assertTrue(ace >= two)
        self.assertTrue(two < ace)
        self.assertTrue(ace <= otherAce)
        self.assertTrue(two <= otherAce)

        # make sure that we can sort an array of cards
        inCardString = 'A2KT3'
        cardList = [solutions.day07.Card(i) for i in inCardString]
        cardList.sort()
        
        cardString = ''.join(cardList)
        expectedCardString = '23TKA'

        self.assertEqual(cardString, expectedCardString)

    def test_handRankings(self):
        # test instantiation from String
        highCardLow = solutions.day07.HighCard('23456')
        highCardHigh = solutions.day07.HighCard('789TJ')

        fiveOfAKindLow = solutions.day07.FiveOfAKind('22222')
        fiveOfAKindHigh = solutions.day07.FiveOfAKind('AAAAA')

        # validation
        self.assertEqual(highCardLow.RANK, 0)
        self.assertEqual(fiveOfAKindLow.RANK, 6)

        # comparison
        self.assertTrue(highCardLow < fiveOfAKindLow)
        self.assertTrue(highCardLow < highCardHigh)
        self.assertTrue(fiveOfAKindLow != fiveOfAKindHigh)
        self.assertTrue(fiveOfAKindLow <= fiveOfAKindHigh)

        # comparison with trickier cases
        fourThrees = solutions.day07.FourOfAKind('33332')
        fourAces = solutions.day07.FourOfAKind('2AAAA')

        self.assertTrue(fourThrees > fourAces)

        eightsOverSevens = solutions.day07.FourOfAKind('77888')
        sevensOverEights = solutions.day07.FourOfAKind('77788')

        self.assertTrue(eightsOverSevens > sevensOverEights)

    def test_hand(self):
        # test to make sure all the hand types instantiate to the correct 
        # ranking class

        solutions.day07.Card.CARD_RANKS = solutions.day07.PARTONE_RANKS

        cardStrings = [('23456 111', solutions.day07.HighCard),
                       ('22345 111', solutions.day07.Pair), 
                       ('22334 111', solutions.day07.TwoPair),
                       ('22333 111', solutions.day07.FullHouse),
                       ('22223 111', solutions.day07.FourOfAKind),
                       ('22222 111', solutions.day07.FiveOfAKind)]

        for cardString, expectedType in cardStrings:
            self.assertEqual(type(solutions.day07.Hand(cardString).ranking), expectedType, msg=f"{cardString} did not rank to {expectedType}")



class TestPartTwo(TestCase):
    def setUpTest(self):
        solutions.day07.Card.CARD_RANKS = solutions.day07.PARTTWO_RANKS 

    def test_partTwo(self):
        cardStrings = [('JJ553 526', solutions.day07.FourOfAKind),
                       ('JJJJJ 302', solutions.day07.FiveOfAKind),
                       ('JJJJ8 466', solutions.day07.FiveOfAKind),
                       ('J365A 466', solutions.day07.Pair)]

        solutions.day07.Card.CARD_RANKS = solutions.day07.PARTTWO_RANKS

        for cardString, expectedType in cardStrings:
            self.assertEqual(type(solutions.day07.Hand(cardString, jokersWild=True).ranking), expectedType, msg=f"{cardString} did not rank to {expectedType}")

        lower = solutions.day07.Hand("JKKK2 111", jokersWild=True)
        higher = solutions.day07.Hand("QQQQ2 111", jokersWild=True)

        self.assertEqual(lower.ranking, solutions.day07.FourOfAKind)
        self.assertEqual(higher.ranking, solutions.day07.FourOfAKind)
        self.assertTrue(higher > lower)

    def tearDownTest(self):
        solutions.day07.Card.CARD_RANKS = solutions.day07.PARTONE_RANKS 

