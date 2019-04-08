import pygame
import time

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self, color):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 20
        height = 20

        self.width = width
        self.height = height

        self.color = color

        self.direction = "none"

        self.sideJumpCount = 0
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        self.hitbox = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

        # Which way is the sprite facing
        self.left = False
        self.right = False
        """Player facing: 
                left = -1
                right = 1
                standing = 0
        """
        self.facing = 0

        # Is the sprite attacking
        self.attacking = False
        self.swipes = []

    def update(self):                
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        pygame.sprite.spritecollide(self, self.level.attackList, True)

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
         
        # If the player gets near the right side, shift the world left (-x)
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
 
        # If the player gets near the left side, shift the world right (+x)
        if self.rect.left < 0:
            self.rect.left = 0
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        if len(block_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.sideJumpCount = 0
        
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
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

    def getAction(self, event):
        #keys = pygame.key.get_pressed()
        attackLoop = 0
        # Get the player's action and act accordingly.
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.go_left()
                self.left = True
                self.right = False
                self.facing = -1
            if event.key == pygame.K_RIGHT:
                self.go_right()
                self.left = False
                self.right = True
                self.facing = 1
            if event.key == pygame.K_UP:
                self.jump()
            if event.key == pygame.K_SPACE and attackLoop == 0:
                self.attack()
                attackLoop = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.change_x < 0:
                self.stop()
            if event.key == pygame.K_RIGHT and self.change_x > 0:
                self.stop()

    def attack(self):
        print(str(self.color) + "HYAHHH!")
        self.attacking = True
        if self.left:
            facing = -1
        else:
            facing = 1
        if len(self.swipes) < 2:
            #self.swipes.append(projectile(round(self.rect.x + self.width // 2), round(self.rect.y + self.height // 2), 6, (0,255,0), facing))
            swordAttack = Sword(self.rect.x, self.rect.y, 20, 60, (0,255,0), self.facing)
            #self.swipes.append(Sword(self.rect.x, self.rect.y, 20, 60, (0,255,0), self.facing))
            self.swipes.append(swordAttack)
 
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

    # Player-controlled movement:
    def boost(self):
        """Fires a look vector"""
        if self.direction == "left":
            self.change_x -= 10
        elif self.direction == "right":
            self.change_x += 10
        
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -4
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 4
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.direction = "none"
        self.change_x = 0

    def executeAction(self, action):
        # actions = [self.go_left, self.go_right, self.jump, self.stop, self.boost]

        if action <= 5:
            self.go_left()
        elif action > 6 and action < 80:
            self.go_right()
        elif action >= 80 and action < 90:
            self.jump()
        else: 
            self.stop()
        # time.sleep(.04)
        # actions[action]()

class Sword(pygame.sprite.Sprite):
    def __init__(self,x,y,height,width,color,facing):

        super().__init__()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, 60, 20))

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
