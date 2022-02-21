from time import strftime, localtime

def printInfo(typeMsg,msg):
    
    timeString = strftime("%H:%M:%S", localtime())
    
    print(f"[{typeMsg.upper()}] {timeString}: {msg}.") ## Displays the time, type of message, and the message itself