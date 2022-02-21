import pygame
from pygame import Surface, draw, SRCALPHA, transform, font as pyfont, Rect
from data.scripts.basic import setTimer, isTimer, getTime, timeElapsed
import data.scripts.globalVar as globalVar

## Sets the alpha for a surface
def setSurfaceAlpha(surf, alpha):
    if alpha < 255:
        surf.set_colorkey((0,0,100))
        surf.set_alpha(alpha)
    
    return surf


## Returns a surface to display text
def createText(text, font, colour, size):

    if font in pyfont.get_fonts():
        fontFormat = pyfont.SysFont(font, size)
    else:
        fontFormat = pyfont.Font(f"{font}.ttf", size)

    message = fontFormat.render(text, True, colour)

    return message


## Creates a surface
def createSurface(width, height, colour, alpha):
    surfaceWidth, surfaceHeight = round(width* globalVar.winScale), round(height * globalVar.winScale)
    
    if colour == None:
        newSurface = Surface((surfaceWidth, surfaceHeight), SRCALPHA)

        newSurface = setSurfaceAlpha(newSurface, alpha)
    
    else:
        newSurface = Surface((surfaceWidth, surfaceHeight))

        newSurface = setSurfaceAlpha(newSurface, alpha)
        
        draw.rect(newSurface, colour, (0,0, surfaceWidth, surfaceHeight))

    return newSurface



## Superclass for UI Elements
class UIElement:
    def __init__(self, x, y, width, height, 
                    alpha = 255, centered = True, 
                    display = True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.setWinPos()
        
        self.alpha = alpha

        self.centered = centered
        self.display = display

    ## Sets x and y pos for menu on window
    def setWinPos(self):
        self.xWinPos = round(self.x * globalVar.winScale)
        self.yWinPos = round(self.y * globalVar.winScale)
        self.xWinPosCenter = round((self.x - self.width/2) * globalVar.winScale)
        self.yWinPosCenter = round((self.y - self.height/2) * globalVar.winScale)

    ## Draw menu surface
    def draw(self, surf):
        if self.display:
            if self.centered == False:
                surf.blit(self.surface, (self.xWinPos, self.yWinPos))
            
            else:
                surf.blit(self.surface, (self.xWinPosCenter, self.yWinPosCenter))
    
    ## Resize the menu
    def resize(self):
        self.setWinPos()
        self.setSurface()





## Button
class Button(UIElement):
    def __init__(self, x, y, alpha = 255, 
                    buttonType = "press", press = False, 
                    pressAudio = None, hoverAudio = None, 
                    centered = True, display = True):
        
        super().__init__(x, y, 0, 0, alpha, centered, display)

        self.press = press
        self.hover = False
        self.pressCounter = 0

        self.update = False

        self.setSurface()
        self.setState(self.press, self.hover)

        ## Used in UI class to say whether pressAudio should play
        self.pressAudioPlay = False
        self.hoverAudioPlay = False

        self.pressAudio = pressAudio
        self.hoverAudio = hoverAudio

    ## Sets surface for a type of button state
    def setButtonSurface(self, originalSurf, width, height):
        newSurf = transform.scale(originalSurf, 
            (round(width * globalVar.winScale), round(height * globalVar.winScale)))

        return setSurfaceAlpha(newSurf, self.alpha)
        
    ## Sets the surface
    def setSurface(self):

        ## Creating button surface states
        self.pressSurface = self.setButtonSurface(self.originalPressSurface, 
            self.pressSurfaceWidth, self.pressSurfaceHeight)

        self.unpressSurface = self.setButtonSurface(self.originalUnpressSurface, 
            self.unpressSurfaceWidth, self.unpressSurfaceHeight)

        self.hoverSurface = self.setButtonSurface(self.originalHoverSurface, 
            self.hoverSurfaceWidth, self.hoverSurfaceHeight)

        ## Rect used for collision, based on unpress surface
        if self.centered:
            self.buttonRect = Rect(round((self.x - self.unpressSurfaceWidth/2) * globalVar.winScale), 
                round((self.y - self.unpressSurfaceHeight/2) * globalVar.winScale), 
                round(self.unpressSurfaceWidth * globalVar.winScale), round(self.unpressSurfaceHeight * globalVar.winScale))
        else:
            self.buttonRect = Rect(self.xWinPos, self.yWinPos, 
                round(self.unpressSurfaceWidth * globalVar.winScale), round(self.unpressSurfaceHeight * globalVar.winScale))


    ## Sets surface, width, height
    def setSurfaceWidthHeight(self, surf, width, height):
            self.surface = surf
            self.width = width
            self.height = height
            self.setWinPos()

    ## Resize the the button
    def resize(self):
        self.setWinPos()
        self.setSurface()

        ## Redraws the button depending on state
        if self.press:
            self.setSurfaceWidthHeight(self.pressSurface, self.pressSurfaceWidth, self.pressSurfaceHeight)
        elif self.hover:
            self.setSurfaceWidthHeight(self.hoverSurface, self.hoverSurfaceWidth, self.hoverSurfaceHeight)
        else:
            self.setSurfaceWidthHeight(self.unpressSurface, self.unpressSurfaceWidth, self.unpressSurfaceHeight)


    ## Sets the button state
    def setState(self, press, hover = False):

        self.pressAudioPlay = False
        self.hoverAudioPlay = False
        
        if self.press == False and press == True:
            self.setSurfaceWidthHeight(self.pressSurface, self.pressSurfaceWidth, self.pressSurfaceHeight)
            self.update = True
            
            self.pressAudioPlay = True

        elif self.hover == False and hover == True: 
            self.setSurfaceWidthHeight(self.hoverSurface, self.hoverSurfaceWidth, self.hoverSurfaceHeight)
            self.update = True
            
            if self.press == False: # Makes sure hover audio doesn't play after letting go of button
                self.hoverAudioPlay = True

        elif (self.press == True or self.hover == True) and press == False and hover == False:
            self.setSurfaceWidthHeight(self.unpressSurface, self.unpressSurfaceWidth, self.unpressSurfaceHeight)
            self.update = True

        self.press = press
        self.hover = hover
    
    ## Check collision with mouse
    def isCollision(self, mousePos):
        return self.buttonRect.collidepoint(mousePos)

    ## Check button press
    def isPress(self, mousePos, mouseClick):
        self.update = False

        if mouseClick:
            if self.isCollision(mousePos):
                self.setState(True)

        else:
            if self.isCollision(mousePos):
                self.setState(False, True)
            else:
                self.setState(False)

        return self.press

class ButtonText(Button):
    def __init__(self, x, y, 
                    pressText, unpressText, 
                    hoverText = None, pressSize = 1,
                    unpressSize = 1, hoverSize = 1, 
                    pressColour = (0, 0, 0), 
                    unpressColour = (0, 0, 0), 
                    hoverColour = (0, 0, 0), 
                    font = "verdana",
                    alpha = 255, buttonType = "press", 
                    press = False, pressAudio = None, 
                    hoverAudio = None, centered = True, 
                    display = True):

                
        self.pressText = pressText
        self.pressSize = pressSize
        self.pressColour = pressColour

        self.unpressText = unpressText
        self.unpressSize = unpressSize
        self.unpressColour = unpressColour

        self.hoverText = hoverText
        self.hoverSize = hoverSize
        self.hoverColour = hoverColour

        self.font = font


        
        super().__init__(x, y, alpha, 
                    buttonType, press, 
                    pressAudio, hoverAudio, 
                    centered, display)

        self.setSurfaceWidthHeight(self.unpressSurface, self.unpressSurface.get_width(), self.unpressSurface.get_height())

        self.resize()

    ## Sets the surface
    def setSurface(self):

        ## Creating button surface states
        self.pressSurface = createText(self.pressText, self.font, self.pressColour, 
                                        round(self.pressSize * globalVar.winScale))

        self.unpressSurface = createText(self.unpressText, self.font, self.unpressColour, 
                                        round(self.unpressSize * globalVar.winScale))

        self.hoverSurface = createText(self.hoverText, self.font, self.hoverColour, 
                                        round(self.hoverSize * globalVar.winScale))


    ## Sets x and y pos for menu on window
    def setWinPos(self):
        self.xWinPos = round(self.x * globalVar.winScale)
        self.yWinPos = round(self.y * globalVar.winScale)
        self.xWinPosCenter = round(self.x * globalVar.winScale) - self.width/2
        self.yWinPosCenter = round(self.y * globalVar.winScale) - self.height/2


    ## Resize the the button
    def resize(self):
        self.setSurface()

        ## Redraws the button depending on state
        if self.press:
            self.setSurfaceWidthHeight(self.pressSurface, self.pressSurface.get_width(), self.pressSurface.get_height())
        elif self.hover:
            self.setSurfaceWidthHeight(self.hoverSurface, self.hoverSurface.get_width(), self.hoverSurface.get_height())
        else:
            self.setSurfaceWidthHeight(self.unpressSurface, self.unpressSurface.get_width(), self.unpressSurface.get_height())

        ## Rect used for collision, based on unpress surface
        if self.centered:
            self.buttonRect = Rect(self.xWinPosCenter, self.yWinPosCenter, 
                self.unpressSurface.get_width(), self.unpressSurface.get_height())
        else:
            self.buttonRect = Rect(self.xWinPos, self.yWinPos, 
                self.unpressSurface.get_width(), self.unpressSurface.get_height())

        self.setWinPos()



    ## Sets the button state
    def setState(self, press, hover = False):

        self.pressAudioPlay = False
        self.hoverAudioPlay = False
        
        if self.press == False and press == True:
            self.setSurfaceWidthHeight(self.pressSurface, self.pressSurface.get_width(), self.pressSurface.get_height())
            self.update = True
            
            self.pressAudioPlay = True

        elif self.hover == False and hover == True: 
            self.setSurfaceWidthHeight(self.hoverSurface, self.hoverSurface.get_width(), self.hoverSurface.get_height())
            self.update = True
            
            if self.press == False: # Makes sure hover audio doesn't play after letting go of button
                self.hoverAudioPlay = True

        elif (self.press == True or self.hover == True) and press == False and hover == False:
            self.setSurfaceWidthHeight(self.unpressSurface, self.unpressSurface.get_width(), self.unpressSurface.get_height())
            self.update = True

        self.press = press
        self.hover = hover




## Image Button
class ButtonImage(Button):
    def __init__(self, x, y, 
                    pressImage, unpressImage, 
                    hoverImage = None, pressScale = 1,
                    unpressScale = 1, hoverSacle = 1,
                    alpha = 255, buttonType = "press", 
                    press = False, pressAudio = None, 
                    hoverAudio = None, centered = True, 
                    display = True):
        
        self.pressImage = pressImage
        self.pressScale = pressScale
        self.originalPressSurface, self.pressSurfaceWidth, self.pressSurfaceHeight = self.getSurfaceSetup(
            self.pressImage, self.pressScale)

        self.unpressImage = unpressImage
        self.unpressScale = unpressScale
        self.originalUnpressSurface, self.unpressSurfaceWidth, self.unpressSurfaceHeight = self.getSurfaceSetup(
            self.unpressImage, self.unpressScale)

        self.hoverImage = hoverImage
        self.hoverSacle = hoverSacle
        self.originalHoverSurface, self.hoverSurfaceWidth, self.hoverSurfaceHeight = self.getSurfaceSetup(
            self.hoverImage, self.hoverSacle)
        
        super().__init__(x, y, alpha, 
                    buttonType, press, 
                    pressAudio, hoverAudio, 
                    centered, display)

        self.setSurfaceWidthHeight(self.pressSurface, self.pressSurfaceWidth, self.pressSurfaceHeight)

    ## Gets the scaled surface & it's width & height
    def getSurfaceSetup(self, image, scale):
        originalImageSurface = self.getScaledImage(image, scale)
        imageSurfaceWidth = originalImageSurface.get_width()
        imageSurfaceHeight = originalImageSurface.get_height()
        
        return originalImageSurface, imageSurfaceWidth, imageSurfaceHeight


    ## Scales button image
    def getScaledImage(self, image, scale):
        buttonSurf = globalVar.getImage(image)
        return transform.scale(buttonSurf, (
            round(buttonSurf.get_width()*scale), 
            round(buttonSurf.get_height()*scale)))


    ## Sets surface for a type of button state
    def setButtonSurface(self, originalSurf, width, height):
        newSurf = transform.scale(originalSurf, 
            (round(width* globalVar.winScale), round(height * globalVar.winScale)))

        return setSurfaceAlpha(newSurf, self.alpha)





## Text
class Text(UIElement):
    def __init__(self, x, y, text, size,
                    font = "verdana", 
                    colour = (0,0,0), alpha = 255, 
                    centered = True, display = True):
        
        super().__init__(x, y, 0, 0, alpha, centered, display)

        self.text = text
        self.size = size
        self.font = font
        self.colour = colour
        self.setSurface()
        self.setWinPos()

    ## Sets the surface
    def setSurface(self):
        self.surface = createText(self.text, self.font, self.colour, round(self.size * globalVar.winScale))

        self.surface = setSurfaceAlpha(self.surface, self.alpha)

        self.width = round(self.surface.get_width() / globalVar.winScale)
        self.height = round(self.surface.get_height() / globalVar.winScale)

    ## Updates the text
    def updateText(self, text):
        self.text = text
        self.setSurface()
        self.setWinPos()




## Image
class Image(UIElement):
    def __init__(self, x, y, 
                    image, scale, alpha = 255, centered = True, 
                    display = True):        
        
        self.image = image
        self.scale = scale

        ## Sets width and height based on image's dimensions and scale
        width = globalVar.getImage(self.image).get_width() * scale
        height = globalVar.getImage(self.image).get_height() * scale
        
        super().__init__(x, y, width, height, alpha, centered, display)

        self.setSurface()

    ## Sets the surface
    def setSurface(self):
        self.surface = createSurface(self.width, self.height, None, self.alpha)
        self.surface.blit(transform.scale(globalVar.getImage(self.image), 
            (round(self.width * globalVar.winScale), round(self.height * globalVar.winScale))), (0,0))

            


## Box
class Box(UIElement):
    def __init__(self, x, y, width, height, 
                    colour = (0,0,0), alpha = 255, 
                    roundedCorner = 0, centered = True, 
                    display = True):
        
        super().__init__(x, y, width, height, alpha, centered, display)

        self.colour = colour
        self.roundedCorner = roundedCorner
        self.setSurface()

    ## Sets the surface
    def setSurface(self):
        if self.roundedCorner > 0:
            self.surface = createSurface(self.width, self.height, None, self.alpha)
        
        else:
            self.surface = createSurface(self.width, self.height, (0,0,0), self.alpha)

        draw.rect(self.surface, self.colour, (0, 0, round(self.width * globalVar.winScale),round(self.height * globalVar.winScale)),
            border_radius = round(self.roundedCorner * globalVar.winScale))

    




## Menu
class Menu(UIElement):
    def __init__(self, x, y, width, height, 
                    colour = (0,0,0), alpha = 255, 
                    centered = True, display = True):
        
        super().__init__(x, y, width, height, alpha, centered, display)

        self.colour = colour
        self.setSurface()

        self.menuElements = {}


    ## Sets the surface
    def setSurface(self):
        self.surface = createSurface(self.width, self.height, self.colour, self.alpha)

    ## Return width
    def getWidth(self):
        return self.width
    
    ## Return height
    def getHeight(self):
        return self.height

    ## Add element to menuElements
    def addElement(self, elementName, element):
        self.menuElements[elementName] = element

    ## Resize elements & menu surface
    def resize(self):
        for eachElement in self.menuElements:
            self.menuElements[eachElement].resize()

        self.setWinPos()
        self.setSurface()

        self.drawElements()

    ## Draws elements on Menu surface
    def drawElements(self):
        if self.colour != None:
            self.surface.fill(self.colour)
        for eachElement in self.menuElements:
            self.menuElements[eachElement].draw(self.surface)

    ## Checks whether it needs to update the surface
    def isPress(self, buttonName, mousePos, mouseClick):
        
        ## Gets the mouse position in relation to the menu
        if self.centered:
            menuMousePos = [mousePos[0] - self.xWinPosCenter, mousePos[1] - self.yWinPosCenter]
        else:
            menuMousePos = [mousePos[0] - self.xWinPos, mousePos[1] - self.yWinPos]
       
        ## Checks the buttons state & if it should be updated
        press = self.menuElements[buttonName].isPress(menuMousePos, mouseClick)
        if self.menuElements[buttonName].update == True:
            self.drawElements()

        return press

    ## Returns a menu element
    def getMenuElement(self, elementName):
        return self.menuElements[elementName]

    ## Updates text element's text
    def updateText(self, elementName, text):
        self.getMenuElement(elementName).updateText(text)
        self.drawElements()




    ## Adds a box to element dict
    def addBox(self, elementName, x, y, width, height, 
                    colour = (0,0,0), alpha = 255, 
                    roundedCorner = 0, centered = True, 
                    display = True):
        
        self.addElement(elementName, Box(x, y, width, height, 
                                        colour, alpha, 
                                        roundedCorner, centered, 
                                        display))

    ## Adds a image to element dict
    def addImage(self, elementName, x, y, 
                    image, scale, 
                    alpha = 255, 
                    centered = True, 
                    display = True):
        
        self.addElement(elementName, Image(x, y, 
                                        image, scale, 
                                        alpha, 
                                        centered, 
                                        display))

    ## Adds a image to element dict
    def addText(self, elementName, x, y, 
                    text, size,
                    font = "verdana", 
                    colour = (0,0,0), alpha = 255, 
                    centered = True, display = True):
        
        self.addElement(elementName, Text(x, y, 
                                        text, size, font, 
                                        colour, alpha, 
                                        centered, display))

    ## Adds Button Image to element dict
    def addButtonImage(self, elementName, x, y, 
                    pressImage, unpressImage, 
                    hoverImage = None, pressScale = 1,
                    unpressScale = 1, hoverSacle = 1,
                    alpha = 255, buttonType = "press", 
                    press = False, pressAudio = None, 
                    hoverAudio = None, centered = True, 
                    display = True):
        
        self.addElement(elementName, ButtonImage(x, y, 
                                            pressImage, unpressImage, 
                                            hoverImage, pressScale,
                                            unpressScale, hoverSacle,
                                            alpha, buttonType, 
                                            press, pressAudio, 
                                            hoverAudio, centered, 
                                            display))


    ## Adds Button Text to element dict
    def addButtonText(self, elementName, x, y, 
                    pressText, unpressText, 
                    hoverText = None, pressSize = 1,
                    unpressSize = 1, hoverSize = 1, 
                    pressColour = (0, 0, 0), 
                    unpressColour = (0, 0, 0), 
                    hoverColour = (0, 0, 0), 
                    font = "verdana",
                    alpha = 255, buttonType = "press", 
                    press = False, pressAudio = None, 
                    hoverAudio = None, centered = True, 
                    display = True):
        
        self.addElement(elementName, ButtonText(x, y, 
                                            pressText, unpressText, 
                                            hoverText, pressSize,
                                            unpressSize, hoverSize, 
                                            pressColour, 
                                            unpressColour, 
                                            hoverColour, font,
                                            alpha, buttonType, 
                                            press, pressAudio, 
                                            hoverAudio, centered, 
                                            display))





##  ------ FPS & Frametime ------  ##

class fpsCounter:
    def __init__(self, display = False):
        self.__setSecondTimer()
        self.frames = 0

        self.__setFrametimeTimer()
        self.frametime = 0

        self.__setFramesText()

    ## Creates text used to diplay fps and ft
    def __setFramesText(self):
        self.framesText = createText(f"{self.frames} fps  |  {self.frametime} ms","bahnschrift", 
                                    (255,255,255), 
                                    round(20*globalVar.winScale))

    ## Sets new 1 sec time so count frames in 1 sec
    def __setSecondTimer(self):
        self.secondTimer = setTimer(1)

    ## Gets the current time
    def __setFrametimeTimer(self):
        self.frametimeTimer = getTime()

    ## Checks how much time has pased since last frame
    ## Converts it into ms, gets the current time again
    def __setFrametime(self):
        self.frametime = timeElapsed(self.frametimeTimer)
        self.frametime = round(self.frametime * 1000) # 1000 converts it from s to ms
        self.__setFrametimeTimer()

    ## Checks if second timer is up and updates
    ## the frame text and rests fram counts
    def __setFrames(self):
        self.frames += 1
        if isTimer(self.secondTimer):
            self.__setFramesText()
            self.__setSecondTimer()
            self.frames = 0

    def checkFrames(self):
        self.__setFrametime()
        self.__setFrames()

    def draw(self, surf):
        surf.blit(self.framesText, (
            round(8*globalVar.winScale), 
            round(3*globalVar.winScale)))

