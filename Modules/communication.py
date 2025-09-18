import time
import socket
import struct
import threading
import Modules.dataRobot as dataRobot
import Modules.varGlobals as varGlobals

def runCom():
    varGlobals.udp = True

    # runThread = threading.Thread(target=send, daemon=True)
    # runThread.start()
    print("Masuk thread komunikasi!")


# ###################################################################################################
# #                                   MENERIMA DATA UDP MULTICAST                                   #
# ###################################################################################################

# def getUDP():

#     # MEMBUAT SOCKET
#     get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     get.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
#     # MENGGUNAKAN UNICAST
#     get.bind((varGlobals.IP, int(varGlobals.PORT)))
#     get.setblocking(0)

#     printed = False
    
#     while varGlobals.udp:
#         try:
#             data, address = get.recvfrom(1024)
#             print("Data:", data)
            
#             if len(data) == 8:
#                 if data[7] == 1:
#                     varGlobals.serviceBot = True
#                     varGlobals.conServiceBot = 'Connected'
#                     dataRobot.robotService(data, address)
#                 elif data[7] == 0:
#                     varGlobals.serviceBot = False

#         except BlockingIOError:
#             if not printed:
#                 print("Data tidak diterima")
#                 printed = True
#             pass
#         except Exception as e:
#             print(f"Terjadi kesalahan: {e}")
#             pass
    
#     get.close()
#     print("Socket sudah ditutup")


###################################################################################################
#                                     KIRIM DATA UDP MULTICAST                                    #
###################################################################################################

def send(data):

    kirim = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if varGlobals.udp:
        try:
            kirim.sendto(data, (int(varGlobals.IP), int(varGlobals.PORT)))
            print(f"Data terkirim : {data}")
        except Exception as e:
            print("Pengiriman Gagal : ", e)
    else:
        kirim.close()