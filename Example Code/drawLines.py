#Kitronik VIEW 128x64 Display
#drawLines.py
#Example of how to draw different types of lines to make a basic house
from microbit import *
from display128x64 import *
view = Kitronik128x64Display()
#house
view.draw_horz_line(30, 30, 20)
view.draw_horz_line(30, 50, 20)
view.draw_vert_line(30, 30, 20)
view.draw_vert_line(50, 30, 20)
#roof
view.draw_diaganal_right(30, 30, 10)
view.draw_diaganal_left(50, 30, 10)
#door
view.draw_vert_line(40, 43, 7)
view.draw_vert_line(41, 43, 7)





    
    
    