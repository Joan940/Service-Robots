import pygame
import sys
import time
import random
import math

# =============================================================================
# KELAS UNTUK MENGELOLA VARIABEL GLOBAL (PENGGANTI varGlobals)
# =============================================================================
class GlobalVars:
    def __init__(self):
        # Pengaturan dasar
        self.res = (800, 600)
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.bgEyes = pygame.Surface(self.res)
        self.bgEyes.fill((200, 200, 255)) # Warna latar belakang biru muda

        # Status program
        self.runEye = True

        # Properti mata & transisi
        self.lebarMata = 100
        self.eyeLeftX = self.res[0] // 2 - 120
        self.eyeRightX = self.res[0] // 2 + 20
        self.eyePosY = self.res[1] // 2 - 100
        self.durasiTransisi = 0.3

        # Variabel state yang diubah di dalam eyeUI
        self.isBlinking = False
        self.startTransisi = 0
        self.startProperties = {}
        self.targetPropertis = {}
        self.SET_AWAL = {}

# Inisialisasi variabel global
varGlobals = GlobalVars()

# =============================================================================
# KONSTANTA WARNA (PENGGANTI cc)
# =============================================================================
class Colors:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

cc = Colors()

# =============================================================================
# DEKLARASI PROPERTI DAN ANIMASI
# =============================================================================
# DEKLARASI AWAL MATA
varGlobals.SET_AWAL = {
    # MATA
    'eyeHeight' : 150,
    'eyeOffsetX': 0,
    'eyeOffsetY': 0,
    
    # ALIS
    'eyebrowOffset_leftY' : 0,
    'eyebrowOffset_rightY': 0,
    'eyebrowAngle_left'   : 0,
    'eyebrowAngle_right'  : 0,

    # MULUT
    'mouthY'      : 0,
    'mouthWidth'  : 0,
    'mouthHeight' : 0,
    'mouthAngle'  : 0,
}

# ANIMASI MATA
ANIMATIONS = {
    'buka': {'eyeHeight': 150, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 0, 'eyebrowOffset_rightY': 0, 'eyebrowAngle_left': 0.1, 'eyebrowAngle_right': -0.1, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 40, 'mouthAngle': 1},
    'kedip': {'eyeHeight': 10, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 0, 'eyebrowOffset_rightY': 0, 'eyebrowAngle_left': 0.1, 'eyebrowAngle_right': -0.1, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 40, 'mouthAngle': 1},
    
    # EKSPRESI
    'marah': {'eyeHeight': 150, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': 15, 'eyebrowOffset_rightY': 15, 'eyebrowAngle_left': 0.3, 'eyebrowAngle_right': -0.3, 'mouthY': 120, 'mouthWidth': 120, 'mouthHeight': 50, 'mouthAngle': 180},
    'sedih': {'eyeHeight': 130, 'eyeOffsetX': 0, 'eyeOffsetY': 30, 'eyebrowOffset_leftY': -10, 'eyebrowOffset_rightY': -10, 'eyebrowAngle_left': -0.3, 'eyebrowAngle_right': 0.3, 'mouthY': 130, 'mouthWidth': 80, 'mouthHeight': 60, 'mouthAngle': 0},
    'terkejut': {'eyeHeight': 180, 'eyeOffsetX': 0, 'eyeOffsetY': 20, 'eyebrowOffset_leftY': -40, 'eyebrowOffset_rightY': -40, 'eyebrowAngle_left': 0, 'eyebrowAngle_right': 0, 'mouthY': 100, 'mouthWidth': 100, 'mouthHeight': 50, 'mouthAngle': 0},
    'senyum': {'eyeHeight': 130, 'eyeOffsetX': 0, 'eyeOffsetY': 10, 'eyebrowOffset_leftY': -15, 'eyebrowOffset_rightY': -15, 'eyebrowAngle_left': -0.2, 'eyebrowAngle_right': 0.2, 'mouthY': 120, 'mouthWidth': 120, 'mouthHeight': 60, 'mouthAngle': 1}
}
varGlobals.ANIMATIONS = ANIMATIONS # Menyimpan ke global vars

# =============================================================================
# FUNGSI PEMBANTU (HELPER FUNCTIONS)
# =============================================================================
def lerp(a, b, t):
    """Interpolasi Linear"""
    return a + (b - a) * t

def easeInOut(t):
    """Fungsi Easing untuk transisi yang lebih halus"""
    return t * t * (3.0 - 2.0 * t)

def rotatePoint(point, center, angle):
    """Memutar sebuah titik di sekitar titik pusat"""
    ox, oy = center
    px, py = point
    
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def mainMenu():
    """Fungsi placeholder jika pengguna menahan klik lama"""
    print("Masuk ke Main Menu...")
    # Di sini Anda bisa menambahkan logika untuk beralih ke layar menu
    # varGlobals.runEye = False # Contoh: menghentikan UI mata
    # menu_function()

# =============================================================================
# FUNGSI UTAMA eyeUI
# =============================================================================
def eyeUI():
    # RESET
    wait = None
    startPos = None
    
    # LOCAL VARIABLE
    blink_interval = random.uniform(3, 6)
    blinkDuration = 0.5
    blinkStartTime = 0

    # Variabel baru untuk melacak aktivitas mouse
    lastMouseActivityTime = time.time()       # Kapan aktivitas mouse terakhir terjadi
    continuousActivityStartTime = None      # Kapan gerakan mouse *terus-menerus* dimulai

    lastBlinkTime = time.time()
    
    # Inisialisasi awal
    varGlobals.startTransisi = time.time()
    varGlobals.startProperties = varGlobals.SET_AWAL.copy()
    varGlobals.targetPropertis = varGlobals.SET_AWAL.copy()

    while varGlobals.runEye:
        # Menambahkan variabel untuk mendeteksi gerakan mouse per frame
        mouseMovedThisFrame = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                varGlobals.runEye = False
                pygame.quit()
                sys.exit()

            # Menambahkan MOUSEMOTION ke dalam kondisi
            # Melacak semua aktivitas mouse (gerakan atau klik)
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                lastMouseActivityTime = time.time() # Update waktu aktivitas terakhir
                mouseMovedThisFrame = True          # Tandai bahwa ada aktivitas di frame ini

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                wait = time.time()
                startPos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Cek apakah klik ditahan lama (untuk masuk menu admin)
                if wait and startPos: # Pastikan wait dan startPos sudah di-set
                    adminSense = time.time() - wait
                    endPos = event.pos
                    dx = endPos[0] - startPos[0]
                    dy = endPos[1] - startPos[1]
                    distance = (dx ** 2 + dy ** 2) ** 0.5

                    if adminSense > 5 and distance < 5:
                        mainMenu()
                
                # Reset setelah mouse dilepas
                wait = None
                startPos = None

        # Memperbarui timer untuk gerakan kontinu
        currentTime = time.time()
        if mouseMovedThisFrame:
            # Jika mouse bergerak dan timer belum dimulai, mulai timer sekarang.
            if continuousActivityStartTime is None:
                continuousActivityStartTime = currentTime
        else:
            # Jika mouse berhenti bergerak di frame ini, reset timer.
            continuousActivityStartTime = None

        # UPDATE POSISI MENGIKUTI MOUSE
        mx, my = pygame.mouse.get_pos()
        center_x = varGlobals.res[0] // 2
        center_y = varGlobals.res[1] // 2
        max_offset = 30
        mouse_offset_x = max(-max_offset, min(max_offset, (mx - center_x) / 10))
        mouse_offset_y = max(-max_offset, min(max_offset, (my - center_y) / 10))
        
        # Simpan offset mouse untuk digabungkan dengan ekspresi nanti
        current_mouse_offset = {'eyeOffsetX': mouse_offset_x, 'eyeOffsetY': mouse_offset_y}

        # RANDOM BLINK
        if time.time() - lastBlinkTime > blink_interval and not varGlobals.isBlinking:
            varGlobals.isBlinking = True
            blinkStartTime = time.time()
            lastBlinkTime = time.time()
            blink_interval = random.uniform(3, 6)

        if varGlobals.isBlinking and time.time() - blinkStartTime > blinkDuration:
            varGlobals.isBlinking = False

        # --- BLOK LOGIKA EKSPRESI BARU ---
        expression_key = 'buka' # Default state adalah 'buka'

        if continuousActivityStartTime is not None:
            # Jika ada aktivitas mouse yang kontinu...
            activityDuration = currentTime - continuousActivityStartTime
            if activityDuration > 5:
                # MARAH: Jika mouse digerakkan terus-menerus > 5 detik
                expression_key = 'marah'
            else:
                # SENYUM: Jika mouse sedang aktif, tapi belum mencapai 5 detik
                expression_key = 'senyum'
        elif currentTime - lastMouseActivityTime > 10:
            # SEDIH: Jika tidak ada aktivitas sama sekali > 10 detik
            expression_key = 'sedih'
        
        # Prioritaskan berkedip di atas ekspresi lain
        if varGlobals.isBlinking:
            expression_key = 'kedip'

        new_expression = varGlobals.ANIMATIONS[expression_key].copy()
        
        # UPDATE KE EKSPRESI BARU
        # Gabungkan offset mouse dengan ekspresi yang dipilih
        final_expression = new_expression.copy()
        final_expression['eyeOffsetX'] += current_mouse_offset['eyeOffsetX']
        final_expression['eyeOffsetY'] += current_mouse_offset['eyeOffsetY']

        if final_expression != varGlobals.targetPropertis:
            varGlobals.startProperties = varGlobals.SET_AWAL.copy()
            varGlobals.targetPropertis = final_expression
            varGlobals.startTransisi = time.time()

        # MENGGUNAKAN RUMUS AGAR LEBIH HALUS
        elapsed = time.time() - varGlobals.startTransisi
        t = min(elapsed / varGlobals.durasiTransisi, 1.0)
        tEased = easeInOut(t)
        for key in varGlobals.targetPropertis:
            varGlobals.SET_AWAL[key] = lerp(
                varGlobals.startProperties.get(key, 0),
                varGlobals.targetPropertis.get(key, 0),
                tEased
            )

        # --- DRAWING SECTION ---
        varGlobals.screen.blit(varGlobals.bgEyes, (0, 0))

        # UPDATE PROPERTI MATA
        tinggiMata = int(varGlobals.SET_AWAL.get('eyeHeight', 0))
        eyeOffsetX_val = varGlobals.SET_AWAL.get('eyeOffsetX', 0)
        eyeOffsetY_val = varGlobals.SET_AWAL.get('eyeOffsetY', 0)
        
        eyeLeftX = varGlobals.eyeLeftX + eyeOffsetX_val
        eyeRightX = varGlobals.eyeRightX + eyeOffsetX_val
        eyePosY = varGlobals.eyePosY + eyeOffsetY_val

        eyeLeft = pygame.Rect(eyeLeftX, eyePosY, varGlobals.lebarMata, tinggiMata)
        eyeRight = pygame.Rect(eyeRightX, eyePosY, varGlobals.lebarMata, tinggiMata)

        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeLeft, border_radius=50)
        pygame.draw.rect(varGlobals.screen, cc.BLACK, eyeRight, border_radius=50)

        # UPDATE PROPERTI MULUT
        mouthY_val = varGlobals.SET_AWAL.get('mouthY', 0)
        mouthWidth_val = varGlobals.SET_AWAL.get('mouthWidth', 0)
        mouthHeight_val = varGlobals.SET_AWAL.get('mouthHeight', 0)
        mouthAngle_val = varGlobals.SET_AWAL.get('mouthAngle', 0)
        
        if mouthWidth_val > 0 and mouthHeight_val > 0:
            mouth_pos_y = varGlobals.res[1] // 2 + mouthY_val
            mouth_rect = pygame.Rect(varGlobals.res[0] // 2 - (mouthWidth_val // 2), mouth_pos_y, mouthWidth_val, mouthHeight_val)
            
            if mouthAngle_val == 1: # Senyum
                start_angle = math.pi
                end_angle = 2 * math.pi
                pygame.draw.arc(varGlobals.screen, cc.BLACK, mouth_rect, start_angle, end_angle, 10)
            elif mouthAngle_val == 180: # Marah (garis lurus)
                start_point = (mouth_rect.left, mouth_rect.centery)
                end_point = (mouth_rect.right, mouth_rect.centery)
                pygame.draw.line(varGlobals.screen, cc.BLACK, start_point, end_point, 10)
            else: # Sedih / Terkejut
                start_angle = 0
                end_angle = math.pi
                pygame.draw.arc(varGlobals.screen, cc.BLACK, mouth_rect, start_angle, end_angle, 10)
        
        # MENGGAMBAR ALIS
        eyebrowOffset_leftY = varGlobals.SET_AWAL.get('eyebrowOffset_leftY', 0)
        eyebrowOffset_rightY = varGlobals.SET_AWAL.get('eyebrowOffset_rightY', 0)
        eyebrowAngle_left = varGlobals.SET_AWAL.get('eyebrowAngle_left', 0)
        eyebrowAngle_right = varGlobals.SET_AWAL.get('eyebrowAngle_right', 0)
        
        eyebrow_start_left = (eyeLeft.centerx - varGlobals.lebarMata / 2 - 10, eyeLeft.top - 20 + eyebrowOffset_leftY)
        eyebrow_end_left = (eyeLeft.centerx + varGlobals.lebarMata / 2 + 10, eyeLeft.top - 20 + eyebrowOffset_leftY)
        eyebrow_start_right = (eyeRight.centerx - varGlobals.lebarMata / 2 - 10, eyeRight.top - 20 + eyebrowOffset_rightY)
        eyebrow_end_right = (eyeRight.centerx + varGlobals.lebarMata / 2 + 10, eyeRight.top - 20 + eyebrowOffset_rightY)

        rotated_start_left = rotatePoint(eyebrow_start_left, eyeLeft.center, eyebrowAngle_left)
        rotated_end_left = rotatePoint(eyebrow_end_left, eyeLeft.center, eyebrowAngle_left)
        pygame.draw.line(varGlobals.screen, cc.BLACK, rotated_start_left, rotated_end_left, 10)

        rotated_start_right = rotatePoint(eyebrow_start_right, eyeRight.center, eyebrowAngle_right)
        rotated_end_right = rotatePoint(eyebrow_end_right, eyeRight.center, eyebrowAngle_right)
        pygame.draw.line(varGlobals.screen, cc.BLACK, rotated_start_right, rotated_end_right, 10)

        # UPDATE TAMPILAN
        varGlobals.clock.tick(60)
        pygame.display.flip()

# =============================================================================
# BLOK EKSEKUSI UTAMA
# =============================================================================
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Interactive Eye UI")
    eyeUI()
    pygame.quit()
    sys.exit()