import math
import pygame
import Modules.varGlobals as varGlobals
from Modules.colors import custom as cc, tts


###################################################################################################
#                                 UNTUK MENAMPILKAN ROBOT PADA MAP                                #
###################################################################################################

def rotatedImage(image, x, y, angle):
    rotated_image = pygame.transform.rotate(image, 360 - angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    varGlobals.screen.blit(rotated_image, new_rect)

def gridMap(screen, x, y, grid_interval = 50):
    # HORIZONTAL
    for hor in range(y, varGlobals.res[1], grid_interval):
        pygame.draw.line(screen, cc.RED, (0, hor), (varGlobals.res[0], hor), 2)
    
    # VERTIKAL
    for ver in range(x, varGlobals.res[0], grid_interval):
        pygame.draw.line(screen, cc.RED, (ver, 0), (ver, varGlobals.res[1]), 2)