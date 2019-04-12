import pygame

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
            self.rect.x = x + 45#50
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
