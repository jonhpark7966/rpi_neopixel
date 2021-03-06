import time
import socket
import math
import numpy as np

import sounddevice as sd

num_pixels = 25
#num_pixels = 414

IP = '192.168.1.107'
PORT = 325
ADDR = (IP, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))


SR = 20000
duration = 120.0 # seconds
delta_f = 200
fftsize = math.ceil(SR / delta_f)
gain = 1.5




def callback(indata, outdata, frames, time, status):
    if (int(time.currentTime*100)%20) < 5:
      return
    power = 0.0
    if status:
        print(status)
    magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
    for i in magnitude:
        power = power + i
    power = power / (SR / delta_f)
        
    # assume min : -10, max = 0
    #pixels_to_turn_on = (math.log(magnitude[1])+10)/10  * num_pixels *gain
    pixels_to_turn_on = (math.log(power)+10)/10  * num_pixels *gain

    
    if pixels_to_turn_on < 0:
      pixels_to_turn_on = 0
    if pixels_to_turn_on > num_pixels:
      pixels_to_turn_on = num_pixels
    
    #pixels = []
    #for i in range(num_pixels):
    #    if ( i < int(pixels_to_turn_on) ):
    #        pixels.append(0x55)
    #        pixels.append(0x55)
    #        pixels.append(0x55)
    #    else:
    #        pixels.append(0x0)
    #        pixels.append(0x0)
    #        pixels.append(0x0)

    #msg = bytes(pixels)
    #print(int(pixels_to_turn_on))
    
    msg = bytes([int(pixels_to_turn_on)])
    print([int(pixels_to_turn_on)])

    
    client_socket.sendall(msg)

with sd.Stream(channels=1, callback=callback, samplerate=SR):
    sd.sleep(int(duration * 1000))

client_socket.close()




