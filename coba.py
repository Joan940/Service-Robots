# --- hanya tampilkan meja terpilih ---
meja_list = [m for m in varGlobals.allMeja if m['meja'] == selected_meja]

# reset checkboxes setiap kali meja berubah
varGlobals.checkboxes = []

for meja_data in meja_list:
    nomor_meja = meja_data['meja']
    pesanan_lines = getPesananByMeja(varGlobals.allOrders, nomor_meja)

    # Judul meja
    title_surface = varGlobals.font.render(f"Meja {nomor_meja}", True, cc.BRIGHT_YELLOW)
    varGlobals.screen.blit(title_surface, (start_x, start_y))

    # Daftar pesanan
    pesanan_idx = 0
    for line in pesanan_lines:
        if line['type'] == 'meja':
            continue

        rect_custom = line['rect'].copy()
        rect_custom.topleft = (start_x + 40, start_y + (pesanan_idx+1) * offset_y)

        # tambahkan checkbox baru
        cb = CheckBox(start_x, start_y + (pesanan_idx+1) * offset_y,
                      size=25,
                      label=line['surface'].get_text() if hasattr(line['surface'], 'get_text') else None,
                      font=varGlobals.font)
        varGlobals.checkboxes.append(cb)

        # gambar label pesanan
        varGlobals.screen.blit(line['surface'], rect_custom)

        pesanan_idx += 1

    start_y += (pesanan_idx + 1) * offset_y + offset_meja

# --- gambar semua checkbox ---
for cb in varGlobals.checkboxes:
    cb.draw(varGlobals.screen)
