"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
"""
 
import pygame
from Player import *
from Level import *
from Game import *
from Sword import *
from Population import *
import random
import os
import time
os.environ['SDL_VIDEO_CENTERED'] = '1'
 
# Global constants
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

FRAMERATE = 60
TOTALTIME = 10

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624

SCREEN_WIDTH_EXT = 1300

#Main 
def main():
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH_EXT, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("State of the Art-ificial Intelligence: AI-Kido")

    # <insert large block of code at bottom if shit goes south>
    showNothing = [False]
    showIndex = [-1] #default showAll

    numGames = 1 #This is the number of sets of players
    pop = Population(numGames, screen)

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    gameUI = Interface(screen, numGames)

    # Set the background music
    #music = pygame.mixer.music.load('SFX/yoshi.mp3')
    #pygame.mixer.music.play(-1)

    # -------- Main Program Loop -----------
    timeremaining = FRAMERATE * TOTALTIME
    while not gameUI.satisfied:
        while not gameUI.done:
            timeremaining -= 1

            # update players --> in update() tell players to think()
            #in the think(), they should run the neural net once
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameUI.done = True
                    gameUI.satisfied = True
                
            # Update items in the level
            for game in pop.games:
                game.level.update()
                game.updateAllHealth()

            pop.draw(showNothing[0],showIndex[0])

            #Put our buttons on the screen
            #screen, text, x, y, width, height, color1, color, function
            gameUI.button(screen, "Show Best",315,602,70,20,RED,BLUE,gameUI.showChamp, showIndex)
            gameUI.button(screen, "Next",390,602,70,20,RED,BLUE,gameUI.nextGame, showIndex)
            gameUI.button(screen, "Prev",465,602,70,20,RED,BLUE,gameUI.prevGame, showIndex)
            gameUI.button(screen, "Show All",240,602,70,20,RED,BLUE,gameUI.showAll,showIndex)
            gameUI.button(screen, "Show None",165,602,70,20,RED,BLUE,gameUI.showNothing,[],showNothing)
            gameUI.button(screen, "Quit", 5, 602, 50, 20, RED, BLUE, gameUI.endGame,[],[],True)
            
            #Display our game stats on the screen
            if not showNothing[0]:
                timemsg = str(int(timeremaining/FRAMERATE))
                gameUI.displayText(screen, timemsg,388,110,140,20, BLUE)

                numGoalsMsg = str(game.player.numGoals - game.enemy.numGoals)
                gameUI.displayText(screen, numGoalsMsg, 388, 175, 120, 20, False)

            # Limit to 60 frames per second
            clock.tick(FRAMERATE)

            if timeremaining <= 0:
                for game in pop.games:
                    game.player.respawn()
                    game.enemy.respawn()
                    game.player.calculateFitness()
                    print("Fitness: " + str(game.player.fitness))
                    gameUI.done = True
    
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        if not gameUI.satisfied:
            gameUI.done = False
            timeremaining = FRAMERATE * TOTALTIME
            pop.naturalSelection()
    # Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
    pygame.quit()

class Interface():
    def __init__(self, screen, numGames):
        self.screen = screen
        self.numGames = numGames
        self.satisfied = False
        self.done = False
        self.buttonsDrawn = False
        self.font = pygame.font.SysFont('Georgia', 15, False, False)

    #Buttons to control what we see on the screen
    def button(self, screen, msg,x,y,w,h,ic,ac,action=None,showAll=[],showNothing=[],lastButton = False):
        if lastButton == True:
            self.buttonsDrawn = True
        if self.buttonsDrawn == False:
            pygame.draw.rect(screen, ic,(x,y,w,h))
            text = self.font.render(msg, True, WHITE)
            pos = [x,y]
            screen.blit(text, pos)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1 and action != None:
                if len(showAll) > 0:
                    action(showAll)
                elif len(showNothing) > 0:
                    action(showNothing)
                else:
                    action() 

#These next few relate to the buttons shown on the screen
    def displayText(self, screen, msg, x, y, w, h, color):
        font = pygame.font.SysFont('Georgia', 24, True, False)
        text = font.render(msg, True, WHITE)
        pos = [x,y]
        screen.blit(text, pos)

    def showAll(self, showIndex):
        showIndex[0] = -1

    def nextGame(self,showIndex): #Fix this
        if showIndex[0] >  -1 and showIndex[0] < self.numGames - 1:
            showIndex[0] += 1
        else: 
            showIndex[0] = 0

    def prevGame(self,showIndex):
        if showIndex[0] > 0:
            showIndex[0] -= 1
        else: 
            showIndex[0] = self.numGames - 1
    
    def showChamp(self,showIndex):
        showIndex[0] = 0
    
    def showNothing(self,showNothing):
        if showNothing[0] == True:
            showNothing[0] = False
        else: 
            showNothing[0] = True
    
    def endGame(self):
        self.satisfied = True
        self.done = True
    
#Main
if __name__ == "__main__":
    main()
