from Player import *
from Enemy import *
from Level import *
import random
import pygame

#Sets up a game between the AI and non-AI
class Game():
    def __init__(self, screen, player=None):
        """ Creates a game that contains two players and a level """
        self.screen = screen
        if player != None:
            self.player = player.clone()
        else:
            self.player = None
        self.enemy = None
        self.level = None
        self.entities = []
        self.intiializeGame() #set up each game

    #Update the health of both
    def updateAllHealth(self):
        self.player.updateHealth()
        self.enemy.updateHealth()
    
    #Add the players to the environment
    def intiializeGame(self):
        #Add the AI
        if self.player == None:
            self.player = Player(self.screen, (0,450))
        self.player.rect.x = 0 # x-position
        self.player.rect.y =  450 # y-position
        self.level = Level_01(self.player,self.screen)
        self.player.level = self.level

        #Add the enemy
        self.enemy = Enemy(self.screen, (800,450))
        self.enemy.rect.x = 800 # x-position
        self.enemy.rect.y =  450 # y-position
        self.enemy.level = self.level
        
        #Add the players to the player list for the game
        self.level.player_list.add(self.player)
        self.level.enemy_list.add(self.enemy)

        self.entities.append(self.player)
        self.entities.append(self.enemy)

        self.player.setEnemy(self.enemy)
        self.enemy.setEnemy(self.player)


