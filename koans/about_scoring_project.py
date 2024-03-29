#!/usr/bin/env python
# -*- coding: utf-8 -*-

from runner.koan import *

# Greed is a dice game where you roll up to five dice to accumulate
# points.  The following "score" function will be used calculate the
# score of a single roll of the dice.
#
# A greed roll is scored as follows:
#
# * A set of three ones is 1000 points
#
# * A set of three numbers (other than ones) is worth 100 times the
#   number. (e.g. three fives is 500 points).
#
# * A one (that is not part of a set of three) is worth 100 points.
#
# * A five (that is not part of a set of three) is worth 50 points.
#
# * Everything else is worth 0 points.
#
#
# Examples:
#
# score([1,1,1,5,1]) => 1150 points
# score([2,3,4,6,2]) => 0 points
# score([3,4,5,3,3]) => 350 points
# score([1,5,1,2,4]) => 250 points
#
# More scoring examples are given in the tests below:
#
# Your goal is to write the score method.

def naiveScore(dice):
    finalScore = 0
    numberCount = [0, 0, 0, 0, 0, 0]
    #add score for 1's and 5's
    for die in dice:
        if die == 1:
            finalScore += 100
        elif die == 5:
            finalScore += 50
        numberCount[die-1] += 1
    #cycle indexing
    i = 0
    #add score for any three number combination
    for count in numberCount:
        i += 1
        if count >= 3:
            #special case, because 1's give 100 points and 
            #set of 1's awards more points
            if i == 1:
                finalScore += 700
            #special case for 5
            elif i == 5:
                finalScore += 350
            else:
                finalScore += i * 100
    return finalScore
    
def score(dice):
    #this solution should scale better, 
    #because there is no list with all possible rolls to go through 

    #trivial case
    if (len(dice) == 0):
        return 0

    finalScore = 0
    streak = 0
    #first roll cannot count towards streak
    lastDie = 0

    #sorted order makes task easier: now all equial rolls are next to each other
    sortedDice = sorted(dice)

    for die in sortedDice:
        if lastDie == die:
            streak += 1
            if streak == 2:#streak of 2 is three in a row
                if die == 1:
                    finalScore += 700
                elif die == 5:
                    finalScore += 350
                else: finalScore += die * 100
                streak = 0
        else:
            streak = 0

        #awards for single 1 and 5 roll
        if die == 1:
            finalScore += 100
        elif die == 5:
            finalScore += 50
        lastDie = die
    return finalScore

class AboutScoringProject(Koan):
    def test_score_of_an_empty_list_is_zero(self):
        self.assertEqual(0, score([]))

    def test_score_of_a_single_roll_of_5_is_50(self):
        self.assertEqual(50, score([5]))

    def test_score_of_a_single_roll_of_1_is_100(self):
        self.assertEqual(100, score([1]))

    def test_score_of_multiple_1s_and_5s_is_the_sum_of_individual_scores(self):
        self.assertEqual(300, score([1,5,5,1]))

    def test_score_of_single_2s_3s_4s_and_6s_are_zero(self):
        self.assertEqual(0, score([2,3,4,6]))

    def test_score_of_a_triple_1_is_1000(self):
        self.assertEqual(1000, score([1,1,1]))

    def test_score_of_other_triples_is_100x(self):
        self.assertEqual(200, score([2,2,2]))
        self.assertEqual(300, score([3,3,3]))
        self.assertEqual(400, score([4,4,4]))
        self.assertEqual(500, score([5,5,5]))
        self.assertEqual(600, score([6,6,6]))

    def test_score_of_mixed_is_sum(self):
        self.assertEqual(250, score([2,5,2,2,3]))
        self.assertEqual(550, score([5,5,5,5]))
        self.assertEqual(1150, score([1,1,1,5,1]))

    def test_ones_not_left_out(self):
        self.assertEqual(300, score([1,2,2,2]))
        self.assertEqual(350, score([1,5,2,2,2]))