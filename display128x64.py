# Kitronik VIEW 128x64 Display micropython library for the micro:bit
# Display uses SSD1306 driver via I2C connection
# Display resolution is 128 x 64
# v0.1

#Import the required microbit functions required
from microbit import Image, i2c

# LCD Control constants
ADDR = 0x3C
screen = bytearray(1025)  # send byte plus pixels
screen[0] = 0x40

def command(c):
    i2c.write(ADDR, b'\x00' + bytearray(c))

def initialize():
    cmd = [
        [0xAE],                     # SSD1306_DISPLAYOFF
        [0xA4],                     # SSD1306_DISPLAYALLON_RESUME
        [0xD5, 0xF0],               # SSD1306_SETDISPLAYCLOCKDIV
        [0xA8, 0x3F],               # SSD1306_SETMULTIPLEX
        [0xD3, 0x00],               # SSD1306_SETDISPLAYOFFSET
        [0 | 0x0],                  # line #SSD1306_SETSTARTLINE
        [0x8D, 0x14],               # SSD1306_CHARGEPUMP
        # 0x20 0x00 horizontal addressing
        [0x20, 0x00],               # SSD1306_MEMORYMODE
        [0x21, 0, 127],             # SSD1306_COLUMNADDR
        [0x22, 0, 63],              # SSD1306_PAGEADDR
        [0xa0 | 0x1],               # SSD1306_SEGREMAP
        [0xc8],                     # SSD1306_COMSCANDEC
        [0xDA, 0x12],               # SSD1306_SETCOMPINS
        [0x81, 0xCF],               # SSD1306_SETCONTRAST
        [0xd9, 0xF1],               # SSD1306_SETPRECHARGE
        [0xDB, 0x40],               # SSD1306_SETVCOMDETECT
        [0xA6],                     # SSD1306_NORMALDISPLAY
        [0xd6, 0],                  # zoom off
        [0xaf]                      # SSD1306_DISPLAYON
    ]
    for c in cmd:
        command(c)

def set_pos(col=0, page=0):
    command([0xb0 | page])  # page number
    # take upper and lower value of col * 2
    #c1, c2 = col * 2 & 0x0F, col >> 3
    c1 = col % 16
    c2 = col >> 4
    command([0x00 | c1])  # lower start column address
    command([0x10 | c2])  # upper start column address

def clear_display(c=0):
    global screen
    set_pos()  #set position to start of display
    i=1
    for i in range(1, 1025): # load screen buf with 0
        screen[i] = 0
    draw_screen() #update screen buf with blank data

def draw_screen():
    set_pos()  #set position to start of display
    i2c.write(ADDR, screen) #write data to the screen

def show(inputData, x, y):
    displayString = str(inputData)
    for i in range(0, min(len(displayString), 12 - x)):
        for c in range(0, 5):
            col = 0
            for r in range(1, 6):
                p = Image(displayString[i]).get_pixel(c, r - 1)
                col = col | (1 << r) if (p != 0) else col
            ind = x * 5 + y * 128 + i * 5 + c + 1
            screen[ind] = col
    set_pos(x * 5, y)
    ind0 = x * 5 + y * 128 + 1
    i2c.write(ADDR, b'\x40' + screen[ind0:ind])