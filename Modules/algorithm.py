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

