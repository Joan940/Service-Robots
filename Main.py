import sys
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
    rotatedImage
)
from Modules.database import (
    addOrders,
    getOrders
)
from Modules.colors import (
    custom as cc,
    tts
)


###################################################################################################
#                            VARIABLE GLOBAL YANG DIINISIALISASI DIAWAL                           #
###################################################################################################

varGlobals.IP = '127.0.0.1'
varGlobals.PORT = '8081'
order_list = []


###################################################################################################
#                                          PRESS BUTTON                                           #
###################################################################################################

def pencetButton(text):

    data = bytearray(3)

    # PAKSA HURUF KECIL
    text = text.lower()
    if text == "run":
        runCom()
        simulation()

    elif text == "configuration":
        print("configuration")
        configuration()

    elif text == "save":
        print("save")
        runCom()
        mainMenu()

    elif text == "back":
        mainMenu()
        # sys.exit(0)

    elif text == "demo 1":
        demo1()

    elif text == "add order":
        order()

    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp_key, inputUser_rects):

    while True:
        
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, inputUser_rects['Save'], 3, border_radius=20)
        tts("Save", cc.RED_BROWN, inputUser_rects['Save'], varGlobals.screen, 50)
       
        for key, rect in inputUser_rects.items():
            if key in ["IP", "PORT"]:
                current_value = ""
                if key == "IP":
                    current_value = varGlobals.IP
                elif key == "PORT":
                    current_value = varGlobals.PORT
                
                if key == inp_key:
                    pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius = 20)
                    tts(current_value, cc.WHITE, rect, varGlobals.screen, 60)
                else:
                    pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                    tts(current_value, cc.RED_BROWN, rect, varGlobals.screen, 50)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if inp_key == "IP":
                        varGlobals.IP = varGlobals.IP[:-1]
                    elif inp_key == "PORT":
                        varGlobals.PORT = varGlobals.PORT[:-1]
                elif event.key == pygame.K_RETURN:
                    return
                else:
                    if inp_key == "IP":
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

def configuration():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = True

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)

    # SET UP POSISI TEXT & UKURAN BUTTON
    PANJANG_BUTTON = varGlobals.res[0] * 0.094
    LEBAR_BUTTON = varGlobals.res[1] * 0.06
    PANJANG_INP_BUTTON = varGlobals.res[0] * 0.1
    LEBAR_INP_BUTTON = varGlobals.res[1] * 0.06

    # POSISI BUTTON
    SAVE_RECT = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_BUTTON * (-1.42)),
        window_rect.centery - LEBAR_BUTTON * (-5),
        PANJANG_BUTTON * 2,
        LEBAR_BUTTON * 1.7
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

    inputUser = {
        "Save" : SAVE_RECT,
        "IP" : INP_IP_RECT,
        "PORT" : INP_PORT_RECT
    }

    while varGlobals.runConfig:
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runConfig = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        mx, my = pygame.mouse.get_pos()

        for key, rect in inputUser.items():
            display_text = key
            if key == "IP":
                display_text = varGlobals.IP
            elif key == "PORT":
                display_text = varGlobals.PORT
            
            if rect.collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 60)
                if click:
                    if key in ["IP", "PORT"]:
                        fillText(key, inputUser)
                    elif key == "Save":
                        pencetButton(key)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 50)

        click = False
        varGlobals.clock.tick(120)
        pygame.display.flip()


###################################################################################################
#                                            ADD ORDER                                            #
###################################################################################################

def order():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = True
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)

    # POSISI TOMBOL
    EXIT = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-0.8)),
        window_rect.centery - (varGlobals.LEBAR_BUTTON * (-2.2)),
        varGlobals.PANJANG_BUTTON * 3,
        varGlobals.LEBAR_BUTTON * 1.7
    )
    PIZZA = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * 4.3),
        window_rect.centery - (varGlobals.LEBAR_BUTTON * 3),
        varGlobals.PANJANG_BUTTON,
        varGlobals.LEBAR_BUTTON
    )
    BURGER = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * 4.3),
        window_rect.centery - (varGlobals.LEBAR_BUTTON * 1.8),
        varGlobals.PANJANG_BUTTON,
        varGlobals.LEBAR_BUTTON
    )

    buttons = {
        "Exit": EXIT
    }

    menu = {
        "Pizza": PIZZA,
        "Burger": BURGER
    }

    while varGlobals.runOrder:

        varGlobals.screen.blit(varGlobals.bgOrder, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runOrder = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True
                mx, my = pygame.mouse.get_pos()

                for button_name in buttons:
                    if buttons[button_name].collidepoint(mx, my):
                        pencetButton(button_name)
                
                for menu_item, rect in menu.items():
                    if rect.collidepoint(mx, my):

                        # INISIALISASI AWAL
                        varGlobals.pesanan = menu_item
                        varGlobals.input = "table"
                        varGlobals.nomorMeja = ""
                        varGlobals.jumlah = ""

                        varGlobals.popupX = rect.right + 20
                        varGlobals.popupY = rect.centery - (varGlobals.tinggiPopup // 2)

                        if varGlobals.popupX + varGlobals.lebarPopup > varGlobals.screen_width:
                            varGlobals.popupX = rect.left - varGlobals.lebarPopup - 20
                        if varGlobals.popupY < 0:
                            varGlobals.popupY = 0
                        if varGlobals.popupY + varGlobals.tinggiPopup > varGlobals.screen_height:
                            varGlobals.popupY = varGlobals.screen_height - varGlobals.tinggiPopup
                        
                        varGlobals.input = "table"

                if varGlobals.pesanan:
                    boxNomorMeja = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 60, varGlobals.lebarPopup - 2 * 10, 50)
                    boxJumlah = pygame.Rect(varGlobals.popupX + 10, varGlobals.popupY + 110, varGlobals.lebarPopup - 2 * 10, 50)
                    boxConfirm = pygame.Rect(varGlobals.popupX + 320, varGlobals.popupY + 10, varGlobals.lebarPopup - 295, 40)
                    
                    if boxNomorMeja.collidepoint(mx, my):
                        varGlobals.input = "table"
                    elif boxJumlah.collidepoint(mx, my):
                        varGlobals.input = "quantity"
                    elif boxConfirm.collidepoint(mx, my):
                        varGlobals.input = "confirm"
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
                    else:
                        pass

            if event.type == pygame.KEYDOWN:
                if varGlobals.pesanan:
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

        # LOGIKA TOMBOL
        for button_name, rect in buttons.items():
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius=20)
                tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 60)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
                tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 50)

        for menu_item, rect in menu.items():
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(menu_item, cc.WHITE, rect, varGlobals.screen, 40)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(menu_item, cc.WHITE, rect, varGlobals.screen, 30)

        # JENDELA TAMBAHAN MUNCUL KETIKA MEMESAN
        if varGlobals.pesanan:

            # MENGGAMBAR KOTAK POP UP BESAR
            kotakPopup = pygame.Rect(varGlobals.popupX, varGlobals.popupY, varGlobals.lebarPopup, varGlobals.tinggiPopup)
            pygame.draw.rect(varGlobals.screen, cc.WHITE, kotakPopup, border_radius=15)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, kotakPopup, 3, border_radius=15)

            # KOTAK INPUT UNTUK NOMOR MEJA DAN JUMLAH PESANAN
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxNomorMeja, border_radius=8)
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxJumlah, border_radius=8)

            # KOTAK KONFIRMASI
            pygame.draw.rect(varGlobals.screen, cc.WHITE, boxConfirm, border_radius=8)
            pygame.draw.rect(varGlobals.screen, cc.BLACK, boxConfirm, 3, border_radius=8)
            
            # HIGHLIGHT BOX
            if varGlobals.input == "table":
                pygame.draw.rect(varGlobals.screen, cc.BLACK, boxNomorMeja, 3, border_radius=8)
            elif varGlobals.input == "quantity":
                pygame.draw.rect(varGlobals.screen, cc.BLACK, boxJumlah, 3, border_radius=8)
            elif varGlobals.input == "confirm":
                pygame.draw.rect(varGlobals.screen, cc.BLACK, boxConfirm, 3, border_radius=8)
            
            # JUDUL UNTUK KOTAK POP UP BESAR
            textJudul = varGlobals.font.render(f"Order {varGlobals.pesanan}", True, cc.BLACK)
            textPos = textJudul.get_rect(centerx = kotakPopup.centerx, top = varGlobals.popupY + 10)
            varGlobals.screen.blit(textJudul, textPos)

            # TEXT PADA INPUTAN DAN WARNANYA
            textMeja = f"Meja     : {varGlobals.nomorMeja}"
            textJumlah = f"Jumlah  : {varGlobals.jumlah}"
            textConfirm = "Done"
            ccMeja = varGlobals.font.render(textMeja, True, cc.BLACK)
            ccJumlah = varGlobals.font.render(textJumlah, True, cc.BLACK)
            ccConfirm = varGlobals.font.render(textConfirm, True, cc.BLACK)

            varGlobals.screen.blit(ccMeja, (boxNomorMeja.x + 10, boxNomorMeja.y + 10))
            varGlobals.screen.blit(ccJumlah, (boxJumlah.x + 10, boxJumlah.y + 10))
            varGlobals.screen.blit(ccConfirm, (boxConfirm.x + 10, boxConfirm.y + 5))

        click = False
        varGlobals.clock.tick(60)
        pygame.display.flip()


###################################################################################################
#                                            MAIN MENU                                            #
###################################################################################################

def mainMenu():

    # BOOLEAN
    click = False
    varGlobals.runSim = False
    varGlobals.runMenu = True
    varGlobals.runOrder = False
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)

    # SET UP POSISI TEXT & UKURAN BUTTON
    PANJANG_STATUS = varGlobals.res[0] * 0.064
    LEBAR_STATUS = varGlobals.res[1] * 0.02

    # POSISI BUTTON
    RUN = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-0.8)),
        window_rect.centery - varGlobals.LEBAR_BUTTON * 2.6,
        varGlobals.PANJANG_BUTTON * 3,
        varGlobals.LEBAR_BUTTON * 1.7
    )
    CONFIGURATION = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-0.8)),
        window_rect.centery - (varGlobals.LEBAR_BUTTON * 0.2),
        varGlobals.PANJANG_BUTTON * 3,
        varGlobals.LEBAR_BUTTON * 1.7
    )
    EXIT = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-0.8)),
        window_rect.centery - (varGlobals.LEBAR_BUTTON * (-2.2)),
        varGlobals.PANJANG_BUTTON * 3,
        varGlobals.LEBAR_BUTTON * 1.7
    )

    # PESAN DISCONNECT DAN CONNECTED
    STATUS = pygame.rect.Rect(
        window_rect.centerx - (PANJANG_STATUS * (-2.6)),
        window_rect.centery - (LEBAR_STATUS * (-15.5)),
        PANJANG_STATUS * 2,
        LEBAR_STATUS * 1.7
    )
    
    # BUTTON
    buttons = {
        "Run" : RUN,
        "Configuration" : CONFIGURATION,
        "Exit" : EXIT,
    }

    # STATUS
    status = {
        varGlobals.conServiceBot : STATUS
    }

    while varGlobals.runMenu:

        varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 5, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 60)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 3, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 50)

        for myStatus in status:
            if varGlobals.serviceBot:
                varGlobals.conServiceBot = "Connected"
                pygame.draw.rect(varGlobals.screen, cc.GREEN, status[myStatus], border_radius = 20)
                tts(varGlobals.conServiceBot, cc.WHITE, status[myStatus], varGlobals.screen, 30)
            else:
                varGlobals.conServiceBot = "Disconnected"
                pygame.draw.rect(varGlobals.screen, cc.RED, status[myStatus], border_radius = 20)
                tts(varGlobals.conServiceBot, cc.WHITE, status[myStatus], varGlobals.screen, 30)

        click = False
        varGlobals.clock.tick(60)
        pygame.display.flip()


###################################################################################################
#                                            SIMULATION                                           #
###################################################################################################

def simulation():

    # BOOLEAN
    click = False
    varGlobals.runSim = True
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False

    # WINDOW
    window_rect = pygame.Surface.get_rect(varGlobals.screen)

    # POSISI TEXT
    BACK = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-3.75)),
        window_rect.centery - varGlobals.LEBAR_BUTTON * 7.8,
        varGlobals.PANJANG_BUTTON,
        varGlobals.LEBAR_BUTTON * 1.2
    )
    
    # POSISI TEXT + KOTAK
    DEMO_1 = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * 0.95),
        window_rect.centery - (varGlobals.LEBAR_BUTTON * 1.5),
        varGlobals.PANJANG_BUTTON,
        varGlobals.LEBAR_BUTTON * 0.8
    )
    TAMBAH_PESANAN = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-1.3)),
        window_rect.centery - varGlobals.LEBAR_BUTTON * (5.85),
        varGlobals.PANJANG_BUTTON * 3,
        varGlobals.LEBAR_BUTTON * 1.7
    )
    HAPUS_PESANAN = pygame.rect.Rect(
        window_rect.centerx - (varGlobals.PANJANG_BUTTON * (-1.3)),
        window_rect.centery - varGlobals.LEBAR_BUTTON * (3.85),
        varGlobals.PANJANG_BUTTON * 3,
        varGlobals.LEBAR_BUTTON * 1.7
    )

    buttons = {
        "Back" : BACK
    }

    kotak_button = {
        "Demo 1" : DEMO_1,
        "Add Order" : TAMBAH_PESANAN,
        "Delete Order" : HAPUS_PESANAN
    }
    
    while varGlobals.runSim:

        infoRobot = [
            ("Compass   : " + str(dataRobot.kompas), (220, 60)),
            ("X     : " + str(dataRobot.xpos), (150, 990)),
            ("Y     : " + str(dataRobot.ypos), (350, 990))
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runSim = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                click = True
            
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

        # MENGGERAKKAN ROBOT DENGAN ARROW [KIRI, KANAN, ATAS, BAWAH]
        # if varGlobals.keys_pressed[pygame.K_DOWN]:
        #     if dataRobot.xpos < varGlobals.res[1] - 1 and dataRobot.xpos <= 600:
        #         dataRobot.xpos += 1
        #         if dataRobot.xpos > 600:
        #             dataRobot.xpos = 600
        # if varGlobals.keys_pressed[pygame.K_UP]:
        #     if dataRobot.xpos > 0 and dataRobot.ypos <= 600:
        #         dataRobot.xpos -= 1
        #     if dataRobot.xpos > 0 and dataRobot.ypos > 600 and dataRobot.xpos > 200:
        #         dataRobot.xpos -= 1
        #         if dataRobot.xpos < 201:
        #             dataRobot.xpos = 201
        # if varGlobals.keys_pressed[pygame.K_LEFT]:
        #     if dataRobot.ypos > 0:
        #         dataRobot.ypos -= 1
        # if varGlobals.keys_pressed[pygame.K_RIGHT]:
        #     if dataRobot.ypos < varGlobals.res[0] - 1 and dataRobot.ypos <= 600 and dataRobot.xpos <= 200:
        #         dataRobot.ypos += 1
        #         if dataRobot.ypos > 600:
        #             dataRobot.ypos = 600
        #     elif dataRobot.ypos < varGlobals.res[0] - 1 and dataRobot.ypos <= 1000 and dataRobot.xpos > 200:
        #         dataRobot.ypos += 1
        #         if dataRobot.ypos > 1000:
        #             dataRobot.ypos = 1000
        # if varGlobals.keys_pressed[pygame.K_LSHIFT]:
        #     dataRobot.kompas += 1
        #     if dataRobot.kompas > 360:
        #         dataRobot.kompas = 0
        # if varGlobals.keys_pressed[pygame.K_LCTRL]:
        #     dataRobot.kompas -= 1
        #     if dataRobot.kompas < 0:
        #         dataRobot.kompas = 360

        varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 60)
                if click:
                    pencetButton(button)
            else:
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 50)
            
        for button in kotak_button:
            if kotak_button[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, kotak_button[button], 5, border_radius = 20)
                tts(button, cc.RED_BROWN, kotak_button[button], varGlobals.screen, 60)
                if click:
                    pencetButton(button)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, kotak_button[button], 3, border_radius = 20)
                tts(button, cc.RED_BROWN, kotak_button[button], varGlobals.screen, 50)
                

        for text_line, pos in infoRobot:
            tts(text_line, cc.RED_BROWN, pygame.Rect(pos[0], pos[1], 10, 10), varGlobals.screen, 30)
        
        # ROTASI IMAGE
        Xbot = varGlobals.offsetX + (dataRobot.ypos * varGlobals.skala)
        Ybot = varGlobals.offsetY + (dataRobot.xpos * varGlobals.skala)
        rotatedImage(varGlobals.bot, Xbot, Ybot, dataRobot.kompas)
        rotatedImage(varGlobals.arrow, 220, 220, dataRobot.kompas)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)

mainMenu()