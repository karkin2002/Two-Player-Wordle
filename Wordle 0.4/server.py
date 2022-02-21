import socket
from _thread import *
from player import Player
import pickle
from random import choice as randomChoice
from time import time


port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f = open("ipAddress.txt", "r")
host = f.readline()

try:
    s.bind((host, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")


wordFile = open("FiveLetterWords.txt", "r")
fiveLetterWordList = []
for eachFile in wordFile:
    fiveLetterWordList.append(eachFile.replace("\n",""))

wordToGuess = randomChoice(fiveLetterWordList)

print(wordToGuess)

players = [Player(None, wordToGuess), Player(None, wordToGuess)] # Store players object on server istead of client, initalising the player



def threaded_client(conn, player): 
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(8048))
            players[player] = data


            if not data:
                print("Disconnected")
                break
            else:

                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]


            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()



currentPlayer = 0

while True:
    conn, addr = s.accept()  
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    
    currentPlayer += 1 