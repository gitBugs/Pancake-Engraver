
#Preamble

#Variables for configuration
numberOfTurns = 20 #how many turns on the spiral
turntableCentreDistanceFromEndstop = 77 #how far is the centre of the turntable from the x-axis endstop?
arcLength = 02      #Burn a spot every n units around the arc
ymmPerRadian = 31.8   #NB: will be dependant on the steps/mm setting on the GRBL board. Can that be set in gcode?
xmmPerRadiusUnit = (40 / numberOfTurns) -.5 #because we have about 75mm to play with
feedrate = 12000

previousX = ""
previousY = ""
previousZ = ""
previousF = ""

#IMPORTS
import numpy as np
import cv2
import math 

#Open file to receive gcode
gcodeFile = open('smiley.gcode',mode='w')

#Write initial gcode to the file
gcodeLine2 = "g0 z0 f10000\n" #set laser to lowest (off) power
gcodeLine3 = "$L1\n" #Enable Laser mode
gcodeLine1 = "$H\n" #home the axes
gcodeLine4 = "g01 X" + str(turntableCentreDistanceFromEndstop) + " Y0 Z0 F600\n" #get to the centre of the turntable, ready to engrave
gcodeFile.write(gcodeLine1)
gcodeFile.write(gcodeLine2)
gcodeFile.write(gcodeLine3) 
gcodeFile.write(gcodeLine4)


#Open image
inputImgBig = cv2.imread('smiley.png', 0)


inputImg = cv2.resize(inputImgBig,None,fx=.2, fy=.2, interpolation = cv2.INTER_CUBIC)
cv2.imshow('image',inputImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

outputImg = np.zeros((inputImg.shape[0],inputImg.shape[1],1), np.uint8)
outputImg[:,:] = 255
                     

#Determine image size
if inputImg.shape[0] < inputImg.shape[1]:
    imageRadius = inputImg.shape[0] / 2
else:
    imageRadius = inputImg.shape[1] / 2

print "imageRadius "
print imageRadius

#Where's the centre pixel in the image?
xCentrePixel = inputImg.shape[0]/2
yCentrePixel = inputImg.shape[1]/2


#Given how many turns we want in the spiral, how many pixels out does each turn travel?
radiusIncreasePerTurn = imageRadius / numberOfTurns
#radiusIncreasePerRad = radiusIncreasePerTurn / (2 * math.pi)
print "radiusIncreasePerTurn "
print radiusIncreasePerTurn 


#Setup for the loop spiralling outwards
currentRadius = 1 
currentAngle = 1 #needs to be >0 or generates divide by 0 error in first loop
maxAngle = numberOfTurns * 2 * math.pi #because 2pi rad in a circle
numberOfCompletedCircles = 0
print "maxangle"
print maxAngle
while currentAngle < maxAngle:
    #print currentAngle
    xPosition = xCentrePixel + (currentRadius * math.cos(currentAngle))
    yPosition = yCentrePixel + (currentRadius * math.sin(currentAngle))
    pixelColour = inputImg[xPosition, yPosition]
    
    outputImg[xPosition,yPosition] = pixelColour

    numberOfCompletedCircles = int(currentAngle / (2*math.pi))
    #print "numberOfCompletedCircles " + str(numberOfCompletedCircles)
    currentRadius = float((numberOfCompletedCircles * radiusIncreasePerTurn) + 1)
    #print "currentRadius " + str(currentRadius)
    #currentRadius = currentAngle * radiusIncreasePerRad
    currentAngle =  currentAngle + (arcLength / currentRadius) #...change in angle calculated to keep arc length constant
    #print "currentAngle " + str(currentAngle)
    #Two possible methods for engraving:
    #1) Move to new position, pause to fire laser for x seconds, then move to next position
    #2) Change laser intensity, and send next coordinate, i.e. laser is on all the time
    # Will try (2) first. Laser intensity controlled by "spindle speed" gcode because allows use of PWM pin


    laserPower = 255-pixelColour 
    if laserPower <20:
        laserPower = 0 #just in case there's some dodgy rounding error stuff going on.
    
    #gcodeLine1 = "G0 Z" + str(laserPower) + "\n" #Set the new spindle speed (used here for laser power PWM)
    X = str(turntableCentreDistanceFromEndstop + (int(numberOfCompletedCircles) * xmmPerRadiusUnit))
    Y = str(int(currentAngle * ymmPerRadian))
    Z = str(laserPower)
    F = str(feedrate/(2 * math.pi * ((numberOfCompletedCircles+1) * xmmPerRadiusUnit)))

    if laserPower < 50:
        Z = str(0)
        F="4000"
        #gcodeLine2 = "G01 X" + str(turntableCentreDistanceFromEndstop + (int(numberOfCompletedCircles) * xmmPerRadiusUnit)) + " Y" + str(int(currentAngle * ymmPerRadian)) + "Z" + str(laserPower) + " F2000\n"
    gcodeLine2 = "G01 X" + X + " Y" + Y + " Z"+ Z + " F" + F + "\n"
    #if any ([X != previousX, Z != previousZ, F != previousF]):
    #    gcodeFile.write(gcodeLine2)
    #    previousX = X
        #previousY = Y
    #    previousZ = Z
    #    previousF = F
    
        #gcodeFile.write(gcodeLine1)
    gcodeFile.write(gcodeLine2) 
    
    
cv2.imshow('image',outputImg)
cv2.waitKey(0)
outputImg[:,:] = 255
cv2.destroyAllWindows()

gcodeFile.write('M5\n') #command to turn off the laser
gcodeFile.write('$H\n')  #Home the carraige
gcodeFile.close()






