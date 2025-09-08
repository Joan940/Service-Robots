import time
import socket
import Modules.varGlobals as varGlobals

def demoMode():
    data = bytearray(8)

    data[0] = 1
    data[1] = 200
    data[2] = 2
    data[3] = 5
    data[4] = 2
    data[5] = 5
    data[6] = 0
    data[7] = 1
    # time.sleep(0.25)
    send(data)

def send(data):
    if varGlobals.ser is None or not varGlobals.ser.is_open:
        print("UART tidak aktif / belum dibuka")
        return

    if varGlobals.uart:
        try:
            if isinstance(data, (list, tuple)):
                data = bytes(data)
            elif isinstance(data, int):
                data = data.to_bytes(2, "big")  # contoh: integer 16-bit

            varGlobals.ser.write(data)
            print("[UART] Data terkirim:", list(data))
        except Exception as e:
            print("Pengiriman UART gagal:", e)