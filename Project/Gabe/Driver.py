"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
"""
 
import pygame
from Player import *
from Level import *
import random
 
# Global constants
 
# Colors
# BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DarkSlateBlue = (72,61,139)
DeepSkyBlue = (0,191,255)
PaleGreen = (152,251,152)
RosyBrown = (188,143,143)
PaleViolet = (219,112,147)


colors = [WHITE, GREEN, RED, BLUE, DarkSlateBlue, RosyBrown, PaleGreen, DeepSkyBlue, PaleViolet]

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Nidhog")

    # Create all the levels
    level_list = []
 
    # Set the current level
    current_level_no = 0

    #create an active sprite list to update collectively
    active_sprite_list = pygame.sprite.Group()

    players = []

    #create a player controlled by the keyboard
    user_player = Player(69, (255,255,0), screen, False)
    level_list.append( Level_01(user_player))
    user_player.level = level_list[0]
    user_player.rect.x = 200
    user_player.rect.y = 200
    active_sprite_list.add(user_player)

    for player in range(2):
        color_index = random.randint(0,len(colors) - 1)
        x_start_pos = random.randint(0,500)
        playerID = player
        player = Player(playerID, colors[color_index], screen)
        players.append(player)

        level_list.append( Level_01(player) )
        current_level = level_list[current_level_no]

        player.level = current_level 

        player.rect.x = x_start_pos
        player.rect.y = SCREEN_HEIGHT - player.rect.height - 200
        active_sprite_list.add(player)
        # possibleActions = [player.go_left, player.go_right, player.jump, player.stop]

    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()


    """
    Creating players brains:
    pop = Population(30)

    for person in pop:
        pop.add(new Player());
        person.brain.generateNetwork();
        person.brain.mutate(innovationHistory);


    """

    # -------- Main Program Loop -----------
    while not done:

        # Update the player.
        active_sprite_list.update()
        
        # update players --> in update() tell players to think()
        #in the think(), they should run the neural net once
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    user_player.executeAction(0)
                if event.key == pygame.K_RIGHT:
                    user_player.executeAction(1)
                if event.key == pygame.K_UP:
                    user_player.executeAction(2)
                if event.key == pygame.K_SPACE:
                    user_player.executeAction(4)
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    user_player.executeAction(3)
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    user_player.executeAction(3)
            
            if event.type == pygame.USEREVENT:
                for player in players:
                    if player.playerID == event.id:
                        eventPlayer = player
                if event.action == "kill":
                    print("Just killed player: ", eventPlayer.playerID, "... removing now")
                    active_sprite_list.remove(eventPlayer)
                    players.remove(eventPlayer)
                    print("players left: ", len(players))
                elif event.action == "attack":
                    eventPlayer.executeAction(4)
                elif event.action == "moveLeft":
                    eventPlayer.executeAction(0)
                    eventPlayer.direction = "left"
                elif event.action == "moveRight":
                    eventPlayer.executeAction(1)
                    eventPlayer.direction = "right"
                elif event.action == "jump":
                    eventPlayer.executeAction(2)
                elif event.action == "stop":
                    eventPlayer.executeAction(3)
                    eventPlayer.direction = "none"
                elif event.action == "damage":
                    eventPlayer.health -= 2
                else:
                    print("unkown event: ", event)

       
        for player in players:
            action = random.randint(0,4)
            player.executeAction(action)
        
        # Update items in the level
        current_level.update()

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # mouse_pos = pygame.mouse.get_pos()

        for player in players:
            # draw the lines between point
            # player.distanceToPoint(mouse_pos, True, BLUE)
            #player.distanceToPoint((800,500),True, RED, "X")
            player.updateHealth()
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
