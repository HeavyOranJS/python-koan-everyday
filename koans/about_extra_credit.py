#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

import random

from runner.koan import *
from about_dice_project import DiceSet

class Player():
    """Player class with player info. 
    By default should be empty, all variables are for testing purposes."""
    def __init__(self, score = 0, scoreInRound = 0, rolledThisTurn = False,
     gotEmtpyRoll = False, stoppedRolling = False, canEarnPoints = False, endGame = False):
        self._score = score
        self._scoreInRound = scoreInRound
        self._rolledThisTurn = rolledThisTurn
        self._gotEmptyRoll = gotEmtpyRoll #doesnt get to have points this turn
        self._stoppedRolling = stoppedRolling #player can stop after first roll
        self._canEarnPoints = canEarnPoints

        self._endGame = endGame

    @property
    def score(self):
        return self._score
    
    @property
    def scoreInRound(self):
        return self._scoreInRound

    @property
    def gotEmptyRoll(self):
        return self._gotEmptyRoll

    @property
    def canEarnPoints(self):
        return self._canEarnPoints

    def _roll(self, diceAmount):
        self._values = [random.randint(1,6) for i in range(diceAmount)]

    def startTurn(self):
        self._stoppedRolling = True

    def endTurn(self):
        if (self._canEarnPoints and not self._gotEmptyRoll): self._score += self._scoreInRound
        self._scoreInRound = 0
        
        self._stoppedRolling = True

class Greed():
    """Greed game. Rules at GREED_RULES.txt
    Minimal amount of players is 2."""
    def __init__(self, playerCount = 2, players = []):
        if playerCount > 2:
            raise ValueError("Minimal amount of players is 2. Your arg was " + str(playerCount)) 
        self._players = players
        for player in range(playerCount):
            self._players.append(Player())

    def game(self):
        pass

    def isEndgame(self):
        for player in self._players:
            if player.score >= 3000:
                return True
        return False

    def howManyPlayers(self):
        return len(self._players)

    #could import this from about_scoring_project if wrap this in class
    def _score(self, dice):
        #trivial case
        if (len(dice) < 0):
            raise ValueError("You tried rolling less than a die. UNACCEPTABLEEee")

        #first roll cannot count towards streak
        finalScore = streak = lastDie = 0

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

class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py
    def test_extra_credit_task(self):
        pass
        
#------------------player tests--------------    
    def test_players_can_roll(self):
        newb = Player()
        self.assertEqual(1, len(newb._roll(1)))
        self.assertEqual(5, len(newb._roll(5)))        

    def test_cannot_earn_points_untill_300_in_one_turn(self):
        sadPlayer = Player(scoreInRound=299)
        sadPlayer.endTurn()
        self.assertEqual(0, sadPlayer.score)
        
        sadPlayer.scoreInRound = 300
        sadPlayer.endTurn()
        self.assertEqual(300, sadPlayer.score)

        sadPlayer.scoreInRound = 1
        sadPlayer.endTurn()
        self.assertEqual(301, sadPlayer.score)


    #TODO implement some sort of controlled rolling, 
    # so i could check certain combinations
    def test_players_cant_roll_more_dice_than_nonscoring_dice_last_turn(self):
        pass

    def test_player_can_end_turn(self):
        #player can stop his turn on any roll after first one 
        #and add current round points to score
        
        #check player cannot roll after he stopped
        #! check player can(must) roll on the next turn
        pass

    def test_lucky_roll(self):
        #if all dice scored, player can roll again all dice
        pass

    def test_unlucky_roll(self):
        #player ends turn after an empty roll
        #player loses all current round points after empty roll
        #
        pass


#------------------game tests-----------------
    def test_greed_player_amounts(self):
        newGame = Greed(2)
        self.assertEqual(newGame.howManyPlayers, 2)

        newGame = Greed(10)
        self.assertEqual(newGame.howManyPlayers, 10)

        with self.assertRaises(ValueError):
            newGame = Greed(1)

    def test_greed_can_score(self):
        #score function was already tested
        pass

    def test_greed_rolls_per_turn(self):
        #cannot have less than one roll per turn, 
        #can have more,
        #player always rolls all five dice at turn one
        # cannot roll after players stopped or rolled empty
        pass

    def test_endgame_happens_when_one_of_players_has_3000_or_more_points(self):
        newGame = Greed()
        #TODO test newGame.isEndstep somehow
        pass

#------------TODO tests ---------------------
    def test_amount_of_nonscoring_dice(self):
        pass
        
    # check in greed tests: player cannot roll more than 5 dice