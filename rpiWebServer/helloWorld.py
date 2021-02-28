from flask import Flask, render_template
import datetime
import multiprocessing
import os
import signal

import time
import board
import neopixel



pixel_pin = board.D18
num_pixels = 414
ORDER = neopixel.GRBW
bright = 1.0

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=bright, auto_write=False, pixel_order=ORDER
)

hour = 6
minute = 40
# monday - sunday.
days = [True,True,True,True,True,False,False]
proc_num = [0,]

def setAlarm(hour, minute, days):
    while True:
        now = datetime.datetime.now()
        if now.hour == hour:
            if now.minute == minute:
                if now.second < 5:
                    if days[datetime.datetime.today().weekday()]:
                        #turn on for 5 seconds.
                        pixels.brightness = 1.0
                        for i in range(0, num_pixels):
                            pixels[i] = (0,0,0,255)
                        pixels.show()
        time.sleep(1)

def turnOffAtSevenHalf():
    while True:
        now = datetime.datetime.now()
        if now.hour == 7:
            if now.minute == 30:
                if now.second < 5:
                    for i in range(0, num_pixels):
                        pixels[i] = (0,0,0,0)
                    pixels.show()
        time.sleep(1)


app = Flask(__name__)
@app.route('/')
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'alarm_time': str(hour) + " : " + str(minute), 
        'days': days,
        'brightness': str(pixels.brightness*100),
    }
    return render_template('index.html', **templateData)


@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    start = 0
    end = 0

    if deviceName == 'proj':
        start = 0
        end = 144
    if deviceName == 'ceil':
        start = 144
        end = 264
    if deviceName == 'side':
        start = 264
        end = 294
    if deviceName == 'bed':
        start = 294
        end = 414
    if deviceName == 'all':
        start = 0
        end = 414

    if deviceName == 'brightness':
        pixels.brightness = float(action)

    for i in range(start, end):
        if action == "on":
            pixels[i] = (0,0,0,255)
        if action == "off":
            pixels[i] = (0,0,0,0)
    pixels.show()
   
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'alarm_time': str(hour) + " : " + str(minute), 
        'days': days,
        'brightness': str(pixels.brightness*100),
    }
 
    return render_template('index.html', **templateData)

@app.route("/alarm/<day>/<action>")
def alarm(day, action):
    os.kill(proc_num[0], signal.SIGTERM)

    turn = True
    if action == 'off':
        turn = False

    days[int(day)] = turn
    proc = multiprocessing.Process(target=setAlarm, args=(hour, minute, days))
    print(days)
    proc.start()
    proc_num[0] = proc.pid

    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
 
    templateData = {
        'title' : 'ALARM!',
        'time': timeString,
        'alarm_time': str(hour) + " : " + str(minute), 
        'days': days,
        'brightness': str(pixels.brightness*100),
    }
 
    return render_template('index.html', **templateData)
 


if __name__ == "__main__":
    proc = multiprocessing.Process(target=setAlarm, args=(hour, minute, days))
    proc.start()
    proc_num[0] = proc.pid
    offProc = multiprocessing.Process(target=turnOffAtSevenHalf, args=())
    offProc.start()

    app.run(host='0.0.0.0', port=80, debug=True)

