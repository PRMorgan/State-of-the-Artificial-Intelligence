import pygame

class Sword(object):
    def __init__(self,x,y,width,height,color,facing):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.facing = facing

    def draw(self,win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, 60, 20))