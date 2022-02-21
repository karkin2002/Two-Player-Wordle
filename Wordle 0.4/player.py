from time import time

class Player():
    def __init__(self, playerName, wordToGuess):
        self.name = playerName
        self.wordleList = ["", "", "", "", "", ""]

        self.wordToGuess = wordToGuess
        self.startTime = None

        self.endTime = None
        self.finished = False

        self.ready = False

    def formatTime(self, time):
        
        timeMin = str(int(time/60))
        timeSec = str(int(time%60))

        if len(timeSec) <= 1:
            timeSec = f"0{timeSec}"

        if len(timeMin) <= 1:
            timeMin = f"0{timeMin}"

        return f"{timeMin}:{timeSec}"


    def setEndTime(self):
        self.endTime = self.getTime()

    def getEndTimeString(self):
        return self.formatTime(self.endTime)
    
    def getTime(self):
        return round(time() - self.startTime)

    def getTimeSting(self):
        return self.formatTime(self.getTime())