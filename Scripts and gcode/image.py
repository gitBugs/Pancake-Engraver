#Preamble

#Variables for configuration
numberOfTurns = 40 #how many turns on the spiral
arcLength = 2      #Burn a spot every n units around the arc
ymmPerRadian = 25   #NB: will be dependant on the steps/mm setting on the GRBL board. Can that be set in gcode?
xmmPerRadiusUnit = 1
feedrate = 300

#IMPORTS
import numpy as np
import cv2
import math 

#Open file to receive gcode
gcodeFile = open('gcodeFile',mode='w')



#Open image
inputImgBig = cv2.imread('pi-sample.jpg', 0)


inputImg = cv2.resize(inputImgBig,None,fx=.2, fy=.2, interpolation = cv2.INTER_CUBIC)
cv2.imshow('image',inputImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

outputImg = np.zeros((inputImg.shape[0],inputImg.shape[1],1), np.uint8)
outputImg[:,:] = 255
                     

#Determine image size - use img.shape
if inputImg.shape[0] < inputImg.shape[1]:
    imageRadius = inputImg.shape[0] / 2
else:
    imageRadius = inputImg.shape[1] / 2

print imageRadius

#Where's the centre pixel in the image?
xCentrePixel = inputImg.shape[0]/2
yCentrePixel = inputImg.shape[1]/2


#Given how many turns we want in the spiral, how many pixels out does each turn travel?
radiusIncreasePerTurn = imageRadius / numberOfTurns
radiusIncreasePerRad = radiusIncreasePerTurn / (2 * math.pi)
print radiusIncreasePerTurn


#Setup for the loop spiralling outwards
currentRadius = 0 
currentAngle = 1 #needs to be >0 or generates divide by 0 error in first loop
maxAngle = numberOfTurns * 2 * math.pi #because 2pi rad in a circle

while currentAngle < maxAngle:
    xPosition = xCentrePixel + (currentRadius * math.cos(currentAngle))
    yPosition = yCentrePixel + (currentRadius * math.sin(currentAngle))
    pixelColour = inputImg[xPosition, yPosition]
    
    outputImg[xPosition,yPosition] = pixelColour
    currentRadius = currentAngle * radiusIncreasePerRad
    currentAngle =  currentAngle + (arcLength / currentRadius) #...change in angle calculated to keep arc length constant

    #Two possible methods for engraving:
    #1) Move to new position, pause to fire laser for x seconds, then move to next position
    #2) Change laser intensity, and send next coordinate, i.e. laser is on all the time
    # Will try (2) first. Laser intensity controlled by "spindle speed" gcode because allows use of PWM pin


    laserPower = 1000-(pixelColour * (1000/255))  #Scale the value from the range used by pixel colour (0-255) to that used by spindle speed (0-1000)
    if laserPower <0:
        laserPower = 0 #just in case there's some dodgy rounding error stuff going on.
    
    gcodeLine1 = "S" + str(laserPower) + "\n" #Set the new spindle speed (used here for laser power PWM)
    gcodeLine2 = "M3\n" #set the actual PWM to the new spindle speed
    gcodeLine3 = "G01 X" + str(int(currentRadius) * xmmPerRadiusUnit) + " Y" + str(int(currentAngle) * ymmPerRadian) + " F" + str(feedrate) + "\n"
    gcodeFile.write(gcodeLine1)
    gcodeFile.write(gcodeLine2)
    gcodeFile.write(gcodeLine3)
    

    
cv2.imshow('image',outputImg)
cv2.waitKey(0)
outputImg[:,:] = 255
cv2.destroyAllWindows()

gcodeFile.write('M5') #command to turn off the laser
gcodeFile.write('H')  #Home the carraige
gcodeFile.close()






