import time
import math
import heapq
import pygame
import numpy as np
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
    box_back = pygame.Rect(start_x + 0, start_y + (button_size + gap) * 3, button_size, button_size)
    pygame.draw.rect(screen, cc.WHITE, box_back, border_radius=8)
    if box_back.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.BLACK, box_back, outline + 1, border_radius=8)
    else:
        pygame.draw.rect(screen, cc.BLACK, box_back, outline, border_radius=8)
    text_del = font.render("Del", True, cc.BLACK)
    text_del_rect = text_del.get_rect(center=box_back.center)
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
        "Del": box_back,
        "Clear": box_clear
    }


###################################################################################################
#                                       MENAMPILKAN PESANAN                                       #
###################################################################################################

def tampilanOrder(orders_list):
    orderStack = []
    ySpacing = 10
    box_lebar_kiri = 80
    padding_text = 120

    grouped_orders = {}
    for pesanan_data in orders_list:
        pesanan_id = pesanan_data[0]
        meja = pesanan_data[1]
        namaPesanan = pesanan_data[3]
        jumlahPesanan = pesanan_data[4]

        if meja not in grouped_orders:
            grouped_orders[meja] = []
        grouped_orders[meja].append({
            'id': pesanan_id,
            'nama': namaPesanan,
            'jumlah': jumlahPesanan
        })

    yStart = 80

    for meja, items in grouped_orders.items():
        group_lines = []
        group_height = 0

        # Tampilkan nomor meja
        text_surf_meja, text_rect_meja = tts2(
            f"{meja}", cc.WHITE, 40, (padding_text, yStart + 60)
        )
        group_lines.append({
            'type': 'meja',
            'surface': text_surf_meja,
            'rect': text_rect_meja
        })
        group_height += text_rect_meja.height + ySpacing

        # Tampilkan daftar pesanan
        pesanan_x = box_lebar_kiri + padding_text
        for item in items:
            text_surf_pesanan, text_rect_pesanan = tts2(
                f"{item['nama']} ({item['jumlah']})",
                cc.BLACK, 18, (pesanan_x, yStart + group_height)
            )
            group_lines.append({
                'type': 'pesanan',
                'id': item['id'],
                'nama': item['nama'],        # tambahin nama
                'jumlah': item['jumlah'],    # tambahin jumlah
                'surface': text_surf_pesanan,
                'rect': text_rect_pesanan
            })

            group_height += text_rect_pesanan.height + ySpacing

        orderStack.append({
            'meja': meja,
            'height': group_height,
            'lines': group_lines
        })

        # Pindahkan ke bawah untuk meja berikutnya
        yStart += group_height - 20

    return orderStack


###################################################################################################
#                                            HEURISTIC                                            #
###################################################################################################

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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

    # Tambahkan ini di awal skrip Anda
    table_positions = {
        1: (4, 2),
        2: (3, 3),
        4: (6, 6),
        5: (10, 7),
        6: (12, 1)
    }

    # Menggunakan set untuk mendapatkan nomor meja yang unik secara efisien
    unique_meja_numbers = set()
    for pesanan_data in orders_list:
        meja = pesanan_data[1]
        unique_meja_numbers.add(meja)
    
    # Membuat kamus baru sesuai format yang diinginkan
    all_meja_with_positions = {}
    for meja in unique_meja_numbers:
        # Periksa apakah nomor meja memiliki posisi yang telah ditentukan
        if meja in table_positions:
            all_meja_with_positions[meja] = table_positions[meja]
    
    return all_meja_with_positions


###################################################################################################
#                                         NUMPAD FOR STAFF                                        #
###################################################################################################

# def getPesananByMeja(orders_list, nomor_meja):
#     for pesanan_data in orders_list:
#         if isinstance(pesanan_data, dict) and pesanan_data.get('meja') == nomor_meja:
#             return pesanan_data['lines']
    
#     return []


###################################################################################################
#                                    GET NAMA & JUMLAH PESANAN                                    #
###################################################################################################

# def getNamaJumlahPesanan(orders_list):
#     nama_list = []
#     jumlah_list = []

#     for meja_data in orders_list:
#         for line in meja_data["lines"]:
#             if line["type"] == "pesanan":
#                 nama_list.append(line["nama"])
#                 jumlah_list.append(line["jumlah"])

#     return nama_list, jumlah_list


###################################################################################################
#                                         NUMPAD FOR STAFF                                        #
###################################################################################################

def numpadStaff(screen, popup_x, popup_y, outline):
    button_size = 100
    gap = 10
    start_x = popup_x + 5
    start_y = popup_y - 45

    font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 25)
    mx, my = pygame.mouse.get_pos()

    # UNTUK KOTAK DARI 1 - 9
    for i in range(9):
        x = start_x + (i % 3) * (button_size + gap)
        y = start_y + (i // 3) * (button_size + gap)
        rect = pygame.Rect(x, y, button_size, button_size)
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
    box_0 = pygame.Rect(start_x + (button_size + gap) * 3, start_y + (button_size + gap) * 2, button_size, button_size)
    if box_0.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.BLACK, box_0, outline + 1, border_radius=8)
    else:
        pygame.draw.rect(screen, cc.BLACK, box_0, outline, border_radius=8)
    text_0 = font.render("0", True, cc.BLACK)
    text_0_rect = text_0.get_rect(center=box_0.center)
    screen.blit(text_0, text_0_rect)

    # UNTUK KOTAK BACK
    box_back = pygame.Rect(start_x + (button_size + gap) * 3, start_y, button_size, button_size * 2 + gap)
    if box_back.collidepoint(mx, my):
        pygame.draw.rect(screen, cc.RED_BROWN, box_back, border_radius=8)
        font = pygame.font.Font("C:\BMP-Robotics\Assets\Oregano-Regular.ttf", 30)
    else:
        pygame.draw.rect(screen, cc.RED_BROWN, box_back, border_radius=8)
    text_del = font.render("Back", True, cc.WHITE)
    text_del_rect = text_del.get_rect(center=box_back.center)
    screen.blit(text_del, text_del_rect)
    
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
        "Back": box_back
    }


###################################################################################################
#                                            DRAW GRID                                            #
###################################################################################################

def drawGrid(grid_size):

    ox = varGlobals.offsetX
    oy = varGlobals.offsetY

    # --- Area 1: Persegi panjang vertikal di KIRI ---
    area1_x_start = int(ox)
    area1_x_end = int(300 + ox)  # Batas kanan area kiri (~378)
    area1_y_start = int(oy)      # Batas atas (~217)
    area1_y_end = int(300 + oy)  # Batas bawah (~517)

    # Menggambar garis vertikal di Area 1
    for x in range(area1_x_start, area1_x_end + 1, grid_size):
        pygame.draw.line(varGlobals.screen, cc.DARK_GREY, (x, area1_y_start), (x, area1_y_end))
        
    # Menggambar garis horizontal di Area 1
    for y in range(area1_y_start, area1_y_end + 1, grid_size):
        pygame.draw.line(varGlobals.screen, cc.DARK_GREY, (area1_x_start, y), (area1_x_end, y))

    # --- Area 2: Persegi panjang horizontal di KANAN BAWAH ---
    area2_x_start = int(300 + ox)   # Mulai dari tempat Area 1 berakhir
    area2_x_end = int(500 + ox)     # Batas kanan map (~578)
    area2_y_start = int(100 + oy)   # Batas atas area ini (~317)
    area2_y_end = int(300 + oy)     # Batas bawah map (~517)
    
    # Menggambar garis vertikal di Area 2
    for x in range(area2_x_start, area2_x_end + 1, grid_size):
        pygame.draw.line(varGlobals.screen, cc.DARK_GREY, (x, area2_y_start), (x, area2_y_end))
        
    # Menggambar garis horizontal di Area 2
    for y in range(area2_y_start, area2_y_end + 1, grid_size):
        pygame.draw.line(varGlobals.screen, cc.DARK_GREY, (area1_x_start, y), (area2_x_end, y))


###################################################################################################
#                                          DRAW CHECKBOX                                          #
###################################################################################################

class CheckBox:
    def __init__(self, x, y, size=1000, checked=False, label=None, font=None, color_box=cc.WHITE, color_tick=cc.GREEN):
        self.rect = pygame.Rect(x, y, size, size)
        self.checked = checked
        self.label = label
        self.font = font
        self.color_box = color_box
        self.color_tick = color_tick

    def draw(self, surface):
        # kotak
        pygame.draw.rect(surface, self.color_box, self.rect, border_radius=5)
        pygame.draw.rect(surface, cc.BLACK, self.rect, 2, border_radius=5)

        # tanda centang
        if self.checked:
            pygame.draw.rect(surface, self.color_tick, self.rect.inflate(-6, -6), border_radius=5)

        # label teks
        if self.label and self.font:
            text_surface = self.font.render(self.label, True, cc.WHITE)
            surface.blit(text_surface, (self.rect.right+10, self.rect.y))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                return True
        return False
    

###################################################################################################
#                                          A* ALGORITHM                                           #
###################################################################################################

# def aStar(start, goal):

#     # DRAW MAP
#     map = np.array([
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     ])

#     grid_rows, grid_cols = map.shape
#     open_set = []
#     heapq.heappush(open_set, (0, start))
#     came_from = {}
#     g_score = { (x, y): float('inf') for y in range(grid_rows) for x in range(grid_cols) }
#     g_score[start] = 0
#     f_score = { (x, y): float('inf') for y in range(grid_rows) for x in range(grid_cols) }
#     f_score[start] = heuristic(start, goal)

#     while open_set:
#         current_f, current = heapq.heappop(open_set)

#         if current == goal:
#             path = []
#             while current in came_from:
#                 path.append(current)
#                 current = came_from[current]
#             path.append(start)
#             return path[::-1]

#         for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#             neighbor = (current[0] + dx, current[1] + dy)
            
#             # Periksa apakah tetangga valid dan bisa dilewati (nilai 1)
#             if 0 <= neighbor[0] < grid_cols and 0 <= neighbor[1] < grid_rows and map[neighbor[1], neighbor[0]] == 1:
#                 tentative_g_score = g_score[current] + 1

#                 if tentative_g_score < g_score.get(neighbor, float('inf')):
#                     came_from[neighbor] = current
#                     g_score[neighbor] = tentative_g_score
#                     f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
#                     heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
#     return None # Tidak ada jalur yang ditemukan