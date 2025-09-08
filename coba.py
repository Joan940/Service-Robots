import serial
import threading
import time

class VarGlobals:
    ser_tx = None   # TX (pengirim)
    ser_rx = None   # RX (penerima)
    uart = False

varGlobals = VarGlobals()

# ==============================
# INIT UART
# ==============================
def init_uart(port_tx="COM14", port_rx="COM15", baudrate=115200):
    try:
        varGlobals.ser_tx = serial.Serial(port_tx, baudrate, timeout=0.25)
        varGlobals.ser_rx = serial.Serial(port_rx, baudrate, timeout=0.25)
        print(f"[UART] Port TX: {varGlobals.ser_tx.name}, Port RX: {varGlobals.ser_rx.name}")
    except Exception as e:
        print("[UART] Gagal buka port:", e)

# ==============================
# TERIMA DATA dari RX
# ==============================
def receive():
    while varGlobals.uart:
        try:
            if varGlobals.ser_rx and varGlobals.ser_rx.in_waiting > 0:
                data = varGlobals.ser_rx.read(varGlobals.ser_rx.in_waiting)
                print("[UART RX] Data diterima:", list(data))
        except Exception as e:
            print("[UART] Error saat baca:", e)
        time.sleep(0.05)

# ==============================
# JALANKAN THREAD RECEIVE
# ==============================
def runCom():
    if varGlobals.ser_tx is None or not varGlobals.ser_tx.is_open:
        init_uart()
    varGlobals.uart = True
    threading.Thread(target=receive, daemon=True).start()
    print("[UART] Thread RX aktif")

# ==============================
# KIRIM DATA lewat TX
# ==============================
def send(data):
    if varGlobals.ser_tx is None or not varGlobals.ser_tx.is_open:
        print("[UART] TX tidak aktif / belum dibuka")
        return

    if varGlobals.uart:
        try:
            if isinstance(data, (list, tuple)):
                data = bytes(data)
            elif isinstance(data, int):
                data = data.to_bytes(2, "big")  # default 16-bit

            varGlobals.ser_tx.write(data)
            print("[UART TX] Data terkirim:", list(data))
        except Exception as e:
            print("[UART] Gagal kirim:", e)

# ==============================
# MAIN PROGRAM
# ==============================
if __name__ == "__main__":
    # COM14 kirim → COM15 terima
    init_uart("COM14", "COM15", 115200)
    runCom()

    try:
        while True:
            packet = [1, 2, 3, 4, 5]
            send(packet)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[UART] Program dihentikan")
        varGlobals.uart = False
        if varGlobals.ser_tx: varGlobals.ser_tx.close()
        if varGlobals.ser_rx: varGlobals.ser_rx.close()
