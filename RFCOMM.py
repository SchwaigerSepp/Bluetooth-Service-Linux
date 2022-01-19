import os
import serial
import time
import json
from threading import Thread
from lib_oled96 import ssd1306
from smbus import SMBus
from PIL import ImageFont

def startRFCOMM():
    try:
        ser = serial.Serial("/dev/rfcomm0")
        if ser.isOpen():
            f = open("/home/pi/Downloads/test.txt","a")
            f.write("\n\rAlready Open")
            f.close()
    except:
        os.system("sudo rfcomm watch hci0")
        

def handleInput():
    while True:
        input = ser.readline()
        print(input)
        
        try:
            json_object = json.loads(input)
            
            for x in json_object['data']:
                speed = str(x['speed'])
                time = str(x['time'])
                dist = str(x['dist'])
                direction = str(x['dir'])
                print (speed + time + dist + direction)
                controlDisplay(speed,time,dist,direction)
                
        except (ValueError, KeyError, TypeError):
            f = open("/home/pi/Downloads/test.txt","a")
            f.write("\n\rError")
            f.close()
                
t = Thread(target = startRFCOMM)
t2 = Thread(target = handleInput)
t.start()

while True:
    try:
        ser = serial.Serial("/dev/rfcomm0")
        if ser.isOpen():
            ser.write(b"Connected")
            t2.start()
            break
    except:
        f = open("/home/pi/Downloads/test.txt","a")
        f.write("\n\rNot Yet Connected")
        f.close()
        time.sleep(1)
        
def controlDisplay(speed, time, dist, direct):
    
    #define Fonts
    FreeSans12 = ImageFont.truetype('FreeSans.ttf',12)
    FreeSans20 = ImageFont.truetype('FreeSans.ttf',20)
    
    # Display einrichten
    i2cbus = SMBus(1)            # 0 = Raspberry Pi 1, 1 = Raspberry Pi > 1
    oled = ssd1306(i2cbus)
    
    draw = oled.canvas
    
    oled.cls()
    oled.display()
    
    draw.text((75,40),time,font = FreeSans20,fill=1)
    
    if int(speed) >= 100:
        draw.text((65,10),speed,font = FreeSans20,fill=1)
    elif int(speed) >= 10:
        draw.text((70,10),speed,font = FreeSans20,fill=1)
    else:
        draw.text((85,10),speed,font = FreeSans20,fill=1)    
        
    draw.text((100,16),"km/h",font = FreeSans12,fill=1)
    
    draw.text((0,40),dist,font = FreeSans20,fill=1)
    
    oled.display()
