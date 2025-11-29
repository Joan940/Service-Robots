import errno
import socket
import threading

# === VARIABLE GLOBALS ===
udp  = bool
IP   = '192.168.110.15'
PORT = '8081'

def runCom():
    before = udp
    udp = True

    if udp != before:
        print("Masuk thread komunikasi!")
    
    runThread = threading.Thread(target=getUDP, daemon=True)
    runThread.start()


###################################################################################################
#                                   MENERIMA DATA UDP MULTICAST                                   #
###################################################################################################

def getUDP():

    # MEMBUAT SOCKET
    get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    get.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # MENGGUNAKAN UNICAST
    get.bind((IP, int(PORT)))
    get.setblocking(0)

    printed = False
    
    while udp:
        try:
            data, address = get.recvfrom(1024)
            print("Data diterima :", data)
        except BlockingIOError:
            if not printed:
                print("Data tidak diterima")
                printed = True
            pass
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            pass
    
    get.close()
    print("Socket sudah ditutup")


###################################################################################################
#                                     KIRIM DATA UDP MULTICAST                                    #
###################################################################################################

def send(data):
    kirim = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    if udp:
        try:
            kirim.sendto(data, (IP, int(PORT)))
            print(f"Data terkirim : {data}")
        except socket.error as e:
            print(f"Pengiriman Gagal, Socket Error: {e}")
            print(f"Kode Error: {e.errno}")
            if e.errno == errno.WSAECONNRESET:
                print("Error : Port tujuan tidak merespons!")
        except Exception as e:
            print("Terjadi error yang tidak terduga: ", e)
    else:
        kirim.close()