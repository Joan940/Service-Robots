import time
import math
import pygame
import Modules.varGlobals as varGlobals
from Modules.colors import custom as cc, tts1, tts2


###################################################################################################
#                                 UNTUK MENAMPILKAN ROBOT PADA MAP                                #
###################################################################################################

def rotatedImage(image, x, y, angle):
    rotated_image = pygame.transform.rotate(image, 360 - angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    varGlobals.screen.blit(rotated_image, new_rect)


###################################################################################################
#                                        MENGGAMBAR NUMPAD                                        #
###################################################################################################

def drawNumberPad(screen, popup_x, popup_y, outline):
    button_size = 50
    gap = 10
    start_x = popup_x + varGlobals.lebarPopup + 20
    start_y = popup_y

    font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 17)
    mx, my = pygame.mouse.get_pos()

    # UNTUK KOTAK DARI 1 - 9
    for i in range(9):
        x = start_x + (i % 3) * (button_size + gap)
        y = start_y + (i // 3) * (button_size + gap)
        rect = pygame.Rect(x, y, button_size, button_size)
        pygame.draw.rect(screen, cc.WHITE, rect, border_radius=8)
        if rect.collidepoint(mx, my):
            pygame.draw.rect(screen, cc.BLACK, rect, outline + 1, border_radius=8)
        else:
            pygame.draw.rect(screen, cc.BLACK, rect, outline, border_radius=8)
        
        # MENAMPILKAN ANGKA
        number = str(i + 1)
        text_surf = font.render(number, True, cc.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    # UNTUK KOTAK 0
    box_0 = pygame.Rect(start_x + (button_size + gap), start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_0, border_radius=8)
    if box_0.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.BLACK, box_0, outline + 1, border_radius=8)
    else:
        pygame.draw.rect(screen, cc.BLACK, box_0, outline, border_radius=8)
    text_0 = font.render("0", True, cc.BLACK)
    text_0_rect = text_0.get_rect(center=box_0.center)
    screen.blit(text_0, text_0_rect)

    # UNTUK KOTAK DELETE
    box_del = pygame.Rect(start_x + 0, start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_del, border_radius=8)
    if box_del.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.BLACK, box_del, outline + 1, border_radius=8)
    else:
        pygame.draw.rect(screen, cc.BLACK, box_del, outline, border_radius=8)
    text_del = font.render("Del", True, cc.BLACK)
    text_del_rect = text_del.get_rect(center=box_del.center)
    screen.blit(text_del, text_del_rect)

    # UNTUK KOTAK CLEAR
    box_clear = pygame.Rect(start_x + (button_size + gap) * 2, start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_clear, border_radius=8)
    if box_clear.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.BLACK, box_clear, outline + 1, border_radius=8)
    else:
        pygame.draw.rect(screen, cc.BLACK, box_clear, outline, border_radius=8)
    text_clear = font.render("Clear", True, cc.BLACK)
    text_clear_rect = text_clear.get_rect(center=box_clear.center)
    screen.blit(text_clear, text_clear_rect)
    
    # MENGEMBALIKAN SEMUA VALUE RECTANGLE
    return {
        "1": pygame.Rect(start_x + (0 % 3) * (button_size + gap), start_y + (0 // 3) * (button_size + gap), button_size, button_size),
        "2": pygame.Rect(start_x + (1 % 3) * (button_size + gap), start_y + (1 // 3) * (button_size + gap), button_size, button_size),
        "3": pygame.Rect(start_x + (2 % 3) * (button_size + gap), start_y + (2 // 3) * (button_size + gap), button_size, button_size),
        "4": pygame.Rect(start_x + (3 % 3) * (button_size + gap), start_y + (3 // 3) * (button_size + gap), button_size, button_size),
        "5": pygame.Rect(start_x + (4 % 3) * (button_size + gap), start_y + (4 // 3) * (button_size + gap), button_size, button_size),
        "6": pygame.Rect(start_x + (5 % 3) * (button_size + gap), start_y + (5 // 3) * (button_size + gap), button_size, button_size),
        "7": pygame.Rect(start_x + (6 % 3) * (button_size + gap), start_y + (6 // 3) * (button_size + gap), button_size, button_size),
        "8": pygame.Rect(start_x + (7 % 3) * (button_size + gap), start_y + (7 // 3) * (button_size + gap), button_size, button_size),
        "9": pygame.Rect(start_x + (8 % 3) * (button_size + gap), start_y + (8 // 3) * (button_size + gap), button_size, button_size),
        "0": box_0,
        "Del": box_del,
        "Clear": box_clear
    }


###################################################################################################
#                                       MENAMPILKAN PESANAN                                       #
###################################################################################################

def tampilanOrder(orders_list):
    orderStack = []
    ySpacing = 10
    box_lebar_kiri = 80  # lebar kotak meja
    padding_text = 120     # jarak teks dari pinggir kotak

    # Grouping berdasarkan nomor meja
    grouped_orders = {}
    for pesanan_data in orders_list:
        meja = pesanan_data[1]
        namaPesanan = pesanan_data[3]
        jumlahPesanan = pesanan_data[4]

        if meja not in grouped_orders:
            grouped_orders[meja] = []
        grouped_orders[meja].append({'nama': namaPesanan, 'jumlah': jumlahPesanan})

    # Hitung tinggi total (untuk scrolling atau posisi awal)
    total_height = 0
    for meja, items in grouped_orders.items():
        group_height = 100  # tinggi awal untuk nomor meja
        group_height += sum([18 + ySpacing for _ in items])  # tinggi tiap pesanan
        total_height += group_height + (ySpacing * 3)

    # Posisi awal Y
    popup_y = 120
    yStart = popup_y + 28

    # Buat data untuk menggambar
    for meja, items in grouped_orders.items():
        group_height = 0
        group_lines = []

        # Nomor meja (di kotak kiri)
        text_surf_meja, text_rect_meja = tts2(
            f"{meja}",
            cc.WHITE,
            40,
            (padding_text, yStart)
        )
        group_lines.append({'type': 'meja', 'surface': text_surf_meja, 'rect': text_rect_meja})

        # Daftar pesanan (di kotak kanan)
        pesanan_x = box_lebar_kiri + padding_text
        for item in items:
            text_surf_pesanan, text_rect_pesanan = tts2(
                f"- {item['nama']} ({item['jumlah']})",
                cc.BLACK,
                18,
                (pesanan_x, yStart + group_height)
            )
            group_lines.append({'type': 'pesanan', 'surface': text_surf_pesanan, 'rect': text_rect_pesanan})
            group_height += text_rect_pesanan.height + ySpacing 

        group_height += text_rect_meja.height

        orderStack.append({'meja': meja, 'height': group_height, 'lines': group_lines})
        yStart += group_height + (ySpacing - 30)

    return orderStack


###################################################################################################
#                                       INTERPOLASI LINEAR                                        #
###################################################################################################

def lerp(start, end, t):
    return start + (end - start) * t


###################################################################################################
#                                          TRANSISI HALUS                                         #
###################################################################################################

def easeInOut(t):
    return t * t * (3 - 2 * t)


###################################################################################################
#                                            SET AWAL                                             #
###################################################################################################

def setAnimation(index, animations, deklarasi):
    varGlobals.startProperties = deklarasi.copy()
    varGlobals.targetPropertis = animations.get(index, animations.get(0)).copy()
    varGlobals.startTransisi = time.time()


###################################################################################################
#                                            SET AWAL                                             #
###################################################################################################

def rotatePoint(p, origin, angle):
    angle_rad = math.radians(angle)
    
    ox, oy = origin
    px, py = p
    
    # Menggunakan rumus rotasi
    qx = ox + (px - ox) * math.cos(angle_rad) - (py - oy) * math.sin(angle_rad)
    qy = oy + (px - ox) * math.sin(angle_rad) + (py - oy) * math.cos(angle_rad)
    
    return int(qx), int(qy)


###################################################################################################
#                                         SLIDE TRANSITION                                        #
###################################################################################################

def transition(surfaceOld, surfaceNew, direction="right", speed=20):
    WIDTH, HEIGHT = surfaceOld.get_size()

    offset = 0
    if direction == "right":
        while offset < WIDTH:
            varGlobals.screen.blit(surfaceOld, (offset, 0))
            varGlobals.screen.blit(surfaceNew, (offset - WIDTH, 0))
            pygame.display.flip()
            varGlobals.clock.tick(60)
            offset += speed
    elif direction == "left":
        while offset > -WIDTH:
            varGlobals.screen.blit(surfaceOld, (offset, 0))
            varGlobals.screen.blit(surfaceNew, (offset + WIDTH, 0))
            pygame.display.flip()
            varGlobals.clock.tick(60)
            offset -= speed
    elif direction == "up":
        while offset > -HEIGHT:
            varGlobals.screen.blit(surfaceOld, (0, offset))
            varGlobals.screen.blit(surfaceNew, (0, offset + HEIGHT))
            pygame.display.flip()
            varGlobals.clock.tick(60)
            offset -= speed
    elif direction == "down":
        while offset < HEIGHT:
            varGlobals.screen.blit(surfaceOld, (0, offset))
            varGlobals.screen.blit(surfaceNew, (0, offset - HEIGHT))
            pygame.display.flip()
            varGlobals.clock.tick(60)
            offset += speed


###################################################################################################
#                                     MENDAPATKAN NOMOR MEJA                                      #
###################################################################################################

def getMeja(orders_list):
    orderStack = []
    ySpacing = 20
    padding_text = 310  # posisi teks

    # Grouping berdasarkan nomor meja
    grouped_orders = {}
    for pesanan_data in orders_list:
        meja = pesanan_data[1]
        if meja not in grouped_orders:
            grouped_orders[meja] = []  # tidak perlu simpan detail pesanan lagi

    # Posisi awal Y
    popup_y = 115
    yStart = popup_y + 28

    for meja in grouped_orders.keys():
        group_height = 60  # cukup tinggi untuk satu nomor meja
        group_lines = []

        # Nomor meja
        text_surf_meja, text_rect_meja = tts2(
            f"{meja}",
            cc.WHITE,
            40,
            (padding_text, yStart)
        )
        group_lines.append({'type': 'meja', 'surface': text_surf_meja, 'rect': text_rect_meja})

        orderStack.append({'meja': meja, 'height': group_height, 'lines': group_lines})
        yStart += group_height + ySpacing

    return orderStack


###################################################################################################
#                                         NUMPAD FOR STAFF                                        #
###################################################################################################

def numpadStaff(screen, popup_x, popup_y, outline):
    button_size = 50
    gap = 10
    start_x = popup_x + varGlobals.lebarPopup + 20
    start_y = popup_y

    font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 17)
    mx, my = pygame.mouse.get_pos()

    # UNTUK KOTAK DARI 1 - 9
    for i in range(9):
        x = start_x + (i % 3) * (button_size + gap)
        y = start_y + (i // 3) * (button_size + gap)
        rect = pygame.Rect(x, y, button_size, button_size)
        pygame.draw.rect(screen, cc.WHITE, rect, border_radius=8)
        if rect.collidepoint(mx, my):
            pygame.draw.rect(screen, cc.BLACK, rect, outline + 1, border_radius=8)
        else:
            pygame.draw.rect(screen, cc.BLACK, rect, outline, border_radius=8)
        
        # MENAMPILKAN ANGKA
        number = str(i + 1)
        text_surf = font.render(number, True, cc.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    # UNTUK KOTAK 0
    box_0 = pygame.Rect(start_x + (button_size + gap), start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_0, border_radius=8)
    if box_0.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.BLACK, box_0, outline + 1, border_radius=8)
    else:
        pygame.draw.rect(screen, cc.BLACK, box_0, outline, border_radius=8)
    text_0 = font.render("0", True, cc.BLACK)
    text_0_rect = text_0.get_rect(center=box_0.center)
    screen.blit(text_0, text_0_rect)
    
    # MENGEMBALIKAN SEMUA VALUE RECTANGLE
    return {
        "1": pygame.Rect(start_x + (0 % 3) * (button_size + gap), start_y + (0 // 3) * (button_size + gap), button_size, button_size),
        "2": pygame.Rect(start_x + (1 % 3) * (button_size + gap), start_y + (1 // 3) * (button_size + gap), button_size, button_size),
        "3": pygame.Rect(start_x + (2 % 3) * (button_size + gap), start_y + (2 // 3) * (button_size + gap), button_size, button_size),
        "4": pygame.Rect(start_x + (3 % 3) * (button_size + gap), start_y + (3 // 3) * (button_size + gap), button_size, button_size),
        "5": pygame.Rect(start_x + (4 % 3) * (button_size + gap), start_y + (4 // 3) * (button_size + gap), button_size, button_size),
        "6": pygame.Rect(start_x + (5 % 3) * (button_size + gap), start_y + (5 // 3) * (button_size + gap), button_size, button_size),
        "7": pygame.Rect(start_x + (6 % 3) * (button_size + gap), start_y + (6 // 3) * (button_size + gap), button_size, button_size),
        "8": pygame.Rect(start_x + (7 % 3) * (button_size + gap), start_y + (7 // 3) * (button_size + gap), button_size, button_size),
        "9": pygame.Rect(start_x + (8 % 3) * (button_size + gap), start_y + (8 // 3) * (button_size + gap), button_size, button_size),
        "0": box_0
    }

