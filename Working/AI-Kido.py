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
import random
import os
import time
os.environ['SDL_VIDEO_CENTERED'] = '1'
 
# Global constants

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

FRAMERATE = 60
TOTALTIME = 30

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

colors = [RED,BLUE,WHITE]

def main():

    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("State of the Art-ificial Intelligence")

    # <insert large block of code at bottom if shit goes south>

    # Loop until the user clicks the close button.
    games = []
    finishedGames = []
    # game1 = Game(screen, 0)
    # game2 = Game(screen, 1)
    
    numGames = 1

    for game in range(numGames):
        tempGame = Game(screen, game)
        games.append(tempGame)

    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    gameUI = Interface(screen, numGames)

    # Set the background music
    #music = pygame.mixer.music.load('SFX/yoshi.mp3')
    #pygame.mixer.music.play(-1)

    # -------- Main Program Loop -----------
    timeremaining = FRAMERATE * TOTALTIME

    while not done:
        timeremaining -= 1
        # for game in games:
        #     if game.isOver():
        #         finishedGames.append(game)
        #         print("Removing game: ", game.gameNum)
        #         games.remove(game)
        #         gameUI.updateGameNums(len(games))

        # update players --> in update() tell players to think()
        #in the think(), they should run the neural net once
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
        # Update items in the level
        
        for game in games:
            game.level.update()
        games[0].level.drawBG(screen)

        # if len(games) == 0:
        #     finishedGames[0].level.draw(screen)
        #     finishedGames[0].level.drawBG(screen)
        # else:
        #     games[0].level.draw(screen)
        #     games[0].level.drawBG(screen)

        #screen, text, x, y, width, height, color1, color, function
        gameUI.button(screen, "Show All",240,10,70,20,RED,BLUE,gameUI.showAll)
        gameUI.button(screen, "Show Best",315,10,70,20,RED,BLUE,gameUI.showBest)
        gameUI.button(screen, "Next",390,10,70,20,RED,BLUE,gameUI.nextGame)
        gameUI.button(screen, "Prev",465,10,70,20,RED,BLUE,gameUI.prevGame)
        
        #screen, text, x, y, width, height, color
        msg = "Game: " + str(gameUI.gameScreen + 1) + "/" + str(len(games))
        gameUI.displayText(screen, msg,353,35,90,20, BLUE)

        timemsg = "Time Remaining: " + str(int(timeremaining/FRAMERATE))
        gameUI.displayText(screen, timemsg,323,120,140,20, BLUE)

        numGoalsMsg = "Levels Cleared: " + str(game.player.numGoals)
        gameUI.displayText(screen, numGoalsMsg, 10, 80, 120, 20, BLUE)

        numGoalsMsg = "Levels Cleared: " + str(game.enemy.numGoals)
        gameUI.displayText(screen, numGoalsMsg, SCREEN_WIDTH - 125, 80, 120, 20, BLUE)


        if gameUI.gameScreen == -1:
            # if 
            for game in games:
                game.level.draw(screen)
                game.player.updateHealth()
                game.enemy.updateHealth()
                game.updateAllHealth()
                # if game.player.deadFlag != True:
                #     game.player.updateHealth()
                # if game.enemy.deadFlag != True:
                #     game.enemy.updateHealth()
        elif len(games) != 0:
            games[gameUI.gameScreen].level.draw(screen)
            games[gameUI.gameScreen].updateAllHealth()


        #time.sleep(.05)

        # mouse_pos = pygame.mouse.get_pos()

        # for player in players:
        #     # draw the lines between point
        #     player.distanceToPoint(player.enemyPos, True, BLUE)
        #     # player.distanceToPoint((800,500),True, RED, "X")
        #     player.updateHealth()
        # playerOne.updateHealth()
        # playerTwo.updateHealth()
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(FRAMERATE)

        if timeremaining <= 0:
            for game in games:
                game.player.respawn()
                game.player.updateFitness()
                print("K: " + str(game.player.numKills) + "\n")
                print("D: " + str(game.player.numDeaths) + "\n")
                print("G: " + str(game.player.numGoals) + "\n")
                print("EG: " + str(game.enemy.numGoals) + "\n")
                print("MD: " + str(game.player.maxDistance) + "\n")
                print("RD: " + str(game.player.runningDistance) + "\n")
                print("Fitness: " + str(game.player.fitness))
            done = True
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

class Interface():
    def __init__(self, screen, gameNums):
        self.screen = screen
        self.gameScreen = -1
        self.gameNums = gameNums
    def button(self, screen, msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()         
        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))
        
        font = pygame.font.SysFont('tahoma', 15, False, False)

        text = font.render(msg, True, WHITE)
        pos = [x,y]
        screen.blit(text, pos)

    def displayText(self, screen, msg,x,y,w,h,color):
        pygame.draw.rect(screen, color,(x,y,w,h))
        font = pygame.font.SysFont('tahoma', 15, False, False)
        text = font.render(msg, True, WHITE)
        pos = [x,y]
        screen.blit(text, pos)

    def showAll(self):
        self.gameScreen = -1
  
    def showBest(self):
        print("Show best Game")

    def nextGame(self):
        if self.gameScreen < self.gameNums - 1:
            self.gameScreen += 1
        else: 
            self.gameScreen = 0
    def prevGame(self):
        if self.gameScreen > 0:
            self.gameScreen -= 1
        else: 
            self.gameScreen = self.gameNums - 1

    def updateGameNums(self, newNum):
        self.gameNums = newNum

    
if __name__ == "__main__":
    main()