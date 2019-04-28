import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load all background images
maps = [pygame.image.load('Images/Backgrounds/FinalRuins.gif'),
        pygame.image.load('Images/Backgrounds/DesertRuins.gif'),
        pygame.image.load('Images/Backgrounds/DojoRuins.gif'),
        pygame.image.load('Images/Backgrounds/CityApocalypse.gif'),
        pygame.image.load('Images/Backgrounds/TownOnFire.gif'),
        pygame.image.load('Images/Backgrounds/HouseFire.gif'),
        pygame.image.load('Images/Backgrounds/Rural.gif'),
        pygame.image.load('Images/Backgrounds/Docks.gif'),
        pygame.image.load('Images/Backgrounds/Forest.gif'),
        pygame.image.load('Images/Backgrounds/Prairie.gif'),
        pygame.image.load('Images/Backgrounds/OriginalDojo.png'),
        pygame.image.load('Images/Backgrounds/Jungle.gif'),
        pygame.image.load('Images/Backgrounds/Waterfall.gif'),
        pygame.image.load('Images/Backgrounds/Beach.gif'),
        pygame.image.load('Images/Backgrounds/Bridge.gif'),
        pygame.image.load('Images/Backgrounds/Carnival.gif'),
        pygame.image.load('Images/Backgrounds/Hanger.gif'),
        pygame.image.load('Images/Backgrounds/Airport.gif'),
        pygame.image.load('Images/Backgrounds/Naboo.gif'),
        pygame.image.load('Images/Backgrounds/Temple.gif'),
        pygame.image.load('Images/Backgrounds/FinalJudgement.gif')]

overlay = pygame.image.load('Images/Backgrounds/MapForeground.png')
bg = pygame.image.load('Images/Backgrounds/OriginalDojo.png')
heart = pygame.image.load('Images/heart.png')
death = pygame.image.load('Images/skull.png')
playerleft = pygame.image.load('Images/playerleftangry.png')
playerright = pygame.image.load('Images/playerrightangry.png')
enemyleft = pygame.image.load('Images/enemyleftangry.png')
enemyright = pygame.image.load('Images/enemyrightangry.png')

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

        self.playerdirection = "right"
        self.enemydirection = "left"
        self.currentmap = 10
         
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
    def draw(self, game):
        #choose player sprite if theyve changed direction
        if game.player.direction != self.playerdirection:
            if game.player.direction == "right":
                game.player.image = playerright
            else:
                game.player.image = playerleft
            self.playerdirection = game.player.direction
        
        if game.enemy.direction != self.enemydirection:
            if game.enemy.direction == "right":
                game.enemy.image = enemyright
            else:
                game.enemy.image = enemyleft
            self.enemydirection = game.enemy.direction

        self.player_attack_list.draw(self.screen) 
        self.enemy_attack_list.draw(self.screen) 
        self.platform_list.draw(self.screen)
        self.enemy_list.draw(self.screen)
        self.player_list.draw(self.screen)

    #Draws the background and player and enemy stats
    def drawBG(self, screen, game):
        # Display the current map in terms of who has more kills.
        # If enemy has more kills, we profress towards their 'goal.'
        # If player has more goals, we progress towards their 'goal.'
        # Each entity has a set of 10 maps and one neutral ground.
        currentMapIndex = (game.player.numGoals - game.enemy.numGoals) + 10
        if currentMapIndex != self.currentmap:
            if currentMapIndex > 20:
                currentMapIndex = 20
            elif currentMapIndex < 0:
                currentMapIndex = 0
            bg = maps[currentMapIndex]
        screen.blit(bg, (0,0))
        screen.blit(overlay, (0,0))
        
        #draw player stats
        for hearts in range(game.player.numHearts):
            self.screen.blit(heart,((game.player.startx + (hearts * 40)), 75))
        for deaths in range(game.player.numDeaths):
            self.screen.blit(death,((game.player.startx + ((deaths % 6) * 40)), (115 + (int(deaths/6)*40))))

        #draw enemy stats
        for hearts in range(game.enemy.numHearts):
            self.screen.blit(heart, ((game.enemy.startx -40 + (hearts * -40)), 75))
        for deaths in range(game.player.numKills):
            self.screen.blit(death,((game.enemy.startx - 40 + ((deaths % 6) * -40)), (115 + (int(deaths/6)*40))))
 
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