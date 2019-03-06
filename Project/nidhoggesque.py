import pygame
pygame.init()

#Set the window size and title
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("Nidhoggesque Fighter")

#Make a list of sprites animations
char = [pygame.image.load('standing0.png'), pygame.image.load('standing1.png'), pygame.image.load('standing2.png'), pygame.image.load('standing3.png')]
walkRight = [pygame.image.load('right0.png'), pygame.image.load('right1.png'), pygame.image.load('right2.png'), pygame.image.load('right3.png'), pygame.image.load('right4.png'), pygame.image.load('right5.png')]
walkLeft = [pygame.image.load('left0.png'), pygame.image.load('left1.png'), pygame.image.load('left2.png'), pygame.image.load('left3.png'), pygame.image.load('left4.png'), pygame.image.load('left5.png')]
atkleft = [pygame.image.load('atkleft0.png'), pygame.image.load('atkleft1.png'), pygame.image.load('atkleft2.png')]
atkright = [pygame.image.load('atkright0.png'), pygame.image.load('atkright1.png'), pygame.image.load('atkright2.png')]

clock = pygame.time.Clock()
score = 0

#Set the background image and music
bg = pygame.image.load('bg.jpg')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

# A class to represent a player
class player(object):
    def __init__(self, x, y, width, height):
        """
        x is the xpos
        y is the ypos
        width is the number of pixels wide the sprite is
        height is the number of pixels tall the sprite is
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5 #Movement speed of the character
        self.isJump = False #A boolean to track if the character is jumping
        self.left = False #A boolean to track if the charcter is moving left
        self.right = False #A boolean to track if the character is moving right
        self.walkCount = 0
        self.jumpCount = 10
        self.atkCount = 0
        self.standing = True #A boolean to track if the character is idling
        self.attacking = False #A boolean to track if the character is attaking
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #A hitbox to surround the character

    #A method to display the character depending on it's current state
    def draw(self, win):
        if self.walkCount + 1 >= 5:
            self.walkCount = 0

        if (self.attacking) and (self.atkCount + 1 >= 5):
            #if self.left:
            win.blit(atkleft[self.atkCount // 1], (self.x,self.y))
            #else:
            #    win.blit(atkright[self.atkCount // 1], (self.x,self.y))

        #If the character isn't loafing about
        if not(self.standing):
            #If the character is moving left
            if self.left:
                win.blit(walkLeft[self.walkCount // 1], (self.x,self.y))
                self.walkCount += 1
            #If the character is moving right
            elif self.right:
                win.blit(walkRight[self.walkCount // 1], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    #A method to display a hit
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(3)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()

# =========================================================================== #

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

# =========================================================================== #

#A class to represent an enemy
class enemy(object):
    #walk = [pygame.image.load('ewalk0.png'), pygame.image.load('ewalk1.png'), pygame.image.load('ewalk2.png'), pygame.image.load('ewalk3.png')]
    walkRight = [pygame.image.load('right0.png'), pygame.image.load('right1.png'), pygame.image.load('right2.png'), pygame.image.load('right3.png'), pygame.image.load('right4.png'), pygame.image.load('right5.png')]
    walkLeft = [pygame.image.load('left0.png'), pygame.image.load('left1.png'), pygame.image.load('left2.png'), pygame.image.load('left3.png'), pygame.image.load('left4.png'), pygame.image.load('left5.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 5:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 1], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 1], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')    

# =========================================================================== #

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (350, 10))
    man.draw(win)
    opponent.draw(win)
    for bullet in swipes:
        bullet.draw(win)
    
    pygame.display.update()

# =========================================================================== #

#def main():
#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(200, 410, 64,64)
opponent = enemy(100, 410, 64, 64, 450)
attackLoop = 0
swipes = []
run = True
while run:
    clock.tick(27)

    if opponent.visible == True:
        if man.hitbox[1] < opponent.hitbox[1] + opponent.hitbox[3] and man.hitbox[1] + man.hitbox[3] > opponent.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > opponent.hitbox[0] and man.hitbox[0] < opponent.hitbox[0] + opponent.hitbox[2]:
                man.hit()
                score -= 5

    if attackLoop > 0:
        attackLoop += 1
    if attackLoop > 3:
        attackLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

       
    for bullet in swipes:
        if bullet.y - bullet.radius < opponent.hitbox[1] + opponent.hitbox[3] and bullet.y + bullet.radius > opponent.hitbox[1]:
            if bullet.x + bullet.radius > opponent.hitbox[0] and bullet.x - bullet.radius < opponent.hitbox[0] + opponent.hitbox[2]:
                #hitSound.play()
                opponent.hit()
                score += 1
                swipes.pop(swipes.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            swipes.pop(swipes.index(bullet))
    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and attackLoop == 0:
        man.attacking = True
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(swipes) < 1:
            swipes.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0,0,0), facing))

        attackLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()

#if __name__ == "__main__":
#    main()







        
