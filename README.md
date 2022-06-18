# -micropython-bmpdecoder-st7735-
a bmp decoder on micropython by killo

about st7735 from 
#driver for Sainsmart 1.8" TFT display ST7735
#Translated by Guy Carver from the ST7735 sample code.
#Modirfied for micropython-esp32 by boochow

about bmpdecoder:
mod by myself
so there could be some bugs

#how to use?
from machine import SPI,Pin
import st7735
import time,random
from bmpdecoder import bmpData,bmpFileData

def initDisplay():
    global display,tftVdd
    tftVdd = Pin(2,Pin.OUT,value = 1)
    display = st7735.TFT(
        SPI(1,baudrate=60000000, polarity=0, phase=0,
            sck=Pin(11),mosi=Pin(7),miso=Pin(9)),
        10,2,3)#spi, aDC, aReset, aCS,ScreenSize = (160, 160)
    display.initr()
    display.invertcolor(True)
    display.rotation(1)
    display._offset = (1,26)#(26,1)
    display.fill(0)
    
initDisplay()
gc.collect()
m1 = gc.mem_free()
b1 = bmpFileData.decode("2233_2.bmp",'hello',biasY = 80)
#b1 = bmpFileData.load("2233_3")
gc.collect()
print('use memory',(m1-gc.mem_free())/1024/1024)
print('free memory',(gc.mem_free())/1024/1024)
t = time.ticks_ms()
# for i in range(50):
#b.render(display,(5*2,0))
# print('50fps in',(time.ticks_ms()-t)/1000)
# t = time.ticks_ms()
# for i in range(50):
m1 = gc.mem_free()
for i in range(60):
    b1.render(display,(random.randint(0,8)*10,random.randint(0,6)))
gc.collect()
print(b1.w,b1.h)
print('use memory',(m1-gc.mem_free())/1024/1024)
print('free memory',(gc.mem_free())/1024/1024)
print('60fps in',(time.ticks_ms()-t)/1000)

