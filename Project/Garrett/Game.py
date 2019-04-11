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
        self.players = []
        self.active_sprite_list = pygame.sprite.Group()
        self.level = None

        drawFlag = False

        self.createPopulation(2)


    def createPopulation(self, numberOfPlayers):
        """ Generate any number of players and add them to an environment"""
        for member in range(numberOfPlayers):
            playerID = str(self.gameNum) + str(member)
            tempPlayer = self.createPlayer(playerID, colors[member], self.screen)
            self.players.append(tempPlayer)
        
        for player in self.players:
            self.setEnvironment(player)    

        for player in self.players:
            if int(player.playerID) % 2 == 0:
                player.setEnemy(self.players[1])    
            else:
                player.setEnemy(self.players[0])
    
    def createPlayer(self, pid, color, position = (400,400), AIFlag = True):
        """ Create a player from player class"""
        player = Player(pid, color, self.screen, AIFlag)
        player.rect.x =  400 # position[0] # x-position
        player.rect.y =  400 # position[1] # y-position
        return player


    def setEnvironment(self, player):
        """ Set up an environment for the players to interact"""
        #if there is no level created, create one and link it to the 1st player
        
        if self.level == None:
            self.level = Level_01(player)
            player.level = self.level
        else:
            player.level = self.level
        
        #add the player to the active sprite list to be updated
        self.active_sprite_list.add(player)
            