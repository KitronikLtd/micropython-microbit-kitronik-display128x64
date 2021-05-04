# functions will set and clear pixel, inputs require an x and y co-ordinates
from microbit import i2c
from ustruct import pack_into

from display128x64 import screen, set_pos, draw_screen

class ViewDisplay:
    #global plotArray() #= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]   
    graphYMax = 1
    graphYMin = 0
    plotArray = []
    def plot(self, plotVariable): 
        #plotArray = [0]  
        GRAPH_Y_MIN_LOCATION = 63
        GRAPH_Y_MAX_LOCATION = 20
        plotVariable = round(plotVariable) #round the variable to use as ints rather than floats
        plotLength = len(self.plotArray)
        if plotLength == 127:     #if the length of the array has reach max number of pixels, shift the array and remove the oldest
            for i in range (plotLength): #shift all the data by 1 and place on the end of the array
                if i == plotLength:
                    self.plotArray[i] = plotVariable
                else:
                    self.plotArray[i] = self.plotArray[i+1]
        else:
            self.plotArray.append(plotVariable) #add plot value to the end of the plot arrary

        #if the varibale exceeds the scale of the Y axis, update the in or max limits
        if plotVariable > self.graphYMax:
            self.graphYMax = plotVariable
        if plotVariable < self.graphYMin:
            self.graphYMin = plotVariable

        #plotting for loop of graph onto display
        arrayPosition = 0
        #for (let arrayPosition = 0; arrayPosition <= plotLength; arrayPosition++)
        for arrayPosition in range (plotLength):
            x = arrayPosition #x is start of screen 
            yPlot = self.plotArray[arrayPosition]
            #map the variables to scale between the min and max values to the min and max graph pixel area
            yPlot = pins.map(yPlot, graphYMin, graphYMax, GRAPH_Y_MIN_LOCATION, GRAPH_Y_MAX_LOCATION)

            if arrayPosition == 0:
                previousYPlot = yPlot
            y = 0
            length = 0

            #determine if the line needs to be drawn from the last point to the new or visa-versa, V line can only be drawn down the screen
            if yPlot < previousYPlot:
                y = yPlot
                length = (previousYPlot-yPlot)
            elif yPlot > previousYPlot:
                y = previousYPlot
                length = (yPlot-previousYPlot)
            else:
                y = yPlot
                length = 1

            #Clear plots in screenBuffer
            page = 0
            i = GRAPH_Y_MAX_LOCATION
            for i in range (GRAPH_Y_MIN_LOCATION):
            #for (let i = GRAPH_Y_MAX_LOCATION; i <= GRAPH_Y_MIN_LOCATION; i++){
                page = i >> 3
                shift_page = i % 8
                ind = x + page * 128 + 1
                screenPixel = clearBit(screenBuf[ind], shift_page)    #clear the screen data byte
                screenBuf[ind] = screenPixel                            #store data in screen buffer

            #plot new data in screenBuffer
            #for (let i = y; i < (y + len); i++){
            i = y
            for i in range ((y + length)):
                page = i >> 3
                shift_page = i % 8
                ind = x + page * 128 + 1
                screenPixel = (screenBuf[ind] | (1 << shift_page))  #set the screen data byte
                screenBuf[ind] = screenPixel                            #store data in screen buffer
            previousYPlot = yPlot
        draw_screen() #refresh screen with new data in screenBuffer