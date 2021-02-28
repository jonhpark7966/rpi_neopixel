import time
import board
import neopixel

import socket

pixel_pin = board.D18
num_pixels = 414

ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
)

IP = ''
PORT = 325
SIZE = 3*num_pixels
ADDR = (IP, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(ADDR)  # 주소 바인딩
    server_socket.listen()  # 클라이언트의 요청을 받을 준비
    while True:
        client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
        msg = client_socket.recv(SIZE)

        for i in range(num_pixels):
            pixels[i] = (msg[3*i], msg[3*i+1], msg[3*i+2])
        pixels.show()
        print("loop!")
