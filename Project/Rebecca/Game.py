from Player import *
from Enemy import *
from Level import *
import random
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

BLUE = (0,0,255)
MEDIUMBLUE = (0,0,205)
MIDNIGHTBLUE = (25,25,112)
ROYALBLUE = (65,105,225)
INDIGO = (75,0,130)
DARKSLATE = (72,61,139)
SLATEBLUE = (106,90,205)

MAROON = (128,0,0)
BROWN = (165,42,42)
FIREBRICK = (178,34,34)
CRIMSON = (220,20,60)
RED = (255,0,0)
ORANGERED = (255,69,0)
TOMATO = (255,99,71)

darkcolors = [BLUE, MEDIUMBLUE, MIDNIGHTBLUE, ROYALBLUE, INDIGO, DARKSLATE, SLATEBLUE]
warmcolors = [MAROON, BROWN, FIREBRICK, CRIMSON, RED, ORANGERED, TOMATO]
class Game():
    def __init__(self, screen, player=None):
        """ Creates a game that contains two players and a level """
        #self.gameNum = gameNum
        self.screen = screen
        self.player = player
        self.enemy = None
        self.level = None

        self.entities = []

        self.intiializeGame()


    def updateAllHealth(self):
        self.player.updateHealth()
        self.enemy.updateHealth()
        

    def intiializeGame(self):
        """ Generate any number of players and add them to an environment"""
        #create player 1
        self.player = Player(darkcolors[random.randint(0,len(darkcolors) - 1)], self.screen, (0,450))
        self.player.rect.x = 0 # x-position
        self.player.rect.y =  450 # y-position
        self.level = Level_01(self.player,self.screen)
        self.player.level = self.level

        #enemyID = str(self.gameNum) + str(2)
        self.enemy = Enemy(warmcolors[random.randint(0,len(warmcolors) - 1)], self.screen, (800,450))
        self.enemy.rect.x = 800 # x-position
        self.enemy.rect.y =  450 # y-position
        self.enemy.level = self.level
        
        self.level.player_list.add(self.player)
        self.level.enemy_list.add(self.enemy)

        self.entities.append(self.player)
        self.entities.append(self.enemy)

        self.player.setEnemy(self.enemy)
        self.enemy.setEnemy(self.player)

