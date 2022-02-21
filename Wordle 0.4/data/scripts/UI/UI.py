import pygame, time, keyboard, data.scripts.globalVar as globalVar
from sys import exit as sysExit
from data.scripts.UI.printInfo import printInfo
from data.scripts.UI.saveLoadData import loadData, getFilename, searchFiles
from data.scripts.UI.audio import UIAudio
from data.scripts.UI.UIElements import Menu, fpsCounter
globalVar.init()

## UI cass
class UI:
    def __init__(self, 
                    winWidth = 1280, caption = "Caption", 
                    icon = None, volume = 50, 
                    backgroundColour = None, fullscreen = False, 
                    resizable = True, frametime = None, 
                    showFPS = False, buttonAudioCat = "UI"):
        
        pygame.init()

        self.fullscreen = fullscreen
        self.resizable = resizable

        self.winWidth = None
        self.setWinWidth(winWidth)

        self.setWin()

        self.setCaption(caption)

        globalVar.imageDict = {} # Stores all the loaded images for the UI

        self.setIcon(icon)

        ## Clock and framerate
        self.clock = pygame.time.Clock()
        self.lastTime = time.time()
        self.dt = time.time() - self.lastTime
        self.frametime = frametime
        self.framerate = 60 # Framerate for all movements / animations
        self.fpsCounter = fpsCounter()
        self.showFPS = showFPS

        ## Display
        self.backgroundColour = backgroundColour
        pygame.font.init()
        self.menuDict = {}

        ## Input's
        self.inputDict = {}
        self.keybindDir = "data/config/keybinds.json"
        self.loadKeybinds()
        self.keyboardInput = []
        self.lastKeyboardInput = []
        self.setMousePos()
        self.mousePress = [0,0,0]  # 0 == No, 1 == Press, 2 == Hold


        ## Audio
        self.maxNumChannels = 16
        self.audio = UIAudio(volume, self.maxNumChannels)
        self.setButtonAudioCat(buttonAudioCat)

        ## Menu
        self.menuDict = {}



    ##  ------ Window ------  ##

    ## Sets the window up
    def setWin(self):
        if self.fullscreen:
            self.win = pygame.display.set_mode((self.winWidth, self.winHeight), pygame.FULLSCREEN)
        
        elif self.resizable:
            self.win = pygame.display.set_mode((self.winWidth, self.winHeight), pygame.RESIZABLE)

        else:
            self.win = pygame.display.set_mode((self.winWidth, self.winHeight))

    ## Sets fullscreen
    def setFullscreen(self, value):
        if type(value) == bool:
            self.fullscreen == value
        else:
            printInfo("Error", f"setFullscreen - Value is not a bool [{value}]")
        
        self.setWin()

    ## Sets resizable
    def setResizeable(self, value):
        if type(value) == bool:
            self.resizable == value
        else:
            printInfo("Error", f"setResizeable - Value is not a bool [{value}]")
        
        self.setWin()

    ## Sets the caption on the window
    def setCaption(self, caption):
        pygame.display.set_caption(caption)

    ## Sets the height based on the width to keep the winow in a 16:9 ratio
    def setWinHeight(self):
        self.winHeight = round((self.winWidth/16)*9)

    ## Sets the width difference between the window and a length of 1920
    def setWinScale(self):
        globalVar.winScale = self.winWidth / 1920

    ## Sets the window's width
    def setWinWidth(self, width):
        if type(width) == int:
            self.winWidth = width
            self.setWinScale()
            self.setWinHeight()
            self.setWin()
        else:
            printInfo("Error", f"setWinWidth - width is not an int [{width}]")

    ## Resizes the window and menus
    def resize(self):
        self.setWinWidth(self.win.get_width())
        self.resizeAllMenu()

    ## Draw background colour
    def drawBackground(self):
        if self.backgroundColour != None:
            self.win.fill(self.backgroundColour)

    ## Updates the window
    def updateDisplay(self):
        pygame.display.update()

    ## Draws all elements of UI in one neat package 
    def draw(self):
        self.drawBackground()
        self.drawAllMenu()
        self.drawFPS()
        self.updateDisplay()

    ##  ------ Images ------  ##

    ## Loads image to image Dict, returns whether the image has been added
    def loadImage(self, imageDir, imageName = None):

        if imageName == None:
            imageName = getFilename(imageDir)
        
        if type(imageDir) == str:
            try:
                globalVar.imageDict[imageName] = pygame.image.load(imageDir)
                printInfo("Info", f"New image added [{imageName}]")
                return True

            except:
                printInfo("Error", f"loadImage - Image not found [{imageDir}]")
                return False

        else:
            printInfo("Error", f"loadImage - Image dir not string [{imageDir}]")
            return False

    ## Loads all images from a source path
    def loadImagePath(self, dir):
        for eachImage in searchFiles(dir, "png"):
            self.loadImage(eachImage)

    ## Returns image
    def getImage(self, imageName):
        globalVar.getImage(imageName)

    ## Sets Icon image
    def setIcon(self, imageDir):
        if imageDir != None:
            if self.loadImage("windowIcon", imageDir):
                pygame.display.set_icon(self.getImage("windowIcon"))




    ##  ------ Clock ------  ##

    ## Updates delta time, updating game bassed on time elapsed
    def __setDeltaTime(self):
        self.dt = time.time() - self.lastTime # Checks how much time passed dt = delta time
        self.dt *= self.framerate # e.g. One second passing == 60 frames
        self.lastTime = time.time()

    ## Sets how many frames the game updates per second
    def __setClockTick(self):
        if self.frametime != None:
            self.clock.tick(self.frametime)

    ## Update time and FPS
    def updateClock(self):
        self.__setClockTick()

        self.__setDeltaTime()

    def drawFPS(self):
        if self.showFPS:
            self.fpsCounter.checkFrames()
            self.fpsCounter.draw(self.win)


    ##  ------ Inputs ------  ##

    ## Gets the cursor position
    def setMousePos(self):
        self.mousePos = pygame.mouse.get_pos()

    ## Get the mouse button's inputs
    def getMousePress(self, position):
        if type(position) == int:
            if position >= 0 and position <= 2:
                return pygame.mouse.get_pressed()[position]
                
            else:
                printInfo("Error", f"getMousePress - Position should be an int from 0-2")
                return False
        else:
            printInfo("Error", f"getMousePress - Position should be an int from 0-2")
            return False

    ## Sets the mousePress values
    def setMousePress(self):
        for eachPos in range(3):
            if self.getMousePress(eachPos):
                if self.mousePress[eachPos] == 0:
                    self.mousePress[eachPos] = 1
                elif self.mousePress[eachPos] == 1:
                    self.mousePress[eachPos] = 2
            else:
                self.mousePress[eachPos] = 0

    ## Returns whether the button is being pressed
    def isPressMouse(self, buttonPos):
        return self.mousePress[buttonPos] == 1
    
    ## Return whether the button is being held
    def isHoldMouse(self, buttonPos):
        return self.mousePress[buttonPos] == 1 or self.mousePress[buttonPos] == 2
                

    ## Loads keybinds
    def loadKeybinds(self):
        self.keybinds = loadData(self.keybindDir)

    ## Recives keyboard Input
    def setKeyboardInputs(self):
        self.lastKeyboardInput = self.keyboardInput
        self.keyboardInput = []
        
        keyboardEvent = keyboard.get_hotkey_name()
        
        if len(keyboardEvent) > 0:
            input = keyboardEvent.lower()
            self.keyboardInput = input.split('+')

    def setInputs(self):
        self.setMousePress()
        self.setMousePos()
        self.setKeyboardInputs()

    ## Check if a key has been pressed
    def isPressKey(self, keybindName):
        if keybindName in self.keybinds:
            return self.keybinds[keybindName] in self.keyboardInput and self.keybinds[keybindName] not in self.lastKeyboardInput
        else:
            printInfo("Info", f"isPress - Keybind doesn't exist [{keybindName}]")
            return False

    ## Check if key is being held
    def isHoldKey(self, keybindName):
        if keybindName in self.keybinds:
            return self.keybinds[keybindName] in self.keyboardInput
        else:
            printInfo("Info", f"isHold - Keybind doesn't exist [{keybindName}]")
            return False

    ## Check Window state deals with resizing and 
    ## exit window button
    def checkWindowState(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sysExit()

            elif event.type == pygame.VIDEORESIZE:
                self.resize()
    



    ##  ------ Menus ------  ##

    ## Adds menu to menu dict
    def addMenu(self, menuName, x, y, width, height,
                                colour = (0,0,0), alpha = 255,
                                centered = True, display = True):
        
        self.menuDict[menuName] = Menu(x, y, width, height, 
                                    colour, alpha,
                                    centered, display)
        
        printInfo("INFO", f"New menu added [{menuName}]")

    ## Returns menu from menu dict according to its indexed name
    def getMenu(self, menuName):
        return self.menuDict[menuName]

    def getMenuElement(self, menuName, elementName):
        return self.getMenu(menuName).getMenuElement(elementName)

    ## Makes menu redraw all their elements
    def drawMenuElements(self, menuName):
        self.getMenu(menuName).drawElements()

    ## Draws a menu on window surface
    def drawMenu(self, menuName):
        self.getMenu(menuName).draw(self.win)

    ## Draws all menus on window surface
    def drawAllMenu(self):
        for eachMenu in self.menuDict:
            self.drawMenu(eachMenu)

    def resizeMenu(self, menuName):
        self.getMenu(menuName).resize()

    ## Draws all menus on window surface
    def resizeAllMenu(self):
        for eachMenu in self.menuDict:
            self.resizeMenu(eachMenu)

    ## Updates text for a menu text element
    def updateText(self, menuName, elementName, text):
        self.getMenu(menuName).updateText(elementName, text)





    ##  ------ Buttons ------  ##

    ## Sets the audio cat for buttons to use &
    ## creates one if there isn't one
    def setButtonAudioCat(self, audioCatName):
        self.buttonAudioCat = audioCatName
        self.addAudioCat(self.buttonAudioCat)

    ## Returns the name of the button audio cat
    def getButtonAudioCat(self):
        return self.buttonAudioCat

    def getButton(self, menuName, buttonName):
        return self.getMenu(menuName).getMenuElement(buttonName)

    ## Plays the buttons audio
    def getButtonAudio(self, menuName, buttonName):
        button = self.getButton(menuName, buttonName)
        
        if button.pressAudio != None:
            if button.pressAudioPlay:
                self.play(self.buttonAudioCat, button.pressAudio)
        
        if button.hoverAudio != None:
            if button.hoverAudioPlay:
                self.play(self.buttonAudioCat, button.hoverAudio)
        

    ## Updates a button being pressed
    def isPressButton(self, menuName, buttonName, mouseButtonPos):
        press = self.getMenu(menuName).isPress(buttonName, self.mousePos, self.isPressMouse(mouseButtonPos))
        self.getButtonAudio(menuName, buttonName)
        return press
    
    ## Updates a button being held
    def isHoldButton(self, menuName, buttonName, mouseButtonPos):
        press = self.getMenu(menuName).isPress(buttonName, self.mousePos, self.isHoldMouse(mouseButtonPos))
        self.getButtonAudio(menuName, buttonName)
        return press

    ## Adds a box to element dict
    def addBox(self, menuName, elementName, x, y, width, height, 
                    colour = (0,0,0), alpha = 255, 
                    roundedCorner = 0, centered = True, 
                    display = True):

        self.getMenu(menuName).addBox(elementName, 
                                        x, y, width, height, 
                                        colour, alpha, 
                                        roundedCorner, centered, 
                                        display)

        self.drawMenuElements(menuName)

        printInfo("INFO", f"New box element added [{menuName}] [{elementName}]")

    ## Adds a image to element dict
    def addImage(self, menuName, elementName, x, y, 
                    image, scale, 
                    alpha = 255, 
                    centered = True, 
                    display = True):
        
        self.getMenu(menuName).addImage(elementName, 
                                        x, y, 
                                        image, scale, 
                                        alpha, 
                                        centered, 
                                        display)
        
        self.drawMenuElements(menuName)

        printInfo("INFO", f"New image element added [{menuName}] [{elementName}]")

    ## Adds a image to element dict
    def addText(self, menuName, elementName, x, y, 
                    text, size,
                    font = "verdana", 
                    colour = (0,0,0), alpha = 255, 
                    centered = True, display = True):
        
        self.getMenu(menuName).addText(elementName,
                                        x, y, 
                                        text, size, font, 
                                        colour, alpha, 
                                        centered, display)
        
        self.drawMenuElements(menuName)

        printInfo("INFO", f"New text element added [{menuName}] [{elementName}]")

    ## Adds Button Image to element dict
    def addButtonImage(self, menuName, elementName, x, y, 
                    pressImage, unpressImage, 
                    hoverImage = None, pressScale = 1,
                    unpressScale = 1, hoverSacle = 1,
                    alpha = 255, buttonType = "press", 
                    press = False, pressAudio = None, 
                    hoverAudio = None, centered = True, 
                    display = True):
        
        self.getMenu(menuName).addButtonImage(elementName,
                                        x, y, 
                                        pressImage, unpressImage, 
                                        hoverImage, pressScale,
                                        unpressScale, hoverSacle,
                                        alpha, buttonType, 
                                        press, pressAudio, 
                                        hoverAudio, centered, 
                                        display)

        self.drawMenuElements(menuName)

        printInfo("INFO", f"New button element added [{menuName}] [{elementName}]")


    ## Adds Button Text to element dict
    def addButtonText(self, menuName, elementName, x, y, 
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
        
        self.getMenu(menuName).addButtonText(elementName, x, y, 
                    pressText, unpressText, 
                    hoverText, pressSize,
                    unpressSize, hoverSize, 
                    pressColour, 
                    unpressColour, 
                    hoverColour, font, 
                    alpha, buttonType, 
                    press, pressAudio, 
                    hoverAudio, centered, 
                    display)

        self.drawMenuElements(menuName)

        printInfo("INFO", f"New button element added [{menuName}] [{elementName}]")




    ##  ------ Audio ------  ##

    ## Adds new audio category
    def addAudioCat(self, catName, volume = 50):
        self.audio.addAudioCat(catName, volume)

    ## Adds a new audio to a category
    def addAudio(self, catName, dir, audioName = None, volume = 50):
        self.audio.addAudio(catName, dir, audioName, volume)

    ## Adds all audio from a source path
    def addAudioPath(self, catName, dir, volume = 50):
        for eachAudio in searchFiles(dir, "wav"):
            self.addAudio(catName, eachAudio, volume = volume)

    ## Sets volume of an audio category
    def setCatVolume(self, catName, value):
        self.audio.setCatVolume(catName, value)
    
    ## Sets volume of an audio
    def setAudioVolume(self, catName, audioName, value):
        self.audio.setAudioVolume(catName, audioName, value)
    
    ## Plays an audio
    def play(self, catName, audioName, loops = 0):
        self.audio.play(catName, audioName, loops)

    ## Pauses an Audio
    def pause(self, catName, audioName):
        self.audio.pause(catName, audioName)
    
    ## Unpauses an audio
    def unpause(self, catName, audioName):
        self.audio.unpause(catName, audioName)

    ## Queues an audio after another audio
    def queue(self, catName, audioName, audioQueue):
        self.audio.queue(catName, audioName, audioQueue)