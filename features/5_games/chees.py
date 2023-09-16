import math as meth

startingpos = [
  ["+rook","+horse","+bishop","+queen","+king","+bishop","+horse","+rook"],
  ["+pawn","+pawn","+pawn","+pawn","+pawn","+pawn","+pawn","+pawn"],
  ["","","","","","","",""],
  ["","","","","","","",""],
  ["","","","","","","",""],
  ["","","","","","","",""],
  ["-pawn","-pawn","-pawn","-pawn","-pawn","-pawn","-pawn","-pawn"],
  ["-rook","-horse","-bishop","-queen","-king","-bishop","-horse","-rook"]
]

game = None

def isNumeric(n) -> bool:
    try:
        return meth.isfinite()
    except ValueError:
        return False

def printgame(board):
    if not board:
        return "game not found"
    out = ""
    for i in range(8, 0, -1):
        for j in board[i]:
            if j == "" or j[2] == "g":
                out+="` ` "
            else:
                out+=("*" if j[0]=="+" else "") + f"*{j[1].upper()}*" + ("* " if j[0]=="+" else " ")
        out += '\n'
    return out

def isempty(board, move):
    """
    Is it normal for a isempty function to output something else than a bool ?\n
    NO !
    """
    mov = [min(move[0],move[2]),
           min(move[1],move[3]),
           max(move[0],move[2]),
           max(move[1],move[3]),
           ]
    dir = [(mov[0]==move[0])*2-1,(mov[1]==move[1])*2-1]
    out = True
    if mov[0] == mov[2]:
        for e in board[mov[0]][mov[1]+1:mov[3]]:
            out &= e == "" or e[2] == "g"
        return 'rook' if out else False
    elif mov[1] == mov[3]:
        for e in board[mov[0]+1:mov[2]]:
            out &= e[mov[1]] == "" or e[mov[1]][2] == "g"
        return "rook" if out else False
    elif mov[2]-mov[0]==mov[3]-mov[1]:
        global game
        j = move[1]
        for i in range(move[0], move[2], dir[0]):
            if game[3][i][j] is not "" and game[3][i][j][1] is not "g": #Raises a SyntaxWarning, I don't care => to fix later by changing is not by !=
                return False
            j+=dir[1]
        #return "vbishop" 				#This is the original, what 0lie put
        return "bishop" 				#And this is the probably working one
    return False

def run(msg, client):
    """
    Run the commands of the game
    """
    if not msg.content.startswith("c!"):
        return
    content = msg.content.split(" ")
    id = msg.author.id
    global game
    switch = {}
    def case():
        temp = client.db.v2get(f"chess/{content[1]}.json")
        msg.reply(printgame(temp[3]))
    switch["c!see"] = case
    def case():
        msg.reply(f"command list:\n> !start <opponent>\n\n> !move <gameid> <move>\n example: !move 69 a1b1\n\n> !cleargames (only for me)\n\n") #But who is "me"
    switch["c!help"] = case
    def case():
        amount = int(client.db.v2get('other/chessgames.txt',0))
        client.db.v2set('other/chessgames.txt',amount+1) #First time I see 0lie not putting the optionnal ;
        import json
        client.db.v2set(f"chess/{amount}.json",json.dumps([id,content[1][2:-1],"+",startingpos,"1111"])) #And this is the 2nd time
        msg.reply(f"game started! id:{amount}") # 3rd time
        msg.reply(printgame(startingpos)) #And then a ; again
    switch["c!start"] = case
    def case():
        amount = client.db.v2get('other/chessgames.txt',0)
        if (not meth.isNumeric(content[1])) or content[1]>=amount:
            msg.reply(f"game id {content[1]} not found :(")
            return True
        import json
        game = json.loads(client.db.v2get(f"chess/${content[1]}.json"))
        if not (game[2] == "+" and game[0] == id or game[2] == "-" and game[1] == id):
            return True
        move = [content[2][1]-1, "abcdefgh".find(content[2][0]), content[2][3]-1, "abcdefgh".find(content[2][2])]
        for x in move:
            if x<0 or x>7:
                msg.reply("moves outside the board :(")
                return True
        _from:str = game[3][move[0]][move[1]]
        to:str = game[3][move[2]][move[3]]
        if move[0]==move[2] and move[1]==move[3]:
            msg.reply("you cant skip a turn!")
            return True
        if _from == "":
            msg.reply("This spot is empty!")
            return True
        if not _from.startswith(game[2]):
            msg.reply("not your figure")
            return True
        if to.startswith(game[2]):
            msg.reply("you can't take your figure")
            return True
        a = move[3] - move[1]
        b = move[2] - move[0]
        a = abs(a)
        b = abs(b)
        switch_move = {}
        def case_move():
            if move[3] == move[1]:
                if (b==1 or (b==2 and (move[0]==1 or move[0]==6) and game[3][(move[2]+move[0])/2][move[1]]=="") and to==""):
                    game[3][move[2]][move[3]] = game[3][move[0]][move[1]]
                    game[3][move[0]][move[1]] = ""
                    if b == 2:
                        game[3][(move[2]+move[0])/2][move[1]] = game[2] + "ghostpawn."
                else:
                    return True
            elif b == 1 and a == 1:
                if to[1:] == "ghostpawn":
                    game[3][move[0]][move[3]] = ""
                game[3][move[2]][move[3]] = game[3][move[0]][move[1]]
                game[3][move[0]][move[1]] = ""
            else:
                return True
            if(move[2]==0 or move[2]==7):
                game[3][move[2]][move[3]] = game[3][move[2]][move[3]][0] + "queen"
        switch_move["pawn"] = case_move
        def case_move():
            if (isempty(game[3], move) == "rook"):
                game[3][move[2]][move[3]] = game[3][move[0]][move[1]]
                game[3][move[0]][move[1]] = ""
            else:
                return True
        switch_move["rook"] = case_move
        def case_move():
            if a*b == 2:
                game[3][move[2]][move[3]] = game[3][move[0]][move[1]]
                game[3][move[0]][move[1]] = ""
            else:
                return True
        switch_move["horse"] = case_move
        def case_move():
            if isempty(game[3],move)=="bishop":
                game[3][move[2]][move[3]] = _from
                game[3][move[0]][move[1]] = ""
            else:
                return True
        switch_move["bishop"] = case_move
        def case_move():
            if isempty(game[3],move): #I think you supposed to try == "rook" and == "bishop" (or 'vbishop') instead of one or the other
                game[3][move[2]][move[3]] = game[3][move[0]][move[1]]
                game[3][move[0]][move[1]] = ""
            else:
                return True
        switch_move["queen"] = case_move
        def case_move():
            if a<2 and b<2 : #I think you're supposed to verify you can't get eaten where you go to verify if there's no draw
                game[3][move[2]][move[3]] = game[3][move[0]][move[1]]
                game[3][move[0]][move[1]] = ""
                return
            if not (a == 2 and b == 0):
                return True
            if not isempty(game[3], move):
                return True
            if ''.join(move) == '0402' and game[4][0] == '1':
                game[3][0][0]=""
                game[3][0][2]="+king"
                game[3][0][3]="+rook"
                game[3][0][4]=""
            elif ''.join(move) == '0406' and game[4][1] == '1':
                game[3][0][4]=""
                game[3][0][5]="+rook"
                game[3][0][6]="+king"
                game[3][0][7]=""
            elif ''.join(move)=="7472" and game[4][2]=="1":
                game[3][7][0]=""
                game[3][7][2]="-king"
                game[3][7][3]="-rook"
                game[3][7][4]=""
            elif ''.join(move)=="7476" and game[4][3]=="1":
                game[3][7][4]=""
                game[3][7][5]="-rook"
                game[3][7][6]="-king"
                game[3][7][7]=""
            else:
                return True
        switch_move["king"] = case_move
        del case_move
        if (switch_move[_from[1:]]()):
            return
        del switch_move
        for i in range(len(game[3])):
            for j in range(len(game[3][i])):
                if game[3][i][j][1:] == "ghostpawn":
                    game[3][i][j] = ""
        for i in range(len(game[3])): #Did you know that "en passant" is French for "passing by" ?
            for j in range(len(game[3][i])):
                if game[3][i][j][1:] == "ghostpawn.":
                    game[3][i][j] = game[3][i][j][0]+"ghostpawn"
        if _from == "+king":
            game[4] = '00'+game[4][2:]
        if _from == "-king":
            game[4] = +game[4][0:2]+'00'
        temp = [[0,0],[0,7],[7,0],[7,7]]
        for i in range(4): #len(temp) = 4
            if [move[0],move[1]]==temp[i] or [move[2],move[3]]==temp[i]:
                game[4][i] = "0"
        msg.reply(printgame(game[3]))
        if game[2] == '+':
            game[2] = '-'
        else:
            game[2] = "+"
        client.db.v2set(f"chess/{content[1]}.json",json.dumps(game))
    switch["c!move"] = case
    def case():
        if id != 438767282328436737:
            return True
        amount = client.db.v2get('other/chessgames.txt',0)
        for x in amount:
            client.db.v2set(f"chess/{x}.json",'[]')
        client.db.v2set('otherchessgames.txt',0) #4th time no ;
    switch["c!cleargames"] = case
    def case():
        game = client.db.v2get(f"chess/{content[1]}.json")
        #if id in [game[0],game[1],438767282328436737]:				#This is the original, what 0lie put
        if not id in [game[0],game[1],438767282328436737]:			#And this is the correct one
            return True
        client.db.v2del(f"chess/{content[1]}.json")
    switch["c!delgame"] = case
    del case
    if (switch[content[0]]()):
        return
    del switch
