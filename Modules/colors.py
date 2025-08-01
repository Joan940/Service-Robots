import pygame
import Modules.varGlobals as varGlobals

class custom:
    RED = (255, 0, 0)
    GREEN = (70, 205, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (245, 245, 245)
    FTEK = (209, 107, 2)
    FTEK2 = (150, 77, 2)
    DARK_BROWN = (101, 67, 33)
    LIGHT_BROWN = (181, 101, 29)
    RED_BROWN = (165, 42, 42)
    YELLOW_BROWN = (153, 101, 21)
    GRAY_BROWN = (128, 105, 72)
    COFFEE_BROWN = (111, 78, 55)
    COPPER_BROWN = (184, 115, 51)
    LIGHT_RED_BROWN = (193, 154, 107)
    BRIGHT_YELLOW = (255, 255, 0)  # Kuning cerah
    ORANGE = (255, 165, 0)        # Oranye
    PURPLE = (128, 0, 128)        # Ungu
    CYAN = (0, 255, 255)          # Cyan (Aqua)
    MAGENTA = (255, 0, 255)       # Magenta (Fuchsia)
    GREY = (192, 192, 192)        # Abu-abu
    DARK_GREY = (64, 64, 64)      # Abu-abu gelap
    LIGHT_BLUE = (173, 216, 230)  # Biru muda
    GOLD = (255, 215, 0)          # Emas
    SILVER = (192, 192, 192)      # Perak
    

def tts(text, color, rect, surface, font_size):
    font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def tts2(text, color, rect, surface, font_size):
    font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midleft=rect.midleft)
    surface.blit(text_surface, text_rect)