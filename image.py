#Preamble

#Variables for configuration
numberOfTurns = 40 #how many turns on the spiral
arcLength = 2      #Burn a spot every n units around the arc

#IMPORTS
import numpy as np
import cv2
import math 


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
    currentAngle = currentAngle + (arcLength / currentRadius) #...change in angle calculated to keep arc length constant

    

   
cv2.imshow('image',outputImg)
cv2.waitKey(0)
outputImg[:,:] = 255
cv2.destroyAllWindows()






