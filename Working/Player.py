import pygame
from Level import *
from Sword import *
from NeuralNet import *
import time
import math
import random

# Screen dimensions

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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self, playerID, color, screen, startPos, freeze = False):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()

        #How many input/outputs do we need??
        genomeInputs = 12
        genomeOutputs = 4

 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 40
        self.height = 60

        self.freeze = freeze

        self.enemy = None
        self.enemyPos = None

        self.maxHearts = 4
        self.numHearts = 4
        # self.deadFlag = False
        # self.numLives = 3

        self.numDeaths = 0
        self.numKills = 0
        self.numGoals = 0
        self.runningDistance = 0
        self.maxDistance = 0
        self.fitness = 0.0

        self.color = color 
        self.playerID = playerID

        self.sword = None
        self.isAttacking = False
        self.attackDelay = 30 #30 frames between each attack

        self.direction = "right"

        # self.damage = pygame.event.Event(pygame.USEREVENT, action = "damage", id= playerID)
        self.sideJumpCount = 0
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


        self.brain = NeuralNet(genomeInputs, genomeOutputs)
        self.vision = self.look(self.enemy, screen)
        self.decision = self.think(self.vision, None, False, None)
    
    def update(self):
        # """ Update our position knowledge """
        if self.attackDelay != 0:
            self.attackDelay -= 1
            
        if self.rect.x >= 760:
            self.numGoals += 1
            self.respawn()
            self.enemy.respawn()

        mouse_pos = pygame.mouse.get_pos()
        self.enemyPos = (self.enemy.rect.x, self.enemy.rect.y)
     
        # """ Who is alive """
        # if self.enemy.numLives == 0:
        #     self.level.enemy_list.remove(self.enemy)
    
        # """ Pass environment data to think """
        self.think(self.enemyPos, mouse_pos, True, self.freeze)

        # """ Move the player. """
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

                # Move up/down
                
        "To implement side jumping"
        # if len(block_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
        #     self.sideJumpCount = 0

    def entityCollision(self):
       
        if pygame.sprite.collide_rect(self, self.enemy):
            y_momentum_diff = abs(self.change_y) - abs(self.enemy.change_y)
            x_momentum_diff = abs(self.change_x) - abs(self.enemy.change_x)
            # print ("Collision! Player", self.rect.right, self.rect.left, self.rect.top, self.rect.bottom)
            # print ("           Enemy", self.enemy.rect.right, self.enemy.rect.left, self.enemy.rect.top, self.enemy.rect.bottom)

            #our right side is inside their left side and our bottom lower than their top
            if (self.rect.right > self.enemy.rect.left) and self.rect.bottom > self.enemy.rect.top + 4:
                #set our right to their left
                # self.rect.right = self.enemy.rect.left
                #if we have more momentum, push them back with the force of our velocity
                if x_momentum_diff > 0:
                    self.enemy.change_x = self.change_x - 4
                    self.change_x = 0
                    # self.enemy.change_y += self.change_y/2
                elif x_momentum_diff < 0:
                    self.change_x = self.enemy.change_x
                    self.enemy.change_x = 0
                else:
                    self.change_x += -4
                    self.enemy.change_x += 4

            #our left side is inside their right side and our bottom lower than their top
            if (self.rect.left < self.enemy.rect.right) and self.rect.bottom > self.enemy.rect.top + 10:
                #set our left to their right
                # self.rect.left = self.enemy.rect.right
                #if we have more momentum, push them back with the force of our velocity
                if x_momentum_diff > 0:
                    self.enemy.change_x = self.change_x + 4
                    self.change_x = 0
                    # self.enemy.change_y += self.change_y/2
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


    def think(self, point, mousePoint = None, mouseFlag = False,  freeze = False,):
        """
        Converts output of neural net into events
        that generate actions for the specific player
        in the main driver class
        """
        if freeze:
            return
        else:
            action = random.randint(0,10)
            self.executeAction(action)
        if mouseFlag == True:
          if (self.rect.x < mousePoint[0] and self.rect.x + self.width > mousePoint[0]) and (self.rect.y < mousePoint[1] and self.rect.y + self.height > mousePoint[1]):
            self.numHearts -= 1
            # pygame.event.post(self.damage)

        # if self.distanceToPoint(point, True, RED, "X") < 50:
        #     self.attack()
 
        if self.rect.x < point[0]:
            self.go_right()
        elif self.rect.x > point[0]:
            self.go_left()
        elif self.distanceToPoint(point) < 100:
            self.jump()

    def look(self, otherPlayers, gameWidth):
        vision = []
        #player_x
        vision.append(self.rect.x)
        #player_y
        vision.append(self.rect.y)
        #player_x_velocity
        vision.append(self.change_x)
        #player_y_velocity
        vision.append(self.change_y)
        #player_is_attacking
        vision.append(self.isAttacking)
        #player_attack_delay
        vision.append(self.attackDelay)
        #player_health
        vision.append(self.numHearts)
        #enemy_x
        vision.append(self.enemy.rect.x)
        #enemy_y
        vision.append(self.enemy.rect.y)
        #enemy_x_velocity
        vision.append(self.enemy.change_x)
        #enemy_y_velocity
        vision.append(self.enemy.change_y)
        #enemy_is_attacking
        vision.append(self.enemy.isAttacking)
        #enemy_attack_delay
        vision.append(self.enemy.attackDelay)
        #enemy_health
        vision.append(self.enemy.numHearts)
        return vision
    
    def setEnemy(self, enemy):
        if enemy == None:
            self.enemy = None
        self.enemy = enemy

    def updateFitness(self):
      self.fitness = (50 * self.numKills) - (50 * self.numDeaths)
      self.fitness += (100 * self.numGoals) - (100*self.enemy.numGoals)
      self.fitness += self.runningDistance/(self.numDeaths + 1)

        # progressToGoal = self.distanceToPoint((800,500), False, RED, "X") / 500
        # timeAlive = self.framesAlive / 60
        # numHearts = self.health / self.maxHealth
        # fitness = timeAlive - progressToGoal + health
        # self.runningFitness += fitness
        # self.totalFitnessCalculations += 1
        # return fitness
    
    def updateHealth(self):
        for hearts in range(self.numHearts):
            self.screen.blit(heart,((self.startx + (hearts * 40)), 35))
        for deaths in range(self.numDeaths):
            self.screen.blit(death,((self.startx + ((deaths % 6) * 40)), (110 + (int(deaths/6)*40))))
        if self.numHearts <= 0:
            self.respawn()
            self.numDeaths += 1
    


        # print(self.playerID, " is updating health: ", self.health)
        """Heart Code"""
        # for heartCount in range(self.numLives):
        #     self.screen.blit(heart, (self.startx + (heartCount*40),35))

        """Health Bar Code -- placed at top"""
        # healthBarLength = (self.health/self.maxHealth) * self.width

        # if (self.health <= 0) and (self.numLives == 0):
        #     print("Killing player: ", self.playerID)
        #     self.deadFlag = True
        #     self.level.player_list.remove(self)
            # Display a health bar with colors corresponding to the player's remaining health
            # if self.health/self.maxHealth > .8:
            #     #
            #     pygame.draw.line(self.screen, GREEN, (self.rect.x, self.rect.y - 10), (self.rect.x + healthBarLength, self.rect.y - 10), 4)
            # elif self.health/self.maxHealth > .5:
            #     pygame.draw.line(self.screen, PALEGREEN, (self.rect.x, self.rect.y - 10), (self.rect.x + healthBarLength, self.rect.y - 10), 4)
            # elif self.health/self.maxHealth > .2:
            #     healthBarLength = (self.health/self.maxHealth) * self.width
            #     pygame.draw.line(self.screen, YELLOW, (self.rect.x, self.rect.y - 10), (self.rect.x + healthBarLength, self.rect.y - 10), 4)
            # else: 
            #     pygame.draw.line(self.screen, RED, (self.rect.x, self.rect.y - 10), (self.rect.x + healthBarLength, self.rect.y - 10), 4)  
    
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

        if (self.rect.left == 0 or self.rect.right == SCREEN_WIDTH) and self.sideJumpCount == 0:
                self.change_y = -10
                self.sideJumpCount = 1
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
                self.change_y = -10
    
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.direction = "left"
        self.image = pygame.image.load('Images/playerleftangry.png')
        if self.change_x < -8:
            self.change_x = -8
        else:
            self.change_x -= .5

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.direction = "right"
        self.image = pygame.image.load('Images/playerrightangry.png')
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
                facing = -1
            if self.direction == "right":
                facing = 1
            if self.direction == "none":
                facing = 0

            self.sword = Sword(self.rect.x, self.rect.y, 25, 10, self.color, facing)
            
            self.level.player_attack_list.add(self.sword)
            self.isAttacking = True
            self.attackDelay = 30

    def executeAction(self, action):
        if action == 0:
            self.go_left()
        elif action == 1:
            self.go_right()
        elif action == 2:
            self.jump()
        elif (action == 4):
            self.attack()

    def respawn(self):
        # Respawn back to starting point       
        self.rect.x = self.startx
        self.rect.y = self.starty
        self.numHearts = self.maxHearts
        self.runningDistance += self.maxDistance
        self.maxDistance = 0
