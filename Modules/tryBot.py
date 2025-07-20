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
    time.sleep(0.25)
    send(data)

def send(data):

    # MEMBUAT SOCKET
    kirim = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # kirim.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    if varGlobals.udp:
        try:
            kirim.sendto(data, (varGlobals.IP, int(varGlobals.PORT)))
        except Exception as e:
            print("Pengiriman Gagal : ", e)
    else:
        kirim.close()