import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Background image filenames
maps = ["FinalRuins.gif",
        "DesertRuins.gif",
        "DojoRuins.gif",
        "CityApocalypse.gif",
        "TownOnFire.gif",
        "HouseFire.gif",
        "Rural.gif",
        "Docks.gif",
        "Forest.gif",
        "Prairie.gif",
        "OriginalDojo.png",
        "Jungle.gif",
        "Waterfall.gif",
        "Beach.gif",
        "Bridge.gif",
        "Carnival.gif",
        "Hanger.gif",
        "Airport.gif",
        "Naboo.gif",
        "Temple.gif",
        "FinalJudgement.gif"]
overlay = pygame.image.load('Images/Backgrounds/MapForeground.png')
bg = pygame.image.load('Images/Backgrounds/OriginalDojo.png')
heart = pygame.image.load('Images/heart.png')
death = pygame.image.load('Images/skull.png')

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player,screen):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.active_sprite_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.player_attack_list = pygame.sprite.Group()
        self.enemy_attack_list = pygame.sprite.Group()
        self.screen = screen
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.active_sprite_list.update()
        self.platform_list.update()
        self.player_list.update()
        self.player_attack_list.update()
        self.enemy_list.update()
        self.enemy_attack_list.update()
 
    #Draws all of the sprite lists 
    def draw(self):
        self.player_attack_list.draw(self.screen) 
        self.enemy_attack_list.draw(self.screen) 
        self.platform_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        self.player_list.draw(self.screen)

    #Draws the background and player and enemy stats
    def drawBG(self, game):
        self.screen.blit(bg, (0,0))
        self.screen.blit(overlay, (0,0))
        
        #draw player stats
        for hearts in range(game.player.numHearts):
            self.screen.blit(heart,((game.player.startx + (hearts * 40)), 90))
        for deaths in range(game.player.numDeaths):
            self.screen.blit(death,((game.player.startx + ((deaths % 6) * 40)), (130 + (int(deaths/6)*40))))

        #draw enemy stats
        for hearts in range(game.enemy.numHearts):
            self.screen.blit(heart, ((game.enemy.startx -40 + (hearts * -40)), 90))
        for deaths in range(game.player.numKills):
            self.screen.blit(death,((game.enemy.startx - 40 + ((deaths % 6) * -40)), (130 + (int(deaths/6)*40))))
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player,screen):
        # Call the parent constructor for Level 1
        Level.__init__(self, player,screen)

        #set up our level
        level = [[800,90,0,SCREEN_HEIGHT-90]]
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

#Creates the area that the players walks on
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        #set up the positioning on the screen
        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()