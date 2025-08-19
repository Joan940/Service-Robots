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
    rotatedImage,
    drawNumberPad,
    tampilanOrder,
    setAnimation,
    easeInOut,
    lerp,
    transition,
    rotatePoint
)
from Modules.database import (
    addOrders,
    getOrders,
    reset_database
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
    make_order as moButton
)


###################################################################################################
#                            VARIABLE GLOBAL YANG DIINISIALISASI DIAWAL                           #
###################################################################################################

pygame.mixer.init()

varGlobals.IP = '127.0.0.1'
varGlobals.PORT = '8081'


###################################################################################################
#                                          PRESS BUTTON                                           #
###################################################################################################

def pencetButton(text):

    data = bytearray(3)

    # PAKSA HURUF KECIL
    text = text.lower()

    if text == "demo 1":
        demo1()

    elif text == "coba":
        makeOrder()

    elif text == "exit":
        sys.exit(0)


###################################################################################################
#                                        TEXT ACTION MENU                                         #
###################################################################################################

def fillText(inp_key, inputUser_rects):

    while True:
        
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, inputUser_rects['Save'], 3, border_radius=20)
        tts("Save", cc.RED_BROWN, inputUser_rects['Save'], varGlobals.screen, 20)
       
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
                    tts(current_value, cc.RED_BROWN, rect, varGlobals.screen, 20)

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
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = True
    varGlobals.runMakeOrder = False

    inputUser = {
        "Save" : confButton.SAVE_RECT,
        "IP" : confButton.INP_IP_RECT,
        "PORT" : confButton.INP_PORT_RECT
    }

    while varGlobals.runConfig:
        varGlobals.screen.blit(varGlobals.bgConfig, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runConfig = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                varGlobals.trueSound.play()
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
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 30)
                if click:
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                    if key in ["IP", "PORT"]:
                        fillText(key, inputUser)
                    elif key == "Save" and (varGlobals.IP and varGlobals.PORT):
                        pencetButton(key)
                        
                        varGlobals.newSurface.blit(varGlobals.bgMenu, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="right", speed=20)
                        
                        print("save")
                        runCom()
                        mainMenu()
                    elif key == "Save" and not (varGlobals.IP and varGlobals.PORT):
                        varGlobals.falseSound.play()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius = 20)
                tts(display_text, cc.RED_BROWN, rect, varGlobals.screen, 20)

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
    varGlobals.runEye = False
    varGlobals.runSim = False
    varGlobals.runMenu = False
    varGlobals.runOrder = True
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False

    buttons = {
        "Back": orderButton.EXIT
    }

    menu = {
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

        # LOGIKA TOMBOL
        for button_name, rect in buttons.items():
            if rect.collidepoint(mx, my) and not varGlobals.pesanan:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 5, border_radius=20)
                tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 30)

                if click:
                    pencetButton(button_name)
                    
                    # MEMBUAT TRANSISI WINDOW
                    varGlobals.oldSurface = varGlobals.screen.copy()
                    varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))

                    if button_name == "Back":
                        varGlobals.newSurface.blit(varGlobals.bgMakeOrder, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="down", speed=20)
                        makeOrder()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
                tts(button_name, cc.RED_BROWN, rect, varGlobals.screen, 20)
        
        for menu_item, rect in menu.items():
            if rect.collidepoint(mx, my) and not varGlobals.pesanan:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(menu_item, cc.WHITE, rect, varGlobals.screen, 20)
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, border_radius=20)
                tts(menu_item, cc.WHITE, rect, varGlobals.screen, 15)

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

# def eyeUI():

#     # RESET
#     varGlobals.oldSurface = None
#     varGlobals.newSurface = None

#     # LOCAL VARIABLE
#     lastBlinkTime = time.time()
#     blink_interval = random.uniform(3, 6)
#     blinkStartTime = 0.0
#     blinkDuration = 0.5
#     startPos = None
#     threshold = 10

#     # BOOLEAN
#     dragging = False
#     varGlobals.runEye = True
#     varGlobals.isBlinking = False

#     varGlobals.startTransisi = time.time()
#     varGlobals.startProperties = varGlobals.SET_AWAL.copy()
#     varGlobals.targetPropertis = varGlobals.SET_AWAL.copy()
    
#     current_expression = varGlobals.ANIMATIONS[0].copy()

#     while varGlobals.runEye:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 varGlobals.runEye = False
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 dragging = True
#                 startPos = event.pos
#             elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 if dragging:
#                     endPos = event.pos
#                     dx = endPos[0] - startPos[0]
#                     dy = endPos[1] - startPos[1]
#                     distance = (dx ** 2 + dy ** 2) ** 0.5
                    
#                     if distance <= threshold or dy < (-20):
#                         print("Klik terdeteksi")
#                         varGlobals.trueSound.play()
#                         varGlobals.oldSurface = varGlobals.screen.copy()
#                         varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
#                         varGlobals.newSurface.blit(varGlobals.bgOrder, (0, 0))
#                         transition(varGlobals.oldSurface, varGlobals.newSurface, direction="up", speed=20)
#                         order()
#                     else:
#                         pass
                
#                 dragging = False
                
#         mx, my = pygame.mouse.get_pos()
#         center_x = varGlobals.res[0] // 2
#         center_y = varGlobals.res[1] // 2
#         distance_from_center = ((mx - center_x) ** 2 + (my - center_y) ** 2) ** 0.5

#         if distance_from_center < 80:
#             new_expression = varGlobals.ANIMATIONS['marah'].copy()
#         elif my < varGlobals.res[1] // 4:
#             new_expression = varGlobals.ANIMATIONS['terkejut'].copy()
#         elif mx < varGlobals.res[0] // 4 or mx > varGlobals.res[0] * 3 // 4:
#             new_expression = varGlobals.ANIMATIONS['sedih'].copy()
#         else:
#             new_expression = varGlobals.ANIMATIONS[0].copy()

#         # 2. Gabungkan pergerakan mata dengan ekspresi yang dipilih
#         max_offset = 70
#         mouse_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 5))
#         mouse_offset_y = max(-max_offset, min(max_offset, (my - center_y) / 5))
        
#         # Tambahkan offset mouse ke properti ekspresi
#         new_expression['eyeOffsetX'] += mouse_offset_x
#         new_expression['eyeOffsetY'] += mouse_offset_y

#         # 3. Mulai transisi ke ekspresi baru jika diperlukan
#         if not varGlobals.isBlinking and new_expression != varGlobals.targetPropertis:
#             varGlobals.startProperties = varGlobals.SET_AWAL.copy()
#             varGlobals.targetPropertis = new_expression.copy()
#             varGlobals.startTransisi = time.time()
#             current_expression = new_expression.copy()

#         # 4. Tangani animasi kedipan
#         if time.time() - lastBlinkTime > blink_interval and not varGlobals.isBlinking:
#             varGlobals.isBlinking = True
#             blinkStartTime = time.time()
            
#             varGlobals.startProperties = varGlobals.SET_AWAL.copy()
#             varGlobals.targetPropertis = varGlobals.ANIMATIONS[5].copy()
#             varGlobals.startTransisi = time.time()
            
#             lastBlinkTime = time.time()
#             blink_interval = random.uniform(3, 6)

#         # 5. Kembali ke ekspresi terakhir setelah kedipan selesai
#         if varGlobals.isBlinking and time.time() - blinkStartTime > blinkDuration:
#             varGlobals.isBlinking = False
            
#             varGlobals.startProperties = varGlobals.SET_AWAL.copy()
#             varGlobals.targetPropertis = current_expression.copy()
#             varGlobals.startTransisi = time.time()

#         # MENGGUNAKAN RUMUS AGAR LEBIH HALUS
#         elapsed = time.time() - varGlobals.startTransisi
#         t = min(elapsed / varGlobals.durasiTransisi, 1.0)
#         tEased = easeInOut(t)

#         for key in varGlobals.targetPropertis:
#             varGlobals.SET_AWAL[key] = lerp(
#                 varGlobals.startProperties.get(key, 0),
#                 varGlobals.targetPropertis[key],
#                 tEased
#             )
            
#         varGlobals.screen.blit(varGlobals.bgEyes, (0, 0))

#         # UPDATE PROPERTI VISUAL
#         tinggiMata = int(varGlobals.SET_AWAL['eyeHeight'])
#         eyeOffsetX_val = varGlobals.SET_AWAL['eyeOffsetX']
#         eyeOffsetY_val = varGlobals.SET_AWAL['eyeOffsetY']
        
#         eyeLeftX = varGlobals.eyeLeftX + eyeOffsetX_val
#         eyeRightX = varGlobals.eyeRightX + eyeOffsetX_val
#         eyePosY = varGlobals.eyePosY + eyeOffsetY_val

#         eyeLeft = pygame.Rect(eyeLeftX, eyePosY, varGlobals.lebarMata, tinggiMata)
#         eyeRight = pygame.Rect(eyeRightX, eyePosY, varGlobals.lebarMata, tinggiMata)

#         pygame.draw.rect(varGlobals.screen, (0,0,0), eyeLeft, border_radius=60)
#         pygame.draw.rect(varGlobals.screen, (0,0,0), eyeRight, border_radius=60)

#         # Menggambar Alis
#         eyebrowOffset_leftY = varGlobals.SET_AWAL['eyebrowOffset_leftY']
#         eyebrowOffset_rightY = varGlobals.SET_AWAL['eyebrowOffset_rightY']
#         eyebrowAngle_left = varGlobals.SET_AWAL['eyebrowAngle_right']
#         eyebrowAngle_right = varGlobals.SET_AWAL['eyebrowAngle_left']
        
#         eyebrow_start_left = (varGlobals.eyeLeftX - 10, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
#         eyebrow_end_left = (varGlobals.eyeLeftX + varGlobals.lebarMata + 10, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
#         eyebrow_start_right = (varGlobals.eyeRightX - 10, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)
#         eyebrow_end_right = (varGlobals.eyeRightX + varGlobals.lebarMata + 10, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)

#         rotated_start_left = rotatePoint(eyebrow_start_left, eyeLeft.center, eyebrowAngle_left)
#         rotated_end_left = rotatePoint(eyebrow_end_left, eyeLeft.center, eyebrowAngle_left)
#         pygame.draw.line(varGlobals.screen, (0,0,0), rotated_start_left, rotated_end_left, 10)

#         rotated_start_right = rotatePoint(eyebrow_start_right, eyeRight.center, eyebrowAngle_right)
#         rotated_end_right = rotatePoint(eyebrow_end_right, eyeRight.center, eyebrowAngle_right)
#         pygame.draw.line(varGlobals.screen, (0,0,0), rotated_start_right, rotated_end_right, 10)

#         varGlobals.clock.tick(60)
#         pygame.display.flip()

def eyeUI():

    # RESET
    startPos = None
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # LOCAL VARIABLE
    blink_interval = random.uniform(3, 6)
    blinkDuration = 0.5
    blinkStartTime = 0

    varGlobals.isLookingRight = False
    varGlobals.isLookingLeft = False
    lastLookTime = time.time()
    lookDuration = 1
    lookInterval = random.uniform(3, 6)

    newExpressTime = 0
    threshold = 10
    distance = 0
    duration = 5

    keKanan = time.time()
    lastBlinkTime = time.time()
    new_expression = varGlobals.ANIMATIONS['buka'].copy()

    # BOOLEAN
    yes = True
    dragging = False
    varGlobals.list = False
    varGlobals.runEye = True
    varGlobals.runSim = False
    varGlobals.isRight = False
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
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                startPos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging:
                    endPos = event.pos

                    dx = endPos[0] - startPos[0]
                    dy = endPos[1] - startPos[1]
                    
                    # MENGHITUNG JARAK TOTAL
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    
                    if distance <= threshold or dy < (-20):

                        # DIANGGAP KLIK
                        print("Klik terdeteksi")
                        varGlobals.trueSound.play()
                        varGlobals.oldSurface = varGlobals.screen.copy()
                        varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                        varGlobals.newSurface.blit(varGlobals.bgMakeOrder, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="up", speed=20)
                        order()
                    
                    else:
                        pass
                
                dragging = False

        # UPDATE POSISI MENGIKUTI MOUSE
        mx, my = pygame.mouse.get_pos()
        center_x = varGlobals.res[0] // 2
        center_y = varGlobals.res[1] // 2
        max_offset = 30

        mouse_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 5))
        mouse_offset_y = max(-max_offset, min(max_offset, (my - center_y) / 5))

        new_expression['eyeOffsetX'] = mouse_offset_x
        new_expression['eyeOffsetY'] = mouse_offset_y

        varGlobals.targetPropertis['eyeOffsetX'] = mouse_offset_x
        varGlobals.targetPropertis['eyeOffsetY'] = mouse_offset_y

        if distance >= 100:
            yes = False

        if yes and distance == 0:
            # UPDATE ANIMASI KEDIP DENGAN MENGAMBIL PROPERTI ANIMATIONS KE 5 (MENUTUP MATA)
            if time.time() - lastBlinkTime > blink_interval and not varGlobals.isBlinking:
                varGlobals.isBlinking = True
                blinkStartTime = time.time()
                new_expression = varGlobals.ANIMATIONS['kedip'].copy()
                
                lastBlinkTime = time.time()
                blink_interval = random.uniform(3, 6)

            # UPDATE ANIMASI KEDIP DENGAN MENGAMBIL PROPERTI ANIMATIONS KE 0 (MEMBUKA MATA)
            if varGlobals.isBlinking and time.time() - blinkStartTime > blinkDuration:
                varGlobals.isBlinking = False
                new_expression = varGlobals.ANIMATIONS['buka'].copy()

        elif not yes and distance >= 100:
            if distance >= 100 and distance < 200:
                if not varGlobals.newExpression:
                    varGlobals.newExpression = True
                    new_expression = varGlobals.ANIMATIONS['terkejut'].copy()
                    newExpressTime = time.time()

            elif distance >= 200 and distance < 300:
                if not varGlobals.newExpression:
                    varGlobals.newExpression = True
                    new_expression = varGlobals.ANIMATIONS['sedih'].copy()
                    newExpressTime = time.time()

            elif distance >= 400:
                if not varGlobals.newExpression:
                    varGlobals.newExpression = True
                    new_expression = varGlobals.ANIMATIONS['marah'].copy()
                    newExpressTime = time.time()

            # KEMBALI KE NORMAL SETELAH DURASI YANG DITENTUKAN
            if varGlobals.newExpression and time.time() - newExpressTime > duration:
                varGlobals.newExpression = False
                distance = 0
                yes = True

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
#                                            MAKE ORDER                                           #
###################################################################################################

def makeOrder():

    # RESET
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # VARIABLE LOCAL
    contentY = 0
    duration = 10
    scroll = False
    scrollPos = None
    lastAction = time.time()

    # BOOLEAN
    click = False
    varGlobals.list = False
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

                    elif button == "Add Order":
                        varGlobals.newSurface.blit(varGlobals.bgOrder, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="up", speed=20)
                        order()
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

    # BOOLEAN
    click = False
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

    # STATUS
    status = {
        varGlobals.conServiceBot : mmButton.STATUS
    }

    while varGlobals.runMenu:

        varGlobals.screen.blit(varGlobals.bgMenu, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runMenu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                varGlobals.trueSound.play()
                click = True

        # LOGIKA TOMBOL
        mx, my = pygame.mouse.get_pos()
        for button in buttons:
            if buttons[button].collidepoint(mx, my):
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 4, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 30)
                if click:
                    pencetButton(button)

                    # MEMBUAT TRANSISI WINDOW
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
                        varGlobals.newSurface.blit(varGlobals.bgConfig, (0, 0))
                        transition(varGlobals.oldSurface, varGlobals.newSurface, direction="left", speed=20)
                        configuration()
            else:
                pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, buttons[button], 2, border_radius = 20)
                tts(button, cc.RED_BROWN, buttons[button], varGlobals.screen, 20)

        for myStatus in status:
            if varGlobals.serviceBot:
                varGlobals.conServiceBot = "Connected"
                pygame.draw.rect(varGlobals.screen, cc.GREEN, status[myStatus], border_radius = 20)
                tts(varGlobals.conServiceBot, cc.WHITE, status[myStatus], varGlobals.screen, 15)
            else:
                varGlobals.conServiceBot = "Disconnected"
                pygame.draw.rect(varGlobals.screen, cc.RED, status[myStatus], border_radius = 20)
                tts(varGlobals.conServiceBot, cc.WHITE, status[myStatus], varGlobals.screen, 15)

        click = False
        varGlobals.clock.tick(30)
        pygame.display.flip()


###################################################################################################
#                                            SIMULATION                                           #
###################################################################################################

def simulation():

    # BOOLEAN
    click = False
    varGlobals.runSim = True
    varGlobals.runEye = False
    varGlobals.runMenu = False
    varGlobals.runOrder = False
    varGlobals.runConfig = False
    varGlobals.runMakeOrder = False

    buttons = {
        "Back" : simButton.BACK,
        "Demo 1" : simButton.DEMO_1
    }
    
    while varGlobals.runSim:

        infoRobot = [
            ("Compass   :   " + str(dataRobot.kompas), (530, 220)),
            ("X               :   " + str(dataRobot.ypos), (530, 240)),
            ("Y               :   " + str(dataRobot.xpos), (530, 260))
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
                    dataRobot.ypos += 200
                elif event.key == pygame.K_LEFT:
                    dataRobot.ypos -= 200
                elif event.key == pygame.K_UP:
                    dataRobot.xpos -= 200
                elif event.key == pygame.K_DOWN:
                    dataRobot.xpos += 200
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

        varGlobals.screen.blit(varGlobals.bgSim, (0, 0))

        # pygame.draw.aaline(varGlobals.screen, cc.RED, (0 + varGlobals.offsetX, 0), (0 + varGlobals.offsetX, 600))
        # pygame.draw.aaline(varGlobals.screen, cc.RED, (0, 0 + varGlobals.offsetY), (1024, 0 + varGlobals.offsetY))

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
            tts(text_line, cc.BLACK, pygame.Rect(pos[0], pos[1], 10, 10), varGlobals.screen, 15)
        
        # ROTASI IMAGE
        Xbot = varGlobals.offsetX + (dataRobot.ypos * varGlobals.skala)
        Ybot = varGlobals.offsetY + (dataRobot.xpos * varGlobals.skala)
        rotatedImage(varGlobals.bot, Xbot, Ybot, dataRobot.kompas)
        rotatedImage(varGlobals.arrow, 446, 250, dataRobot.kompas)

        click = False
        pygame.display.flip()
        varGlobals.clock.tick(60)

reset_database()
mainMenu()