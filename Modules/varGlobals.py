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
# screen_width, screen_height = info.current_w, info.current_h
screen_width, screen_height = 1024, 600
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
# -- List Pesanan
meja = None
checkboxes = []

# -- Transisi Surface
oldSurface = None
newSurface = None

# -- Lainnya
input = None
warna = None
pesanan = None
temporary = None

# BOOLEAN
# -- Surface
runMakeOrder = bool
runConfig = bool
runStaff = bool
runOrder = bool
runMenu = bool
runSim = bool
runEye = bool
updateOrder = True

# -- Animasi Mata
isLookingRight = bool
isLookingLeft = bool
newExpression = bool
isBlinking = bool
mouseActive = bool

# -- Komunikasi
ser = None
udp = bool
uart = bool
notAutonomus = bool
serviceBot = False

# -- List Pesanan
list = bool

# STACK
allMeja = []
allOrders = []
startProperties = {}
targetPropertis = {}

# RESOLUSI WINDOW
offsetX = res[0] / 13.1
offsetY = res[1] / 2.76
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

# DEKLARASI AWAL MATA
SET_AWAL = {
    # MATA
    'eyeHeight': 150,
    'eyeOffsetX': 0,
    'eyeOffsetY': 0,
    
    # ALIS
    'eyebrowOffset_leftY': 0,
    'eyebrowOffset_rightY': 0,
    'eyebrowAngle_left': 0,
    'eyebrowAngle_right': 0,

    # MULUT
    'mouthY': 0,
    'mouthWidth': 0,
    'mouthHeight': 0,
    'mouthAngle': 0,
}

# ANIMASI MATA
ANIMATIONS = {
    'buka': {'eyeHeight': 150, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 0, 'eyebrowOffset_rightY': 0, 'eyebrowAngle_left': 0, 'eyebrowAngle_right': 0, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 40, 'mouthAngle': 1},
    'kedip': {'eyeHeight': 10, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 0, 'eyebrowOffset_rightY': 0, 'eyebrowAngle_left': -0.1, 'eyebrowAngle_right': 0.1, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 40, 'mouthAngle': 1},
    'kanan': {'eyeHeight': 150, 'eyeOffsetX': 100, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 0, 'eyebrowOffset_rightY': 0, 'eyebrowAngle_left': 0, 'eyebrowAngle_right': 0, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 40, 'mouthAngle': 1},
    'kiri': {'eyeHeight': 150, 'eyeOffsetX': -100, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 0, 'eyebrowOffset_rightY': 0, 'eyebrowAngle_left': 0, 'eyebrowAngle_right': 0, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 40, 'mouthAngle': 1},
    
    # EKSPRESI
    'marah': {'eyeHeight': 150, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 5, 'eyebrowOffset_rightY': 5, 'eyebrowAngle_left': -10, 'eyebrowAngle_right': 10, 'mouthY': 100, 'mouthWidth': 120, 'mouthHeight': 50, 'mouthAngle': 180},
    'sedih': {'eyeHeight': 130, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': -10, 'eyebrowOffset_rightY': -10, 'eyebrowAngle_left': 10, 'eyebrowAngle_right': -10, 'mouthY': 100, 'mouthWidth': 80, 'mouthHeight': 10, 'mouthAngle': 0},
    'terkejut': {'eyeHeight': 180, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': -40, 'eyebrowOffset_rightY': -40, 'eyebrowAngle_left': 0, 'eyebrowAngle_right': 0, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 50, 'mouthAngle': 0},
    'senyum': {'eyeHeight': 80, 'eyeOffsetX': 0, 'eyeOffsetY': 10, 'eyebrowOffset_leftY': 5, 'eyebrowOffset_rightY': 5, 'eyebrowAngle_left': 0, 'eyebrowAngle_right': 0, 'mouthY': 120, 'mouthWidth': 120, 'mouthHeight': 40, 'mouthAngle': 0}
}

# NUMERIK
# -- Orderan
popupX = res[0] // 2 - 220
popupY = res[1] // 2 - 113
lebarPopup = 300
tinggiPopup = 230
startTransisi = 0
durasiTransisi = 0.5

# -- List Pesanan
antrian = 1

# -- Animasi Mata
eyeRightX = 565
lebarMata = 100
eyeLeftX = 365
eyePosY = 170

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
font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 25)

# SOUND EFFECT
trueSound = pygame.mixer.Sound(r"C:\BMP-Robotics\Assets\true.wav")
falseSound = pygame.mixer.Sound(r"C:\BMP-Robotics\Assets\false.wav")
ketikSound = pygame.mixer.Sound(r"C:\BMP-Robotics\Assets\ketik.wav")


###################################################################################################
#                                           BACKGROUND                                            #
###################################################################################################

bgSocketConfig = pygame.image.load("C:\BMP-Robotics\Assets\socketConfig.png").convert_alpha()
bgPidConfig = pygame.image.load("C:\BMP-Robotics\Assets\pidConfig.png").convert_alpha()
bgMakeOrder = pygame.image.load("C:\BMP-Robotics\Assets\makeOrder.png").convert_alpha()
bgSim = pygame.image.load("C:\BMP-Robotics\Assets\simulator.png").convert_alpha()
bgOrder = pygame.image.load("C:\BMP-Robotics\Assets\order.png").convert_alpha()
bgStaff = pygame.image.load("C:\BMP-Robotics\Assets\staff.png").convert_alpha()
bgMenu = pygame.image.load("C:\BMP-Robotics\Assets\menu.png").convert_alpha()
bgEyes = pygame.image.load("C:\BMP-Robotics\Assets\eye.png").convert_alpha()

bot = pygame.image.load(r"C:\BMP-Robotics\Assets\bot.png").convert_alpha()
bot = pygame.transform.scale(bot, (20, 20))

arrow = pygame.image.load(r"C:\BMP-Robotics\Assets\arrow.png").convert_alpha()
arrow = pygame.transform.scale(arrow, (40, 40))


###################################################################################################
#                                             CLASS                                               #
###################################################################################################

class orderan:
    EXIT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.2)),
        window_rect.centery - (LEBAR_BUTTON * (-3.5)),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )

    # SETIAP TURUN DIKURANGI 1.8
    MENU_1 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.4),
        window_rect.centery - (LEBAR_BUTTON * 4),
        PANJANG_BUTTON * 1.5,
        LEBAR_BUTTON * 1.5
    )
    MENU_2 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.4),
        window_rect.centery - (LEBAR_BUTTON * 2.2),
        PANJANG_BUTTON * 1.5,
        LEBAR_BUTTON * 1.5
    )
    MENU_3 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.4),
        window_rect.centery - (LEBAR_BUTTON * 0.4),
        PANJANG_BUTTON * 1.5,
        LEBAR_BUTTON * 1.5
    )
    MENU_4 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.4),
        window_rect.centery - (LEBAR_BUTTON * (-1.4)),
        PANJANG_BUTTON * 1.5,
        LEBAR_BUTTON * 1.5
    )
    MENU_5 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 4.4),
        window_rect.centery - (LEBAR_BUTTON * (-3.2)),
        PANJANG_BUTTON * 1.5,
        LEBAR_BUTTON * 1.5
    )

class main_menu:
    RUN = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.5)),
        window_rect.centery - LEBAR_BUTTON * 2.6,
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
    )
    SIMULATION = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.5)),
        window_rect.centery - (LEBAR_BUTTON * 0.2),
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
    )
    CONFIGURATION = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.5)),
        window_rect.centery - (LEBAR_BUTTON * (-2.2)),
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
    )
    EXIT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.5)),
        window_rect.centery - (LEBAR_BUTTON * (-4.6)),
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
    )
    STATUS = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_STATUS * 7.5),
        window_rect.centery - (LEBAR_STATUS * 23.5),
        PANJANG_STATUS * 2,
        LEBAR_STATUS * 1.7
    )
    SOCKET = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 0.7),
        window_rect.centery - (LEBAR_BUTTON * (-1.3)),
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
    )
    PID = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 0.7),
        window_rect.centery - (LEBAR_BUTTON * (-3.1)),
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
    )

class simulasi:
    BACK = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-3.75)),
        window_rect.centery - LEBAR_BUTTON * 7.8,
        PANJANG_BUTTON,
        LEBAR_BUTTON * 1.2
    )
    DEMO_1 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1)),
        window_rect.centery - (LEBAR_BUTTON * 0),
        PANJANG_BUTTON,
        LEBAR_BUTTON * 6.7
    )

class config:
    SAVE_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_SAVE_BUTTON * 1.08),
        window_rect.centery - LEBAR_SAVE_BUTTON * (-5.2),
        PANJANG_SAVE_BUTTON * 1,
        LEBAR_SAVE_BUTTON * 1.7
    )
    EXIT_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_SAVE_BUTTON * (-0.07)),
        window_rect.centery - LEBAR_SAVE_BUTTON * (-5.2),
        PANJANG_SAVE_BUTTON * 1,
        LEBAR_SAVE_BUTTON * 1.7
    )

    # POSISI INPUT USER
    INP_IP_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_INP_BUTTON),
        window_rect.centery - (LEBAR_INP_BUTTON * 1.2),
        PANJANG_INP_BUTTON * 2,
        LEBAR_INP_BUTTON * 1.7
    )
    INP_PORT_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_INP_BUTTON),
        window_rect.centery - LEBAR_INP_BUTTON * (-2.95),
        PANJANG_INP_BUTTON * 2,
        LEBAR_INP_BUTTON * 1.7
    )

class make_order:
    BACK = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-3.75)),
        window_rect.centery - LEBAR_BUTTON * 7.8,
        PANJANG_BUTTON,
        LEBAR_BUTTON * 1.2
    )
    LIST_PESANAN = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.3)),
        window_rect.centery - LEBAR_BUTTON * (5.85),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 1.7
    )

class staffConfig:
    BACK = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.4)),
        window_rect.centery - (LEBAR_BUTTON * (-3.2)),
        PANJANG_BUTTON,
        LEBAR_BUTTON * 2
    )
    TRAY_1 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 3.4),
        window_rect.centery - LEBAR_BUTTON * 3,
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 3.5
    )
    TRAY_2 = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 3.4),
        window_rect.centery - LEBAR_BUTTON * (-1),
        PANJANG_BUTTON * 3,
        LEBAR_BUTTON * 3.5
    )
    BOX_SETUP = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 2.4),
        window_rect.centery - LEBAR_BUTTON * 5,
        PANJANG_BUTTON * 4.8,
        LEBAR_BUTTON * 10.2
    )
    BOX_KONFIRMASI = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * 2.4),
        window_rect.centery - (LEBAR_BUTTON * (-3.2)),
        PANJANG_BUTTON,
        LEBAR_BUTTON * 2
    )
    PLUS = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.3)),
        window_rect.centery - (LEBAR_BUTTON),
        PANJANG_BUTTON - 75,
        LEBAR_BUTTON - 7
    )
    MIN = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-2)),
        window_rect.centery - (LEBAR_BUTTON),
        PANJANG_BUTTON - 75,
        LEBAR_BUTTON - 7
    )
    TOTAL = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.65)),
        window_rect.centery - (LEBAR_BUTTON),
        PANJANG_BUTTON - 75,
        LEBAR_BUTTON - 7
    )