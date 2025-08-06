import pygame
import time
import math

# --- Setup Pygame ---
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eye Animations on Screen (Rectangle)")
clock = pygame.time.Clock()

# --- Warna ---
class cc:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (150, 150, 150)
    
# --- Fungsi Utilitas ---
def lerp(start, end, t):
    """Interpolasi Linier untuk transisi halus."""
    return start + (end - start) * t

def ease_in_out(t):
    """Fungsi easing (melambat) untuk membuat transisi lebih alami."""
    return t * t * (3.0 - 2.0 * t)

# --- Properti Mata ---
current_properties = {
    'eye_open_y': 100,   # Tinggi mata saat terbuka
}

target_properties = current_properties.copy()
start_properties = current_properties.copy()

transition_duration = 0.5
transition_start_time = time.time()

# --- Animasi (Menggantikan case Arduino) ---
ANIMATIONS = {
    0: {'eye_open_y': 100},  # wakeup / mata normal
    1: {'eye_open_y': 100},  # center_eyes
    2: {'eye_open_y': 100},  # move_right
    3: {'eye_open_y': 100},  # move_left
    4: {'eye_open_y': 0},    # blink
    5: {'eye_open_y': 100},  # happy_eye
    6: {'eye_open_y': 0}     # sleep
}

def set_animation(index):
    global start_properties, target_properties, transition_start_time
    start_properties = current_properties.copy()
    target_properties = ANIMATIONS.get(index, ANIMATIONS[0]).copy()
    transition_start_time = time.time()

# --- Main Loop ---
current_animation_index = 0
last_animation_change_time = time.time()
set_animation(current_animation_index)

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ganti animasi setiap 2 detik (meniru for loop Arduino)
    if time.time() - last_animation_change_time > 0.5:
        current_animation_index = (current_animation_index + 1) % len(ANIMATIONS)
        set_animation(current_animation_index)
        last_animation_change_time = time.time()
        
    # --- Transisi Properti ---
    # BUG FIX: Perbaikan pada perhitungan waktu yang telah berlalu
    elapsed = time.time() - transition_start_time
    t = min(elapsed / transition_duration, 1.0)
    
    # Gunakan easing untuk transisi yang lebih halus
    t_eased = ease_in_out(t)
    
    for key in target_properties:
        current_properties[key] = lerp(start_properties.get(key, 0), target_properties[key], t_eased)

    # --- Menggambar di Layar ---
    screen.fill(cc.GRAY)

    # Posisi mata
    eye_width = 200
    eye_height = int(current_properties['eye_open_y'])
    eye_left_x = 150
    eye_right_x = 450
    eye_y = SCREEN_HEIGHT // 2 - eye_height // 2

    # Gambar mata kiri dan kanan
    eye_rect_left = pygame.Rect(eye_left_x, eye_y, eye_width, eye_height)
    eye_rect_right = pygame.Rect(eye_right_x, eye_y, eye_width, eye_height)
    
    pygame.draw.rect(screen, cc.WHITE, eye_rect_left)
    pygame.draw.rect(screen, cc.WHITE, eye_rect_right)
    pygame.draw.rect(screen, cc.BLACK, eye_rect_left, 5)
    pygame.draw.rect(screen, cc.BLACK, eye_rect_right, 5)

    # Tampilkan teks animasi saat ini
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Animation Index: {current_animation_index}", True, cc.BLACK)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()