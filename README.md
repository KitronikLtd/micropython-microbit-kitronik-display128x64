# micropython-microbit-kitronik-display128x64
A class and sample code to use the Kitronik VIEW 128x64 Display for BBC micro:bit. (www.kitronik.co.uk/56115)

## Import display128x64.py and construct an instance:
    from display128x64 import *
    view = Kitronik128x64Display

This will initialise the PCA to default values.
## Clear the display:
    view.clear_display(view)
This will remove all data on the screen

## Set pixel:
    view.set_px(view, x, y)
Set pixel will allow control of a single pixel to turn on where:
* x => 0 to 127
* y => 0 to 63

## Clear pixel:
    view.clear_px(view, x, y)
Clear pixel will allow control of a single pixel to turn pff where:
* x => 0 to 127
* y => 0 to 63

### Draw vertical line:
    view.draw_vert_line(view, x, y, length)
Allow to draw a vertical on ths display where:
* x => 0 to 127
* y => 0 to 63
* length => 0 to 63
The line is draw from top edge downwards

### Draw horizontal line:
    view.draw_horz_line(view, x, y, length)
Allow to draw a horizontal on ths display where:
* x => 0 to 127
* y => 0 to 63
* length => 0 to 127
The line is draw from left edge to the right

### Draw rectangle shape:
    view.draw_rect(view, x, y, width, height)
Allow to draw a rectange or sqaure with a starting point in the top left:
* x => 0 to 127
* y => 0 to 63
* width => 0 to 127
* height => 0 to 63
