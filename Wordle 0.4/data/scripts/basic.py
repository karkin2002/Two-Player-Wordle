from pygame import mask as pymask
from math import sin, sqrt
from time import time, sleep


## ------ Math  ------ ##

## Returns a x or y, from an x or y input
def sinWave(value, origin, wavelength, amplitude):
    return sin(value/wavelength) * amplitude + origin

## Returns distance between two points
def distanceBetweenPoints(x1,y1,x2,y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

## Expoentially move towards a point
def exponential(point1, point2, velocity, exponentialValue, dt):
    distance = abs(point1 - point2)

    distanceVelocity = distance / exponentialValue

    if point1 > point2:
        point1 -= (velocity * distanceVelocity) * dt
    
    elif point1 < point2:
        point1 += (velocity * distanceVelocity) * dt

    return point1

## Checks whether a point is in a circle
def inCircle(circlePos,r,pointPos): 
    return ((pointPos[0] - circlePos[0]) * (pointPos[0] - circlePos[0]) + 
        (pointPos[1] - circlePos[1]) * (pointPos[1] - circlePos[1]) <= r * r)



## ------  Collide  ------ ##

## Create a mask from an image
def createMask(image):
    return pymask.from_surface(image)

## Checks if the mask is collides with another
def checkMaskCollision(mask1, x1, y1, mask2, x2, y2):

    offset = (round(x2 - x1), round(y2 - y1))

    return mask1.overlap(mask2, offset)



## ------  Time  ------ ##

## Returns the time in seconds
def getTime():
    return time()

## Shows the amount of time passed in seconds
def timeElapsed(oldTime):
    return time() - oldTime

## Enter the time in seconds until the timer ends
def setTimer(seconds):
    return time() + seconds

## Retruns True if the timer is done
def isTimer(timer):
    return timer - time() <= 0