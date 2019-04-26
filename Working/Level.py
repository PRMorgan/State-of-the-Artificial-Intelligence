import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
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
        # self.enemy_list.update()
        # self.player_list.update()
        # self.attack_list.update()
        # self.player.update()
 
    def draw(self):
        """ Draw everything on this level. """
 
        # Draw all the sprite lists that we have
        self.player_attack_list.draw(self.screen) 
        self.enemy_attack_list.draw(self.screen) 
        self.platform_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        self.player_list.draw(self.screen)

    def drawBG(self, game):
        currentmapindex = (game.player.numGoals - game.enemy.numGoals) + 10
        if currentmapindex > 20:
            currentmapindex = 20
        elif currentmapindex < 0:
            currentmapindex = 0
        bg = pygame.image.load('Images/Backgrounds/' + maps[currentmapindex])
        self.screen.blit(bg, (0,0))
        self.screen.blit(overlay, (0,0))
        
        #draw player stats
        for hearts in range(game.player.numHearts):
            self.screen.blit(heart,((game.player.startx + (hearts * 40)), 90))
        for deaths in range(game.player.numDeaths):
            self.screen.blit(death,((game.player.startx + ((deaths % 6) * 40)), (130 + (int(deaths/6)*40))))

        #draw enemy stats
        for hearts in range(game.enemy.numHearts):
            self.screen.blit(heart, ((game.enemy.startx - 160 + (hearts * 40)), 90))
        for deaths in range(game.player.numKills):
            self.screen.blit(death,((game.enemy.startx - 40 + ((deaths % 6) * -40)), (130 + (int(deaths/6)*40))))

       
        

 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player,screen):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player,screen)
 
        # Array with width, height, x, and y of platform
        """
        # Stairs up on left 1/3 of the screen
        level = [[100, 20, 0, SCREEN_HEIGHT - 20],
                 [100, 40, 100, SCREEN_HEIGHT - 40],
                 [100, 60, 200, SCREEN_HEIGHT - 60],
                 ]
        """

        # Arena-style... arena...
        """
        level = [[100, 60, 0, SCREEN_HEIGHT - 60],
                [100, 40, 100, SCREEN_HEIGHT - 40],
                [100, 20, 200, SCREEN_HEIGHT - 20],
                [100, 20, SCREEN_WIDTH - 500, SCREEN_HEIGHT - 5],
                [100, 20, SCREEN_WIDTH - 400, SCREEN_HEIGHT - 5],
                [100, 20, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 20],
                [100, 40, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40],
                [100, 60, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60],
                ]
        """

        level = [[800,90,0,SCREEN_HEIGHT-90]]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        #self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()

    def draw(self):
        print("let's draw a sword")