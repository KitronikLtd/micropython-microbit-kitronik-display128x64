# Kitronik VIEW 128x64 Display micropython library for the micro:bit
# Display uses SSD1306 driver via I2C connection
# Display resolution is 128 x 64
# v0.1

#Import the required microbit functions required
from microbit import Image, i2c
from ustruct import pack_into

class Kitronik128x64Display:

    # LCD Control constants
    ADDR = 0x3C
    screen = bytearray(1025)  # send byte plus pixels
    screen[0] = 0x40

    def command(self, c):
        i2c.write(self.ADDR, b'\x00' + bytearray(c))

    def __init__(self):
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
            i2c.write(self.ADDR, b'\x00' + bytearray(c))
        self.clear_display()

    def set_pos(self, col=0, page=0):
        self.command([0xb0 | page])  # page number
        # take upper and lower value of col * 2
        c1 = col % 16
        c2 = col >> 4
        self.command([0x00 | c1])  # lower start column address
        self.command([0x10 | c2])  # upper start column address

    def clear_display(self, c=0):
        self.set_pos(0, 0)  #set position to start of display
        i=1
        for i in range(1, 1025): # load screen buf with 0
            self.screen[i] = 0
        i2c.write(self.ADDR, self.screen) #update screen buf with blank data
        
    def set_px(self, x, y):
        if x > 127:     #check that x does not exceed display limit
            x = 127     # if it does set to display limit
        if y > 63:      #check that y does not exceed display limit
            y = 63      # if it does set to display limit
        page = y >> 3
        shift_page = y % 8
        ind = x + page * 128 + 1
        screenPixel = (self.screen[ind] | (1 << shift_page))
        pack_into(">BB", self.screen, ind, screenPixel)
        self.set_pos(x, page)
        print(screenPixel)
        i2c.write(self.ADDR, bytearray([0x40, screenPixel]))

    def clear_px(self, x, y):
        if x > 127:     #check that x does not exceed display limit
            x = 127     # if it does set to display limit
        if y > 63:      #check that y does not exceed display limit
            y = 63      # if it does set to display limit
        page = y >> 3
        shift_page = y % 8
        ind = x + page * 128 + 1
        screenPixel = (self.screen[ind] & ~ (1 << shift_page))
        pack_into(">B", self.screen, ind, screenPixel)
        self.set_pos(x, page)
        i2c.write(self.ADDR, bytearray([0x40, screenPixel]))

    #draw vertical line from a x,y point, line will be drawn from top to bottom
    def draw_vert_line(self, x, y, length):
        if length > 63:     #check that length does not exceed display limit
            length = 63     # if it does set to display limit
        i = y
        for i in range(y, (y + length)):
            self.set_px(x, i)

    #draw horizontal line from a x,y point, line will be drawn from left to right
    def draw_horz_line(self, x, y, length):
        if length > 127:     #check that length does not exceed display limit
            length = 127     # if it does set to display limit
        i = x
        for i in range(x, (x + length)):
            self.set_px(i, y)

    #draw diaganal line to the right and up a x,y point
    def draw_diaganal_right(self, x, y, length):
        i = x
        for i in range(x, (x + length)):
            self.set_px(i, y)
            y -= 1

    #draw diaganal line to the left and up a x,y point
    def draw_diaganal_left(self, x, y, length):
        x = x - length
        i = x
        y = y - length
        for i in range(x, (x + length)):
            self.set_px(i, y)
            y += 1
    
    #draw a rectangle with x-y being top left of the rectangle. The width and height being the number of pixels from that point
    def draw_rect(self, x, y, width, height):
        if width > 127:     #check that length does not exceed display limit
            width = 127     # if it does set to display limit
        if height > 63:     #check that length does not exceed display limit
            height = 63     # if it does set to display limit
        self.draw_horz_line(self, x, y, width - x + 1)
        self.draw_horz_line(self, x, height, width - x + 1)
        self.draw_vert_line(self, x, y, height - y + 1)
        self.draw_vert_line(self, width, y, height - y + 1)

    #update will
    def update_screen(self):
        self.set_pos()  #set position to start of display
        i2c.write(self.ADDR, self.screen) #write data to the screen

    #Taking a number or string to display a text representation onto the screen
    #x is the number of charectors along the display (or charector coloum) with a range of 0 to 23
    #row is the charector line of the display with a range of 0 to 7
    def display_as_text(self, inputData, x, row):
        if row > 7:
            row = 7
        if x > 23:
            x = 23
        displayString = str(inputData)
        for i in range(0, min(len(displayString), 12 - x)):
            for c in range(0, 5):
                col = 0
                for r in range(1, 6):
                    p = Image(displayString[i]).get_pixel(c, r - 1)
                    col = col | (1 << r) if (p != 0) else col
                ind = x * 5 + row * 128 + i * 5 + c + 1
                self.screen[ind] = col
        self.set_pos(x * 5, row)
        ind0 = x * 5 + row * 128 + 1
        i2c.write(self.ADDR, b'\x40' + self.screen[ind0:ind])