# functions will set and clear pixel, inputs require an x and y co-ordinates
from microbit import i2c
from ustruct import pack_into

from display128x64 import screen, set_pos

def set_px(x, y):
    shift_page = y % 8
    page = y >> 3
    #page, shift_page = divmod(y, 8)
    ind = x + page * 128 + 1
    screenPixel = (screen[ind] | (1 << shift_page))
    pack_into(">BB", screen, ind, screenPixel)
    set_pos(x, page)
    i2c.write(0x3c, bytearray([0x40, screenPixel]))

def clear_px(x, y):
    shift_page = y % 8
    page = y >> 3
    #page, shift_page = divmod(y, 8)
    ind = x + page * 128 + 1
    screenPixel = (screen[ind] & ~ (1 << shift_page))
    pack_into(">BB", screen, ind, screenPixel)
    set_pos(x, page)
    i2c.write(0x3c, bytearray([0x40, screenPixel]))

#draw vertical line will take a x,y point and increament y and set pixel at each point 
def draw_vert_line(length, x, y):
    i = y
    for i in range(y, (y + length)):
        set_px(x, i)

#draw horizontal line will take a x,y point and increament x and set pixel at each point 
def draw_horz_line(length, x, y):
    i = x
    for i in range(x, (x + length)):
        set_px(i, y)
        
def draw_rect(width, height, x, y):
    draw_horz_line(x, y, width - x + 1)
    draw_horz_line(x, height, width - x + 1)
    draw_vert_line(x, y, height - y + 1)
    draw_vert_line(width, y, height - y + 1)