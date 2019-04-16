from Player import *
from Level import *
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

        self.entities = []

        self.createPopulation()

    def createPopulation(self):
        """ Generate any number of players and add them to an environment"""
        #create player 1
        playerID = str(self.gameNum) + str(1)
        self.player = Player(playerID, BLUE, self.screen, True)
        self.player.rect.x = 100 # x-position
        self.player.rect.y =  300 # y-position
        self.level = Level_01(self.player)
        self.player.level = self.level


        enemyID = str(self.gameNum) + str(2)
        self.enemy = Player(enemyID, RED, self.screen, False)
        self.enemy.rect.x = 800 # x-position
        self.enemy.rect.y =  300 # y-position
        self.enemy.level = self.level
        
        self.level.player_list.add(self.player)
        self.level.enemy_list.add(self.enemy)

        self.entities.append(self.player)
        self.entities.append(self.enemy)



        self.player.setEnemy(self.enemy)
        self.enemy.setEnemy(self.player)

    
    # def createPlayer(self, pid, color, position, AIFlag = True, freeze = False):
    #     """ Create a player from player class"""
    #     player = Player(pid, color, self.screen, AIFlag, freeze)
    #     player.rect.x =  position[0] # x-position
    #     player.rect.y =  position[1] # y-position
    #     self.players.append(player)
    #     self.setEnvironment(player)
    #     return player


    # def setEnvironment(self, player):
    #     """ Set up an environment for the players to interact"""
    #     #if there is no level created, create one and link it to the 1st player
        
    #     if self.level == None:
    #         self.level = Level_01(player)
    #         player.level = self.level
    #     else:
    #         player.level = self.level
        
    #     #add the player to the active sprite list to be updated
    #     self.active_sprite_list.add(player)
