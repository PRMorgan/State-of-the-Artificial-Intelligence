import pygame

pygame.init()

windowidth = 1000
windowheight = 500
win = pygame.display.set_mode((windowidth, windowheight ))

pygame.display.set_caption("first game")

x = 50
y = 50
width = 40
height = 40
vel = 7

isJump = False
jumpHeight = 15
jumpCount = jumpHeight

pXblocked = False
nXblocked = False
pYblocked = False
nYblocked = False

run = True
while run:
    pygame.time.delay(10)

    pXblocked = x >= windowidth - vel - width
    nXblocked = x <= vel
    pYblocked = y >= windowidth - height - vel
    nYblocked = y <= vel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not nXblocked:
        x -= vel
    if keys[pygame.K_RIGHT] and not pXblocked:
        x += vel
    
    if not isJump:

        if keys[pygame.K_UP] and not nYblocked:
            y -= vel
        if keys[pygame.K_DOWN] and not pYblocked:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= 0 - jumpHeight:
            y -= (jumpCount * abs(jumpCount)) * 0.125
            jumpCount -= 1
        else: 
            jumpCount = jumpHeight
            isJump = False
    
    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0, 255), (x, y, width, height))
    pygame.draw.rect(win, (255, 0, 0), (250, 250, width, height))
    pygame.display.update()

pygame.quit()