import pygame
from Level import *
from Sword import *
import time
import math
import random

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
heart = pygame.image.load('Images/heart.png')
death = pygame.image.load('Images/skull.png')

#hurtSound = pygame.mixer.Sound("SFX/LinkHurtEnemy.wav")
#attackSound = pygame.mixer.Sound("SFX/LinkAttackEnemy.wav")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# *BUG* player doesn't move down when colliding with other players. 
# This results in top player getting the kill 9 times out of 10.

class Enemy(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self, playerID, color, screen, startPos, freeze = False):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 40
        self.height = 60

        self.freeze = freeze

        self.enemy = None
        self.enemyPos = None

        self.maxHearts = 4
        self.numHearts = self.maxHearts
        self.numGoals = 0

        self.color = color 
        self.playerID = playerID

        self.sword = None
        self.isAttacking = False
        self.attackDelay = 30 #30 frames between each attack

        self.direction = "left"

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)

        # So our player can modify the overall screen
        self.screen = screen
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        #coordinate point
        self.player_coord = (self.rect.x, self.rect.y)
        self.startPos = startPos
        self.startx = self.startPos[0]
        self.starty = self.startPos[1]

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
    
    
    def update(self):
        #update neural network
        mouse_pos = pygame.mouse.get_pos()

        if self.attackDelay != 0:
            self.attackDelay -= 1

        self.enemyPos = (self.enemy.rect.x, self.enemy.rect.y)
        self.think(self.enemyPos, mouse_pos, True, self.freeze)

        if self.rect.x <= 0:
            self.numGoals += 1
            self.respawn()
            self.enemy.respawn()

        """ Move the player. """
        # Gravity
        self.calc_grav()
        self.rect.x += self.change_x
        self.calc_friction()

        # Move left/right
    
        if self.isAttacking == True:
            if len(self.level.enemy_attack_list) == 0:
                self.isAttacking = False
                self.sword = None

        # """ Did we just get stabbed? """
        if pygame.sprite.spritecollide(self, self.level.player_attack_list, True):
            # pygame.mixer.Sound.play(hurtSound)
            self.change_x += 10
            self.change_y -= 4
            self.numHearts -= 1


        # ---------------------- INTERACTION WITH PLATFORMS AND SIDE --------------------------

        self.rect.y += self.change_y
        "BOUNDS CHECKING"
        # If the player gets near the right side, shift the world left (-x)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if self.rect.left < 0:
            self.rect.left = 0

        "PLATFORM COLLISION - Y"
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Stop our vertical movement
            self.change_y = 0

        "BLOCK COLLISION - X"
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right


    def think(self, point, mousePoint = None, mouseFlag = False,  freeze = False,):
        """
        Converts output of neural net into events
        that generate actions for the specific player
        in the main driver class
        """
        if freeze:
            return
        # else:
        #     action = random.randint(0,2)
        #     self.executeAction(action)
        if mouseFlag == True:
            if (self.rect.x < mousePoint[0] and self.rect.x + self.width > mousePoint[0]) and (self.rect.y < mousePoint[1] and self.rect.y + self.height > mousePoint[1]):
                self.numHearts -= 1

        if self.distanceToPoint(point, True, RED, "X") < 50:
            self.attack()

        if self.rect.y > point[1]:
            self.jump()
        if self.rect.x < point[0]:
            self.go_right()
        elif self.rect.x > point[0]:
            self.go_left()
    
    def setEnemy(self, enemy):
        if enemy == None:
            self.enemy = None
        self.enemy = enemy

    def updateHealth(self):
        for hearts in range(self.numHearts):
                self.screen.blit(heart, ((self.startx - 160 + (hearts * 40)), 90))
        for deaths in range(self.enemy.numKills):
            self.screen.blit(death,((self.startx - 40 + ((deaths % 6) * -40)), (130 + (int(deaths/6)*40))))
        if self.numHearts <= 0:
            self.respawn()
            self.enemy.numKills += 1
        
    def distanceToPoint(self, point, drawFlag = False, color = WHITE, axis = "BOTH"):
        x_goal = point[0]
        y_goal = point[1]

        player_pos = (self.rect.x + (self.width/2), self.rect.y + (self.height/2))
        x_player = player_pos[0]
        y_player = player_pos[1]

        x_distance = abs(x_goal - x_player)
        y_distance = abs(y_goal - y_player)

        if axis == "BOTH":
            total_distance = x_distance*x_distance + y_distance*y_distance
            total_distance = math.sqrt(total_distance)
            total_distance = int(total_distance)
        if axis == "X":
            total_distance = x_distance
        if axis == "Y":
            total_distance = y_distance

        if drawFlag == True:
            font = pygame.font.SysFont('tahoma', 15, False, False)
            # HIT TEXT
            distanceText = font.render(str(total_distance), True, WHITE)
            x_mid = x_player
            y_mid = y_player
            if x_player <= x_goal:
                x_mid += x_distance/2
            else:
                x_mid -= x_distance/2
            if y_player <= y_goal:
                y_mid += y_distance/2
            else:
                y_mid -= y_distance/2

            if axis =="X":
                pygame.draw.line(self.screen, color, player_pos, (x_goal, y_player), 1)
                midPoint = (x_mid, y_player)
            else:
                pygame.draw.line(self.screen, self.color, player_pos, point, 1)
                midPoint = (x_mid, y_mid)
            self.screen.blit(distanceText, midPoint)

        return total_distance

    def calc_friction(self):
        if self.change_x > 0:
            self.change_x -= .2
        if self.change_x < 0:
            self.change_x += .2
    
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .45
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 4
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 4

 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.change_y = -10
    
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.direction = "left"
        self.image = pygame.image.load('Images/enemyleftangry.png')
        if self.change_x < -4:
            self.change_x = -4
        else:
            self.change_x -= .5

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.direction = "right"
        self.image = pygame.image.load('Images/enemyrightangry.png')
        if self.change_x > 4:
            self.change_x = 4
        else:
            self.change_x += .5

    def attack(self):
        if self.isAttacking == True:
            pass
        elif self.attackDelay == 0:
            # print(self.playerID, " is attacking!")
            if self.direction == "left":
                self.image = pygame.image.load('Images/enemyleftangry.png')
                facing = -1
            if self.direction == "right":
                self.image = pygame.image.load('Images/enemyrightangry.png')
                facing = 1
            if self.direction == "none":
                facing = 0

            self.sword = Sword(self.rect.x, self.rect.y, 40, 20, self.color, facing)
            
            self.level.enemy_attack_list.add(self.sword)
            self.isAttacking = True
            self.attackDelay = 30

    def executeAction(self, action):
        if action == 0:
            self.go_left()
        elif action == 1:
            self.go_right()
        elif action == 2:
            self.jump()
        elif (action == 3 or action == 4):
            self.attack()

    def respawn(self):
        # Respawn back to starting point       
        self.rect.x = self.startx
        self.rect.y = self.starty
        self.numHearts = self.maxHearts