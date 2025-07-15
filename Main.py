import sys
import pygame
import Modules.varGlobals as varGlobals

from Modules.communication import (
    runCom,
    send
)
from Modules.colors import colors as cc, tts


varGlobals.IP = '127.0.0.1'
varGlobals.PORT = '8081'

###################################################################################################
#                                          PRESS BUTTON                                           #
###################################################################################################

def pencetButton(text):

    data = bytearray(3)

    # PAKSA HURUF KECIL
    text = text.lower()
    if text == "run":
        # print("run")
        # data[0] = 200
        # data[1] = 2
        # send(data)
        simulation()

    elif text == "back":
        mainMenu()

    elif text == "configuration":
        print("configuration")
        configuration()

    elif text == "save":
        print("save")
        runCom()
        mainMenu()

    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp, inputUser):

    # BOOLEAN
    varGlobals.hapus = True

    # INPUT TEXT
    if inp == varGlobals.IP:
        print("IP Address")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            varGlobals.IP = varGlobals.IP[:-1]
                        elif event.key == pygame.K_RETURN:
                            return
                        else:
                            varGlobals.IP += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.draw.rect(varGlobals.screen, 
                             cc.FTEK2, 
                             inputUser[inp], 
                             border_radius = 20)
            tts(varGlobals.IP, cc.WHITE, inputUser[inp], varGlobals.screen, 30)
            
            pygame.display.flip()
            varGlobals.clock.tick(120)

    elif inp == varGlobals.PORT:
        print("Port Address")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            varGlobals.PORT = varGlobals.PORT[:-1]
                        elif event.key == pygame.K_RETURN:
                            return
                        else:
                            varGlobals.PORT += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.draw.rect(varGlobals.screen, 
                             cc.FTEK2,
                             inputUser[inp], 
                             border_radius = 20)
            tts(varGlobals.PORT, cc.WHITE, inputUser[inp], varGlobals.screen, 30)
            
            pygame.display.flip()
            varGlobals.clock.tick(120)

    else:
        print('Wrong Place')


###################################################################################################
#                                          CONFIGURATION                                          #
###################################################################################################

def configuration():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runConfig = True

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)
    varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

    # UKURAN BUTTON
    PANJANG_BUTTON = varGlobals.res[0] * 0.094
    LEBAR_BUTTON = varGlobals.res[1] * 0.06
    PANJANG_INP_BUTTON = varGlobals.res[0] * 0.1
    LEBAR_INP_BUTTON = varGlobals.res[1] * 0.06

    # POSISI BUTTON
    SAVE = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-1.75)),
                            window_rect.centery - LEBAR_BUTTON * (-5),
                            PANJANG_BUTTON * 2, LEBAR_BUTTON * 1.7)

    # BUTTON
    buttons = {
        "Save" : SAVE
    }

    # POSISI INPUT USER
    INP_IP = pygame.rect.Rect(window_rect.centerx - (PANJANG_INP_BUTTON * (-1.07)),
                            window_rect.centery - LEBAR_INP_BUTTON * (1.9),
                            PANJANG_INP_BUTTON * 3, LEBAR_INP_BUTTON * 1.7)
    
    INP_PORT = pygame.rect.Rect(window_rect.centerx - (PANJANG_INP_BUTTON * (-1.07)),
                            window_rect.centery - LEBAR_INP_BUTTON * (-2.25),
                            PANJANG_INP_BUTTON * 3, LEBAR_INP_BUTTON * 1.7)

    # INPUT TEXT IP ADDRESS & PORT
    inputUser = {
        varGlobals.IP : INP_IP, 
        varGlobals.PORT : INP_PORT
    }

    while varGlobals.runConfig:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runConfig = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, buttons[button], border_radius = 20)
                tts(button, cc.WHITE, buttons[button], varGlobals.screen, 30)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.FTEK, buttons[button], border_radius = 20)
                tts(button, cc.FTEK2, buttons[button], varGlobals.screen, 30)

        # INPUT TEXT
        for text in inputUser:
            if inputUser[text].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, inputUser[text], border_radius = 20)
                tts(text, cc.WHITE, inputUser[text], varGlobals.screen, 30)
                if click:
                    fillText(text, inputUser)
            else:
                pygame.draw.rect(varGlobals.screen, cc.FTEK, inputUser[text], border_radius = 20)
                tts(text, cc.FTEK2, inputUser[text], varGlobals.screen, 30)

        pygame.display.flip()
        varGlobals.clock.tick(60)

    pygame.display.flip()
    varGlobals.clock.tick(60)


###################################################################################################
#                                            MAIN MENU                                            #
###################################################################################################

def mainMenu():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = True
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)
    varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

    # UKURAN BUTTON
    PANJANG_BUTTON = varGlobals.res[0] * 0.1
    LEBAR_BUTTON = varGlobals.res[1] * 0.06

    # POSISI BUTTON
    RUN = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
                            window_rect.centery - LEBAR_BUTTON * 2.6,
                            PANJANG_BUTTON * 3, LEBAR_BUTTON * 1.7)
    CONFIGURATION = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
                            window_rect.centery - (LEBAR_BUTTON * 0.2),
                            PANJANG_BUTTON * 3, LEBAR_BUTTON * 1.7)
    EXIT = pygame.rect.Rect(window_rect.centerx - (PANJANG_BUTTON * (-0.8)),
                            window_rect.centery - (LEBAR_BUTTON * (-2.2)),
                            PANJANG_BUTTON * 3, LEBAR_BUTTON * 1.7)

    # PESAN DISCONNECT DAN CONNECTED
    status_msg_x = varGlobals.screen.get_width() - 600
    status_msg_y = 900
    status_rect = pygame.Rect(status_msg_x, status_msg_y, 180, 30)
    
    # BUTTON
    buttons = {
        "Run" : RUN,
        "Configuration" : CONFIGURATION,
        "Exit" : EXIT
    }

    while varGlobals.runMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.FTEK2, buttons[button], border_radius = 20)
                tts(button, cc.WHITE, buttons[button], varGlobals.screen, 30)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.FTEK, buttons[button], border_radius = 20)
                tts(button, cc.FTEK2, buttons[button], varGlobals.screen, 30)

        if varGlobals.serviceBot:
            status_text = "Connected"
            tts(status_text, cc.GREEN, status_rect, varGlobals.screen, 30)
        else:
            status_text = "Disconnected"
            tts(status_text, cc.RED, status_rect, varGlobals.screen, 30)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)

def simulation():

    # BOOLEAN
    click = False
    varGlobals.runSim = True
    varGlobals.runMenu = False
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)
    varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

    back_x = varGlobals.screen.get_width() - 200
    back_y = 20
    back_pos = pygame.Rect(back_x, back_y, 180, 130)

    buttons = {
        "Back" : back_pos
    }

    while varGlobals.runSim:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()

        varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 40)
                if click:
                    pencetButton(button)
            else:
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 30)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)

mainMenu()