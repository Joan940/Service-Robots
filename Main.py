import sys
import time
import math
import random
import pygame
import Modules.dataRobot as dataRobot
import Modules.varGlobals as varGlobals

from itertools import chain
from Modules.communication import (
    runCom,
    send
)
from Skills.demoMode import (
    meja1,
    meja2,
    meja3,
    meja4
)
from Modules.algorithm import (
    drawNumberPad,
    tampilanOrder,
    rotatedImage,
    numpadConfig,
    rotatePoint,
    numpadStaff,
    transition,
    easeInOut,
    drawGrid,
    getMeja,
    lerp,
    aStar
)
from Modules.database import (
    reset_database,
    delete_orders,
    getOrders,
    addOrders
)
from Modules.colors import (
    custom as cc,
    tts1,
    tts2,
    tts,
)
from Modules.varGlobals import (
    staffConfig as scButton,
    daftar_menu as dmButton,
    make_order as moButton,
    orderan as orderButton,
    paketMM as packButton,
    main_menu as mmButton,
    simulasi as simButton,
    satisfied as sfButton,
    config as confButton,
    PID as pidButton
)


###################################################################################################
#                            VARIABLE GLOBAL YANG DIINISIALISASI DIAWAL                           #
###################################################################################################

pygame.mixer.init()

varGlobals.IP   = '192.168.110.195'
varGlobals.PORT = '8081'
varGlobals.P    = '0'
varGlobals.I    = '0'
varGlobals.D    = '0'


###################################################################################################
#                                          PRESS BUTTON                                           #
###################################################################################################

def pencetButton(text):

    # PAKSA HURUF KECIL
    text = text.lower()

    if text == "meja 1":
        meja1()
    elif text == "meja 2":
        meja2()
    elif text == "meja 3":
        meja3()
    elif text == "meja 4":
        meja4()
    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp_key, inputUser_rects, done_rect):

    if varGlobals.runPID:

        numpad_button = {}

        while True:
            
            varGlobals.screen.blit(varGlobals.bgPidConfig, (0, 0))

            numpad_button = numpadConfig(varGlobals.screen, 545, 260, 3)

            for itemKu, rect in done_rect.items():
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(itemKu, cc.WHITE, rect, varGlobals.screen, 25)
        
            for key, rect in inputUser_rects.items():
                if key in ["P", "I", "D"]:
                    current_value = ""
                    if key == "P":
                        current_value = varGlobals.P
                    elif key == "I":
                        current_value = varGlobals.I
                    elif key == "D":
                        current_value = varGlobals.D
                    
                    if key == inp_key:
                        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius = 20)
                        tts(current_value, cc.WHITE, rect, varGlobals.screen, 30)
                    else:
                        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                        tts(current_value, cc.RED_BROWN, rect, varGlobals.screen, 25)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    varGlobals.ketikSound.play()
                    if event.key == pygame.K_BACKSPACE:
                        if inp_key == "P":
                            varGlobals.P = varGlobals.P[:-1]
                        elif inp_key == "I":
                            varGlobals.I = varGlobals.I[:-1]
                        elif inp_key =="D":
                            varGlobals.D = varGlobals.D[:-1]
                    elif event.key == pygame.K_RETURN:
                        return
                    else:
                        if inp_key == "P":
                            if event.unicode.isdigit():
                                varGlobals.P += event.unicode
                        elif inp_key == "I":
                            if event.unicode.isdigit():
                                varGlobals.I += event.unicode
                        elif inp_key == "D":
                            if event.unicode.isdigit():
                                varGlobals.D += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_on_numpad = False
                    
                    for number, rect in numpad_button.items():
                        if rect.collidepoint(event.pos):
                            varGlobals.ketikSound.play()
                            clicked_on_numpad = True
                            
                            if number.isdigit():
                                if inp_key == "P":
                                    varGlobals.P += number
                                elif inp_key == "I":
                                    varGlobals.I += number
                                elif inp_key == "D":
                                    varGlobals.D += number
                            
                            elif number == "Del":
                                if inp_key == "P":
                                    varGlobals.P = varGlobals.P[:-1]
                                elif inp_key == "I":
                                    varGlobals.I = varGlobals.I[:-1]
                                elif inp_key == "D":
                                    varGlobals.D = varGlobals.D[:-1]
                            
                            elif number == ".":
                                if inp_key == "P":
                                    varGlobals.P += number
                                elif inp_key == "I":
                                    varGlobals.I += number
                                elif inp_key == "D":
                                    varGlobals.D += number
                            break

                    if not clicked_on_numpad:
                        if not inputUser_rects[inp_key].collidepoint(event.pos):
                            return # Keluar dari mode input

            pygame.display.flip()
            varGlobals.clock.tick(120)
        
    elif varGlobals.runConfig:

        numpad_button = {}

        while True:
            
            varGlobals.screen.blit(varGlobals.bgSocketConfig, (0, 0))

            numpad_button = numpadConfig(varGlobals.screen, 545, 260, 3)

            for itemKu, rect in done_rect.items():
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(itemKu, cc.WHITE, rect, varGlobals.screen, 25)
        
            for key, rect in inputUser_rects.items():
                if key in ["IP", "PORT"]:
                    current_value = ""
                    if key == "IP":
                        current_value = varGlobals.IP
                    elif key == "PORT":
                        current_value = varGlobals.PORT
                    
                    if key == inp_key:
                        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius = 20)
                        tts(current_value, cc.WHITE, rect, varGlobals.screen, 30)
                    else:
                        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                        tts(current_value, cc.RED_BROWN, rect, varGlobals.screen, 25)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    varGlobals.ketikSound.play()
                    if event.key == pygame.K_BACKSPACE:
                        if inp_key == "IP":
                            varGlobals.IP = varGlobals.IP[:-1]
                        elif inp_key == "PORT":
                            varGlobals.PORT = varGlobals.PORT[:-1]
                    elif event.key == pygame.K_RETURN:
                        return
                    else:
                        if inp_key == "IP":
                            if event.unicode.isdigit():
                                varGlobals.IP += event.unicode
                        elif inp_key == "PORT":
                            if event.unicode.isdigit():
                                varGlobals.PORT += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_on_numpad = False
                    
                    for number, rect in numpad_button.items():
                        if rect.collidepoint(event.pos):
                            varGlobals.ketikSound.play()
                            clicked_on_numpad = True
                            
                            if number.isdigit():
                                if inp_key == "IP":
                                    varGlobals.IP += number
                                elif inp_key == "PORT":
                                    varGlobals.PORT += number
                            
                            elif number == "Del":
                                if inp_key == "IP":
                                    varGlobals.IP = varGlobals.IP[:-1]
                                elif inp_key == "PORT":
                                    varGlobals.PORT = varGlobals.PORT[:-1]
                            
                            elif number == ".":
                                if inp_key == "IP":
                                    varGlobals.IP += number
                                elif inp_key == "PORT":
                                    varGlobals.PORT += number
                            break

                    if not clicked_on_numpad:
                        if not inputUser_rects[inp_key].collidepoint(event.pos):
                            return # Keluar dari mode input

            pygame.display.flip()
            varGlobals.clock.tick(120)


###################################################################################################
#                                          CONFIGURATION                                          #
###################################################################################################
        
def pidConfig():

    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # BOOLEAN
    click = False
    varGlobals.runPID              = True
    varGlobals.runEye              = False
    varGlobals.runSim              = False
    varGlobals.runMenu             = False
    varGlobals.runStaff            = False
    varGlobals.runConfig           = False
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = False

    buttons = {
        "P": pidButton.P,
        "I": pidButton.I,
        "D": pidButton.D
    }

    done = {
        "Save": pidButton.SAVE_RECT,
        "Back": pidButton.EXIT_RECT
    }

    while varGlobals.runPID:
        
        varGlobals.screen.blit(varGlobals.bgPidConfig, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runPID = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                varGlobals.trueSound.play()
                click = True

        mx, my = pygame.mouse.get_pos()

        for button, rect in done.items():
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(button, cc.WHITE, rect, varGlobals.screen, 30)
                if click:
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

                    if button == "Save":
                        data = bytearray(7)
                        
                        data[0] = 200
                        valueP  = int(varGlobals.P)
                        data[1] = (valueP >> 8) & 0xFF
                        data[2] = valueP & 0xFF

                        valueI  = int(varGlobals.I)
                        data[3] = (valueI >> 8) & 0xFF
                        data[4] = valueI & 0xFF

                        valueD  = int(varGlobals.D)
                        data[5] = (valueD >> 8) & 0xFF
                        data[6] = valueD & 0xFF
                        send(data)
                    
                    elif button == "Back":
                        varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                        mainMenu()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(button, cc.WHITE, rect, varGlobals.screen, 25)

        for button, rect in buttons.items():
            display_text = button
            if button == "P":
                display_text = varGlobals.P
            elif button == "I":
                display_text = varGlobals.I
            elif button == "D":
                display_text = varGlobals.D

            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius=20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 30)
                if click:
                    if button in ["P", "I", "D"]:
                        fillText(button, buttons, done)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 25)

        click = False
        varGlobals.clock.tick(60)
        pygame.display.flip()
    

###################################################################################################
#                                          CONFIGURATION                                          #
###################################################################################################

def configuration():

    # BOOLEAN
    click = False
    varGlobals.runPID              = False
    varGlobals.runEye              = False
    varGlobals.runSim              = False
    varGlobals.runMenu             = False
    varGlobals.runStaff            = False
    varGlobals.runConfig           = True
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = False

    buttons = {
        "Save" : confButton.SAVE_RECT,
        "Back" : confButton.EXIT_RECT
    }
    
    inputUser = {
        "IP"   : confButton.INP_IP_RECT,
        "PORT" : confButton.INP_PORT_RECT
    }

    while varGlobals.runConfig:

        varGlobals.screen.blit(varGlobals.bgSocketConfig, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runConfig = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                varGlobals.trueSound.play()
                click = True

        mx, my = pygame.mouse.get_pos()

        for button, rect in buttons.items():
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius = 20)
                tts(button, cc.WHITE, rect, varGlobals.screen, 30)
                if click:
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

                    if button == "Save" and (varGlobals.IP and varGlobals.PORT):
                        print("save")
                        runCom()
                    elif button == "Save" and not (varGlobals.IP and varGlobals.PORT):
                        varGlobals.falseSound.play()
                    elif button == "Back" and (varGlobals.IP and varGlobals.PORT):
                        varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                        mainMenu()
                    elif button == "Back" and not (varGlobals.IP and varGlobals.PORT):
                        varGlobals.IP = '127.0.0.1'
                        varGlobals.PORT = '8081'
                        
                        varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                        mainMenu()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius = 20)
                tts(button, cc.WHITE, rect, varGlobals.screen, 25)

        for key, rect in inputUser.items():
            display_text = key
            if key == "IP":
                display_text = varGlobals.IP
            elif key == "PORT":
                display_text = varGlobals.PORT
            
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 30)
                if click:
                    if key in ["IP", "PORT"]:
                        fillText(key, inputUser, buttons)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 25)

        click = False
        varGlobals.clock.tick(120)
        pygame.display.flip()


###################################################################################################
#                                     SATISFIED CONFIGURATION                                     #
###################################################################################################

def satisfiedConfiguration():

    # BOOLEAN
    taken = True
    varGlobals.runPID              = False
    varGlobals.runEye              = False
    varGlobals.runSim              = False
    varGlobals.runMenu             = False
    varGlobals.runStaff            = False
    varGlobals.runConfig           = False
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = True

    buttons = {
        "Yes"   : sfButton.YES,
        "No"    : sfButton.NO
    }

    while varGlobals.runServiceSatisfied:

        mx, my = pygame.mouse.get_pos()
        varGlobals.screen.blit(varGlobals.bgSatisfied, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runConfig = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                varGlobals.trueSound.play()
                if taken:
                    for button, rect in buttons.items():
                        if rect.collidepoint(mx, my):
                            if button == "Yes":
                                varGlobals.takenOrder = 1
                                taken                 = True
                                varGlobals.runServiceSatisfied = False
                                varGlobals.runEye              = True
                                eyeUI()
                            elif button == "No":
                                varGlobals.takenOrder = 0
                                taken                 = False
                else:
                    taken = not taken

        for button, rect in buttons.items():
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
                pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 6, border_radius=20)
                tts(button, cc.BLACK, rect, varGlobals.screen, 50)
            else:
                pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
                pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 3, border_radius=20)
                tts(button, cc.BLACK, rect, varGlobals.screen, 45)

        if not taken:
            boxPenghalang = pygame.Rect(0, 0, varGlobals.res[0], varGlobals.res[1])
            overlay       = pygame.Surface((boxPenghalang.width, boxPenghalang.height), pygame.SRCALPHA)

            pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
            varGlobals.screen.blit(overlay, (0, 0))

            pygame.draw.rect(varGlobals.screen, cc.WHITE, sfButton.MESSAGE, border_radius=20)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, sfButton.MESSAGE, 5, border_radius=20)
            tts("Get Your Food!", cc.BLACK, sfButton.MESSAGE, varGlobals.screen, 65)


        varGlobals.clock.tick(120)
        pygame.display.flip()


###################################################################################################
#                                          CHINESE CUSINE                                         #
###################################################################################################

# def chineseCusine():

#     # RESET
#     varGlobals.oldSurface = None
#     varGlobals.newSurface = None

#     # MENYIMPAN BUTTON TAB ANGKA
#     number_pad_buttons = {}

#     # BOOLEAN
#     click = False
#     varGlobals.runPID        = False
#     varGlobals.runEye        = False
#     varGlobals.runSim        = False
#     varGlobals.runMenu       = False
#     varGlobals.runStaff      = False
#     varGlobals.runConfig     = False
#     varGlobals.runPaketCB    = False
#     varGlobals.runPaketMM    = False
#     varGlobals.runChinese    = True
#     varGlobals.runJavanese   = False
#     varGlobals.runMakeOrder  = False
#     varGlobals.runDaftarMenu = False

#     buttons = {
#         "Back" : orderButton.EXIT
#     }

#     menu = {
#         "Goreng Tepung"           : orderButton.MENU_1,
#         "Asam Manis"              : orderButton.MENU_2,
#         "Bestik Ayam Saus Tomat"  : orderButton.MENU_3,
#         "Ayam Gongso"             : orderButton.MENU_4,
#         "Sapi Lada Hitam"         : orderButton.MENU_5,
#         "Cap Cay Goreng"          : orderButton.MENU_6,
#         "Kamar Bola"              : orderButton.MENU_7,
#         "Angsio Tahu"             : orderButton.MENU_8,
#         "(Bakmi/Soun) Goreng"     : orderButton.MENU_9,
#         "Fu Yung Hai"             : orderButton.MENU_10,
#         "Brokoli Ca Bawang Putih" : orderButton.MENU_11,
#         "Sambal"                  : orderButton.MENU_12,
#         "Kerupuk"                 : orderButton.MENU_13,
#         "Teh Tawar Panas"         : orderButton.MENU_14,
#         "Kopi Tawar Panas"        : orderButton.MENU_15,
#         "Air Mineral"             : orderButton.MENU_16
#     }

#     font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 17)

#     while varGlobals.runChinese:

#         varGlobals.screen.blit(varGlobals.bgChineseCusine, (0, 0))
#         mx, my = pygame.mouse.get_pos()
        
#         # DEKLARASI POP UP
#         popupPesanan = pygame.Rect(varGlobals.popupX, varGlobals.popupY, varGlobals.lebarPopup + 20, varGlobals.tinggiPopup)
#         numPad       = pygame.Rect(popupPesanan.width + 10, varGlobals.popupY, 450, varGlobals.tinggiPopup)
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 varGlobals.runChinese = False
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 click = True
#                 varGlobals.trueSound.play()
                
#                 if varGlobals.pesanan:

#                     # POP UP HILANG JIKA DIKLIK DI LUAR BUTTON
#                     if not popupPesanan.collidepoint(mx, my) and not numPad.collidepoint(mx, my):
#                         varGlobals.pesanan   = None
#                         varGlobals.input     = None
#                         varGlobals.nomorMeja = ""
#                         varGlobals.jumlah    = ""
#                     else:

#                         # LOGIKA POP UP
#                         if boxNomorMeja.collidepoint(mx, my):
#                             varGlobals.input = "table"
#                         elif boxJumlah.collidepoint(mx, my):
#                             varGlobals.input = "quantity"
#                         elif boxConfirm.collidepoint(mx, my):
#                             if varGlobals.nomorMeja and varGlobals.jumlah:
#                                 addOrders(varGlobals.nomorMeja, varGlobals.antrian, varGlobals.pesanan, varGlobals.jumlah)
                                
#                                 # RESET
#                                 varGlobals.pesanan   = None
#                                 varGlobals.nomorMeja = ""
#                                 varGlobals.jumlah    = ""
#                                 varGlobals.antrian  += 1
#                                 varGlobals.input     = None

#                                 # RESET NUMPAD
#                                 number_pad_buttons = {}
#                             else:
#                                 print("Nomor meja dan jumlah harus diisi!")
#                                 varGlobals.falseSound.play()

#                         # LOGIKA NUMPAD
#                         if number_pad_buttons:
#                             for number, rect in number_pad_buttons.items():
#                                 if rect.collidepoint(mx, my):
#                                     if number.isdigit():
#                                         if varGlobals.input == "table":
#                                             varGlobals.nomorMeja += number
#                                         elif varGlobals.input == "quantity":
#                                             varGlobals.jumlah += number
#                                     elif number == "Del":
#                                         if varGlobals.input == "table":
#                                             varGlobals.nomorMeja = varGlobals.nomorMeja[:-1]
#                                         elif varGlobals.input == "quantity":
#                                             varGlobals.jumlah = varGlobals.jumlah[:-1]
#                                     elif number == "Clear":
#                                         if varGlobals.input == "table":
#                                             varGlobals.nomorMeja = ""
#                                         elif varGlobals.input == "quantity":
#                                             varGlobals.jumlah = ""

#                 else:

#                     for menu_item, rect in menu.items():
#                         if rect.collidepoint(mx, my):
#                             varGlobals.pesanan   = menu_item
#                             varGlobals.input     = "table"
#                             varGlobals.nomorMeja = ""
#                             varGlobals.jumlah    = ""
#                             break

#                     for menu_item, rect in buttons.items():
#                         if rect.collidepoint(mx, my):
#                             varGlobals.oldSurface = varGlobals.screen.copy()
#                             varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

#                             if menu_item == "Back":
#                                 varGlobals.newSurface.blit(varGlobals.bgMakeOrder, (0, 0))
#                                 transition(varGlobals.oldSurface, varGlobals.newSurface, direction="down", speed=20)
#                                 makeOrder()

#                     for button_name in buttons:
#                         if buttons[button_name].collidepoint(mx, my):
#                             pencetButton(button_name)

#             if event.type == pygame.KEYDOWN and varGlobals.pesanan:
#                 if varGlobals.input == "table":
#                     if event.unicode.isnumeric():
#                         varGlobals.nomorMeja += event.unicode
#                     elif event.key == pygame.K_BACKSPACE and varGlobals.nomorMeja:
#                         varGlobals.nomorMeja = varGlobals.nomorMeja[:-1]
#                     elif event.key == pygame.K_RETURN:
#                         if varGlobals.nomorMeja:
#                             varGlobals.input = "quantity"
#                         else:
#                             print("Nomor meja tidak boleh kosong.")
#                             varGlobals.falseSound.play()

#                 elif varGlobals.input == "quantity":
#                     if event.unicode.isnumeric():
#                         varGlobals.jumlah += event.unicode
#                     elif event.key == pygame.K_BACKSPACE and varGlobals.jumlah:
#                         varGlobals.jumlah = varGlobals.jumlah[:-1]
#                     elif event.key == pygame.K_RETURN:
#                         if varGlobals.nomorMeja and varGlobals.jumlah:
#                             addOrders(varGlobals.nomorMeja, varGlobals.antrian, varGlobals.pesanan, varGlobals.jumlah)
                            
#                             # RESET
#                             varGlobals.pesanan   = None
#                             varGlobals.nomorMeja = ""
#                             varGlobals.jumlah    = ""
#                             varGlobals.antrian  += 1
#                             varGlobals.input     = None
#                         else:
#                             print("Nomor meja dan jumlah harus diisi!")
#                             varGlobals.falseSound.play()

#         # # LOGIKA TOMBOL
#         for button_name, rect in buttons.items():
#             if rect.collidepoint(mx, my) and not varGlobals.pesanan:
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius=20)
#                 tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 30)
#             else:
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
#                 tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 25)
        
#         for menu_item, rect in menu.items():
#             if rect.collidepoint(mx, my) and not varGlobals.pesanan:
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
#                 tts(menu_item, cc.WHITE, rect, varGlobals.screen, 20)
#             else:
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
#                 tts(menu_item, cc.WHITE, rect, varGlobals.screen, 15)

#         # JENDELA TAMBAHAN MUNCUL KETIKA MEMESAN
#         if varGlobals.pesanan:

#             boxNomorMeja = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 61, varGlobals.lebarPopup - 2 * 10, 50)
#             boxJumlah    = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 116, varGlobals.lebarPopup - 2 * 10, 50)
#             boxConfirm   = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 171, varGlobals.lebarPopup - 2 * 10, 50)
            
#             boxPenghalang = pygame.Rect(0, 0, varGlobals.res[0], varGlobals.res[1])
#             overlay       = pygame.Surface((boxPenghalang.width, boxPenghalang.height), pygame.SRCALPHA)

#             pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
#             varGlobals.screen.blit(overlay, (0, 0))

#             # MENGGAMBAR KOTAK POP UP BESAR
#             kotakPopup = pygame.Rect(varGlobals.popupX, varGlobals.popupY, varGlobals.lebarPopup, varGlobals.tinggiPopup)
#             pygame.draw.rect(varGlobals.screen, cc.WHITE, kotakPopup, border_radius=15)
#             pygame.draw.rect(varGlobals.screen, cc.BLACK, kotakPopup, 2, border_radius=15)

#             # KOTAK INPUT UNTUK NOMOR MEJA DAN JUMLAH PESANAN
#             pygame.draw.rect(varGlobals.screen, cc.WHITE, boxNomorMeja, border_radius=8)
#             pygame.draw.rect(varGlobals.screen, cc.WHITE, boxJumlah, border_radius=8)

#             # KOTAK KONFIRMASI
#             pygame.draw.rect(varGlobals.screen, cc.WHITE, boxConfirm, border_radius=8)
#             if boxConfirm.collidepoint(mx, my):
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, boxConfirm, border_radius=25)
#                 tts("Done", cc.WHITE, boxConfirm, varGlobals.screen, 17)
#             else:
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, boxConfirm, border_radius=8)
#                 tts("Done", cc.WHITE, boxConfirm, varGlobals.screen, 17)

#             # HIGHLIGHT BOX
#             if varGlobals.input == "table":
#                 pygame.draw.rect(varGlobals.screen, cc.BLACK, boxNomorMeja, 2, border_radius=8)
#             elif varGlobals.input == "quantity":
#                 pygame.draw.rect(varGlobals.screen, cc.BLACK, boxJumlah, 2, border_radius=8)
#             elif varGlobals.input == "confirm":
#                 pygame.draw.rect(varGlobals.screen, cc.BLACK, boxConfirm, 2, border_radius=8)
            
#             # JUDUL UNTUK KOTAK POP UP BESAR
#             textJudul = varGlobals.font.render(f"Order {varGlobals.pesanan}", True, cc.BLACK)
#             textPos   = textJudul.get_rect(centerx = kotakPopup.centerx, top = varGlobals.popupY + 10)
#             varGlobals.screen.blit(textJudul, textPos)

#             # TEXT PADA INPUTAN DAN WARNANYA
#             textMeja   = f"Meja     :   {varGlobals.nomorMeja}"
#             textJumlah = f"Jumlah  :   {varGlobals.jumlah}"
#             ccMeja     = font.render(textMeja, True, cc.BLACK)
#             ccJumlah   = font.render(textJumlah, True, cc.BLACK)

#             varGlobals.screen.blit(ccMeja, (boxNomorMeja.x + 10, boxNomorMeja.y + 13))
#             varGlobals.screen.blit(ccJumlah, (boxJumlah.x + 10, boxJumlah.y + 13))

#             number_pad_buttons = drawNumberPad(varGlobals.screen, varGlobals.popupX, varGlobals.popupY, 2)

#         click = False
#         varGlobals.clock.tick(120)
#         pygame.display.flip()


###################################################################################################
#                                      PAKET MAKAN DAN MINUM                                      #
###################################################################################################

# def daftarMenu():

#     # BOOLEAN
#     click = False
#     varGlobals.runPID        = False
#     varGlobals.runEye        = False
#     varGlobals.runSim        = False
#     varGlobals.runMenu       = False
#     varGlobals.runStaff      = False
#     varGlobals.runConfig     = False
#     varGlobals.runPaketCB    = False
#     varGlobals.runPaketMM    = False
#     varGlobals.runChinese    = False
#     varGlobals.runJavanese   = False
#     varGlobals.runMakeOrder  = False
#     varGlobals.runDaftarMenu = True

#     buttons = {
#         "Paket Makan Minum"  : dmButton.PAKET_MM,
#         "Chinese Cuisine"    : dmButton.CHINESE_CUISINE,
#         "Javanese Cuisine"   : dmButton.JAVANESE_CUISINE,
#         "Paket Coffee Break" : dmButton.PAKET_CB
#     }

#     while varGlobals.runDaftarMenu:

#         varGlobals.screen.blit(varGlobals.bgOrder, (0, 0))
#         mx, my = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 varGlobals.runDaftarMenu = False
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 click = True
#                 varGlobals.trueSound.play()

#         for button, rect in buttons.items():
#             if rect.collidepoint(mx, my):
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 7, border_radius=20)
#                 tts(button, cc.RED_BROWN, rect, varGlobals.screen, 40)
#                 if click:
#                     varGlobals.oldSurface = varGlobals.screen.copy()
#                     varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

#                     if button == "Paket Makan Minum":
#                         varGlobals.newSurface.blit(varGlobals.bgPaket1, (0, 0))
#                         transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
#                         paketMakanMinum()
#                     elif button == "Chinese Cuisine":
#                         varGlobals.newSurface.blit(varGlobals.bgChineseCusine, (0, 0))
#                         transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
#                         chineseCusine()
#                     elif button == "Javanese Cuisine":
#                         break
#                     elif button == "Paket Coffee Break":
#                         break
#             else:
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 4, border_radius=20)
#                 tts(button, cc.RED_BROWN, rect, varGlobals.screen, 35)

#         click = False
#         varGlobals.clock.tick(120)
#         pygame.display.flip()


###################################################################################################
#                                       PAKET MAKAN & MINUM                                       #
###################################################################################################

# def paketMakanMinum():

#     varGlobals.protein = False
#     varGlobals.sayuran = False

#     # BOOLEAN
#     varGlobals.runPID        = False
#     varGlobals.runEye        = False
#     varGlobals.runSim        = False
#     varGlobals.runMenu       = False
#     varGlobals.runStaff      = False
#     varGlobals.runConfig     = False
#     varGlobals.runPaketCB    = False
#     varGlobals.runPaketMM    = True
#     varGlobals.runChinese    = False
#     varGlobals.runJavanese   = False
#     varGlobals.runMakeOrder  = False
#     varGlobals.runDaftarMenu = False

#     buttons = {
#         "Back"       : packButton.EXIT,
#         "Protein"    : packButton.PROTEIN,
#         "Vegetables" : packButton.VEGETABLES
#     }

#     daging = {
#         "Ikan" : packButton.IKAN,
#         "Ayam" : packButton.AYAM,
#         "Sapi" : packButton.SAPI
#     }
#     nabati = {
#         "Sayur"  : packButton.SAYUR,
#         "Olahan" : packButton.OLAHAN
#     }

#     while varGlobals.paketMM:

#         varGlobals.screen.blit(varGlobals.bgPaket1, (0, 0))
#         mx, my = pygame.mouse.get_pos()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 varGlobals.runMenu = False
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 varGlobals.trueSound.play()

#                 if varGlobals.protein:
#                     if not packButton.BOX.collidepoint(mx, my):
#                         varGlobals.protein = False
#                     else:
#                         for button, rect in daging.items():
#                             if rect.collidepoint(mx, my):
#                                 varGlobals.pilihDaging = button

#                 elif varGlobals.sayuran:
#                     if not packButton.BOX.collidepoint(mx, my):
#                         varGlobals.sayuran = False
#                     else:
#                         for button, rect in nabati.items():
#                             if rect.collidepoint(mx, my):
#                                 varGlobals.pilihSayur = button

#                 else:
#                     for button, rect in buttons.items():
#                         if rect.collidepoint(mx, my):
#                             varGlobals.oldSurface = varGlobals.screen.copy()
#                             varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
#                             if button == "Protein":
#                                 varGlobals.protein = True
#                                 varGlobals.sayuran = False
#                             elif button == "Vegetables":
#                                 varGlobals.protein = False
#                                 varGlobals.sayuran = True
#                             elif button == "Back":
#                                 varGlobals.newSurface.blit(varGlobals.bgOrder, (0, 0))
#                                 transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
#                                 daftarMenu()

#         for button, rect in buttons.items():
#             if rect.collidepoint(mx, my):
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius=20)
#                 tts(button, cc.RED_BROWN, rect, varGlobals.screen, 40)
#             else:
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
#                 tts(button, cc.RED_BROWN, rect, varGlobals.screen, 35)

#         if varGlobals.protein:

#             boxPenghalang = pygame.Rect(0, 0, varGlobals.res[0], varGlobals.res[1])
#             overlay       = pygame.Surface((boxPenghalang.width, boxPenghalang.height), pygame.SRCALPHA)

#             pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
#             varGlobals.screen.blit(overlay, (0, 0))

#             pygame.draw.rect(varGlobals.screen, cc.WHITE, packButton.BOX, border_radius=20)
#             pygame.draw.rect(varGlobals.screen, cc.BLACK, packButton.BOX, 3, border_radius=20)
#             tts2("Select One", cc.BLACK, packButton.BOX, varGlobals.screen, 30)

#             for button, rect in daging.items():
#                 if rect.collidepoint(mx, my):
#                     pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                     pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 5, border_radius=20)
#                     tts(button, cc.BLACK, rect, varGlobals.screen, 35)
#                 else:
#                     pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                     pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 3, border_radius=20)
#                     tts(button, cc.BLACK, rect, varGlobals.screen, 30)

#         if varGlobals.sayuran:

#             boxPenghalang = pygame.Rect(0, 0, varGlobals.res[0], varGlobals.res[1])
#             overlay       = pygame.Surface((boxPenghalang.width, boxPenghalang.height), pygame.SRCALPHA)

#             pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
#             varGlobals.screen.blit(overlay, (0, 0))

#             pygame.draw.rect(varGlobals.screen, cc.WHITE, packButton.BOX, border_radius=20)
#             pygame.draw.rect(varGlobals.screen, cc.BLACK, packButton.BOX, 3, border_radius=20)
#             tts2("Select One", cc.BLACK, packButton.BOX, varGlobals.screen, 30)

#             for button, rect in nabati.items():
#                 if rect.collidepoint(mx, my):
#                     pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                     pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 5, border_radius=20)
#                     tts(button, cc.BLACK, rect, varGlobals.screen, 35)
#                 else:
#                     pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
#                     pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 3, border_radius=20)
#                     tts(button, cc.BLACK, rect, varGlobals.screen, 30)

#         varGlobals.clock.tick(120)
#         pygame.display.flip()


###################################################################################################
#                                           MAKE AN EYES                                          #
###################################################################################################

def eyeUI():

    # RESET
    wait                  = None
    endPos                = None
    startPos              = None
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # LOCAL VARIABLE
    smooth_offset_x    = 0
    smooth_offset_y    = 0
    distance           = 0
    isAngry            = False
    angryStartTime     = 0
    angryDuration      = 5
    angryCooldownUntil = 0

    # VARIABEL BARU UNTUK RANDOM EKSPRESI
    lastMouseActivityTime       = time.time()
    continuousActivityStartTime = None

    # BOOLEAN
    dragging                 = False
    varGlobals.list          = False
    varGlobals.diantar       = False
    varGlobals.isBlinking    = False
    varGlobals.updateOrder   = True
    varGlobals.mouseActive   = False
    varGlobals.newExpression = False

    varGlobals.runPID              = False
    varGlobals.runEye              = True
    varGlobals.runSim              = False
    varGlobals.runMenu             = False
    varGlobals.runStaff            = False
    varGlobals.runConfig           = False
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = False

    varGlobals.startTransisi   = time.time()
    varGlobals.startProperties = varGlobals.SET_AWAL.copy()
    varGlobals.targetPropertis = varGlobals.SET_AWAL.copy()

    while varGlobals.runEye:

        mouseMovedThisFrame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runEye = False
                pygame.quit()
                sys.exit()

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                lastMouseActivityTime = time.time()
                mouseMovedThisFrame = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                wait     = time.time()
                startPos = event.pos
                distance = 0

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if wait is not None:
                    adminSense = time.time() - wait

                    endPos   = event.pos
                    if startPos:
                        dx       = endPos[0] - startPos[0]
                        dy       = endPos[1] - startPos[1]
                        distance = (dx ** 2 + dy ** 2) ** 0.5

                        if adminSense > 5 and distance < 5:
                            mainMenu()

                if varGlobals.diantar:
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                    varGlobals.newSurface.blit(varGlobals.bgSatisfied, (0, 0))
                    satisfiedConfiguration()

                        # elif adminSense < 5:
                        #     varGlobals.oldSurface = varGlobals.screen.copy()
                        #     varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                        #     varGlobals.newSurface.blit(varGlobals.bgSatisfied, (0, 0))
                        #     satisfiedConfiguration()

                # elif dragging:
                #     if distance <= threshold or dy < -20:
                #         varGlobals.trueSound.play()
                #         varGlobals.oldSurface = varGlobals.screen.copy()
                #         varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                #         varGlobals.newSurface.blit(varGlobals.bgOrder, (0, 0))
                #         transition(varGlobals.oldSurface, varGlobals.newSurface, direction="up", speed=20)
                #         daftarMenu()

                wait     = None
                startPos = None
        
        currentTime = time.time()
        if mouseMovedThisFrame:
            if continuousActivityStartTime is None:
                continuousActivityStartTime = currentTime
        else:
            continuousActivityStartTime = None

        # UPDATE POSISI MENGIKUTI MOUSE
        mx, my = pygame.mouse.get_pos()
        center_x = varGlobals.res[0] // 2
        center_y = varGlobals.res[1] // 2
        max_offset = 30
        target_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 5))
        target_offset_y = max(-max_offset, min(max_offset, (my - center_y) / 5))

        smooth_offset_x = lerp(smooth_offset_x, target_offset_x, 0.1)
        smooth_offset_y = lerp(smooth_offset_y, target_offset_y, 0.1)

        # RANDOM BLINK
        if (continuousActivityStartTime is not None and 
            not isAngry and currentTime > angryCooldownUntil):
            
            activityDuration = currentTime - continuousActivityStartTime
            if activityDuration > 5:
                isAngry        = True
                angryStartTime = currentTime

        if isAngry:
            expression_key = 'marah'
            if currentTime - angryStartTime > angryDuration:
                isAngry = False
                angryCooldownUntil = currentTime + 5.0 

        elif varGlobals.isBlinking:
            expression_key = 'kedip'
        elif continuousActivityStartTime is not None:
            expression_key = 'senyum'
        elif currentTime - lastMouseActivityTime > 10:
            expression_key = 'sedih'
        else:
            expression_key = 'buka'

        new_expression = varGlobals.ANIMATIONS[expression_key].copy()

        if new_expression != varGlobals.targetPropertis:
            varGlobals.startProperties = varGlobals.SET_AWAL.copy()
            varGlobals.targetPropertis = new_expression.copy() 
            varGlobals.startTransisi = time.time()

        # MENGGUNAKAN RUMUS AGAR LEBIH HALUS
        elapsed = time.time() - varGlobals.startTransisi
        t       = min(elapsed / varGlobals.durasiTransisi, 1.0)
        tEased  = easeInOut(t)

        for key in varGlobals.targetPropertis:
            varGlobals.SET_AWAL[key] = lerp(
                varGlobals.startProperties.get(key, 0),
                varGlobals.targetPropertis.get(key, 0),
                tEased
            )

        varGlobals.screen.blit(varGlobals.bgEyes, (0, 0))

        tinggiMata   = int(varGlobals.SET_AWAL['eyeHeight'])
        base_offsetX = varGlobals.SET_AWAL['eyeOffsetX']
        base_offsetY = varGlobals.SET_AWAL['eyeOffsetY']

        eyeLeftX  = varGlobals.eyeLeftX + base_offsetX + smooth_offset_x
        eyeRightX = varGlobals.eyeRightX + base_offsetX + smooth_offset_x
        eyePosY   = varGlobals.eyePosY + base_offsetY + smooth_offset_y

        eyeLeft  = pygame.Rect(eyeLeftX, eyePosY, varGlobals.lebarMata, tinggiMata)
        eyeRight = pygame.Rect(eyeRightX, eyePosY, varGlobals.lebarMata, tinggiMata)

        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeLeft, border_radius=60)
        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeRight, border_radius=60)

        mouthY_val      = varGlobals.SET_AWAL.get('mouthY', 0)
        mouthWidth_val  = varGlobals.SET_AWAL.get('mouthWidth', 0)
        mouthHeight_val = varGlobals.SET_AWAL.get('mouthHeight', 0)
        mouthAngle_val  = varGlobals.SET_AWAL.get('mouthAngle', 0)

        # Gambar mulut jika propertinya tidak nol
        if mouthWidth_val > 0 and mouthHeight_val > 0:
            mouth_pos_y = varGlobals.res[1] // 2 + mouthY_val
            mouth_rect  = pygame.Rect(varGlobals.res[0] // 2 - (mouthWidth_val // 2), mouth_pos_y, mouthWidth_val, mouthHeight_val)
            
            if mouthAngle_val == 1:
                start_angle = math.pi
                end_angle   = 2 * math.pi
                pygame.draw.arc(varGlobals.screen, cc.BLACK, mouth_rect, start_angle, end_angle, 10)
            elif mouthAngle_val == 180:
                start_point = (mouth_rect.left, mouth_rect.centery)
                end_point   = (mouth_rect.right, mouth_rect.centery)
                pygame.draw.line(varGlobals.screen, cc.BLACK, start_point, end_point, 10)
            else:
                start_angle = 0
                end_angle   = math.pi
                pygame.draw.arc(varGlobals.screen, cc.BLACK, mouth_rect, start_angle, end_angle, 10)

        # pygame.draw.aaline(varGlobals.screen, cc.RED, (varGlobals.res[0] // 2, 0), (varGlobals.res[0] // 2, varGlobals.res[1]), 2)

        # MENGGAMBAR ALIS
        eyebrowOffset_leftY  = varGlobals.SET_AWAL['eyebrowOffset_leftY']
        eyebrowOffset_rightY = varGlobals.SET_AWAL['eyebrowOffset_rightY']
        eyebrowAngle_left    = varGlobals.SET_AWAL['eyebrowAngle_right']
        eyebrowAngle_right   = varGlobals.SET_AWAL['eyebrowAngle_left']
        
        eyebrow_start_left  = (varGlobals.eyeLeftX - 20, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
        eyebrow_end_left    = (varGlobals.eyeLeftX + varGlobals.lebarMata + 15, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
        eyebrow_start_right = (varGlobals.eyeRightX - 20, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)
        eyebrow_end_right   = (varGlobals.eyeRightX + varGlobals.lebarMata + 15, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)

        rotated_start_left = rotatePoint(eyebrow_start_left, eyeLeft.center, eyebrowAngle_left)
        rotated_end_left   = rotatePoint(eyebrow_end_left, eyeLeft.center, eyebrowAngle_left)
        pygame.draw.line(varGlobals.screen, cc.BLACK, rotated_start_left, rotated_end_left, 10)

        rotated_start_right = rotatePoint(eyebrow_start_right, eyeRight.center, eyebrowAngle_right)
        rotated_end_right   = rotatePoint(eyebrow_end_right, eyeRight.center, eyebrowAngle_right)
        pygame.draw.line(varGlobals.screen, cc.BLACK, rotated_start_right, rotated_end_right, 10)

        varGlobals.clock.tick(60)
        pygame.display.flip()


###################################################################################################
#                                       STAFF CONFIGURATION                                       #
###################################################################################################

def staffConfiguration():

    # RESET
    goBack                   = time.time()
    numpad                   = {}
    selectedMeja             = None
    varGlobals.selectedMeja1 = None
    varGlobals.selectedMeja2 = None
    
    # BOOLEAN
    tray1                    = False
    tray2                    = False
    trayMeja                 = False

    varGlobals.runPID              = False
    varGlobals.runEye              = False
    varGlobals.runSim              = False
    varGlobals.runMenu             = False
    varGlobals.runStaff            = True
    varGlobals.runConfig           = False
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = False
    
    while varGlobals.runStaff:

        varGlobals.screen.blit(varGlobals.bgStaff, (0, 0))

        buttons = {
            "Back"                  : scButton.EXIT,
            varGlobals.mejaPesanan1 : scButton.TRAY_1,
            varGlobals.mejaPesanan2 : scButton.TRAY_2
        }

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runStaff = False
                pygame.quit()
                sys.exit()

            for cb in varGlobals.checkboxes:
                cb.handleEvent(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    eyeUI()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                goBack = time.time()

                # NUMPAD DALAM MEMILIH MEJA
                if trayMeja:
                    if numpad:
                        for number, rect in numpad.items():
                            if rect.collidepoint(mx, my):
                                if number.isdigit():
                                    selectedMeja = int(number)
                                    
                                    # KODE YANG DIPINDAHKAN
                                    if tray1:
                                        varGlobals.mejaPesanan1  = f'Meja {selectedMeja}'
                                        varGlobals.selectedMeja1 = selectedMeja
                                        tray1                    = False
                                    elif tray2:
                                        varGlobals.mejaPesanan2  = f'Meja {selectedMeja}'
                                        varGlobals.selectedMeja2 = selectedMeja
                                        tray2                    = False
                                    
                                    trayMeja = False

                                    if varGlobals.selectedMeja1 and varGlobals.selectedMeja2:
                                        # data = bytearray(3)
                                        # data[0] = 100
                                        # data[1] = int(selectedMeja1)
                                        # data[2] = int(selectedMeja2)
                                        # send(data)

                                        varGlobals.runEye   = True
                                        varGlobals.runStaff = False
                                        return varGlobals.selectedMeja1, varGlobals.selectedMeja2
                                    
                                elif number == "Back":
                                    trayMeja = False
                
                # PENANGANAN TOMBOL TRAY
                else:
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                    for button, rect in buttons.items():
                        if rect.collidepoint(mx, my):
                            if button == varGlobals.mejaPesanan1:
                                trayMeja = True
                                tray1    = True
                                tray2    = False
                            elif button == varGlobals.mejaPesanan2:
                                trayMeja = True
                                tray2    = True
                                tray1    = False
                            elif button == "Back":
                                varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                                transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                                mainMenu()

        # if time.time() - goBack > 10:
        #     eyeUI()

        # MENGAMBIL DATA PESANAN (MEJA)
        listOrder              = getOrders()
        varGlobals.allMeja     = getMeja(listOrder)
        varGlobals.updateOrder = False

        # MENGGAMBAR OPSI TRAY (1 ATAU 2)
        for button, rect in buttons.items():
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
                pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 5, border_radius=20)
                tts(button, cc.BLACK, rect, varGlobals.screen, 35)
            else:
                pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
                pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 3, border_radius=20)
                tts(button, cc.BLACK, rect, varGlobals.screen, 30)

        # MENGGAMBAR NUMPAD UNTUK MEMILIH MEJA
        if trayMeja:
            boxPenghalang = pygame.Rect(0, 0, varGlobals.res[0], varGlobals.res[1])
            overlay = pygame.Surface((boxPenghalang.width, boxPenghalang.height), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
            varGlobals.screen.blit(overlay, (0, 0))

            pygame.draw.rect(varGlobals.screen, cc.WHITE, scButton.BOX_SETUP, border_radius=20)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, scButton.BOX_SETUP, 3, border_radius=20)

            numpad = numpadStaff(varGlobals.screen, varGlobals.popupX, varGlobals.popupY, 3)

            varGlobals.checkboxes = []

        pygame.display.flip()
        varGlobals.clock.tick(60)


###################################################################################################
#                                            MAKE ORDER                                           #
###################################################################################################

# def makeOrder():

#     # RESET
#     varGlobals.oldSurface = None
#     varGlobals.newSurface = None

#     # VARIABLE LOCAL
#     contentY   = 0
#     lastAction = time.time()

#     # SCROLL DENGAN DRAG MOUSE
#     scrolling    = False
#     last_mouse_y = 0

#     # BOOLEAN
#     click = False
#     varGlobals.list          = False
#     varGlobals.updateOrder   = True

#     varGlobals.runPID        = False
#     varGlobals.runEye        = False
#     varGlobals.runSim        = False
#     varGlobals.runMenu       = False
#     varGlobals.runStaff      = False
#     varGlobals.runConfig     = False
#     varGlobals.runPaketCB    = False
#     varGlobals.runPaketMM    = False
#     varGlobals.runChinese    = False
#     varGlobals.runJavanese   = False
#     varGlobals.runMakeOrder  = True
#     varGlobals.runDaftarMenu = False

#     buttons = {
#         "Back"       : moButton.BACK,
#         "List Order" : moButton.LIST_PESANAN
#     }

#     while varGlobals.runMakeOrder:
        
#         # DITAMBAHKAN: Reset perubahan posisi mouse setiap frame
#         mouse_dy = 0

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 varGlobals.runMenu = False
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 varGlobals.trueSound.play()
#                 lastAction = time.time()
#                 scrolling  = False
#                 click      = True
                
#             # --- LOGIKA SCROLLING ---
#             if varGlobals.list:
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if event.button == 4:
#                         contentY += 30
#                         lastAction = time.time()
#                     elif event.button == 5:
#                         contentY -= 30
#                         lastAction = time.time()
                
#                 # LOGIKA DRAG MOUSE
#                 popupRect = pygame.Rect(65, 110, 400, 460)
#                 if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     if popupRect.collidepoint(event.pos):
#                         scrolling    = True
#                         last_mouse_y = event.pos[1]

#                 if event.type == pygame.MOUSEMOTION and scrolling:
#                     current_mouse_y = event.pos[1]
#                     mouse_dy        = current_mouse_y - last_mouse_y
#                     last_mouse_y    = current_mouse_y

#         # CEK TIMEOUT
#         if time.time() - lastAction >= 15:
#             eyeUI()
#             lastAction = time.time()

#         if varGlobals.updateOrder:
#             listOrder              = getOrders()
#             varGlobals.allOrders   = tampilanOrder(listOrder)
#             varGlobals.updateOrder = False

#         varGlobals.screen.blit(varGlobals.bgMakeOrder, (0, 0))

#         # LOGIKA TOMBOL
#         mx, my = pygame.mouse.get_pos()
#         for button in buttons:
#             if buttons[button].collidepoint(mx, my):
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, buttons[button], border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 5, border_radius=20)
#                 tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 30)
#                 if click:
#                     pencetButton(button)
#                     varGlobals.oldSurface = varGlobals.screen.copy()
#                     varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
#                     if button == "List Order":
#                         varGlobals.list = not varGlobals.list
#                         varGlobals.updateOrder = True
#                     elif button == "Back":
#                         varGlobals.newSurface.blit(varGlobals.bgEyes, (0, 0))
#                         transition(varGlobals.oldSurface, varGlobals.newSurface, direction="down", speed=20)
#                         eyeUI()
#             else:
#                 pygame.draw.rect(varGlobals.screen, cc.WHITE, buttons[button], border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 3, border_radius=20)
#                 tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 20)

#         # MENAMBAHKAN DRAG MOUSE KE VARIABLE 'contentY'
#         contentY += mouse_dy
#         if varGlobals.list:
#             popupRect = pygame.Rect(65, 110, 400, 460)
#             pygame.draw.rect(varGlobals.screen, cc.WHITE, popupRect, border_radius=20)
#             pygame.draw.rect(varGlobals.screen, cc.BLACK, popupRect, 3, border_radius=20)
            
#             total_content_height = sum(group['height'] + 30 for group in varGlobals.allOrders)
#             maxScroll            = max(0, total_content_height - popupRect.height)
#             contentY             = max(-maxScroll, min(10, contentY))

#             clipping_rect = pygame.Rect(popupRect.x, popupRect.y + 10, popupRect.width, popupRect.height - 20)
#             varGlobals.screen.set_clip(clipping_rect)
            
#             currentY = 0
#             for group in varGlobals.allOrders:
#                 yPosOffset    = currentY + contentY + popupRect.y
#                 mejaLine      = group['lines'][0]
#                 xPos          = mejaLine['rect'].x - 45
#                 tinggiDinamis = group['height'] - 30
                
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, (xPos, yPosOffset, 380, tinggiDinamis), 3, border_radius=20)
#                 pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, (xPos, yPosOffset, 100, tinggiDinamis), border_radius=20)

#                 for line in group['lines']:
#                     line_rect = line['rect'].copy()
#                     line_rect.y += contentY
#                     varGlobals.screen.blit(line['surface'], line_rect)

#                 currentY += tinggiDinamis + 10
            
#             varGlobals.screen.set_clip(None)

#         click = False
#         varGlobals.clock.tick(60)
#         pygame.display.flip()


###################################################################################################
#                                            MAIN MENU                                            #
###################################################################################################

def mainMenu():

    # RESET
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # LOCAL VARIABLE
    popUp = False

    # BOOLEAN
    click                          = False
    varGlobals.runPID              = False
    varGlobals.runEye              = False
    varGlobals.runSim              = False
    varGlobals.runMenu             = True
    varGlobals.runStaff            = False
    varGlobals.runConfig           = False
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = False
    
    # BUTTON
    buttons = {
        "Run"           : mmButton.RUN,
        "Simulation"    : mmButton.SIMULATION,
        "Configuration" : mmButton.CONFIGURATION,
        "Exit"          : mmButton.EXIT,
    }

    pilihan = {
        "Configuration"       : mmButton.SOCKET,
        "PID Configuration"   : mmButton.PID,
        "Staff Configuration" : mmButton.STAFF
    }

    # STATUS
    status = {
        varGlobals.conServiceBot : mmButton.STATUS
    }

    while varGlobals.runMenu:

        varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

        boxPopUp = pygame.Rect(433, 308, 217, 203)

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                varGlobals.trueSound.play()
                click = True

                if not boxPopUp.collidepoint(mx, my):
                    popUp = False

        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 4, border_radius=20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 30)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 2, border_radius=20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 20)

        # === INTERAKSI TOMBOL UTAMA (hanya saat popup tidak aktif) ===
        if not popUp and click:
            for button in buttons:
                if buttons[button].collidepoint(mx, my):
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

                    if button == "Run":
                        varGlobals.newSurface.blit(varGlobals.bgEyes, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
                        runCom()
                        eyeUI()

                    elif button == "Simulation":
                        varGlobals.newSurface.blit(varGlobals.bgSim, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
                        runCom()
                        simulation()

                    elif button == "Configuration":
                        popUp = True

                    elif button == "Exit":
                        pygame.quit()
                        sys.exit()

        # === POPUP (jika aktif, hanya popup yang interaktif) ===
        if popUp:
            boxChoice = pygame.Rect(433, 307, 217, 203)
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxChoice, border_radius=20)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, boxChoice, 2, border_radius=20)

            for pilih, rect in pilihan.items():
                if rect.collidepoint(mx, my):
                    pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=15)
                    tts(pilih, cc.WHITE, rect, varGlobals.screen, 25)

                    if click:
                        if pilih == "Configuration":
                            varGlobals.newSurface.blit(varGlobals.bgSocketConfig, (0, 0))
                            transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
                            configuration()

                        elif pilih == "PID Configuration":
                            varGlobals.newSurface.blit(varGlobals.bgPidConfig, (0, 0))
                            transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
                            pidConfig()

                        elif pilih == "Staff Configuration":
                            varGlobals.newSurface.blit(varGlobals.bgStaff, (0, 0))
                            transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
                            staffConfiguration()

                        elif pilih == "Close":
                            popUp = False
                else:
                    pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=15)
                    tts(pilih, cc.WHITE, rect, varGlobals.screen, 20)

        # === STATUS (selalu ditampilkan non-interaktif) ===
        for text, rect in status.items():
            if varGlobals.conServiceBot == "Disconnected":
                pygame.draw.rect(varGlobals.screen, cc.RED, rect, border_radius=20)
                tts(text, cc.WHITE, rect, varGlobals.screen, 20)
            elif varGlobals.conServiceBot == "Connected":
                pygame.draw.rect(varGlobals.screen, cc.GREEN, rect, border_radius=20)
                tts(text, cc.WHITE, rect, varGlobals.screen, 20)

        click = False
        varGlobals.clock.tick(30)
        pygame.display.flip()


###################################################################################################
#                                            SIMULATION                                           #
###################################################################################################

def simulation():

    path_index = 0

    # MENGAMBIL DATA PESANAN (MEJA)
    listOrder              = getOrders()
    varGlobals.allMeja     = getMeja(listOrder)
    varGlobals.updateOrder = False

    # BOOLEAN
    click                          = False
    varGlobals.runPID              = False
    varGlobals.runEye              = False
    varGlobals.runSim              = True
    varGlobals.runMenu             = False
    varGlobals.runStaff            = False
    varGlobals.runConfig           = False
    varGlobals.runPaketCB          = False
    varGlobals.runPaketMM          = False
    varGlobals.runChinese          = False
    varGlobals.runJavanese         = False
    varGlobals.runMakeOrder        = False
    varGlobals.runDaftarMenu       = False
    varGlobals.runServiceSatisfied = False

    buttons = {
        "Back"   : simButton.BACK,
        "Meja 1" : simButton.DEMO_1,
        "Meja 2" : simButton.DEMO_2,
        "Meja 3" : simButton.DEMO_3,
        "Meja 4" : simButton.DEMO_4
    }

    # path = aStar((dataRobot.xpos // 25, dataRobot.ypos // 25), varGlobals.allMeja[6])

    # if path:
    #     print("Jalur ditemukan : ", path)
    # else:
    #     print("Path tidak ditemukan")
    
    while varGlobals.runSim:

        # if path and path_index < len(path):
        #     next_pos_grid = path[path_index]

        #     dataRobot.xpos = (next_pos_grid[1] * 50) - 25
        #     dataRobot.ypos = (next_pos_grid[0] * 50) - 25

        #     path_index += 1

        #     pygame.time.wait(500)

        varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

        infoRobot = [
            ("Compass   :   " + str(dataRobot.kompas), (500, 220)),
            ("X                :   " + str(dataRobot.ypos), (500, 240)),
            ("Y                :   " + str(dataRobot.xpos), (500, 260))
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runSim = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                varGlobals.trueSound.play()
                click = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    dataRobot.ypos += 50
                elif event.key == pygame.K_LEFT:
                    dataRobot.ypos -= 50
                elif event.key == pygame.K_UP:
                    dataRobot.xpos -= 50
                elif event.key == pygame.K_DOWN:
                    dataRobot.xpos += 50
                elif event.key == pygame.K_LSHIFT:
                    dataRobot.kompas += 20
                elif event.key == pygame.K_LCTRL:
                    dataRobot.kompas -= 20
            
            # PENANGANAN BOOLEAN (PRESS BUTTON)
            if event.type == pygame.KEYDOWN:
                if event.key in varGlobals.keys_pressed:
                    varGlobals.keys_pressed[event.key] = True
                    varGlobals.notAutonomus            = True
            elif event.type == pygame.KEYUP:
                if event.key in varGlobals.keys_pressed:
                    varGlobals.keys_pressed[event.key] = False
                    varGlobals.notAutonomus            = False

        # MENGIRIM DATA PRESS ARROW 
        data = bytearray(3)
        keys = pygame.key.get_pressed()
        for key in varGlobals.keys_pressed.keys():
            if keys[key]:
                if pygame.key.name(key) == "down":
                    data[0] = 99
                    data[1] = 55
                    data[2] = 90
                    send(data)
                    print(data[0], data[1])
                elif pygame.key.name(key) == "up":
                    data[0] = 99
                    data[1] = 56
                    data[2] = 90
                    send(data)
                    print(data[0], data[1])
                elif pygame.key.name(key) == "left":
                    data[0] = 99
                    data[1] = 57
                    data[2] = 90
                    send(data)
                    print(data[0], data[1])
                elif pygame.key.name(key) == "right":
                    data[0] = 99
                    data[1] = 58
                    data[2] = 90
                    send(data)
                    print(data[0], data[1])

        drawGrid(25)

        # # AMBIL DATA MEJA
        # for mejaData in varGlobals.allMeja:
        #     print(mejaData)
        #     grid_x, grid_y = mejaData[1]
            
        #     pixel_x = varGlobals.offsetX + (grid_x * 25)
        #     pixel_y = varGlobals.offsetY + (grid_y * 25)

        #     mejaRect = pygame.Rect(pixel_x - 25, pixel_y - 25, 25, 25)
        #     pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, mejaRect)
        #     tts(str(mejaData), cc.WHITE, mejaRect, varGlobals.screen, 25)

        # CONTOH SIMULASI
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (varGlobals.offsetX, 218), (varGlobals.offsetX, 518))
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (78, varGlobals.offsetY), (378, varGlobals.offsetY))
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (300 + varGlobals.offsetX, 218), (300 + varGlobals.offsetX, 317))
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (78, 300 + varGlobals.offsetY), (578, 300 + varGlobals.offsetY))
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (500 + varGlobals.offsetX, 318), (500 + varGlobals.offsetX, 518))
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (378, 100 + varGlobals.offsetY), (578, 100 + varGlobals.offsetY))

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 3, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 20)
                if click:
                    pencetButton(button)
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                    if button == "Back":
                        varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                        mainMenu()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 2, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 15)
                
        for text_line, pos in infoRobot:
            tts1(text_line, cc.BLACK, pygame.Rect(pos[0], pos[1], 10, 10), varGlobals.screen, 15)
        
        # ROTASI IMAGE
        Xbot = varGlobals.offsetX + (dataRobot.ypos * varGlobals.skala) - 1
        Ybot = varGlobals.offsetY + (dataRobot.xpos * varGlobals.skala) - 1
        rotatedImage(varGlobals.bot, Xbot, Ybot, dataRobot.kompas)
        rotatedImage(varGlobals.arrow, 446, 250, dataRobot.kompas)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)


###################################################################################################
#                                           PROGRAM MAIN                                          #
###################################################################################################

reset_database()
mainMenu()