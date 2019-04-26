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
TOTALTIME = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 624

SCREEN_WIDTH_EXT = 1300

colors = [RED,BLUE,WHITE]

def main():

    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH_EXT, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("State of the Art-ificial Intelligence")

    # <insert large block of code at bottom if shit goes south>
    showNothing = [False]
    showIndex = [-1] #default showAll

    numGames = 10
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

            #pop.games[0].level.drawBG(screen,pop.games[0])

            # if showIndex[0] == -1: #show all
            #     for game in pop.games:
            #         game.level.draw(screen)
            #         game.player.updateHealth()
            #         game.enemy.updateHealth()
            #         game.updateAllHealth()
            # elif len(pop.games) != 0:
            #     pop.games[showIndex[0]].level.draw(screen)
            #     pop.games[showIndex[0]].updateAllHealth()

            #screen, text, x, y, width, height, color1, color, function
            gameUI.button(screen, "Show Best",315,602,70,20,RED,BLUE,gameUI.showChamp, showIndex)
            gameUI.button(screen, "Next",390,602,70,20,RED,BLUE,gameUI.nextGame, showIndex)
            gameUI.button(screen, "Prev",465,602,70,20,RED,BLUE,gameUI.prevGame, showIndex)
            gameUI.button(screen, "Show All",240,602,70,20,RED,BLUE,gameUI.showAll,showIndex)
            gameUI.button(screen, "Show None",165,602,70,20,RED,BLUE,gameUI.showNothing,[],showNothing)
            gameUI.button(screen, "Quit", 5, 602, 50, 20, RED, BLUE, gameUI.endGame, True)
            
            if not showNothing[0]:
                timemsg = str(int(timeremaining/FRAMERATE))
                gameUI.displayText(screen, timemsg,397,143,140,20, BLUE)

                numGoalsMsg = str(game.player.numGoals - game.enemy.numGoals)
                gameUI.displayText(screen, numGoalsMsg, 403, 207, 120, 20, False)

            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
            # Limit to 60 frames per second
            clock.tick(FRAMERATE)

            if timeremaining <= 0:
                for game in pop.games:
                    game.player.respawn()
                    game.player.calculateFitness()
                    print("K: " + str(game.player.numKills))
                    print("D: " + str(game.player.numDeaths))
                    print("G: " + str(game.player.numGoals))
                    print("EG: " + str(game.enemy.numGoals))
                    print("MD: " + str(game.player.maxDistance))
                    print("RD: " + str(game.player.runningDistance))
                    print("Fitness: " + str(game.player.fitness))
                    gameUI.done = True
    
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        gameUI.done = False
        timeremaining = FRAMERATE * TOTALTIME
        #pop.naturalSelection()

        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
    pygame.quit()

class Interface():
    def __init__(self, screen, numGames):
        self.screen = screen
        #self.gameScreen = -1
        self.numGames = numGames
        self.satisfied = False
        self.done = False
        self.buttonsDrawn = False
        self.font = pygame.font.SysFont('Georgia', 15, False, False)

    def button(self, screen, msg,x,y,w,h,ic,ac,action=None,showAll=[],showNothing=[],lastButton = False):
        if lastButton == True:
            self.buttonsDrawn = True
        if self.buttonsDrawn == False:
            pygame.draw.rect(screen, ic,(x,y,w,h))
            text = self.font.render(msg, True, WHITE)
            pos = [x,y]
            screen.blit(text, pos)
        #else:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            #pygame.draw.rect(screen, ac,(x,y,w,h))
            if click[0] == 1 and action != None:
                if len(showAll) > 0:
                    action(showAll)
                elif len(showNothing) > 0:
                    action(showNothing)
                else:
                    action()

    def displayText(self, screen, msg,x,y,w,h,color):
        #pygame.draw.rect(screen, color,(x,y,w,h))
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
    

    
if __name__ == "__main__":
    main()