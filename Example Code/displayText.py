#Kitronik VIEW 128x64 Display
#displayText.py
#Example of how to display text, numbers and variables
from microbit import *
from display128x64 import *

view = Kitronik128x64Display()

view.display_as_text("This is the top line", 0, 0) #add a string to top line
view.display_as_text(200, 0, 2) # add a number to line 3

incNumber = 0
while True:
    view.display_as_text(incNumber, 0, 4)  #add a variable increasing on line 5
    if incNumber < 100:
        incNumber += 1
    sleep(1000)