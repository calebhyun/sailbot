import pygame, sys
from pygame.locals import *
import math
import time

#FPS = 30

#fpsClock = pygame.time.Clock()

SCREENWIDTH = 600
SCREENHEIGHT = 600

pygame.init()
DISPLAYSURF = pygame.display.set_mode(((SCREENWIDTH, SCREENHEIGHT)))

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE = (0,0, 255)
RED = (255, 0, 0)

fontObj = pygame.font.Font('freesansbold.ttf', 32)

cLen = 300
dir = 50

while True:
    DISPLAYSURF.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == QUIT: 
                pygame.quit()
                sys.exit
        elif(event.type == KEYDOWN):
            if(event.key == K_UP):
                print("k")
    centerX = 300
    centerY = 300
    endX = centerX + cLen * math.sin(math.radians(dir))
    endY = centerY + cLen * math.cos(math.radians(dir))
    
    pygame.draw.circle(DISPLAYSURF, WHITE, (centerX, centerY), 300)
        

    pygame.draw.circle(DISPLAYSURF, RED, (centerX, centerY), dir+30)
    pygame.draw.circle(DISPLAYSURF, WHITE, (centerX, centerY), dir+27)

    pygame.draw.line(DISPLAYSURF, GREEN, (centerX, centerY), (endX, endY), 10)
    dir += 1
    time.sleep(.05)

    txtNorthSurf = fontObj.render('RADAR', True, BLUE)
    txtNorthRect = txtNorthSurf.get_rect()
    txtNorthRect.center = (300, 500)

    DISPLAYSURF.blit(txtNorthSurf, txtNorthRect)

    pygame.display.update()
    #fpsClock.tick(FPS)
