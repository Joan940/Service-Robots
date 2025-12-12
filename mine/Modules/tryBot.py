import time
import socket
import Modules.varGlobals as varGlobals

def send(data):

    kirim = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if varGlobals.udp:
        try:
            kirim.sendto(data, (varGlobals.IP, int(varGlobals.PORT)))
        except Exception as e:
            print("Pengiriman Gagal : ", e)
    else:
        kirim.close()