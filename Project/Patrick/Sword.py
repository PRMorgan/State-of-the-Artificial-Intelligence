import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,color,facing):

        super().__init__()
        self.facing = facing
        self.x = x
        self.y = y

        self.image = pygame.image.load('Images/swordRight.png')#Surface([width, height])
        #self.image.fill((192,192,192))
        self.rect = self.image.get_rect()
        self.width = width

        self.timer = 0

        if facing == -1:
            self.rect.x = x - 50
            self.rect.y = y + 30
            self.image = pygame.image.load('Images/swordLeft.png')
            #pygame.transform.flip(self.image, True, False)
        elif facing == 1:
            self.rect.x = x + 45#50
            self.rect.y = y + 30
            self.image = pygame.image.load('Images/swordRight.png')
            #pygame.transform.flip(self.image, False, True)
        else:
            self.rect.x = x + width
            self.rect.y = y - 20

    def update(self):
        if self.facing == -1:
            self.rect.x = self.x - 50
            self.rect.y = self.y + 30
        elif self.facing == 1:
            self.rect.x = self.x + 45#50
            self.rect.y = self.y + 30
        else:
            self.rect.x = self.x + self.width
            self.rect.y = self.y - 20
        self.timer += 1

        if self.timer >= 3:
            self.kill()