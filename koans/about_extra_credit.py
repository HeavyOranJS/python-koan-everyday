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

class Player:
    """Player class with player info. 
    Number is effectivly ID, dice is amount of dice player can use in one roll"""
    def __init__(self, number = 1, dice = 5):
        self.__number = number
        self._score = 0
        self._scoreInRound = 0
        self._rolledThisTurn = False
        self._gotEmptyRoll = False #doesnt get to have points this turn
        self._stoppedRolling = False #player can stop after first roll
        self._canEarnPoints = False
        self._diceCount = dice
        self.currentDiceCount = self._diceCount

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

    def info(self):
        """returns nicely formatted string with player ID and score"""
        return "[Player " + str(self.__number)+ ": "+ str(self.score) + "]" 

    def askIfWantToRollAgain(self):
        """ask player if he wants to roll again on this round"""
        print(self.info() + " Do you want to roll again? Y/N")
        answer = input()
        while not (answer == "Y" or answer == "N"):
            print("""Please, answer "Y"/"N" """)
            answer = input()
        if answer == "Y":
            return True
        return False

    def roll(self):
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
        if not self._canEarnPoints:
            print("To start earn points you need to get 300 points in one round.")
        print(self.info() + " has finished their turn with " +
            str(self._scoreInRound) + " points and now has " +
            str(self._score) + " points.")        
        self._scoreInRound = 0
        self.currentDiceCount = 0
        self._stoppedRolling = True

class Greed:
    """Greed game. Rules at GREED_RULES.txt
    Minimal amount of players is 2.
    gameEndingPoints defines how many points is needed to trigger last round. Default is 3000"""
    def __init__(self, playerCount = 2, gameEndingPoints = 3000, players = []):
        if playerCount < 2:
            raise ValueError("Minimal amount of players is 2. Your arg was " + str(playerCount)) 
        self._players = players
        self._gameEndingPoints = gameEndingPoints

        self._players = []#resets players between games
        #without this append just adds new players to end of previous player list

        playerNumber = 0
        for player in range(playerCount):
            playerNumber += 1
            self._players.append(Player(playerNumber))

    def _game(self):
        print("Game has started.")
        endgameStarts = False
        roundNumber = 0
        #repeat rounds until someone has enough points to trigger endGame
        while not endgameStarts:
            #while self.isEndgame finishes game as soon as someone gets gameEndingPoints
            #but there should be one more round
            endgameStarts = self.isEndgame()
            roundNumber += 1
            self._round(roundNumber)
        self._scoreboard()
        print("Game has ended.")

    def _scoreboard(self):
        """Print scoreboard and winner of the game"""
        winnerScore = 0
        winnerNumber = -1
        print("-----SCOREBOARD-----")
        for player in self._players:
            print(player.info())
            if winnerScore < player.score:
                winnerScore = player.score
                winnerNumber = player.number 
        print("[Player " + str(winnerNumber) + "] won with " + str(winnerScore) + " points!")  

    def _round(self, roundNumber):
        #get all players ready for round
        rollNumber = 0
        for player in self._players:
            player.startTurn()
        #everybody rolls first roll of the round
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
                        print(player.info() + " is rolling " + str(player.currentDiceCount) + " dice...")
                        #roll and find score
                        score, nonScoringDice = self._score(player.roll())
                        #check, if roll is empty, then end turn and award no points 
                        if not score == 0:
                            player._scoreInRound += score
                            #if player scored all dice in a throw they can roll all dice again
                            if nonScoringDice == 0:
                                player.canRollAllDiceAgain()
                            else:
                                player.currentDiceCount = nonScoringDice
                            print("Now your score in round is " + str(player._scoreInRound) + 
                                " and you have " + str(player.currentDiceCount) + " dice left.")
                        else:
                            player.rolledEmpty()
                    else:
                        player.endTurn()
            firstRoll = False
    #TODO print stats

    def isEndgame(self):
        """Check if one of the players have enough points to trigger endgame.
            If endgame is triggered print info about in"""
        for player in self._players:
            if player.score >= self._gameEndingPoints:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(player.info() + " has more than " +
                    str(self._gameEndingPoints) +
                    " points! This round is your last chance to catch up!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
                        finalScore += 700
                    elif die == 5:
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
        if finalScore == 0:
            print("BUST!")
        print("You've rolled " + ', '.join(str(roll) for roll in dice) + 
            ", and got " + str(finalScore) + " points.")
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
        newb.currentDiceCount = 1 
        self.assertEqual(1, len(newb.roll()))

        gosu = Player()
        gosu.currentDiceCount = 10
        self.assertEqual(10, len(gosu.roll()))        

    def test_cannot_earn_points_untill_rolled_more_than_300_in_one_turn(self):
        sadPlayer = Player()
        sadPlayer.scoreInRound = 300
        sadPlayer.endTurn()
        self.assertEqual(0, sadPlayer.score)

    def test_can_earn_points_after_rolled_more_than_300_in_one_turn(self):
        #should get 300 points
        luckyPlayer = Player()
        luckyPlayer.scoreInRound = 301
        luckyPlayer.endTurn()
        self.assertEqual(301, luckyPlayer.score)

        #should get points after he got 300 points
        luckyPlayer._scoreInRound= 1
        luckyPlayer.endTurn()
        self.assertEqual(302, luckyPlayer.score)

    def test_player_can_end_turn(self):
        player = Player()
        player.endTurn()
        self.assertEquals(True, player._stoppedRolling)

    def test_player_can_start_turn(self):
        player = Player()
        player._stoppedRolling = True
        player.currentDiceCount = 0
        player.startTurn()
        self.assertEquals(False, player._stoppedRolling)
        self.assertEquals(player.currentDiceCount, player._diceCount)

    def test_lucky_roll(self):
        luckyPlayer = Player()
        luckyPlayer.currentDiceCount = 0
        luckyPlayer.canRollAllDiceAgain()
        self.assertEqual(luckyPlayer._diceCount, len(luckyPlayer.roll()))

    def test_unlucky_roll(self):
        unluckyPlayer = Player()
        unluckyPlayer.rolledEmpty()
        self.assertEqual(0, unluckyPlayer.currentDiceCount)


#------------------game tests-----------------
    def test_greed_player_amount(self):
        newGame = Greed()
        print("players = " + str(len(newGame._players)))
        self.assertEqual(newGame.howManyPlayers(), 2)

        newGame = Greed(playerCount=10)
        self.assertEqual(newGame.howManyPlayers(), 10)

        with self.assertRaises(ValueError):
            newGame = Greed(1)

    def test_greed_can_score(self):
        newGame = Greed()
        score, nonScoringDice = newGame._score([1,1,1])
        self.assertEqual(score, 1000)
        self.assertEqual(nonScoringDice, 0)

    def test_greed_scores_special_streaks(self):
        newGame = Greed()
        score, nonScoringDice = newGame._score([5, 5, 5, 5])
        self.assertEqual(score, 550)
        self.assertEqual(nonScoringDice, 0)

    def test_greed_scores_streaks(self):
        newGame = Greed()
        score, nonScoringDice = newGame._score([6, 6, 6, 6])
        self.assertEqual(score, 600)
        self.assertEqual(nonScoringDice, 1)
        
    def test_greed_scores_empty_rolls(self):
        newGame = Greed()
        score, nonScoringDice = newGame._score([2, 3, 4, 6])
        self.assertEqual(score, 0)
        self.assertEqual(nonScoringDice, 4)

    def test_endgame_doesnt_happen_until_one_of_players_has_3000_or_more_points(self):
        newGame = Greed(gameEndingPoints=3000)
        newGame._players[0]._score = 2999 
        self.assertEqual(newGame.isEndgame(), False)

    def test_endgame_happens_when_one_of_players_has_3000_or_more_points(self):
        newGame = Greed(gameEndingPoints=3000)
        newGame._players[0]._score = 3000 
        self.assertEqual(newGame.isEndgame(), True)