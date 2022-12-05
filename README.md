# Two-Player-Wordle

This is an adaptation of the popular online game Wordle, written from scratch in Python. Two players go head to head to guess a five letter word. The first player to get the word wins, however each player only gets 6 guesses, making the game a balance between time and accuracy. After an intense game you can share your results using the “share” button which copies the results onto your clipboard, ready for you to post!

Python Sockets were implemented to allow users to play between devices across a network. For the visuals I used the pygame framework along with my own custom UI code.

For the gameplay, the server selects a word from a list and send it to each client. Players type their names in and the timer begins. Although players can’t see their opponents guesses, they can still view their progression through the coloured boxes. After each player has either completed or failed the timer stops and the players can share their results.

RUN REQUIREMENTS:
- Python 3.10
- pygame 2.0

Make sure to run the server file first before running the Wordle file

Put your IV4 IP address into the IPADDRESS.txt file
