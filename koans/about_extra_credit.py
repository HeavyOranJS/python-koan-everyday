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
    def __init__(self, number = 1, score = 0, scoreInRound = 0, rolledThisTurn = False,
     gotEmtpyRoll = False, stoppedRolling = False, canEarnPoints = False, endGame = False, dice = 5):
        self.__number = number
        self._score = score
        self._scoreInRound = scoreInRound
        self._rolledThisTurn = rolledThisTurn
        self._gotEmptyRoll = gotEmtpyRoll #doesnt get to have points this turn
        self._stoppedRolling = stoppedRolling #player can stop after first roll
        self._canEarnPoints = canEarnPoints
        self._diceCount = dice
        self.currentDiceCount = self._diceCount

        self._endGame = endGame

    @property
    def score(self):
        return self._score
    
    @property
    def scoreInRound(self):
        return self._scoreInRound

    @scoreInRound.setter
    def scoreInRound(self, score):
        self._scoreInRound = score

    @property
    def gotEmptyRoll(self):
        return self._gotEmptyRoll

    @property
    def canEarnPoints(self):
        return self._canEarnPoints

    @property
    def stoppedRolling(self):
        return self._stoppedRolling

    @stoppedRolling.setter
    def stoppedRolling(self, value):
        self._stoppedRolling = value

    @property
    def number(self):
        """returns player ID number"""
        return self.__number

    def askIfWantToRollAgain(self):
        """ask player if he wants to roll again on this round"""
        print("Player " + str(self.__number) + ". Do you want to roll again? Y/N")
        answer = input()
        while not (answer == "Y" or answer == "N"):
            print("""Please, answer "Y"/"N" """)
            answer = input()
        if answer == "Y":
            return True
        return False

    def _roll(self):
        """returns list with amount of rolls equal to current avaliable dice"""
        return [random.randint(1,6) for i in range(self.currentDiceCount)]

    def rolledEmpty(self):
        """ends turn with mark that player rolled empty"""
        self._gotEmptyRoll = True
        self._scoreInRound = 0
        self.endTurn()

    def canRollAllDiceAgain(self):
        """restores currentDiceCount to full"""
        self.currentDiceCount = self._diceCount

    def startTurn(self):
        """get player ready for a new turn:
            player havent got empty roll in this round yet,
            player havent stopped rolling,
            player's current dice count is full"""
        self._gotEmptyRoll = False
        self._stoppedRolling = False
        self.canRollAllDiceAgain()

    def endTurn(self):
        """apply scores and removie ability to roll"""
        #check if can earn points
        if not self._canEarnPoints:
            if self._scoreInRound > 300:
                self._canEarnPoints = True

        if (self._canEarnPoints and not self._gotEmptyRoll): self._score += self._scoreInRound
        #TODO add print if they havent rolled 300 in one turn yet
        print("Player " + str(self.__number) + " has finished their turn with " +
            str(self._scoreInRound) + " points and now has " +
            str(self._score) + " points.")        
        self._scoreInRound = 0
        self.dice = 0
        self._stoppedRolling = True

class Greed:
    """Greed game. Rules at GREED_RULES.txt
    Minimal amount of players is 2.
    gameEndingPoints defines how many points is needed to trigger last round. Default is 3000"""
    def __init__(self, playerCount = 2, gameEndingPoints = 3000, players = []):
        if playerCount > 2:
            raise ValueError("Minimal amount of players is 2. Your arg was " + str(playerCount)) 
        self._players = players
        self._gameEndingPoints = gameEndingPoints
        playerNumber = 0
        for player in range(playerCount):
            playerNumber += 1
            self._players.append(Player(playerNumber))

    def _game(self):
        print("Game has started.")
        gameIsEnding = False
        roundNumber = 0
        while not gameIsEnding:
            #check if someone has enough points to trigger endgame
            for player in self._players:
                if player.score >= self._gameEndingPoints:
                    gameIsEnding = True
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("Player " + str(player.number) + " has more than " +
                        str(self._gameEndingPoints) +
                        " points! This round is your last chance to catch up!")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            roundNumber += 1
            self._round(roundNumber)
        self._findWinner()
        print("Game has ended.")

    def _findWinner(self):
        winnerScore = 0
        winnerNumber = -1
        for player in self._players:
            if winnerScore < player.score:
                winnerScore = player.score
                winnerNumber = player.number
        print("Player " + str(winnerNumber) + " won with " + str(winnerScore) + "points!")  

    def _round(self, roundNumber):
        #get all players ready for round
        rollNumber = 0
        for player in self._players:
            player.startTurn()
        #everybody rolls first roll of the roundf
        firstRoll = True
        #start round
        #while anyone still wants to roll
        while any(player.stoppedRolling == False for player in self._players):
            #get all players who havent stopped rolling
            rollNumber += 1
            print("-----Round " + str(roundNumber) + " Roll " + str(rollNumber) + "-----")
            for player in self._players:
                if player.stoppedRolling == False:
                    #if this is not a first roll in round check if player wants to stop
                    if firstRoll or player.askIfWantToRollAgain():
                        print("Rolling " + str(player.currentDiceCount) + " dice...")
                        #roll and find score
                        score, nonScoringDice = self._score(player._roll())
                        #check, if roll has no points, then end turn and award no points 
                        if not score == 0:
                            player._scoreInRound += score
                            #if player scored all dice in a throw they can roll all dice again
                            if nonScoringDice == 0:
                                player.canRollAllDiceAgain()
                            else:
                                player.currentDiceCount = nonScoringDice
                            print("Now your score in round is " + str(player._scoreInRound) + "and you have " + str(player.currentDiceCount) + " dice left.")
                        else:
                            player.rolledEmpty()
                    else:
                        player.endTurn()
            firstRoll = False
    #TODO print stats

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
        if (len(dice) < 1):
            raise ValueError("You tried rolling less than a die. UNACCEPTABLEEee")

        #first roll cannot count towards streak
        finalScore = streak = lastDie = scoringDice = 0

        #sorted order makes task easier: now all equial rolls are next to each other
        sortedDice = sorted(dice)

        for die in sortedDice:
            if lastDie == die:
                streak += 1
                if streak == 2:#streak of 2 is three in a row
                    if die == 1:
                        scoringDice += 1
                        finalScore += 700
                    elif die == 5:
                        scoringDice += 1
                        finalScore += 350
                    else: 
                        finalScore += die * 100
                        scoringDice += 3
                    streak = 0
            else:
                streak = 0
            #awards for single 1 and 5 roll
            if die == 1:
                scoringDice += 1
                finalScore += 100
            elif die == 5:
                scoringDice += 1
                finalScore += 50
            lastDie = die
        #TODO tell 0 points is bust and means no points for this round
        print("You've rolled " + ', '.join(str(roll) for roll in dice) + ", this equals to " + str(finalScore) + " points.")
        #if all dice are scoring dice, player can roll all of them again
        #return rolled score and how many dice were non-scoring and can be rolled again
        return finalScore, len(dice) - scoringDice

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
        
        luckyPlayer = Player(300)
        luckyPlayer.endTurn()
        self.assertEqual(300, luckyPlayer.score)

        luckyPlayer._scoreInRound= 1
        luckyPlayer.endTurn()
        self.assertEqual(301, luckyPlayer.score)


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