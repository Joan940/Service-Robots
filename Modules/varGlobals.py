import pygame
import os, sys

###################################################################################################
#                                           MAIN WINDOW                                           #
###################################################################################################

if sys.platform in ["win32", "win64"]: os.environ["SDL_VIDEO_CENTERED"] = "1"

pygame.init()
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
res = (screen_width, screen_height)

screen = pygame.display.set_mode(res)
window_rect = pygame.Surface.get_rect(screen)
print(int(screen_width), int(screen_height))


###################################################################################################
#                                            VARIABLE                                             #
###################################################################################################

# KOSONGAN
IP = ''
PORT = ''
jumlah = ''
nomorMeja = ''

# NONE
input = None
warna = None
pesanan = None

# BOOLEAN
notAutonomus = bool
serviceBot = False
updateOrder = True
runConfig = bool
runOrder = bool
runMenu = bool
runSim = bool
hapus = bool
list = bool
udp = bool

# STACK
allOrders = []

# RESOLUSI WINDOW
offsetX = res[0] / 14.53
offsetY = res[1] / 2.68
skala = res[1] / 1200

# UKURAN BUTTON
PANJANG_BUTTON = res[0] * 0.1
LEBAR_BUTTON = res[1] * 0.06
PANJANG_STATUS = res[0] * 0.064
LEBAR_STATUS = res[1] * 0.02
PANJANG_SAVE_BUTTON = res[0] * 0.094
LEBAR_SAVE_BUTTON = res[1] * 0.06
PANJANG_INP_BUTTON = res[0] * 0.1
LEBAR_INP_BUTTON = res[1] * 0.06

# NUMERIK
popupX = 0
popupY = 0
antrian = 1
lebarPopup = 350
tinggiPopup = 170

# KEYBOARD
keys_pressed = {
    pygame.K_UP : False,
    pygame.K_DOWN : False,
    pygame.K_LEFT : False,
    pygame.K_RIGHT : False,
    pygame.K_LSHIFT : False,
    pygame.K_LCTRL : False
}

# TEXT
conServiceBot = 'Disconnected' 

# FONT
font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 20)

# SOUND EFFECT
trueSound = pygame.mixer.Sound(r"C:\BMP-Robotics\Assets\true.wav")
falseSound = pygame.mixer.Sound(r"C:\BMP-Robotics\Assets\false.wav")
ketikSound = pygame.mixer.Sound(r"C:\BMP-Robotics\Assets\ketik.wav")


###################################################################################################
#                                           BACKGROUND                                            #
###################################################################################################

bgMenu = pygame.image.load("C:\BMP-Robotics\Assets\menu.png").convert_alpha()
bgConfig = pygame.image.load("C:\BMP-Robotics\Assets\configuration.png").convert_alpha()
bgSim = pygame.image.load("C:\BMP-Robotics\Assets\simulator.png").convert_alpha()
bgOrder = pygame.image.load("C:\BMP-Robotics\Assets\order.png").convert_alpha()

bot = pygame.image.load(r"C:\BMP-Robotics\Assets\bot.png").convert_alpha()
bot = pygame.transform.scale(bot, (40, 40))

arrow = pygame.image.load(r"C:\BMP-Robotics\Assets\arrow.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (100, 100))


###################################################################################################
#                                             CLASS                                               #
###################################################################################################

class orderan:
    EXIT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
        window_rect.centery - (LEBAR_BUTTON * (-2.2)),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )

    # SETIAP TURUN DIKURANGI 1.2
    MENU_1 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.3),
        window_rect.centery - (LEBAR_BUTTON * 3),
        PANJANG_BUTTON,
        LEBAR_BUTTON
    )
    MENU_2 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.3),
        window_rect.centery - (LEBAR_BUTTON * 1.8),
        PANJANG_BUTTON,
        LEBAR_BUTTON
    )
    MENU_3 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.3),
        window_rect.centery - (LEBAR_BUTTON * 0.6),
        PANJANG_BUTTON,
        LEBAR_BUTTON
    )
    MENU_4 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.3),
        window_rect.centery - (LEBAR_BUTTON * (-0.6)),
        PANJANG_BUTTON,
        LEBAR_BUTTON
    )
    MENU_5 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.3),
        window_rect.centery - (LEBAR_BUTTON * (-1.8)),
        PANJANG_BUTTON,
        LEBAR_BUTTON
    )

class main_menu:
    RUN = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
        window_rect.centery - LEBAR_BUTTON * 2.6,
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )
    CONFIGURATION = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
        window_rect.centery - (LEBAR_BUTTON * 0.2),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )
    EXIT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
        window_rect.centery - (LEBAR_BUTTON * (-2.2)),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )
    STATUS = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_STATUS * (-2.6)),
        window_rect.centery - (LEBAR_STATUS * (-15.5)),
        PANJANG_STATUS * 2,
        LEBAR_STATUS * 1.7
    )

class simulasi:
    BACK = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-3.75)),
        window_rect.centery - LEBAR_BUTTON * 7.8,
        PANJANG_BUTTON,
        LEBAR_BUTTON * 1.2
    )
    DEMO_1 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 0.95),
        window_rect.centery - (LEBAR_BUTTON * 1.5),
        PANJANG_BUTTON,
        LEBAR_BUTTON * 0.8
    )
    TAMBAH_PESANAN = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.3)),
        window_rect.centery - LEBAR_BUTTON * (5.85),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )
    LIST_PESANAN = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.3)),
        window_rect.centery - LEBAR_BUTTON * (3.85),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )

class config:
    SAVE_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_SAVE_BUTTON * (-1.42)),
        window_rect.centery - LEBAR_SAVE_BUTTON * (-5),
        PANJANG_SAVE_BUTTON * 2,
        LEBAR_SAVE_BUTTON * 1.7
    )

    # POSISI INPUT USER
    INP_IP_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_INP_BUTTON * (-0.78)),
        window_rect.centery - (LEBAR_INP_BUTTON * 1.66),
        PANJANG_INP_BUTTON * 3,
        LEBAR_INP_BUTTON * 1.7
    )
    INP_PORT_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_INP_BUTTON * (-0.78)),
        window_rect.centery - LEBAR_INP_BUTTON * (-1.8),
        PANJANG_INP_BUTTON * 3,
        LEBAR_INP_BUTTON * 1.7
    )