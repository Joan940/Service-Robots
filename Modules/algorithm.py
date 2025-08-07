import time
import math
import pygame
import Modules.varGlobals as varGlobals
from Modules.colors import custom as cc, tts2


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

def drawNumberPad(screen, popup_x, popup_y):
    button_size = 50
    gap = 10
    start_x = popup_x + varGlobals.lebarPopup + 20
    start_y = popup_y + 100

    # UNTUK KOTAK DARI 1 - 9
    for i in range(9):
        x = start_x + (i % 3) * (button_size + gap)
        y = start_y + (i // 3) * (button_size + gap)
        rect = pygame.Rect(x, y, button_size, button_size)
        pygame.draw.rect(screen, cc.WHITE, rect, border_radius=8)
        pygame.draw.rect(screen, cc.BLACK, rect, 3, border_radius=8)
        
        # MENAMPILKAN ANGKA
        number = str(i + 1)
        text_surf = varGlobals.font.render(number, True, cc.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    # UNTUK KOTAK 0
    box_0 = pygame.Rect(start_x + (button_size + gap), start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_0, border_radius=8)
    pygame.draw.rect(screen, cc.BLACK, box_0, 3, border_radius=8)
    text_0 = varGlobals.font.render("0", True, cc.BLACK)
    text_0_rect = text_0.get_rect(center=box_0.center)
    screen.blit(text_0, text_0_rect)

    # UNTUK KOTAK DELETE
    box_del = pygame.Rect(start_x + 0, start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_del, border_radius=8)
    pygame.draw.rect(screen, cc.BLACK, box_del, 3, border_radius=8)
    text_del = varGlobals.font.render("Del", True, cc.BLACK)
    text_del_rect = text_del.get_rect(center=box_del.center)
    screen.blit(text_del, text_del_rect)

    # UNTUK KOTAK CLEAR
    box_clear = pygame.Rect(start_x + (button_size + gap) * 2, start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_clear, border_radius=8)
    pygame.draw.rect(screen, cc.BLACK, box_clear, 3, border_radius=8)
    text_clear = varGlobals.font.render("Clear", True, cc.BLACK)
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

def tamilanOrder(orders_list):
    orderStack = []
    yStart = 500
    ySpacing = 2
    
    # CEK APAKAH MEJA SUDAH ADA DALAM ARRAY, JIKA BELUM MEJA AKAN DIMAKSUKKAN
    grouped_orders = {}
    for pesanan_data in orders_list:
        meja = pesanan_data[1]
        namaPesanan = pesanan_data[3]
        jumlahPesanan = pesanan_data[4]
        
        if meja not in grouped_orders:
            grouped_orders[meja] = []
        grouped_orders[meja].append({'nama': namaPesanan, 'jumlah': jumlahPesanan})

    # INI DIGUNAKAN UNTUK MENGEMBALIKAN VALUE
    for meja, items in grouped_orders.items():
        group_height = 0
        group_lines = []

        # Baris untuk nomor meja
        text_surf_meja, text_rect_meja = tts2(f"{meja}", cc.BLACK, 60, (1350, yStart))
        group_lines.append({'type': 'meja', 'surface': text_surf_meja, 'rect': text_rect_meja})
        
        # Baris untuk setiap pesanan
        for item in items:
            text_surf_pesanan, text_rect_pesanan = tts2(f"- {item['nama']} ({item['jumlah']})", cc.BLACK, 20, (1420, yStart + group_height - 26))
            group_lines.append({'type': 'pesanan', 'surface': text_surf_pesanan, 'rect': text_rect_pesanan})
            group_height += text_rect_pesanan.height + ySpacing
            
        # Simpan seluruh grup ke dalam orderStack
        orderStack.append({'meja': meja, 'height': group_height, 'lines': group_lines})
        yStart += group_height + (ySpacing * 2)
            
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