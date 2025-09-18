# import serial
# import threading
# import time

# class VarGlobals:
#     ser_tx = None   # TX (pengirim)
#     ser_rx = None   # RX (penerima)
#     uart = False

# varGlobals = VarGlobals()

# # ==============================
# # INIT UART
# # ==============================
# def init_uart(port_tx="COM14", port_rx="COM15", baudrate=115200):
#     try:
#         varGlobals.ser_tx = serial.Serial(port_tx, baudrate, timeout=0.25)
#         varGlobals.ser_rx = serial.Serial(port_rx, baudrate, timeout=0.25)
#         print(f"[UART] Port TX: {varGlobals.ser_tx.name}, Port RX: {varGlobals.ser_rx.name}")
#     except Exception as e:
#         print("[UART] Gagal buka port:", e)

# # ==============================
# # TERIMA DATA dari RX
# # ==============================
# def receive():
#     while varGlobals.uart:
#         try:
#             if varGlobals.ser_rx and varGlobals.ser_rx.in_waiting > 0:
#                 data = varGlobals.ser_rx.read(varGlobals.ser_rx.in_waiting)
#                 print("[UART RX] Data diterima:", list(data))
#         except Exception as e:
#             print("[UART] Error saat baca:", e)
#         time.sleep(0.05)

# # ==============================
# # JALANKAN THREAD RECEIVE
# # ==============================
# def runCom():
#     if varGlobals.ser_tx is None or not varGlobals.ser_tx.is_open:
#         init_uart()
#     varGlobals.uart = True
#     threading.Thread(target=receive, daemon=True).start()
#     print("[UART] Thread RX aktif")

# # ==============================
# # KIRIM DATA lewat TX
# # ==============================
# def send(data):
#     if varGlobals.ser_tx is None or not varGlobals.ser_tx.is_open:
#         print("[UART] TX tidak aktif / belum dibuka")
#         return

#     if varGlobals.uart:
#         try:
#             if isinstance(data, (list, tuple)):
#                 data = bytes(data)
#             elif isinstance(data, int):
#                 data = data.to_bytes(2, "big")  # default 16-bit

#             varGlobals.ser_tx.write(data)
#             print("[UART TX] Data terkirim:", list(data))
#         except Exception as e:
#             print("[UART] Gagal kirim:", e)

# # ==============================
# # MAIN PROGRAM
# # ==============================
# if __name__ == "__main__":
#     # COM14 kirim → COM15 terima
#     init_uart("COM14", "COM15", 115200)
#     runCom()

#     try:
#         while True:
#             packet = [1, 2, 3, 4, 5]
#             send(packet)
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\n[UART] Program dihentikan")
#         varGlobals.uart = False
#         if varGlobals.ser_tx: varGlobals.ser_tx.close()
#         if varGlobals.ser_rx: varGlobals.ser_rx.close()

#################################################
#                   trayPesanan                 #
#################################################

# # MENAMPILKAN PESANAN BERDASARKAN MEJA
        # if trayPesanan:

        #     if not varGlobals.checkboxes:   # hanya buat sekali
        #         pesanan_lines = getPesananByMeja(varGlobals.allOrders, selectedMeja)

        #         varGlobals.checkboxes = []
        #         start_x = scButton.BOX_SETUP.x + 30
        #         start_y = scButton.BOX_SETUP.y + 40
        #         offset_y = 35

        #         pesanan_idx = 0
        #         for line in pesanan_lines:
        #             if line['type'] == 'meja':
        #                 continue

        #             rect_custom = line['rect'].copy()
        #             rect_custom.topleft = (start_x + 40, start_y + (pesanan_idx + 1) * offset_y)

        #             cb = CheckBox(start_x, rect_custom.y + 2, 20, False, None, varGlobals.font)
        #             cb.data_id = line['id']
        #             cb.label = getattr(line, 'menu', str(line.get('id')))
        #             varGlobals.checkboxes.append(cb)

        #             pesanan_idx += 1

        #     # MENGGAMBAR OVERLAY (OPACITY)
        #     overlay = pygame.Surface((varGlobals.res[0], varGlobals.res[1]), pygame.SRCALPHA)
        #     pygame.draw.rect(overlay, (0, 0, 0, 100), overlay.get_rect())
        #     varGlobals.screen.blit(overlay, (0, 0))

        #     pygame.draw.rect(varGlobals.screen, cc.WHITE, scButton.BOX_SETUP, border_radius=20)
        #     pygame.draw.rect(varGlobals.screen, cc.BLACK, scButton.BOX_SETUP, 3, border_radius=20)
            
        #     for penyesuaian, rect in adjust.items():
        #         if rect.collidepoint(mx, my):
        #             pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 4, border_radius=20)
        #             tts(penyesuaian, cc.RED_BROWN, rect, varGlobals.screen, 35)
        #         else:
        #             pygame.draw.rect(varGlobals.screen, cc.RED_BROWN, rect, 3, border_radius=20)
        #             tts(penyesuaian, cc.RED_BROWN, rect, varGlobals.screen, 30)

        #     tts(antar, cc.RED_BROWN, scButton.TOTAL, varGlobals.screen, 25)

        #     for boxes, rect in box.items():
        #         if rect.collidepoint(mx, my):
        #             pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
        #             pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 4, border_radius=20)
        #             tts(boxes, cc.BLACK, rect, varGlobals.screen, 30)
        #         else:
        #             pygame.draw.rect(varGlobals.screen, cc.WHITE, rect, border_radius=20)
        #             pygame.draw.rect(varGlobals.screen, cc.BLACK, rect, 3, border_radius=20)
        #             tts(boxes, cc.BLACK, rect, varGlobals.screen, 25)

        #     # MENEMPATKAN TEXT PADA SAMPING CHECKBOXS
        #     mejaList = [m for m in varGlobals.allMeja if m == selectedMeja]
        #     startX = scButton.BOX_SETUP.x + 30
        #     startY = scButton.BOX_SETUP.y + 40
        #     offsetY = 35
        #     offsetMeja = 50

        #     for mejaData in mejaList:
        #         nomor_meja = mejaData
        #         pesanan_lines = getPesananByMeja(varGlobals.allOrders, nomor_meja)

        #         title_surface = varGlobals.font.render(f"Meja {nomor_meja}", True, cc.BLACK)
        #         varGlobals.screen.blit(title_surface, (startX, startY - 20))

        #         pesanan_idx = 0
        #         for line, cb in zip([l for l in pesanan_lines if l['type'] != 'meja'], varGlobals.checkboxes):
        #             rect_custom = line['rect'].copy()
        #             rect_custom.topleft = (startX + 40, startY + (pesanan_idx + 1) * offsetY)

        #             # gambar teks
        #             varGlobals.screen.blit(line['surface'], rect_custom)

        #             # gambar checkbox
        #             cb.draw(varGlobals.screen)
        #             pesanan_idx += 1

        #         startY += (pesanan_idx + 1) * offsetY + offsetMeja


# # PENANGANAN POPUP PESANAN BERDASARKAN MEJA
                # elif trayPesanan:
                #     if scButton.BACK.collidepoint(mx, my) and trayPesanan and not trayMeja:
                #         trayPesanan = False
                #         trayMeja = True

                #     # PENANGANAN TOMBOL KONFIRMASI
                #     elif scButton.BOX_KONFIRMASI.collidepoint(mx, my):
                #         selected_ids = [cb.data_id for cb in varGlobals.checkboxes if cb.checked]

                #         if selected_ids:
                #             delete_orders(selected_ids)
                #             print("Terhapus:", selected_ids)

                #             # Refresh data
                #             varGlobals.allOrders = getOrders()
                #             varGlobals.allOrders = tampilanOrder(varGlobals.allOrders)
                #             varGlobals.checkboxes = []

                #     elif scButton.PLUS.collidepoint(mx, my):
                #         antar += 1
                #     elif scButton.MIN.collidepoint(mx, my):
                #             if antar > 0:
                #                 antar -= 1
                #             else:
                #                 pass