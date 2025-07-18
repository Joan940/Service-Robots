import time
import socket
import struct
import threading
import Modules.dataRobot as dataRobot
import Modules.varGlobals as varGlobals


def runCom():
    varGlobals.udp = True
    threading.Thread(target = getUDP, daemon = True).start()
    print("Masuk Thread")


###################################################################################################
#                                   MENERIMA DATA UDP MULTICAST                                   #
###################################################################################################

def getUDP():
    
    # MEMBUAT SOCKET
    get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    get.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    get.bind(('', int(varGlobals.PORT)))
    get.setblocking(0)

    # req = struct.pack('4sl', socket.inet_aton(varGlobals.IP), socket.INADDR_ANY)
    # get.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)

    while varGlobals.udp:
        try:
            data, address = get.recvfrom(1024)
            print("Data : ", data)
            
            if len(data) == 8:
                if data[7] == 1:
                    varGlobals.serviceBot = True
                    varGlobals.conServiceBot = 'Connected'
                    dataRobot.robotService(data, address)
                elif data[7] == 0:
                    varGlobals.serviceBot = False

        except Exception as e:
            print("Data tidak diterima")

    get.close()
    print("Socket sudah ditutup")


###################################################################################################
#                                     KIRIM DATA UDP MULTICAST                                    #
###################################################################################################

def send(data):

    # MEMBUAT SOCKET
    kirim = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    kirim.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    if varGlobals.udp:
        try:
            kirim.sendto(data, (varGlobals.IP, int(varGlobals.PORT)))
        except Exception as e:
            print("Pengiriman Gagal : ", e)
    else:
        kirim.close()