from machine import SPI,Pin,freq,PWM
import random
import st7735
import time
from st7735 import TFTColor
from bmpdecoder import bmpData
freq(240000000)
displayOn = PWM(Pin(11),duty=1023,freq=1000)
spi = SPI(2,baudrate=60000000, sck = Pin(13),mosi = Pin(14))
display = st7735.TFT(spi,8,4,3)#spi, aDC, aReset, aCS
display._size = (128,160)
display.initg()
display.fill(0)
p = bmpData.bmpDecoder("2233_3.bmp",screenSize = (160,160),isbgr=False)
t = time.ticks_us()

for i in range(60):
    p.render(display,(random.randint(0,6)*10,random.randint(0,6)*10))

print((time.ticks_us()-t)/1000000)
