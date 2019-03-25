"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
 
Explanation video: http://youtu.be/BCxWJgN4Nnc
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
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


colors = [BLACK, WHITE, GREEN, RED, BLUE, DarkSlateBlue, RosyBrown, PaleGreen, DeepSkyBlue, PaleViolet]

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Platformer Jumper")
 
    # Create the player
    # player = Player(BLUE)
    # player2 = Player(RED)

    # Create all the levels
    level_list = []
 
    # Set the current level
    current_level_no = 0
    
 
    active_sprite_list = pygame.sprite.Group()

    players = []

    for player in range(5):
        color_index = random.randint(0,len(colors) - 1)
        x_start_pos = random.randint(0,500)
        player = Player(colors[color_index])
        players.append(player)

        level_list.append( Level_01(player) )
        current_level = level_list[current_level_no]

        player.level = current_level 

        player.rect.x = x_start_pos
        player.rect.y = SCREEN_HEIGHT - player.rect.height - 200
        active_sprite_list.add(player)
        possibleActions = [player.go_left, player.go_right, player.jump, player.stop]
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    possibleActions = [player.go_left, player.go_right, player.jump, player.stop]
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.direction = "left"
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.direction = "right"
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_f:
                    player.boost()
  
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()


        for player in players:
            action1 = random.randint(0,100)
            # action2 = random.randint(0,100)
            player.executeAction(action1)
            # player.executeAction(action2)
        

        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(100)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
