from Player import *
from Level import *
from NeuralNet import *
import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARKSLATEBLUE = (72,61,139)
DEEPSKYBLUE = (0,191,255)
PALEGREEN = (152,251,152)
ROSYBROWN = (188,143,143)
PALEVIOLET = (219,112,147)
YELLOW = (255,255,0)

colors = [RED, BLUE, WHITE, GREEN, DARKSLATEBLUE, DEEPSKYBLUE, PALEGREEN, ROSYBROWN, PALEVIOLET, YELLOW]

class Game():
    def __init__(self, screen, gameNum):
        """ Creates a game that contains two players and a level """
        self.gameNum = gameNum
        self.screen = screen
        self.player = None
        self.enemy = None
        self.level = None
        super().__init__()
        self.entities = []
        self.createPopulation()

    def createPopulation(self):
        """ Generate any number of players and add them to an environment"""
        #create player 1
        playerID = str(self.gameNum) + str(1)
        self.player = Player(playerID, BLUE, self.screen, (100, 300), True)
        self.player.rect.x = 100 # x-position
        self.player.rect.y =  300 # y-position
        self.level = Level_01(self.player)
        self.player.level = self.level

        enemyID = str(self.gameNum) + str(2)
        self.enemy = Player(enemyID, RED, self.screen, (800, 300), False)
        self.enemy.rect.x = 800 # x-position
        self.enemy.rect.y =  300 # y-position
        self.enemy.level = self.level
        
        self.level.player_list.add(self.player)
        self.level.enemy_list.add(self.enemy)

        self.entities.append(self.player)
        self.entities.append(self.enemy)

        self.player.setEnemy(self.enemy)
        self.enemy.setEnemy(self.player)
        #WWWWWWWWWWWWWWWWWWWWWWW
        self.player.brain.generateNetwork()
        self.player.brain.mutate(innovationHistory)
