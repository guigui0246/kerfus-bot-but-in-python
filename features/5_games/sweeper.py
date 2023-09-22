"""This is a minesweeper working differently than other minesweeper\n
The catch is that what's shown is using cosinu, sinus and rounding\n
Now please give me size !!!"""
import math

DEF_SIZE = 5
MINEAMOUNT = 0.2
OUTSIZE = 5

isNumeric = math.isfinite
"""
not used as this exists due to js implementation
"""

def printboard(board, amount):
    "Prints the board"
    out = ""
    for x in range(len(board)):
        outt=""
        for y in range(len(board[x])):
            if board[x][y] == -1:
                sum = [0, 0]
                for x1 in range(-1, 2):
                    for y1 in range(-1, 2):
                        if x-x1>-1 and y-y>-1 and x-x1<size and y-y1<size:
                            if board[x - x1][y - 1]>0:
                                sum[0] += math.cos(board[x-x1][y-y1]*6.283185/amount)
                                sum[1] += math.sin(board[x-x1][y-y1]*6.283185/amount)
                real = str(round(sum[0], 4))
                imag = str(round(sum[1], 4))
                if real=='0':
                    out += '`'+" "*OUTSIZE+'` '
                else:
                    out += '`'+real[0:OUTSIZE]+" "*(OUTSIZE-len(real))+'` '
                if imag=='0':
                    outt += '`'+" "*math.floor(OUTSIZE)+'` '
                else:
                    outt += '`'+real[0:OUTSIZE]+" "*(math.floor(OUTSIZE-len(real)))+'` '
            else:
                out += '`'+"#"*OUTSIZE+'` '
                outt += '`'+"#"*OUTSIZE+'` '
        out += "\n"+outt+"\n\n"
    return out

import json
def run(msg, client):
    "Run the minesweeper"
    if not msg.content.lower().startswith('m!'):
        return
    args = msg.content.split(' ')[1:]
    player = json.loads(client.db.v2getuser("sweeper",msg.author.id))
    switch = {}
    def case():
        if len(args) < 1:
            msg.reply('too little arguments')
            return
        size = args[1] or DEF_SIZE
        board = []
        import random
        for x in range(size):
            board.append([])
            for _ in range(size):
                if random.random()<MINEAMOUNT:
                    board[x].append(math.floor(random.random()*args[0])+1)
                else:
                    board[x].append(0)
        player = {}
        player["board"] = board
        player["mta"] = args[0]
        msg.reply('started probably idk') #I'm scared if even 0lie doesn't know if the start function works
        return
    switch["start"] = case
    def case():
        if not player:
            msg.reply('you have to start a game!')
            return
        if len(args) < 2:
            msg.reply('too few agruments')
            return
        if (not math.isfinite(args[0]) or not math.isfinite(args[1])): #Might need to convert first
            msg.reply('expected 2 intigers') #Integers not intigers
            return
        x, y = args[:2]
        if player["board"][x][y]>0:
            msg.reply('you clicker a mine!')
            del player["board"]
            del player["mta"]
        else:
            player["board"][x][y] = -1
            msg.reply(printboard(player["board"],player["mta"]))
        return
    switch["sweep"] = case
    def case():
        msg.reply('welcome to the complex minesweeper!\nin this minesweeper, there are N different mine types\neach mine\'s value is one of the Nths roots of unity\nthe values on the cells are the sum of values of the neighbouring 8 cells(empty=0)\ntop is the real part, bottom is the imaginary part\n\ncommands:\n[]-> optional,\n> m!start mine_type_amount [board_size=5]\n\n> m!sweep x y\nnote: 0-indexed, so for a 5x5 board the possibilities are 0,1,2,3,4')
        return
    switch["help"] = case
    del case
    switch[msg.content.split(' ')[0][2:].lower()]()
    del switch
    if player == {}:
        client.db.v2deluser("sweeper",msg.author.id)
    else:
        client.db.v2setuser("sweeper",msg.author.id,json.dumps(player))
