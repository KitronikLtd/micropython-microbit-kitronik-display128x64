# microbit-module: Kitronik128x64Display@1.0.0
# Kitronik VIEW 128x64 Display micropython library for the micro:bit
# Display uses SSD1306 driver via I2C connection
# Display resolution is 128 x 64
# v0.1

#Import the required microbit functions required
from microbit import Image, i2c
from ustruct import pack_into

class Kitronik128x64Display:
 ADDR = 0x3C
 screen = bytearray(1025)
 screen[0] = 0x40

 def command(self, c):
  i2c.write(self.ADDR, b'\x00' + bytearray(c))

 def __init__(self):
  cmd = [
   [0xAE],[0xA4],[0xD5, 0xF0],[0xA8, 0x3F],[0xD3, 0x00],[0 | 0x0],[0x8D, 0x14],
   [0x20, 0x00],[0x21, 0, 127],[0x22, 0, 63],[0xa0 | 0x1],[0xc8],[0xDA, 0x12],
   [0x81, 0xCF],[0xd9, 0xF1],[0xDB, 0x40],[0xA6],[0xd6, 0],[0xaf]]
  for c in cmd:
   i2c.write(self.ADDR, b'\x00' + bytearray(c))
  self.clear_display()

 def set_pos(self, col=0, page=0):
  self.command([0xb0 | page])  # page number
  c1, c2 = col % 16, col >> 4
  self.command([0x00 | c1])
  self.command([0x10 | c2])

 def clear_display(self, c=0):
  self.set_pos(0, 0)
  i=1
  for i in range(1, 1025):
   self.screen[i] = 0
  i2c.write(self.ADDR, self.screen)
        
 def set_px(self, x, y):
  x = 127 if x > 127 else x
  y = 63 if y > 63 else y
  page, shift_page = y >> 3, y % 8
  ind = x + page * 128 + 1
  screenPixel = (self.screen[ind] | (1 << shift_page))
  pack_into(">BB", self.screen, ind, screenPixel)
  self.set_pos(x, page)
  i2c.write(self.ADDR, bytearray([0x40, screenPixel]))

 def clear_px(self, x, y):
  x = 127 if x > 127 else x
  y = 63 if y > 63 else y
  page, shift_page = y >> 3, y % 8
  ind = x + page * 128 + 1
  screenPixel = (self.screen[ind] & ~ (1 << shift_page))
  pack_into(">B", self.screen, ind, screenPixel)
  self.set_pos(x, page)
  i2c.write(self.ADDR, bytearray([0x40, screenPixel]))

 def draw_vert_line(self, x, y, length):
  length = 63 if length > 63 else length
  i = y
  for i in range(y, (y + length)):
   self.set_px(x, i)

 def draw_horz_line(self, x, y, length):
  length = 127 if length > 127 else length
  i = x
  for i in range(x, (x + length)):
   self.set_px(i, y)

 def draw_diaganal_right(self, x, y, length):
  i = x
  for i in range(x, (x + length)):
   self.set_px(i, y)
   y -= 1

 def draw_diaganal_left(self, x, y, length):
  x, i, y = x - length, x, y - length
  for i in range(x, (x + length)):
   self.set_px(i, y)
   y += 1

 def draw_rect(self, x, y, width, height):
  width = 127 if width > 127 else width
  height = 63 if height > 63 else height
  self.draw_horz_line(x, y, width - x + 1)
  self.draw_horz_line(x, height, width - x + 1)
  self.draw_vert_line(x, y, height - y + 1)
  self.draw_vert_line(width, y, height - y + 1)

 def update_screen(self):
  self.set_pos()
  i2c.write(self.ADDR, self.screen)

 def display_as_text(self, inputData, x, row):
  row = 7 if row > 7 else row
  x = 23 if x > 23 else x
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
