import pygame
import time
import math
import random
import sys

# Asumsi: Modul dan variabel global sudah terdefinisi, seperti:
# varGlobals.screen, varGlobals.res, varGlobals.lebarMata, varGlobals.durasiTransisi, dll.
# cc.BLACK, cc.WHITE, dll.
# lerp, easeInOut, setAnimation sudah ada di modul algorithm.py

def makeOrder():
    # --- DEKLARASI GLOBAL ---
    varGlobals.SET_AWAL = {
        'eye_height': 150,
        'eye_offset_x': 0,
        'eye_offset_y': 0,
    }
    varGlobals.ANIMATIONS = {
        0: {'eye_height': 150, 'eye_offset_x': 0, 'eye_offset_y': 0},
        1: {'eye_height': 150, 'eye_offset_x': 0, 'eye_offset_y': 0},
        2: {'eye_height': 150, 'eye_offset_x': 50, 'eye_offset_y': 0},
        3: {'eye_height': 150, 'eye_offset_x': -50, 'eye_offset_y': 0},
        4: {'eye_height': 10, 'eye_offset_x': 0, 'eye_offset_y': 0},
        5: {'eye_height': 10, 'eye_offset_x': 0, 'eye_offset_y': 0},
        6: {'eye_height': 150, 'eye_offset_x': 0, 'eye_offset_y': 0},
        7: {'eye_height': 10, 'eye_offset_x': 0, 'eye_offset_y': 0},
    }

    # LOCAL VARIABLE
    index = 0
    perubahanAnimasi = time.time()
    
    # PERBAIKAN: Tambahkan variabel untuk melacak status mouse dan animasi
    last_mouse_pos = pygame.mouse.get_pos()
    last_mouse_move_time = time.time()
    is_animation_active = False

    # BOOLEAN
    click = False
    varGlobals.list = False
    varGlobals.runMakeOrder = True
    varGlobals.updateOrder = True

    buttons = {
        "Back": moButton.BACK,
        "Add Order": moButton.TAMBAH_PESANAN,
        "List Order": moButton.LIST_PESANAN
    }
    
    # Inisialisasi awal transisi
    varGlobals.startTransisi = time.time()
    varGlobals.startProperties = varGlobals.SET_AWAL.copy()
    varGlobals.targetPropertis = varGlobals.SET_AWAL.copy()

    while varGlobals.runMakeOrder:
        # Pindahkan event loop ke atas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                varGlobals.trueSound.play()
                click = True

        # --- LOGIKA ANIMASI MATA ---
        mx, my = pygame.mouse.get_pos()
        
        # Cek apakah mouse bergerak
        if (mx, my) != last_mouse_pos:
            last_mouse_move_time = time.time()
            is_animation_active = False
            last_mouse_pos = (mx, my)
            
            # Jika mouse bergerak, matikan animasi berjangka waktu
            perubahanAnimasi = time.time()

        # LOGIKA PERGERAKAN MOUSE
        # Ini akan selalu berjalan, dan mengupdate target properti
        # jika mode animasi tidak aktif
        center_x = varGlobals.res[0] // 2
        center_y = varGlobals.res[1] // 2
        max_offset = 70 

        mouse_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 5))
        mouse_offset_y = max(-max_offset, min(max_offset, (my - center_y) / 5))
        
        if not is_animation_active:
            varGlobals.targetPropertis['eye_offset_x'] = mouse_offset_x
            varGlobals.targetPropertis['eye_offset_y'] = mouse_offset_y

        # LOGIKA ANIMASI BERJANGKA WAKTU
        # Ini akan berjalan hanya jika mouse diam lebih dari 1 detik
        if time.time() - last_mouse_move_time > 1 and not is_animation_active:
            is_animation_active = True
            
            # Pemicu animasi berjangka waktu pertama
            index = (index + 1) % len(varGlobals.ANIMATIONS)
            setAnimation(index, varGlobals.ANIMATIONS, varGlobals.SET_AWAL)
            perubahanAnimasi = time.time()
            
        # Pemicu animasi berjangka waktu selanjutnya
        if is_animation_active and time.time() - perubahanAnimasi > 1:
            index = (index + 1) % len(varGlobals.ANIMATIONS)
            setAnimation(index, varGlobals.ANIMATIONS, varGlobals.SET_AWAL)
            perubahanAnimasi = time.time()
            
            # Jika semua animasi sudah selesai, nonaktifkan flag
            if index == len(varGlobals.ANIMATIONS) - 1:
                is_animation_active = False

        # --- LERP & MENGGAMBAR ---
        elapsed = time.time() - varGlobals.startTransisi
        t = min(elapsed / varGlobals.durasiTransisi, 1.0)
        tEased = easeInOut(t)

        for key in varGlobals.targetPropertis:
            varGlobals.SET_AWAL[key] = lerp(
                varGlobals.startProperties.get(key, 0),
                varGlobals.targetPropertis[key],
                tEased
            )
        
        varGlobals.screen.blit(varGlobals.bgMakeOrder, (0, 0))

        tinggiMata = int(varGlobals.SET_AWAL['eye_height'])
        eyeOffsetX_val = varGlobals.SET_AWAL['eye_offset_x']
        eyeOffsetY_val = varGlobals.SET_AWAL['eye_offset_y']
        
        eyeLeftX = varGlobals.eyeLeftX + eyeOffsetX_val
        eyeRightX = varGlobals.eyeRightX + eyeOffsetX_val
        eyePosY = varGlobals.eyePosY + eyeOffsetY_val

        eyeLeft = pygame.Rect(eyeLeftX, eyePosY, varGlobals.lebarMata, tinggiMata)
        eyeRight = pygame.Rect(eyeRightX, eyePosY, varGlobals.lebarMata, tinggiMata)

        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeLeft, border_radius=50)
        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeRight, border_radius=50)

        # LOGIKA TOMBOL & POP-UP
        # ... (tetap sama seperti sebelumnya)

        click = False
        varGlobals.clock.tick(60)
        pygame.display.flip()