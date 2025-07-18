# VARIABLE GLOBAL
service_bot_ip = ''
kompas = 0
xpos = 0
ypos = 0
battery = 0
connect = 0

def robotService(data, address):
    global service_bot_ip, kompas, xpos, ypos, connect, battery

    service_bot_ip = address[0]

    if data[0] == 0:
        kompas = data[1]
    elif data[0] == 1:
        kompas = (360 - data[1])

    xpos = (data[2] << 8) | data[3]
    ypos = (data[4] << 8) | data[5]

    battery = data[6]

    connect = data[7]