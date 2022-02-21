from pygame import mixer
from data.scripts.UI.printInfo import printInfo
from data.scripts.UI.saveLoadData import getFilename

## Sets volume of audio class
def setAudioVolume(audio, value):
    audio.set_volume(value/100)
        


## Sets num of audio channels
def setNumChannels(value):
    mixer.set_num_channels(value)

## Gets the num of audio channels
def getNumChannels():
    return mixer.get_num_channels()

## Adds a new channel
def addChannel():
    setNumChannels(getNumChannels()+1)

## finds an empty channel, creates new if no empty
def findChannel(maxChannels):
    audioChannel = mixer.find_channel()
    
    if audioChannel != None:
        return audioChannel
    
    else:
        if getNumChannels() < maxChannels:
            addChannel()
            printInfo("Info", f"Added new Channel [{getNumChannels()}]")
            return mixer.Channel(getNumChannels()-1)

        else:
            printInfo("Info", f"findChannel - Max Channels reached [{getNumChannels()}]")





## Audio Category
class AudioCategory:
    def __init__(self, name, volume, channel = False):
        self.name = name
        self.volume = volume
        self.mute = False

        self.audioDict = {}
    

    ## Returns the name of the audio category
    def getName(self):
        return self.name
    
    ## Returns the volume of an audio
    def getVolume(self):
        return self.volume
    
    ## checks if an audio is in the audioDict
    def isAudio(self, name):
        if name in self.audioDict:
            return True
        else:
            printInfo("Error", f"isAudio - Audio doesn't exist [{name}]")

    ## returns a audio class
    def __getAudio(self, name):
        return self.audioDict[name]

    # Sets the volume of the category
    def setCatVolume(self, overallVolume, value):
        self.volume = value
        for eachAudio in self.audioDict:
            self.setAudioVolume(eachAudio, overallVolume)

    ## Sets the volume of an audio
    def setAudioVolume(self, name, overallVolume, value = None):
        if self.isAudio(name):
            audio = self.__getAudio(name)
            if value != None:
                audio.setVolume(value)

            # (overall*(category/100))*(audio/100)
            volumeValue = (overallVolume * (self.volume/100)) * (audio.getVolume()/100)
            setAudioVolume(audio.getAudio(), volumeValue)
        else:
            printInfo("Error", f"setAudioVolume - Audio doesn't exist [{name}]")

    ## Adds audio to the audioDict and sets its volume, doesn't play the audio
    def addAudio(self, name, dir, overallVolume, volume = 50):
        if name == None:
            name = getFilename(dir)
        self.audioDict[name] = Audio(name, dir, volume)
        self.setAudioVolume(name, overallVolume, value = None)
        
        printInfo("INFO", f"New audio added [{self.name}] [{name}]")

    ## Plays audio
    def playAudio(self, name, maxChannels, loops = 0):
        self.__getAudio(name).play(maxChannels, loops)

    ## Finds which channel an audio is playing in
    def __findChannelByAudio(self, name):
        audio = self.__getAudio(name).audio
        for eachChannel in range(getNumChannels()):
            if mixer.Channel(eachChannel).get_sound() == audio:
                return eachChannel

    ## Pauses an audio
    def pauseAudio(self, name):
        mixer.Channel(self.__findChannelByAudio(name)).pause()

    ## Unpauses an audio
    def unpauseAudio(self, name):
        mixer.Channel(self.__findChannelByAudio(name)).unpause()

    ## Queues an audio after another audio on a channel
    def queueAudio(self, audioName, audioQueueName):
        if self.isAudio(audioName) and self.isAudio(audioQueueName):
            channel = self.__findChannelByAudio(audioName)
            mixer.Channel(channel).queue(self.__getAudio(audioQueueName).getAudio())

        else:
            printInfo("Error", f"queueAudio - audioName or audioQueueName name is invalid [{audioName, audioQueueName}]")



## Audio
class Audio:
    def __init__(self, name, dir, volume = 50):
        self.name = name
        self.setVolume(volume)

        self.audio = mixer.Sound(dir) 

    def getName(self):
        return self.name

    def getVolume(self):
        return self.volume

    def setVolume(self, value):
        self.volume = value

    def getAudio(self):
        return self.audio

    def play(self, maxChannels, loops = 0):
        channel = findChannel(maxChannels)
        if channel != None:
            channel.play(self.audio, loops)







## Class used for all audio on the UI
class UIAudio:
    def __init__(self, volume, maxChannels = 16, frequency = 44100, size = -16, channels = 2, buffer = 512, deviceName = None):
        self.volume = volume

        self.catDict = {}

        mixer.pre_init(frequency, size, channels, buffer, deviceName) # Initialising the mixer
        mixer.init()

        self.maxChannels = maxChannels

        if maxChannels < getNumChannels():
            setNumChannels(maxChannels)
        
    ## Returns whether the category exists
    def __isCat(self, catName):
        return catName in self.catDict

    ## Retruns the audio cat object
    def __getAudioCat(self, catName):
        return self.catDict[catName]

    ## Adds a new Audio Cat to a dict
    def addAudioCat(self, catName, volume = 50):
        if not self.__isCat(catName):
            self.catDict[catName] = AudioCategory(catName, volume)
        else:
            printInfo("Info", f"addAudioCat - Audio Category already exist [{catName}]")

    ## Adds an audio to an audioCat
    def addAudio(self, catName, dir, audioName = None , volume = 50):
        if self.__isCat(catName):
            self.__getAudioCat(catName).addAudio(audioName, dir, self.volume, volume)
    
    ## Sets the volume of the audioCat
    def setCatVolume(self, catName, value):
        if self.__isCat(catName):
            self.__getAudioCat(catName).setCatVolume(self.volume, value)

    ## Sets the audio in the audioCat
    def setAudioVolume(self, catName, audioName, value):
        if self.__isCat(catName):
            self.__getAudioCat(catName).setAudioVolume(audioName, self.volume, value)

    ## Plays an audio
    def play(self, catName, audioName, loops = 0):
        if self.__isCat(catName):
            if self.__getAudioCat(catName).isAudio(audioName):
                self.__getAudioCat(catName).playAudio(audioName, self.maxChannels, loops)

    ## Pauses the audio
    def pause(self, catName, audioName):
        if self.__isCat(catName):
            if self.__getAudioCat(catName).isAudio(audioName):
                self.__getAudioCat(catName).pauseAudio(audioName)

    ## Unpauses the audio
    def unpause(self, catName, audioName):
        if self.__isCat(catName):
            if self.__getAudioCat(catName).isAudio(audioName):
                self.__getAudioCat(catName).unpauseAudio(audioName)

    ## Queue an audio
    def queue(self, catName, audioName, audioQueueName):
        if self.__isCat(catName):
            self.__getAudioCat(catName).queueAudio(audioName, audioQueueName)