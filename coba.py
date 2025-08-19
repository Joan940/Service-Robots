def eyeUI():
    # RESET
    varGlobals.oldSurface = None
    varGlobals.newSurface = None

    # LOCAL VARIABLE
    lastBlinkTime = time.time()
    blink_interval = random.uniform(3, 6)
    blinkStartTime = 0.0
    blinkDuration = 0.5
    startPos = None
    threshold = 10
    
    # Variabel untuk melacak ekspresi yang sedang aktif
    current_expression = varGlobals.ANIMATIONS[0].copy()

    # BOOLEAN
    dragging = False
    varGlobals.runEye = True
    varGlobals.isBlinking = False

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
                startPos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if dragging:
                    endPos = event.pos
                    dx = endPos[0] - startPos[0]
                    dy = endPos[1] - startPos[1]
                    distance = (dx ** 2 + dy ** 2) ** 0.5
                    
                    if distance <= threshold or dy < (-20):
                        print("Klik terdeteksi")
                        # Transisi UI (pastikan variabel global ada)
                        # varGlobals.trueSound.play()
                        # varGlobals.oldSurface = varGlobals.screen.copy()
                        # varGlobals.newSurface = pygame.Surface((varGlobals.res[0], varGlobals.res[1]))
                        # varGlobals.newSurface.blit(varGlobals.bgOrder, (0, 0))
                        # transition(varGlobals.oldSurface, varGlobals.newSurface, direction="up", speed=20)
                        # order()
                    else:
                        pass
                
                dragging = False
                
        # --- LOGIKA KEDIP DAN EKSPRESI ---
        # 1. Tentukan ekspresi dasar berdasarkan posisi mouse
        mx, my = pygame.mouse.get_pos()
        center_x = varGlobals.res[0] // 2
        center_y = varGlobals.res[1] // 2
        distance_from_center = ((mx - center_x) ** 2 + (my - center_y) ** 2) ** 0.5

        if distance_from_center < 80:
            new_expression = varGlobals.ANIMATIONS['marah'].copy()
        elif my < varGlobals.res[1] // 4:
            new_expression = varGlobals.ANIMATIONS['terkejut'].copy()
        elif mx < varGlobals.res[0] // 4 or mx > varGlobals.res[0] * 3 // 4:
            new_expression = varGlobals.ANIMATIONS['sedih'].copy()
        else:
            new_expression = varGlobals.ANIMATIONS[0].copy()

        # 2. Gabungkan pergerakan mata dengan ekspresi yang dipilih
        max_offset = 70
        mouse_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 5))
        mouse_offset_y = max(-max_offset, min(max_offset, (my - center_y) / 5))
        
        # Tambahkan offset mouse ke properti ekspresi
        new_expression['eyeOffsetX'] += mouse_offset_x
        new_expression['eyeOffsetY'] += mouse_offset_y

        # 3. Mulai transisi ke ekspresi baru jika diperlukan
        if not varGlobals.isBlinking and new_expression != varGlobals.targetPropertis:
            varGlobals.startProperties = varGlobals.SET_AWAL.copy()
            varGlobals.targetPropertis = new_expression.copy()
            varGlobals.startTransisi = time.time()
            current_expression = new_expression.copy()

        # 4. Tangani animasi kedipan
        if time.time() - lastBlinkTime > blink_interval and not varGlobals.isBlinking:
            varGlobals.isBlinking = True
            blinkStartTime = time.time()
            
            varGlobals.startProperties = varGlobals.SET_AWAL.copy()
            varGlobals.targetPropertis = varGlobals.ANIMATIONS[5].copy()
            varGlobals.startTransisi = time.time()
            
            lastBlinkTime = time.time()
            blink_interval = random.uniform(3, 6)

        # 5. Kembali ke ekspresi terakhir setelah kedipan selesai
        if varGlobals.isBlinking and time.time() - blinkStartTime > blinkDuration:
            varGlobals.isBlinking = False
            
            varGlobals.startProperties = varGlobals.SET_AWAL.copy()
            varGlobals.targetPropertis = current_expression.copy()
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

        # UPDATE PROPERTI VISUAL
        tinggiMata = int(varGlobals.SET_AWAL['eyeHeight'])
        eyeOffsetX_val = varGlobals.SET_AWAL['eyeOffsetX']
        eyeOffsetY_val = varGlobals.SET_AWAL['eyeOffsetY']
        
        eyeLeftX = varGlobals.eyeLeftX + eyeOffsetX_val
        eyeRightX = varGlobals.eyeRightX + eyeOffsetX_val
        eyePosY = varGlobals.eyePosY + eyeOffsetY_val

        eyeLeft = pygame.Rect(eyeLeftX, eyePosY, varGlobals.lebarMata, tinggiMata)
        eyeRight = pygame.Rect(eyeRightX, eyePosY, varGlobals.lebarMata, tinggiMata)

        pygame.draw.rect(varGlobals.screen, (0,0,0), eyeLeft, border_radius=60)
        pygame.draw.rect(varGlobals.screen, (0,0,0), eyeRight, border_radius=60)

        # Menggambar Alis
        eyebrowOffset_leftY = varGlobals.SET_AWAL['eyebrowOffset_leftY']
        eyebrowOffset_rightY = varGlobals.SET_AWAL['eyebrowOffset_rightY']
        eyebrowAngle_left = varGlobals.SET_AWAL['eyebrowAngle_left']
        eyebrowAngle_right = varGlobals.SET_AWAL['eyebrowAngle_right']
        
        eyebrow_start_left = (varGlobals.eyeLeftX - 10, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
        eyebrow_end_left = (varGlobals.eyeLeftX + varGlobals.lebarMata + 10, varGlobals.eyePosY - 40 + eyebrowOffset_leftY)
        eyebrow_start_right = (varGlobals.eyeRightX - 10, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)
        eyebrow_end_right = (varGlobals.eyeRightX + varGlobals.lebarMata + 10, varGlobals.eyePosY - 40 + eyebrowOffset_rightY)

        rotated_start_left = rotatePoint(eyebrow_start_left, eyeLeft.center, eyebrowAngle_left)
        rotated_end_left = rotatePoint(eyebrow_end_left, eyeLeft.center, eyebrowAngle_left)
        pygame.draw.line(varGlobals.screen, (0,0,0), rotated_start_left, rotated_end_left, 10)

        rotated_start_right = rotatePoint(eyebrow_start_right, eyeRight.center, eyebrowAngle_right)
        rotated_end_right = rotatePoint(eyebrow_end_right, eyeRight.center, eyebrowAngle_right)
        pygame.draw.line(varGlobals.screen, (0,0,0), rotated_start_right, rotated_end_right, 10)

        varGlobals.clock.tick(60)
        pygame.display.flip()