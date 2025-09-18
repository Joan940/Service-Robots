import sys
import time
import math
import random
import pygame
import Modules.dataRobot as dataRobot
import Modules.varGlobals as varGlobals

from Modules.communication import (
    runCom,
    send
)
from Skills.demoMode import (
    demo1
)
from Modules.algorithm import (
    # getPesananByMeja,
    drawNumberPad,
    tampilanOrder,
    rotatedImage,
    rotatePoint,
    numpadStaff,
    transition,
    easeInOut,
    drawGrid,
    CheckBox,
    getMeja,
    # aStar,
    lerp,
)
from Modules.database import (
    reset_database,
    delete_orders,
    getOrders,
    addOrders
)
from Modules.colors import (
    custom as cc,
    tts,
    tts1,
    tts2
)
from Modules.varGlobals import (
    orderan as orderButton,
    main_menu as mmButton,
    simulasi as simButton,
    config as confButton,
    make_order as moButton,
    staffConfig as scButton,
    PID as pidButton
)


###################################################################################################
#                            VARIABLE GLOBAL YANG DIINISIALISASI DIAWAL                           #
###################################################################################################

pygame.mixer.init()

varGlobals.IP = '192.168.110.15'
varGlobals.PORT = '8081'
varGlobals.P = '0'
varGlobals.I = '0'
varGlobals.D = '0'


###################################################################################################
#                                          PRESS BUTTON                                           #
###################################################################################################

def pencetButton(text):

    # data = bytearray(3)

    # PAKSA HURUF KECIL
    text = text.lower()

    if text == "demo 1":
        demo1()

    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp_key, inputUser_rects, done_rect):

    if varGlobals.runPID:    
        while True:
            
            varGlobals.screen.blit(varGlobals.bgPidConfig, (0, 0))

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
                    if not inputUser_rects[inp_key].collidepoint(event.pos):
                        return

            pygame.display.flip()
            varGlobals.clock.tick(120)
        
    elif varGlobals.runConfig:
        while True:
            
            varGlobals.screen.blit(varGlobals.bgSocketConfig, (0, 0))

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
                    if not inputUser_rects[inp_key].collidepoint(event.pos):
                        return

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
    varGlobals.runPID = True
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False

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
                        data = bytearray(4)
                        
                        data[0] = 200
                        data[1] = int(varGlobals.P)
                        data[2] = int(varGlobals.I)
                        data[3] = int(varGlobals.D)
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
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = True
    varGlobals.runMakeOrder = False

    buttons = {
        "Save" : confButton.SAVE_RECT,
        "Back" : confButton.EXIT_RECT
    }
    
    inputUser = {
        "IP" : confButton.INP_IP_RECT,
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
#                                            ADD ORDER                                            #
###################################################################################################

def order():

    # RESET
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # MENYIMPAN BUTTON TAB ANGKA
    number_pad_buttons = {}

    # BOOLEAN
    click = False
    varGlobals.runPID = False
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = True
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False

    buttons = {
    }

    menu = {
        "Back": orderButton.EXIT,
        "Pizza": orderButton.MENU_1,
        "Burger": orderButton.MENU_2,
        "Tahu Gimbal": orderButton.MENU_3,
        "Spageti": orderButton.MENU_4,
        "Nasi Telur": orderButton.MENU_5
    }

    font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 17)

    while varGlobals.runOrder:

        varGlobals.screen.blit(varGlobals.bgOrder, (0, 0))
        mx, my = pygame.mouse.get_pos()
        
        # DEKLARASI POP UP
        popupPesanan = pygame.Rect(varGlobals.popupX, varGlobals.popupY, varGlobals.lebarPopup + 20, varGlobals.tinggiPopup)
        numPad = pygame.Rect(popupPesanan.width + 10, varGlobals.popupY, 450, varGlobals.tinggiPopup)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runOrder = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True
                varGlobals.trueSound.play()
                
                if varGlobals.pesanan:

                    # POP UP HILANG JIKA DIKLIK DI LUAR BUTTON
                    if not popupPesanan.collidepoint(mx, my) and not numPad.collidepoint(mx, my):
                        varGlobals.pesanan = None
                        varGlobals.input = None
                        varGlobals.nomorMeja = ""
                        varGlobals.jumlah = ""
                    else:

                        # LOGIKA POP UP
                        if boxNomorMeja.collidepoint(mx, my):
                            varGlobals.input = "table"
                        elif boxJumlah.collidepoint(mx, my):
                            varGlobals.input = "quantity"
                        elif boxConfirm.collidepoint(mx, my):
                            if varGlobals.nomorMeja and varGlobals.jumlah:
                                addOrders(varGlobals.nomorMeja, varGlobals.antrian, varGlobals.pesanan, varGlobals.jumlah)
                                
                                # RESET
                                varGlobals.pesanan = None
                                varGlobals.nomorMeja = ""
                                varGlobals.jumlah = ""
                                varGlobals.antrian += 1
                                varGlobals.input = None

                                # RESET NUMPAD
                                number_pad_buttons = {}
                            else:
                                print("Nomor meja dan jumlah harus diisi!")
                                varGlobals.falseSound.play()

                        # LOGIKA NUMPAD
                        if number_pad_buttons:
                            for number, rect in number_pad_buttons.items():
                                if rect.collidepoint(mx, my):
                                    if number.isdigit():
                                        if varGlobals.input == "table":
                                            varGlobals.nomorMeja += number
                                        elif varGlobals.input == "quantity":
                                            varGlobals.jumlah += number
                                    elif number == "Del":
                                        if varGlobals.input == "table":
                                            varGlobals.nomorMeja = varGlobals.nomorMeja[:-1]
                                        elif varGlobals.input == "quantity":
                                            varGlobals.jumlah = varGlobals.jumlah[:-1]
                                    elif number == "Clear":
                                        if varGlobals.input == "table":
                                            varGlobals.nomorMeja = ""
                                        elif varGlobals.input == "quantity":
                                            varGlobals.jumlah = ""

                else:
                    for menu_item, rect in menu.items():
                        if rect.collidepoint(mx, my):
                            varGlobals.oldSurface = varGlobals.screen.copy()
                            varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

                            if menu_item == "Back":
                                varGlobals.newSurface.blit(varGlobals.bgMakeOrder, (0, 0))
                                transition(varGlobals.oldSurface, varGlobals.newSurface, direction="down", speed=20)
                                makeOrder()
                            else:
                                varGlobals.pesanan = menu_item
                                varGlobals.input = "table"
                                varGlobals.nomorMeja = ""
                                varGlobals.jumlah = ""

                    for button_name in buttons:
                        if buttons[button_name].collidepoint(mx, my):
                            pencetButton(button_name)

            if event.type == pygame.KEYDOWN and varGlobals.pesanan:
                if varGlobals.input == "table":
                    if event.unicode.isnumeric():
                        varGlobals.nomorMeja += event.unicode
                    elif event.key == pygame.K_BACKSPACE and varGlobals.nomorMeja:
                        varGlobals.nomorMeja = varGlobals.nomorMeja[:-1]
                    elif event.key == pygame.K_RETURN:
                        if varGlobals.nomorMeja:
                            varGlobals.input = "quantity"
                        else:
                            print("Nomor meja tidak boleh kosong.")
                            varGlobals.falseSound.play()

                elif varGlobals.input == "quantity":
                    if event.unicode.isnumeric():
                        varGlobals.jumlah += event.unicode
                    elif event.key == pygame.K_BACKSPACE and varGlobals.jumlah:
                        varGlobals.jumlah = varGlobals.jumlah[:-1]
                    elif event.key == pygame.K_RETURN:
                        if varGlobals.nomorMeja and varGlobals.jumlah:
                            addOrders(varGlobals.nomorMeja, varGlobals.antrian, varGlobals.pesanan, varGlobals.jumlah)
                            
                            # RESET
                            varGlobals.pesanan = None
                            varGlobals.nomorMeja = ""
                            varGlobals.jumlah = ""
                            varGlobals.antrian += 1
                            varGlobals.input = None
                        else:
                            print("Nomor meja dan jumlah harus diisi!")
                            varGlobals.falseSound.play()

        # # LOGIKA TOMBOL
        # for button_name, rect in buttons.items():
        #     if rect.collidepoint(mx, my) and not varGlobals.pesanan:
        #         pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius=20)
        #         tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 30)

        #         # if click:
        #         #     pencetButton(button_name)
                    
        #         #     # MEMBUAT TRANSISI WINDOW
        #         #     varGlobals.oldSurface = varGlobals.screen.copy()
        #         #     varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

        #         #     if button_name == "Back":
        #         #         varGlobals.newSurface.blit(varGlobals.bgMakeOrder, (0, 0))
        #         #         transition(varGlobals.oldSurface, varGlobals.newSurface, direction="down", speed=20)
        #         #         makeOrder()
        #     else:
        #         pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
        #         tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 20)
        
        for menu_item, rect in menu.items():
            if rect.collidepoint(mx, my) and not varGlobals.pesanan:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(menu_item, cc.WHITE, rect, varGlobals.screen, 30)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(menu_item, cc.WHITE, rect, varGlobals.screen, 25)

        # JENDELA TAMBAHAN MUNCUL KETIKA MEMESAN
        if varGlobals.pesanan:

            boxNomorMeja = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 61, varGlobals.lebarPopup - 2 * 10, 50)
            boxJumlah = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 116, varGlobals.lebarPopup - 2 * 10, 50)
            boxConfirm = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 171, varGlobals.lebarPopup - 2 * 10, 50)
            
            boxPenghalang = pygame.Rect(0, 0, varGlobals.res[0], varGlobals.res[1])
            overlay = pygame.Surface((boxPenghalang.width, boxPenghalang.height), pygame.SRCALPHA)

            pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
            varGlobals.screen.blit(overlay, (0, 0))

            # MENGGAMBAR KOTAK POP UP BESAR
            kotakPopup = pygame.Rect(varGlobals.popupX, varGlobals.popupY, varGlobals.lebarPopup, varGlobals.tinggiPopup)
            pygame.draw.rect(varGlobals.screen, cc.WHITE, kotakPopup, border_radius=15)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, kotakPopup, 2, border_radius=15)

            # KOTAK INPUT UNTUK NOMOR MEJA DAN JUMLAH PESANAN
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxNomorMeja, border_radius=8)
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxJumlah, border_radius=8)

            # KOTAK KONFIRMASI
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxConfirm, border_radius=8)
            if boxConfirm.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, boxConfirm, border_radius=25)
                tts("Done", cc.WHITE, boxConfirm, varGlobals.screen, 17)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, boxConfirm, border_radius=8)
                tts("Done", cc.WHITE, boxConfirm, varGlobals.screen, 17)

            # HIGHLIGHT BOX
            if varGlobals.input == "table":
                pygame.draw.rect(varGlobals.screen, cc.BLACK, boxNomorMeja, 2, border_radius=8)
            elif varGlobals.input == "quantity":
                pygame.draw.rect(varGlobals.screen, cc.BLACK, boxJumlah, 2, border_radius=8)
            elif varGlobals.input == "confirm":
                pygame.draw.rect(varGlobals.screen, cc.BLACK, boxConfirm, 2, border_radius=8)
            
            # JUDUL UNTUK KOTAK POP UP BESAR
            textJudul = varGlobals.font.render(f"Order {varGlobals.pesanan}", True, cc.BLACK)
            textPos = textJudul.get_rect(centerx = kotakPopup.centerx, top = varGlobals.popupY + 10)
            varGlobals.screen.blit(textJudul, textPos)

            # TEXT PADA INPUTAN DAN WARNANYA
            textMeja = f"Meja     :   {varGlobals.nomorMeja}"
            textJumlah = f"Jumlah  :   {varGlobals.jumlah}"
            ccMeja = font.render(textMeja, True, cc.BLACK)
            ccJumlah = font.render(textJumlah, True, cc.BLACK)

            varGlobals.screen.blit(ccMeja, (boxNomorMeja.x + 10, boxNomorMeja.y + 13))
            varGlobals.screen.blit(ccJumlah, (boxJumlah.x + 10, boxJumlah.y + 13))

            number_pad_buttons = drawNumberPad(varGlobals.screen, varGlobals.popupX, varGlobals.popupY, 2)

        click = False
        varGlobals.clock.tick(120)
        pygame.display.flip()


###################################################################################################
#                                           MAKE AN EYES                                          #
###################################################################################################

def eyeUI():

    # RESET
    wait = None
    endPos = None
    startPos = None
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # LOCAL VARIABLE
    blink_interval = random.uniform(3, 6)
    blinkDuration = 0.5
    blinkStartTime = 0

    # VARIABEL BARU UNTUK RANDOM EKSPRESI
    lastExpressionTime = time.time()
    expressionInterval = random.uniform(5, 10)

    varGlobals.isLookingRight = False
    varGlobals.isLookingLeft = False

    newExpressTime = 0
    threshold = 10
    distance = 0
    duration = 5

    lastBlinkTime = time.time()
    new_expression = varGlobals.ANIMATIONS['buka'].copy()

    # BOOLEAN
    dragging = False
    varGlobals.list = False
    varGlobals.runEye = True
    varGlobals.runPID = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.isBlinking = False
    varGlobals.updateOrder = True
    varGlobals.mouseActive = False
    varGlobals.runMakeOrder = False
    varGlobals.newExpression = False

    varGlobals.startTransisi = time.time()
    varGlobals.startProperties = varGlobals.SET_AWAL.copy()
    varGlobals.targetPropertis = varGlobals.SET_AWAL.copy()

    while varGlobals.runEye:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runEye = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                wait = time.time()
                startPos = event.pos
                distance = 0

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                adminSense = time.time() - wait

                endPos = event.pos
                dx = endPos[0] - startPos[0]
                dy = endPos[1] - startPos[1]
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if adminSense > 5 and distance < 5:
                    staffConfiguration()

                elif dragging:
                    print(distance)
                    if distance <= threshold or dy < -20:
                        varGlobals.trueSound.play()
                        varGlobals.oldSurface = varGlobals.screen.copy()
                        varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                        varGlobals.newSurface.blit(varGlobals.bgMakeOrder, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="up", speed=20)
                        order()

                dragging = False

        # UPDATE POSISI MENGIKUTI MOUSE
        mx, my = pygame.mouse.get_pos()
        center_x = varGlobals.res[0] // 2
        center_y = varGlobals.res[1] // 2
        max_offset = 30

        mouse_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 5))
        mouse_offsetY = max(-max_offset, min(max_offset, (my - center_y) / 5))

        new_expression['eyeOffsetX'] = mouse_offset_x
        new_expression['eyeOffsetY'] = mouse_offsetY

        varGlobals.targetPropertis['eyeOffsetX'] = mouse_offset_x
        varGlobals.targetPropertis['eyeOffsetY'] = mouse_offsetY

        # RANDOM BLINK
        if time.time() - lastBlinkTime > blink_interval and not varGlobals.isBlinking:
            varGlobals.isBlinking = True
            blinkStartTime = time.time()
            new_expression = varGlobals.ANIMATIONS['kedip'].copy()
            
            lastBlinkTime = time.time()
            blink_interval = random.uniform(3, 6)

        if varGlobals.isBlinking and time.time() - blinkStartTime > blinkDuration:
            varGlobals.isBlinking = False
            new_expression = varGlobals.ANIMATIONS['buka'].copy()

        # RANDOM EKSPRESI SETIAP BEBERAPA DETIK
        if time.time() - lastExpressionTime > expressionInterval:
            pilihan = random.choice(['terkejut', 'sedih', 'marah'])
            new_expression = varGlobals.ANIMATIONS[pilihan].copy()

            lastExpressionTime = time.time()
            expressionInterval = random.uniform(5, 10)

        # RESET KE NORMAL SETELAH DURASI
        if varGlobals.newExpression and time.time() - newExpressTime > duration:
            varGlobals.newExpression = False
            new_expression = varGlobals.ANIMATIONS['buka'].copy()

        # UPDATE KE EKSPRESI BARU
        if new_expression != varGlobals.targetPropertis:
            varGlobals.startProperties = varGlobals.SET_AWAL.copy()
            varGlobals.targetPropertis = new_expression.copy()
            varGlobals.startTransisi = time.time()

        # MENGGUNAKAN RUMUS AGAR LEBIH HALUS
        elapsed = time.time() - varGlobals.startTransisi
        t = min(elapsed / varGlobals.durasiTransisi, 1.0)
        tEased = easeInOut(t)

        for key in varGlobals.targetPropertis:
            varGlobals.SET_AWAL[key] = lerp(
                varGlobals.startProperties.get(key, 0),
                varGlobals.targetPropertis[key],
                tEased
            )

        varGlobals.screen.blit(varGlobals.bgEyes, (0, 0))

        # UPDATE PROPERTI
        tinggiMata = int(varGlobals.SET_AWAL['eyeHeight'])
        eyeOffsetX_val = varGlobals.SET_AWAL['eyeOffsetX']
        eyeOffsetY_val = varGlobals.SET_AWAL['eyeOffsetY']
        
        eyeLeftX = varGlobals.eyeLeftX + eyeOffsetX_val
        eyeRightX = varGlobals.eyeRightX + eyeOffsetX_val
        eyePosY = varGlobals.eyePosY + eyeOffsetY_val

        eyeLeft = pygame.Rect(eyeLeftX, eyePosY, varGlobals.lebarMata, tinggiMata)
        eyeRight = pygame.Rect(eyeRightX, eyePosY, varGlobals.lebarMata, tinggiMata)

        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeLeft, border_radius=60)
        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeRight, border_radius=60)

        mouthY_val = varGlobals.SET_AWAL.get('mouthY', 0)
        mouthWidth_val = varGlobals.SET_AWAL.get('mouthWidth', 0)
        mouthHeight_val = varGlobals.SET_AWAL.get('mouthHeight', 0)
        mouthAngle_val = varGlobals.SET_AWAL.get('mouthAngle', 0)

        # Gambar mulut jika propertinya tidak nol
        if mouthWidth_val > 0 and mouthHeight_val > 0:
            mouth_pos_y = varGlobals.res[1] // 2 + mouthY_val
            mouth_rect = pygame.Rect(varGlobals.res[0] // 2 - (mouthWidth_val // 2), mouth_pos_y, mouthWidth_val, mouthHeight_val)
            
            if mouthAngle_val == 0:
                start_angle = 3.14 * 0.01
                end_angle = 0
            elif mouthAngle_val == 1:
                start_angle = 3.14
                end_angle = 0
            else:
                start_angle = 0
                end_angle = math.pi
                
            pygame.draw.arc(varGlobals.screen, cc.BLACK, mouth_rect, start_angle, end_angle, 10)

        # pygame.draw.aaline(varGlobals.screen, cc.RED, (varGlobals.res[0] // 2, 0), (varGlobals.res[0] // 2, varGlobals.res[1]), 2)

        # MENGGAMBAR ALIS
        eyebrowOffset_leftY = varGlobals.SET_AWAL['eyebrowOffset_leftY']
        eyebrowOffset_rightY = varGlobals.SET_AWAL['eyebrowOffset_rightY']
        eyebrowAngle_left = varGlobals.SET_AWAL['eyebrowAngle_right']
        eyebrowAngle_right = varGlobals.SET_AWAL['eyebrowAngle_left']
        
        eyebrow_start_left = (varGlobals.eyeLeftX - 20, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
        eyebrow_end_left = (varGlobals.eyeLeftX + varGlobals.lebarMata + 15, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
        eyebrow_start_right = (varGlobals.eyeRightX - 20, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)
        eyebrow_end_right = (varGlobals.eyeRightX + varGlobals.lebarMata + 15, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)

        rotated_start_left = rotatePoint(eyebrow_start_left, eyeLeft.center, eyebrowAngle_left)
        rotated_end_left = rotatePoint(eyebrow_end_left, eyeLeft.center, eyebrowAngle_left)
        pygame.draw.line(varGlobals.screen, cc.BLACK, rotated_start_left, rotated_end_left, 10)

        rotated_start_right = rotatePoint(eyebrow_start_right, eyeRight.center, eyebrowAngle_right)
        rotated_end_right = rotatePoint(eyebrow_end_right, eyeRight.center, eyebrowAngle_right)
        pygame.draw.line(varGlobals.screen, cc.BLACK, rotated_start_right, rotated_end_right, 10)

        varGlobals.clock.tick(60)
        pygame.display.flip()


###################################################################################################
#                                       STAFF CONFIGURATION                                       #
###################################################################################################

def staffConfiguration():

    # RESET
    goBack = time.time()
    numpad = {}
    selectedMeja = None
    selectedMeja1 = None
    selectedMeja2 = None
    
    # BOOLEAN
    tray1 = False
    tray2 = False
    trayMeja = False
    varGlobals.runPID = False
    varGlobals.runSim = False
    varGlobals.runEye = False
    varGlobals.runStaff = True
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False
    
    while varGlobals.runStaff:

        varGlobals.screen.blit(varGlobals.bgStaff, (0, 0))

        buttons = {
            "Back": scButton.EXIT,
            varGlobals.mejaPesanan1: scButton.TRAY_1,
            varGlobals.mejaPesanan2: scButton.TRAY_2
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
                                        varGlobals.mejaPesanan1 = f'Meja {selectedMeja}'
                                        selectedMeja1 = selectedMeja
                                        tray1 = False
                                    elif tray2:
                                        varGlobals.mejaPesanan2 = f'Meja {selectedMeja}'
                                        selectedMeja2 = selectedMeja
                                        tray2 = False
                                    
                                    trayMeja = False

                                    if selectedMeja1 and selectedMeja2:
                                        varGlobals.runEye = True

                                        data = bytearray(3)
                                        data[0] = 100
                                        data[1] = int(selectedMeja1)
                                        data[2] = int(selectedMeja2)
                                        send(data)
                                    
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
                                tray1 = True
                                tray2 = False
                            elif button == varGlobals.mejaPesanan2:
                                trayMeja = True
                                tray2 = True
                                tray1 = False
                            elif button == "Back":
                                varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                                transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                                mainMenu()

        # if time.time() - goBack > 10:
        #     eyeUI()

        # MENGAMBIL DATA PESANAN (MEJA)
        listOrder = getOrders()
        varGlobals.allMeja = getMeja(listOrder)
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

def makeOrder():

    # RESET
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # VARIABLE LOCAL
    contentY = 0
    duration = 10
    lastAction = time.time()

    # BOOLEAN
    click = False
    varGlobals.list = False
    varGlobals.runPID = False
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.updateOrder = True
    varGlobals.runMakeOrder = True

    buttons = {
        "Back": moButton.BACK,
        "List Order": moButton.LIST_PESANAN
    }

    while varGlobals.runMakeOrder:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                varGlobals.trueSound.play()
                click = True
                lastAction = time.time()
                
            # LOGIKA SCROLLING MENGGUNAKAN RODA MOUSE
            # Button 4 = Roda mouse ke atas, Button 5 = Roda mouse ke bawah
            if varGlobals.list and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  
                    contentY += 30
                    lastAction = time.time()
                elif event.button == 5: 
                    contentY -= 30
                    lastAction = time.time()

        # CEK TIMEOUT
        if time.time() - lastAction >= duration:
            eyeUI() 
            lastAction = time.time()

        if varGlobals.updateOrder:
            listOrder = getOrders()
            varGlobals.allOrders = tampilanOrder(listOrder)
            varGlobals.updateOrder = False

        varGlobals.screen.blit(varGlobals.bgMakeOrder, (0, 0))

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 5, border_radius=20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 30)
                if click:
                    pencetButton(button)

                    # MEMBUAT TRANSISI WINDOW
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                
                    if button == "List Order":
                        varGlobals.list = not varGlobals.list
                        varGlobals.updateOrder = True
                    elif button == "Back":
                        varGlobals.newSurface.blit(varGlobals.bgEyes, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="down", speed=20)
                        eyeUI()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 3, border_radius=20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 20)
                if click and varGlobals.list:
                    varGlobals.list = False

        if varGlobals.list:
            
            # MENGGAMBAR JENDELA POP UP
            popupRect = pygame.Rect(65, 110, 400, 460)
            pygame.draw.rect(varGlobals.screen, cc.WHITE, popupRect, border_radius=20)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, popupRect, 3, border_radius=20)

            # MENGHITUNG TINGGI CONTENT
            total_content_height = sum(group['height'] + 30 for group in varGlobals.allOrders)
            
            # BATAS SCROLLING
            maxScroll = max(0, total_content_height - popupRect.height)
            contentY = max(-maxScroll, min(10, contentY))

            # Buat area gambar yang dipotong agar konten hanya terlihat di dalam pop-up
            clipping_rect = pygame.Rect(popupRect.x, popupRect.y + 10, popupRect.width, popupRect.height - 20)
            varGlobals.screen.set_clip(clipping_rect)
            
            # Menggambar semua orderan dengan offset Y
            currentY = 0
            for group in varGlobals.allOrders:
                # OFFSET SCROLLING PADA POSISI Y
                yPosOffset = currentY + contentY + popupRect.y

                # Mendapatkan posisi x dari elemen pertama
                mejaLine = group['lines'][0]
                xPos = mejaLine['rect'].x - 45

                tinggiDinamis = group['height'] - 30
                
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, (xPos, yPosOffset, 380, tinggiDinamis), 3, border_radius=20)
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, (xPos, yPosOffset, 100, tinggiDinamis), border_radius=20)

                for line in group['lines']:
                    # RESET POSISI Y
                    line_rect = line['rect'].copy()
                    line_rect.y += contentY
                    varGlobals.screen.blit(line['surface'], line_rect)

                # BATAS ANTARA GROUP
                currentY += tinggiDinamis + 10
            
            # HAPUS CLIPPING
            varGlobals.screen.set_clip(None)

        click = False
        varGlobals.clock.tick(60)
        pygame.display.flip()


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
    click = False
    varGlobals.runPID = False
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = True
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False
    
    # BUTTON
    buttons = {
        "Run" : mmButton.RUN,
        "Simulation" : mmButton.SIMULATION,
        "Configuration" : mmButton.CONFIGURATION,
        "Exit" : mmButton.EXIT,
    }

    pilihan = {
        "Configuration" : mmButton.SOCKET,
        "PID Configuration" : mmButton.PID
    }

    # STATUS
    status = {
        varGlobals.conServiceBot : mmButton.STATUS
    }

    while varGlobals.runMenu:

        varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

        boxPopUp = pygame.Rect(433, 340, 217, 138)

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
                        runCom()
                        popUp = True

                    elif button == "Exit":
                        pygame.quit()
                        sys.exit()

        # === POPUP (jika aktif, hanya popup yang interaktif) ===
        if popUp:
            boxChoice = pygame.Rect(433, 340, 217, 138)
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
    listOrder = getOrders()
    varGlobals.allMeja = getMeja(listOrder)
    varGlobals.updateOrder = False

    # BOOLEAN
    click = False
    varGlobals.runSim = True
    varGlobals.runPID = False
    varGlobals.runEye = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False

    buttons = {
        "Back" : simButton.BACK,
        "Demo 1" : simButton.DEMO_1
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
                    varGlobals.notAutonomus = True
            elif event.type == pygame.KEYUP:
                if event.key in varGlobals.keys_pressed:
                    varGlobals.keys_pressed[event.key] = False
                    varGlobals.notAutonomus = False

        # MENGIRIM DATA PRESS ARROW 
        data = bytearray(2)
        keys = pygame.key.get_pressed()
        for key in varGlobals.keys_pressed.keys():
            if keys[key]:
                if pygame.key.name(key) == "down":
                    data[0] = 99
                    data[1] = 55
                    send(data)
                    print(data[0], data[1])
                elif pygame.key.name(key) == "up":
                    data[0] = 99
                    data[1] = 56
                    send(data)
                    print(data[0], data[1])
                elif pygame.key.name(key) == "left":
                    data[0] = 99
                    data[1] = 57
                    send(data)
                    print(data[0], data[1])
                elif pygame.key.name(key) == "right":
                    data[0] = 99
                    data[1] = 58
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

# reset_database()
mainMenu()