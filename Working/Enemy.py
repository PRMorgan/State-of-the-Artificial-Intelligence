import pygame
from Level import *
from Sword import *
import time
import math
import random

#hurtSound = pygame.mixer.Sound("SFX/LinkHurtEnemy.wav")
#attackSound = pygame.mixer.Sound("SFX/LinkAttackEnemy.wav")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#The enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, startPos, freeze = False): 
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

        self.sword = None
        self.isAttacking = False
        self.attackDelay = 30 #30 frames between each attack
        self.respawnDelay = 30 #Don't redraw the enemy upon death for 30 frames

        self.direction = "left"

        #The enemy starts by looking left
        self.image = pygame.image.load('Images/enemyleftangry.png')

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
    
    #Updates for each frame so the enemy can interact with the environment 
    def update(self):
        mouse_pos = pygame.mouse.get_pos() #We can use the mouse to effect the enemy

        if self.attackDelay != 0:
            self.attackDelay -= 1
        if self.attackDelay == 0:
            self.attack()

        #Figure out where the other player is
        self.enemyPos = (self.enemy.rect.x, self.enemy.rect.y)

        #Pick an action (Not an AI)
        self.think(self.enemyPos, mouse_pos, True, self.freeze)

        #If we died, we need to respawn
        if self.rect.x <= 0:
            self.numGoals += 1
            self.respawn()
            self.enemy.respawn()

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
            self.enemy.numHits += 1


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

    #An algorithm that chooses what action to do based on where the enemy is
    #also allows us to hurt the enemy with a mouse
    def think(self, point, mousePoint = None, mouseFlag = False,  freeze = False,):
        """
        Converts output of neural net into events
        that generate actions for the specific player
        in the main driver class
        """
        if freeze:
            return
        #add some random vairation
        action = random.randint(0,70)
        if action == 0:
            self.go_left()
        if action == 1:
            self.go_right()
        if action == 2:
            self.jump()
        if action == 3:
            self.attack()

        if mouseFlag == True:
            if (self.rect.x < mousePoint[0] and self.rect.x + self.width > mousePoint[0]) and (self.rect.y < mousePoint[1] and self.rect.y + self.height > mousePoint[1]):
                self.numHearts -= 1

        if self.rect.y > point[1]:
            self.jump()
        if self.rect.x < point[0]:
            self.go_right()
        elif self.rect.x > point[0]:
            self.go_left()
    
    #Set the enemy
    def setEnemy(self, enemy):
        if enemy == None:
            self.enemy = None
        self.enemy = enemy

    #Update the health of the enemy
    def updateHealth(self):
        if self.numHearts <= 0:
            if self.respawnDelay == 0:
                self.respawn() #Respawn on death
                self.enemy.numKills += 1
                self.respawnDelay = 30
            else:
                self.respawnDelay -= 1
                self.rect.x = self.startx
                self.rect.y = -self.height

    #Calculate friction
    def calc_friction(self):
        if self.change_x > 0:
            self.change_x -= .2
        if self.change_x < 0:
            self.change_x += .2
    
    #Calculate the effect of gravity
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .45
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
    
    #Make a jump
    def jump(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 4
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 4
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.change_y = -10
    
    #Move to the left
    def go_left(self):
        self.direction = "left"
        if self.change_x < -4:
            self.change_x = -4
        else:
            self.change_x -= .5

    #Move to the right
    def go_right(self):
        self.direction = "right"
        if self.change_x > 4:
            self.change_x = 4
        else:
            self.change_x += .5

    #Make an attack
    def attack(self):
        if self.isAttacking == True:
            pass
        elif self.attackDelay == 0:
            if self.direction == "left":
                facing = -1
            if self.direction == "right":
                facing = 1
            if self.direction == "none":
                facing = 0
            self.sword = Sword(self.rect.x, self.rect.y, 40, 20, facing)
            self.level.enemy_attack_list.add(self.sword)
            self.isAttacking = True
            self.attackDelay = 30

    #Respawn back to the starting point
    def respawn(self):     
        self.rect.x = self.startx
        self.rect.y = self.starty
        self.numHearts = self.maxHearts