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
SCREEN_HEIGHT = 600 #This is strictly for the game partition
SCREEN_WIDTH_EXT = 1300 #Extension side for data display

# Background image filenames
MapForeground = "MapForeground.png"
Airport = "Airport.gif"
Beach = "Beach.gif"
Bridge = "Bridge.gif"
Carnival = "Carnival.gif"
CityApocalypse = "CityApocalypse.gif"
DesertRuins = "DesertRuins.gif"
Docks = "Docks.gif"
DojoRuins = "DojoRuins.gif"
CityApocalypse = "CityApocalypse.gif"
FinalJudgement = "FinalJudgement.gif"
FinalRuins = "FinalRuins.gif"
Forest = "Forest.gif"
Hanger = "Hanger.gif"
HouseFire = "HouseFire.gif"
Jungle = "Jungle.gif"
Naboo = "Naboo.gif"
OriginalDojo = "OriginalDojo.png"
Prairie = "Prairie.gif"
Rural = "Rural.gif"
Temple = "Temple.gif"
TownOnFire = "TownOnFire.gif"
Waterfall = "Waterfall.gif"

maps = [FinalRuins,DesertRuins,DojoRuins,CityApocalypse,TownOnFire,
        HouseFire,Rural,Docks,Forest,OriginalDojo,Jungle,Waterfall,
        Prairie,Beach,Carnival,Hanger,Airport,Naboo,Temple,FinalJudgement]
randomBackground = maps[random.randint(0,len(maps))]
                  
bg = pygame.image.load('Images/Backgrounds/' + randomBackground)
overlay = pygame.image.load('Images/Backgrounds/' + MapForeground)
#bg = pygame.image.load('Images/Backgrounds/arena86.jpg')

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.active_sprite_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.player_attack_list = pygame.sprite.Group()
        self.enemy_attack_list = pygame.sprite.Group()
         
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
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        # screen.fill(BLACK)
 
        # Draw all the sprite lists that we have
        self.player_attack_list.draw(screen) 
        self.enemy_attack_list.draw(screen) 
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.player_list.draw(screen)

    def drawBG(self, screen):
        screen.blit(bg, (0,0))
        screen.blit(overlay, (0,0))
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
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