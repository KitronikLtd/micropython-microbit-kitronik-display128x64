#Kitronik VIEW 128x64 Display
#controlPixels.py
#Example of how to turn on and off particular pixel on the display
from microbit import *
from display128x64 import *

view = Kitronik128x64Display()

while True:
    view.set_px(0, 0)       #set pixels X and Y
    view.set_px(127, 63)
    sleep(500)
    view.clear_px(0, 0)     #clear pixels X and Y
    view.clear_px(127, 63)
    sleep(500)

    
    
    