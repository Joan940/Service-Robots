import time
import socket
import struct
import serial
import threading
import Modules.dataRobot as dataRobot
import Modules.varGlobals as varGlobals


# ###################################################################################################
# #                                     INISIALISASI PORT UART                                      #
# ###################################################################################################

# def init_uart(port="/dev/serial0", baudrate=115200):
#     try:
#         varGlobals.ser = serial.Serial(port, baudrate, timeout=0.25)
#         print("[UART] Port terbuka:", varGlobals.ser.name)
#     except Exception as e:
#         print("[UART] Gagal buka port:", e)

# def runCom():
#     if varGlobals.ser is None or not varGlobals.ser.is_open:
#         init_uart()
#     varGlobals.uart = True
#     threading.Thread(target=receive, daemon=True).start()
#     print("Masuk Thread")


# ###################################################################################################
# #                                       MENERIMA DATA UART                                        #
# ###################################################################################################

# def receive():
#     while varGlobals.uart:
#         try:
#             if varGlobals.ser and varGlobals.ser.in_waiting > 0:
#                 data = varGlobals.ser.read(varGlobals.ser.in_waiting)
#                 print("[UART] Data diterima:", list(data))
#         except Exception as e:
#             print("[UART] Error saat baca:", e)
#         time.sleep(0.05)


# ###################################################################################################
# #                                       MENGIRIM DATA UART                                        #
# ###################################################################################################

# def send(data):
#     if varGlobals.ser is None or not varGlobals.ser.is_open:
#         print("[UART] Port tidak aktif / belum dibuka")
#         return

#     try:
#         # 1. Inisialisasi buffer dan checksum
#         tx_buffer = []
#         checksum = 0
        
#         # 2. Tambahkan Start Byte
#         tx_buffer.append(0xFF)
        
#         # 3. Tambahkan Length Byte
#         length = len(data)
#         if length > 255:
#             print("[UART] Error: Jumlah data melebihi 255")
#             return
#         tx_buffer.append(length)

#         # 4. Proses setiap integer dalam data_list
#         for integer_value in data:
#             # Pastikan integer dalam rentang 16-bit (sesuai asumsi 'int' di STM32)
#             if not -32768 <= integer_value <= 32767:
#                  print(f"[UART] Peringatan: Nilai {integer_value} di luar rentang int16.")

#             # Konversi ke unsigned untuk bitwise operation
#             # struct.pack akan menangani nilai negatif dengan benar
#             packed_int = struct.pack('>h', integer_value) # '>h' = big-endian, signed short (2 bytes)
            
#             # Tambahkan High Byte dan Low Byte ke buffer
#             tx_buffer.append(packed_int[0]) # High Byte
#             tx_buffer.append(packed_int[1]) # Low Byte
            
#             # Tambahkan nilai integer asli ke checksum
#             checksum += integer_value

#         # 5. Tambahkan Checksum (hanya Low Byte-nya)
#         tx_buffer.append(checksum & 0xFF)
        
#         # 6. Kirim data
#         data_to_send = bytes(tx_buffer)
#         varGlobals.ser.write(data_to_send)
#         print("[UART] Data terkirim:", list(data_to_send))

#     except Exception as e:
#         print("[UART] Pengiriman gagal:", e)

# # Contoh penggunaan:
# # Misal Anda ingin mengirim dua integer: 1000 dan 5
# # panggil fungsi ini:
# # send_integers([1000, 5])

def runCom():
    varGlobals.udp = True

    runThread = threading.Thread(target=getUDP, daemon=True)
    runThread.start()
    print("Masuk thread komunikasi!")

###################################################################################################
#                                   MENERIMA DATA UDP MULTICAST                                   #
###################################################################################################

def getUDP():
    
    # MEMBUAT SOCKET
    get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    get.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    get.bind(('', int(varGlobals.PORT)))
    get.setblocking(0)

    req = struct.pack('4sl', socket.inet_aton(varGlobals.IP), socket.INADDR_ANY)
    get.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)

    printed = False

    while varGlobals.udp:
        try:
            data, address = get.recvfrom(1024)
            print("Data diterima : ", data)
            
            if len(data) == 8:
                if data[7] == 1:
                    varGlobals.serviceBot = True
                    varGlobals.conServiceBot = 'Connected'
                    dataRobot.robotService(data, address)
                elif data[7] == 0:
                    varGlobals.serviceBot = False

        except Exception as e:
            if not printed:
                print("Data tidak diterima")
                printed = True

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