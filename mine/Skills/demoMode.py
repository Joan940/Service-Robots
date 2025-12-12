from Modules.communication import send

data    = bytearray(3)

def meja1():
    # print("Masuk demo 1")
    data[0] = 200
    data[1] = 1
    data[2] = 90
    send(data)

def meja2():
    # print("Masuk demo 2")
    data[0] = 200
    data[1] = 2
    data[2] = 90
    send(data)

def meja3():
    # print("Masuk demo 3")
    data[0] = 200
    data[1] = 3
    data[2] = 90
    send(data)

def meja4():
    # print("Masuk demo 4")
    data[0] = 200
    data[1] = 4
    data[2] = 90
    send(data)