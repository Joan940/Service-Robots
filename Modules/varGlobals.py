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
offsetX= res[0] / 13.5
offsetY= res[1] / 7.1
skala = res[1] / 1200

offsetResetPosX = 50 * skala
offsetResetPosY = 50 * skala

# TEXT
conServiceBot = 'Disconnected' 

# FONT
font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 50)


###################################################################################################
#                                           BACKGROUND                                            #
###################################################################################################

bgMenu = pygame.image.load("C:\BMP-Robotics\Assets\menu.png").convert_alpha()
bgConfig = pygame.image.load("C:\BMP-Robotics\Assets\configuration.png").convert_alpha()
bgSim = pygame.image.load("C:\BMP-Robotics\Assets\simulator.png").convert_alpha()

bot = pygame.image.load(r"C:\BMP-Robotics\Assets\bot.png").convert_alpha()
bot = pygame.transform.scale(bot, (40, 40))

arrow = pygame.image.load(r"C:\BMP-Robotics\Assets\arrow.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (100, 100))