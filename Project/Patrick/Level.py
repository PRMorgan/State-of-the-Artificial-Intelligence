import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.attack_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        self.attack_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLACK)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.attack_list.draw(screen) 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[100, 20, 0, SCREEN_HEIGHT - 20],
                 [100, 40, 100, SCREEN_HEIGHT - 40],
                 [100, 60, 200, SCREEN_HEIGHT - 60],
                 ]
 
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
 
        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()



class Sword(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color,facing):

        super().__init__()
        self.facing = facing

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        if facing == -1:
            self.rect.x = x - 50
            self.rect.y = y + 30
        elif facing == 1:
            self.rect.x = x + 50
            self.rect.y = y + 30
        else:
            self.rect.x = x + width
            self.rect.y = y - 20

        # for sword in attack_list:
        #     sword.rect.x = self.x
        #     sword.rect.y = self.y
        # self.attack_list.add(sword)

    # def draw(self, win):
    #     pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, 60, 20))
