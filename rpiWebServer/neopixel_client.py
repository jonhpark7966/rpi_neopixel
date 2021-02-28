import time

import socket

num_pixels = 414

IP = ''
PORT = 325
SIZE = 3*num_pixels
ADDR = (IP, PORT)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

pixels = []
for i in range(num_pixels):
    pixels.append(0x55)
    pixels.append(0x55)
    pixels.append(0x00)

msg = bytes(pixels)

client_socket.sendall(msg)
