import pygame
import os, sys

###################################################################################################
#                                           MAIN WINDOW                                           #
###################################################################################################

if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_CENTERED']='1'
info = pygame.display.Info()
screen_width,screen_height = info.current_w, info.current_h
res = (screen_width,screen_height)

screen =pygame.display.set_mode(res)
print(int(screen_width),int(screen_height))


###################################################################################################
#                                            VARIABLE                                             #
###################################################################################################

# IP DAN PORT
IP = ''
PORT = ''

# BOOLEAN
serviceBot = False
runConfig = bool
runMenu = bool
runSim = bool
hapus = bool
udp = bool

# NUMERIK
# PANJANG = 
# LEBAR =

# TEXT
conServiceBot = 'Disconnected' 


###################################################################################################
#                                           BACKGROUND                                            #
###################################################################################################

bgMenu = pygame.image.load("C:\BMP-Robotics\Assets\menu.png").convert_alpha()
bgConfig = pygame.image.load("C:\BMP-Robotics\Assets\configuration.png").convert_alpha()
bgSim = pygame.image.load("C:\BMP-Robotics\Assets\simulator.png").convert_alpha()