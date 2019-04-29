import pygame
from Level import *
from Sword import *
from NeuralNet import *
import time
import math
import random

#Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#The AI player
class Player(pygame.sprite.Sprite):
    def __init__(self, screen, startPos, fitness=0.0): 
        # Call the parent's constructor
        super().__init__()
 
        # Create a player
        self.width = 40 #width of player
        self.height = 60 #height of player
        self.enemy = None #initialize the opponent
        self.enemyPos = None #Later, will be used to track where the opponent is

        self.maxHearts = 4 #max "health"
        self.numHearts = 4 #track how many hits we've taken

        self.numDeaths = 0 #track how many times we've died 
        self.numKills = 0 #track how many times we've killed the opponent
        self.numGoals = 0 #How many times have we made it to the other side of the board?
        self.numHits = 0 #How many times the player has made a successful attack
        self.runningDistance = 0 #How far have the player moved (running total per life)
        self.maxDistance = 0 #How far the player moved during the round
        self.fitness = fitness #the total fitness of this player

        self.sword = None
        self.isAttacking = False
        self.attackDelay = 30 #30 frames between each attack
        self.jumpDelay = 30
        self.respawnDelay = 30 #Don't redraw the player upon death for 30 frames

        self.direction = "right"
        self.image = pygame.image.load('Images/playerrightangry.png')

        # So our player can modify the overall screen
        self.screen = screen

        #The Neural Net (initialized)
        self.brain = None

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        #coordinate point
        self.startPos = startPos
        self.startx = self.startPos[0]
        self.starty = self.startPos[1]

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

        self.genomeInputs = 6
        self.genomeOutputs = 4
        self.brain = NeuralNet(self.genomeInputs, self.genomeOutputs)
        self.vision = []

    #Make a clone of the player
    def clone(self):
        clone = Player(self.screen, self.startPos, self.fitness)
        clone.brain = self.brain.clone()
        clone.brain.generateNetwork()
        return clone
    
    #Update the screen with the AI's and enemy's decisions
    def update(self):
        if self.attackDelay != 0:
            self.attackDelay -= 1 
        if self.jumpDelay != 0:
            self.attackDelay -= 1
        if self.rect.x >= 760:
            self.numGoals += 1
            self.respawn()
            self.enemy.respawn()

        self.enemyPos = (self.enemy.rect.x, self.enemy.rect.y)
     
        #Update Neural Net and choose an action
        self.look()
        self.think()

        # Gravity
        self.calc_grav()
        self.calc_friction()

        # Move left/right
        self.rect.x += self.change_x

        # """ Update sword status"""
        #this is true once we generate swords
        if self.isAttacking == True:
            #if it doesn't need to be true anymore
            if len(self.level.player_attack_list) == 0:
                self.isAttacking = False
                self.sword = None

        # """ Did we just get stabbed? """
        if pygame.sprite.spritecollide(self, self.level.enemy_attack_list, True):
            # 4 hits to kill
            self.change_x -= 10
            self.change_y -= 4
            self.numHearts -= 1
            
    
        "---------------------- LOOKING AT PLAYER'S COLLISIONS WITH OTHER OBJECTS --------------------------"
        self.entityCollision()

                
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

        if self.rect.x/7.6 > self.maxDistance:
            self.maxDistance = self.rect.x/7.6

                
    def entityCollision(self):
       
        if pygame.sprite.collide_rect(self, self.enemy):
            x_momentum_diff = abs(self.change_x) - abs(self.enemy.change_x)

            #our right side is inside their left side and our bottom lower than their top
            if (self.rect.right > self.enemy.rect.left) and self.rect.bottom > self.enemy.rect.top + 4:
                #if we have more momentum, push them back with the force of our velocity
                if x_momentum_diff > 0:
                    self.enemy.change_x = self.change_x - 4
                    self.change_x = 0
                elif x_momentum_diff < 0:
                    self.change_x = self.enemy.change_x
                    self.enemy.change_x = 0
                else:
                    self.change_x += -4
                    self.enemy.change_x += 4

            #our left side is inside their right side and our bottom lower than their top
            if (self.rect.left < self.enemy.rect.right) and self.rect.bottom > self.enemy.rect.top + 10:
                #if we have more momentum, push them back with the force of our velocity
                if x_momentum_diff > 0:
                    self.enemy.change_x = self.change_x + 4
                    self.change_x = 0
                elif x_momentum_diff < 0:
                    self.change_x = self.enemy.change_x
                    self.enemy.change_x = 0
                else:
                    self.change_x += -4
                    self.enemy.change_x += 4
            
            #our right side is inside their left side and our bottom is higher than their top
            if (self.rect.right > self.enemy.rect.left) and self.rect.bottom < self.enemy.rect.top + 10:
                #set our right to their left
                self.rect.bottom = self.enemy.rect.top
                #bounce a lil
                self.change_y -= 1
            
            if (self.rect.right > self.enemy.rect.left) and self.rect.top > self.enemy.rect.bottom - 10:
                self.enemy.rect.bottom = self.rect.top
                self.enemy.change_y -= 1

            #our left side is inside their right side and our bottom is higher than their top
            if (self.rect.left < self.enemy.rect.right) and self.rect.bottom < self.enemy.rect.top + 10:
                #set our bottom to their top
                self.rect.bottom = self.enemy.rect.top
                #bounce a lil
                self.change_y -= 1

            if (self.rect.left < self.enemy.rect.right) and self.rect.top > self.enemy.rect.bottom - 10:
                self.enemy.rect.bottom = self.rect.top
                self.enemy.change_y -= 1

            if self.rect.left == self.enemy.rect.left and self.rect.top > self.enemy.rect.bottom - 10:
                self.enemy.rect.bottom = self.rect.top
                self.enemy.change_y -= 1
            
            if self.rect.left == self.enemy.rect.left and self.rect.bottom < self.enemy.rect.top + 10:
                self.rect.bottom = self.enemy.rect.top
                self.change_y -= 4

    def think(self): #execute action(s) returned from the neural net
        #get the output of the neural network
        decision = self.brain.feedForward(self.vision)

        #Choose an action
        for i in range(len(decision)):
            if decision[i] > 0.7:
                if i == 0:
                    self.go_right()
                elif i == 1:
                    self.go_left()
                elif i == 2:
                    self.jump()
                elif i == 3:
                    self.attack()

    #Look around at the environment --> this is fed into the neural net
    def look(self): 
        self.vision = []
        # x difference between player and enemy
        x = (self.rect.x + 100) / 100
        enemyx = (self.enemy.rect.x + 100) / 100
        self.vision.append(x - enemyx)
        # y difference between player and enemy
        y = (self.rect.y + 100) / 100
        enemyy = (self.enemy.rect.y + 100) / 100
        self.vision.append(y - enemyy)
        # x difference in velocity
        vel = self.change_x
        enemyvel = self.enemy.change_x
        self.vision.append(vel - enemyvel)
        # distance to goal
        goalx = SCREEN_WIDTH - self.width
        x = ((goalx - self.rect.x) + 100) / 100
        self.vision.append(x)
        #player_is_attacking
        if self.isAttacking:
            self.vision.append(1)
        else:
            self.vision.append(0)
        #enemy_is_attacking
        if self.enemy.isAttacking:
            self.vision.append(1)
        else:
            self.vision.append(0)
    
    def setEnemy(self, enemy):
        if enemy == None:
            self.enemy = None
        self.enemy = enemy

    #Caclulate the current fitness
    def calculateFitness(self):
        self.fitness = (50 * self.numKills) - (50 * self.numDeaths)
        self.fitness += (100 * self.numGoals) - (100*self.enemy.numGoals)
        self.fitness += (12.5 * self.numHits)
        self.fitness += self.runningDistance/(self.numDeaths + 1)
    
    #Update the AI's health
    def updateHealth(self):
        if self.numHearts <= 0:
            if self.respawnDelay == 0:
                self.respawn() #Respawn on death
                self.numDeaths += 1
                self.respawnDelay = 30
            else:
                self.respawnDelay -= 1
                self.rect.x = self.startx
                self.rect.y = -self.height

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
    
    #The jumping action
    def jump(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        # if self.jumpDelay == 0:
        self.rect.y += 4
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 4

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.change_y = -10
        self.jumpDelay = 0
        # else: 
        #     return
    
    #Move to the left
    def go_left(self):
        self.direction = "left"
        if self.change_x < -8:
            self.change_x = -8
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

            self.sword = Sword(self.rect.x, self.rect.y, 25, 10, facing)            
            self.level.player_attack_list.add(self.sword)
            self.isAttacking = True
            self.attackDelay = 30

    #Respawn at the starting point
    def respawn(self):
        self.rect.x = self.startx
        self.rect.y = self.starty
        self.numHearts = self.maxHearts
        self.runningDistance += self.maxDistance
        self.maxDistance = 0
    
    def crossover(self, parent2):
        child = Player(self.screen, self.startPos)
        child.brain = None
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generateNetwork()
        return child

    def resetFitness(self):
        self.numDeaths = 0
        self.numKills = 0
        self.numGoals = 0
        self.runningDistance = 0
        self.maxDistance = 0
        self.fitness = 0.0