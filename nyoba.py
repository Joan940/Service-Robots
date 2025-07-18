import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Mendapatkan resolusi layar
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
res = (screen_width, screen_height)

# Pengaturan layar
screen = pygame.display.set_mode(res)
pygame.display.set_caption("Visualisasi Offset")

# Variabel Offset
offsetX = res[0] / 6
offsetY = res[1] / 20
skala = res[1] / 1200

# Warna untuk garis
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Pembuatan clock
clock = pygame.time.Clock()

# Loop utama
running = True
while running:
    screen.fill((0, 0, 0))  # Mengisi layar dengan warna hitam

    # Menggambar garis horizontal berdasarkan offsetY
    pygame.draw.line(screen, RED, (0, offsetY), (res[0], offsetY), 2)  # Garis horizontal di offsetY

    # Menggambar garis vertikal berdasarkan offsetX
    pygame.draw.line(screen, RED, (offsetX, 0), (offsetX, res[1]), 2)  # Garis vertikal di offsetX

    # Menampilkan offset di layar
    font = pygame.font.Font(None, 36)
    text_offsetX = font.render(f"OffsetX: {offsetX}", True, WHITE)
    text_offsetY = font.render(f"OffsetY: {offsetY}", True, WHITE)

    screen.blit(text_offsetX, (10, 10))
    screen.blit(text_offsetY, (10, 50))

    # Mengupdate layar
    pygame.display.flip()

    # Menangani event keluar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mengatur FPS
    clock.tick(60)

# Menutup Pygame
pygame.quit()
sys.exit()
