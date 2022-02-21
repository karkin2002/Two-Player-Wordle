from data.scripts.UI.UI import UI
from time import time
from random import randint
from network import Network
from player import Player
import pyperclip

def addBlockText(menuName, blockName, fontSize):
    x = window.getMenuElement(menuName, blockName).x
    y = window.getMenuElement(menuName, blockName).y
    window.addText(menuName, f"Text {blockName}", x, y-3, " ", fontSize, "WordleFontBold", colour=(255, 255, 255))




def addWordleBlock(menuName, rowNum, startY, gapSize, blockScale):

    centerMenu = window.getMenu(menuName).width / 2

    window.addImage(menuName, f"Block {rowNum}-2", centerMenu, startY, "wordleBlock", blockScale)
    width = window.getMenuElement(menuName, f"Block {rowNum}-2").width
    height = window.getMenuElement(menuName, f"Block {rowNum}-2").height

    window.addImage(menuName, f"Block {rowNum}-1", centerMenu - (width + gapSize), startY, "wordleBlock", blockScale)

    window.addImage(menuName, f"Block {rowNum}-0", centerMenu - (width*2 + gapSize*2), startY, "wordleBlock", blockScale)
    window.addImage(menuName, f"Block {rowNum}-3", centerMenu + (width + gapSize), startY, "wordleBlock", blockScale)
    window.addImage(menuName, f"Block {rowNum}-4", centerMenu + (width*2 + gapSize*2), startY, "wordleBlock", blockScale)

    for i in range(5):
        addBlockText(menuName, f"Block {rowNum}-{i}", 45)

    return startY + height + gapSize




def addWordleBoard(menuName, startY, gapSize, blockScale):
    for i in range(6):
        startY = addWordleBlock(menuName, i, startY, gapSize, blockScale)



def updateLetter(menuName, rowNum, letterIndex, type):
    x = window.getButton(menuName, f"Block {rowNum}-{letterIndex}").x
    y = window.getButton(menuName, f"Block {rowNum}-{letterIndex}").y
    scale = window.getButton(menuName, f"Block {rowNum}-{letterIndex}").scale
    
    if type == 0:
        window.addImage(menuName, f"Block {rowNum}-{letterIndex}", x, y, "wordleBlockGrey", scale)
    elif type == 1:
        window.addImage(menuName, f"Block {rowNum}-{letterIndex}", x, y, "wordleBlockYellow", scale)
    else:
        window.addImage(menuName, f"Block {rowNum}-{letterIndex}", x, y, "wordleBlockGreen", scale)












window = UI(1280, caption="Wordle", showFPS=True)

window.loadImagePath("data/images/UI/")
window.addAudioPath("UI", "data/audio/UI/")
window.addAudioCat("Click", 100)
window.addAudioPath("Click", "data/audio/click/", 100)

window.addMenu("Client Wordle", 960, 0, 960, 1080, (18, 18, 19), centered = False)
addWordleBoard("Client Wordle", 180, 10, 3)
window.addText("Client Wordle", "Title", 480, 70, "YOUR WORDLE", 40, "WordleFontRoman", colour=(255,255,255))

window.addMenu("Server Wordle", 0, 0, 960, 1080, (18, 18, 19), centered = False)
addWordleBoard("Server Wordle", 180, 10, 3)
window.addText("Server Wordle", "Title", 480, 70, "OPPONENT WORDLE", 40, "WordleFontRoman", colour=(255,255,255))

window.addMenu("Timer", 960, 440, 230, 80, colour = (18, 18, 19), centered=True)
window.addText("Timer", "Timer", 115, 40, "00:00", 80, "WordleFontLight", colour=(255, 255, 255))

nameWidth = 740
nameHeight = 180
window.addMenu("NameBack", 960, 400, nameWidth, nameHeight, colour = (0,0,0), alpha = 150, centered=True)
window.addBox("NameBack", "Background", 0, 0, nameWidth, nameHeight, centered=False)
window.addMenu("Name", 960, 400, nameWidth, nameHeight, colour = None, centered=True)
addWordleBlock("Name", 0, nameHeight/2, 10, 4)
addBlockText("Name", "Block 0-0", 60)

window.addMenu("Share", 960, 800, 260, 100, colour = (18, 18, 19), centered=True, display=False )
window.addBox("Share", "Background", 0, 0, 260, 100, colour=(83, 141, 78), roundedCorner=10, centered=False)
window.addButtonText("Share", "ShareButton", 129, 47, "SHARE", "SHARE", "SHARE", 40, 40, 40,
    (178, 178, 178), (255, 255, 255), (204, 204, 204), "WordleFontBold")


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


n = Network()
clientServerData = n.getP() # recieves inital player object from server


gameEnd = False

maxGuesses = 6
guessNum = 0
otherClientGuesses = 0
letterIndex = 0

wordToGuess = clientServerData.wordToGuess
wordList = ["", "", "", "", ""]
word = ""

timer = ""

p2Results = False


wordFile = open("FiveLetterWords.txt", "r")
fiveLetterWordList = []
for eachFile in wordFile:
    fiveLetterWordList.append(eachFile.replace("\n",""))



while clientServerData.name == None:
    ## Timing and Inputs
    window.updateClock()
    window.setInputs()
    window.checkWindowState()

    if letterIndex < 5:
        for eachLetter in alphabet:
            if window.isPressKey(eachLetter):
                window.play("Click", f"click ({randint(1,4)})")
                wordList[letterIndex] = eachLetter
                window.updateText("Name", f"Text Block 0-{letterIndex}", eachLetter.upper())
                letterIndex += 1
    else:
        if window.isPressKey("enter"):
            for eachLetter in wordList:
                word += eachLetter
            
            clientServerData.name = word
            window.updateText("Client Wordle", "Title", f"{word.upper()} WORDLE")

    if letterIndex > 0:
        if window.isPressKey("backspace"):
            letterIndex -= 1
            window.updateText("Name", f"Text Block 0-{letterIndex}", " ")

    ## Drawing
    window.draw()

window.getMenu("Name").display = False
window.getMenu("NameBack").display = False

letterIndex = 0
wordList = ["", "", "", "", ""]
word = ""

p2Name = None


while clientServerData.startTime == None:
    ## Timing and Inputs
    window.updateClock()
    window.setInputs()
    window.checkWindowState()

    p2 = n.send(clientServerData)

    if p2Name == None:
        if p2.name != None:
            window.updateText("Server Wordle", "Title", f"{p2.name.upper()} WORDLE")
        p2Name = p2.name

    if window.isHoldKey("enter"):
        clientServerData.ready = True
    else:
        clientServerData.ready = False
    
    if clientServerData.ready == True and p2.ready == True:
            clientServerData.startTime = time()

    ## Drawing
    window.draw()


clipboardString = None

## Main Loop
runGame = True
while runGame:
    ## Timing and Inputs
    window.updateClock()
    window.setInputs()
    window.checkWindowState()

    if not gameEnd:
        if letterIndex < 5:
            for eachLetter in alphabet:
                if window.isPressKey(eachLetter):
                    window.play("Click", f"click ({randint(1,4)})")
                    wordList[letterIndex] = eachLetter
                    window.updateText("Client Wordle", f"Text Block {guessNum}-{letterIndex}", eachLetter.upper())
                    letterIndex += 1
        else:
            if window.isPressKey("enter"):
                
                for eachLetter in wordList:
                    word += eachLetter

                if word in fiveLetterWordList:
                    
                    clientServerData.wordleList[guessNum] = ""

                    i = 0
                    for eachLetter in word:
                        if eachLetter == wordToGuess[i]:
                            updateLetter("Client Wordle", guessNum, i, 2)
                            clientServerData.wordleList[guessNum] += "G"
                        elif eachLetter in wordToGuess:
                            updateLetter("Client Wordle", guessNum, i, 1)
                            clientServerData.wordleList[guessNum] += "Y"
                        else:
                            updateLetter("Client Wordle", guessNum, i, 0)
                            clientServerData.wordleList[guessNum] += "X"
                        i += 1

                    guessNum += 1

                    if wordToGuess == word or guessNum == maxGuesses:
                        gameEnd = True
                        print("GAME OVER")

                    letterIndex = 0
                    wordList = ["", "", "", "", ""]
                
                word = ""

        if letterIndex > 0:
            if window.isPressKey("backspace"):
                letterIndex -= 1
                window.updateText("Client Wordle", f"Text Block {guessNum}-{letterIndex}", " ")
    
    else:
        if clientServerData.endTime == None:
            clientServerData.setEndTime()
            
            window.addText("Client Wordle", "endTime", 480, 850, 
                clientServerData.getEndTimeString(), 60, 
                "WordleFontLight", colour=(255, 255, 255))
            
            if clientServerData.wordleList[guessNum-1] == "GGGGG":
                window.addText("Client Wordle", "endText", 480, 950, 
                    "COMPLETE", 60, 
                    "WordleFontBold", colour=(100, 200, 100))
            
            else:
                window.addText("Client Wordle", "endText", 480, 950, 
                    "FAIL", 60, 
                    "WordleFontBold", colour=(200, 100, 100))
            
            clientServerData.finished = True

    





    p2 = n.send(clientServerData)


    if p2Results == False:
        if otherClientGuesses < maxGuesses:
            p2Word = p2.wordleList[otherClientGuesses]

            if p2Word != "":

                for eachLetter in wordList:
                    word += eachLetter

                i = 0
                for eachBlock in p2Word:
                    if p2Word[i] == "G":
                        updateLetter("Server Wordle", otherClientGuesses, i, 2)
                    elif p2Word[i] == "Y":
                        updateLetter("Server Wordle", otherClientGuesses, i, 1)
                    else:
                        updateLetter("Server Wordle", otherClientGuesses, i, 0)
                    i += 1
                
                otherClientGuesses += 1
        
        if p2.endTime != None:
            window.addText("Server Wordle", "endTime", 480, 850, 
                p2.getEndTimeString(), 60, 
                "WordleFontLight", colour=(255, 255, 255))
            
            if p2.wordleList[otherClientGuesses-1] == "GGGGG":
                window.addText("Server Wordle", "endText", 480, 950, 
                    "COMPLETE", 60, 
                    "WordleFontBold", colour=(100, 200, 100))
            
            else:
                window.addText("Server Wordle", "endText", 480, 950, 
                    "FAIL", 60, 
                    "WordleFontBold", colour=(200, 100, 100))
            
            p2Results = True


    if not(p2Results == True and clientServerData.endTime != None):
        clientTime = clientServerData.getTimeSting()
        if timer != clientTime:
            timer = clientTime
            window.updateText("Timer", "Timer", clientTime)
    
    else:
        if window.isHoldButton("Share", "ShareButton", 0):
            pyperclip.copy(clipboardString)

        if clipboardString == None:
            window.getMenu("Share").display = True

            clipboardString = f"{p2.getEndTimeString()} **{p2.name.upper()}** =VS= **{clientServerData.name.upper()}** {clientServerData.getEndTimeString()}\n"
            for i in range(6):
                
                if p2.wordleList[i] != "":
                    clipboardString += p2.wordleList[i].replace("X","⬛").replace("Y","🟨").replace("G","🟩")
                else:
                    clipboardString += "⬛⬛⬛⬛⬛"
                
                clipboardString += " "
                
                if clientServerData.wordleList[i] != "":
                    clipboardString += clientServerData.wordleList[i].replace("X","⬛").replace("Y","🟨").replace("G","🟩")
                else:
                    clipboardString += "⬛⬛⬛⬛⬛"
                
                clipboardString += "\n"
            

    ## Drawing
    window.draw()