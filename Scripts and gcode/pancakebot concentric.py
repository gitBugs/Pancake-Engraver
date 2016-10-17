#Preamble

#Variables for configuration
numberOfTurns = 40 #how many turns on the spiral
turntableCentreDistanceFromEndstop = 75 #how far is the centre of the turntable from the x-axis endstop?
arcLength = 02      #Burn a spot every n units around the arc
ymmPerRadian = 31.8   #NB: will be dependant on the steps/mm setting on the GRBL board. Can that be set in gcode?
xmmPerRadiusUnit = (75 / numberOfTurns) #because we have about 75mm to play with
feedrate = 2000

#IMPORTS
import numpy as np
import cv2
import math 

#Open file to receive gcode
gcodeFile = open('gcodeFile',mode='w')

#Write initial gcode to the file
gcodeLine1 = "S0\n" #Laser PWM to 0, just in case
gcodeLine2 = "$H\n" #home the X-axis
gcodeLine3 = "G10 P0 L20 Y0\n" #Reset the Y axis
gcodeLine4 = "g01 X" + str(turntableCentreDistanceFromEndstop) + " Y0 F600\n" #get to the centre of the turntable, ready to engrave
gcodeFile.write(gcodeLine1)
gcodeFile.write(gcodeLine2)
gcodeFile.write(gcodeLine3)
gcodeFile.write(gcodeLine4)


#Open image
inputImgBig = cv2.imread('shhmlogo.png', 0)


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


    laserPower = 1000-(pixelColour * ( float(1000)/float(255)))  #Scale the value from the range used by pixel colour (0-255) to that used by spindle speed (0-1000). NB: Need to explicitly cast at least one of the numbers in a division as a float, otherwise Python defaults to integer maths (e.g. 1/2=0).
    if laserPower <0:
        laserPower = 0 #just in case there's some dodgy rounding error stuff going on.
    
    gcodeLine1 = "S" + str(laserPower) + "\n" #Set the new spindle speed (used here for laser power PWM)
    gcodeLine2 = "M3\n" #set the actual PWM to the new spindle speed
    gcodeLine3 = "G01 X" + str(turntableCentreDistanceFromEndstop + (int(numberOfCompletedCircles) * xmmPerRadiusUnit)) + " Y" + str(int(currentAngle * ymmPerRadian)) + " F" + str(feedrate/((float(numberOfCompletedCircles/4)*xmmPerRadiusUnit*1.5)+1)) + "\n"
    if laserPower < 100:
        gcodeLine3 = "G01 X" + str(turntableCentreDistanceFromEndstop + (int(numberOfCompletedCircles) * xmmPerRadiusUnit)) + " Y" + str(int(currentAngle * ymmPerRadian)) + " F2000\n"
    gcodeFile.write(gcodeLine1)
    gcodeFile.write(gcodeLine2)
    gcodeFile.write(gcodeLine3)
    

    
cv2.imshow('image',outputImg)
cv2.waitKey(0)
outputImg[:,:] = 255
cv2.destroyAllWindows()

gcodeFile.write('M5') #command to turn off the laser
gcodeFile.write('$H')  #Home the carraige
gcodeFile.close()






