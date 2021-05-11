from microbit import accelerometer, sleep
from display128x64Plot import *

plot = Kitronik128x64DisplayPlot()

graphYMax = 32
graphYMin = 12
graphYRange = graphYMax - graphYMin
variableMax = 2000
variableMin = -2000
variableRange = variableMax - variableMin

screenRatio = graphYRange/variableRange
x = 0
y = 0
length = 0

while True:
    yPlot = accelerometer.get_y()
    
    plot.display_as_text("      ", 0, 0)
    plot.display_as_text(yPlot, 0, 0)
    
    yPlotMapped = graphYMax - ((yPlot-variableMin) * screenRatio)
    yPlotMapped = round(yPlotMapped)
    
    if x == 0:
        previousYPlot = yPlotMapped
    
    if yPlotMapped < previousYPlot:
        y = yPlotMapped
        length = (previousYPlot-yPlotMapped)
    elif yPlotMapped > previousYPlot:
        y = previousYPlot
        length = (yPlotMapped-previousYPlot)
    else:
        y = yPlotMapped
        length = 1
        
    if x == 63:
        plot.clear_display()
        x=0
    else:
        plot.draw_vert_line(x, y, length)
        previousYPlot = yPlotMapped
        x += 1
        
    sleep(500)
    
    
    
    
    
    
    