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
    
    # CEK APAKAH MEJA SUDAH ADA DALAM ARRAY, JIKA BELUM MEJA AKAN DIMASUKKAN
    grouped_orders = {}
    for pesanan_data in orders_list:
        meja = pesanan_data[1]
        namaPesanan = pesanan_data[3]
        jumlahPesanan = pesanan_data[4]
        
        if meja not in grouped_orders:
            grouped_orders[meja] = []
        grouped_orders[meja].append({'nama': namaPesanan, 'jumlah': jumlahPesanan})

    total_height = 0
    ySpacing = 10
    
    for meja, items in grouped_orders.items():
        group_height = 0
        text_surf_meja, text_rect_meja = tts2(f"{meja}", cc.WHITE, 40, (0, 0))
        group_height += text_rect_meja.height
        
        for item in items:
            text_surf_pesanan, text_rect_pesanan = tts2(f"- {item['nama']} ({item['jumlah']})", cc.BLACK, 18, (0, 0))
            group_height += text_rect_pesanan.height + ySpacing
        
        # MENAMBAHKAN SPASI TIAP PESANAN BERDASARKAN NOMOR MEJA
        total_height += group_height + (ySpacing * 3)
    
    # Menghitung posisi Y awal agar tampilan berada di tengah
    popup_y = 110
    yStart = popup_y + (group_height - total_height // 2)
    
    # INI DIGUNAKAN UNTUK MENGEMBALIKAN VALUE
    for meja, items in grouped_orders.items():
        group_height = 0
        group_lines = []

        text_surf_meja, text_rect_meja = tts2(f"{meja}", cc.WHITE, 40, (120, yStart))
        # print(f"yStart : {yStart}")

        group_lines.append({'type': 'meja', 'surface': text_surf_meja, 'rect': text_rect_meja})
        group_height += text_rect_meja.height
        
        for item in items:
            text_surf_pesanan, text_rect_pesanan = tts2(f"- {item['nama']} ({item['jumlah']})", cc.BLACK, 18, (200, (yStart + group_height)))
            group_lines.append({'type': 'pesanan', 'surface': text_surf_pesanan, 'rect': text_rect_pesanan})
            group_height += text_rect_pesanan.height + ySpacing
        
        orderStack.append({'meja': meja, 'height': group_height, 'lines': group_lines})
        yStart += group_height + (ySpacing * 3) - 70
            
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