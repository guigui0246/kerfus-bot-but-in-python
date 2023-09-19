def printgame(game):
    def printrow(row):
        out = ""
        i = 0
        while i < len(row):
            if row[i] == 0:
                out += "\\| "
            else:
                out += "\\| " * row[i] - 1 + "\\|" + '~~'
                i+= row[i] - 1
            i += 1
        return out
    out = ""
    for i in range(len(game)):
        out += 'abcdefghijklmno'[i] + printrow(game[i]) + '\n'
    return out

import json
def run(msg, client):
    """The way to run kreski\n
    I don't know what kreski is but I don't care"""
    if not msg.content.startswith('k!'):
        return
    n = client.db.get('kreskigames.txt',0)
    args = msg.content.split(' ')[1:]
    switch = {}
    def case():
        msg.reply('k!start @opponent to start a game\nk!move (gameid) (move) to move')
        return
    switch["help"] = case
    def case():
        try:
            args[1]
        except IndexError:
            args[1] = 4
        starting = [[0]]
        for i in range(args[1] - 1):
            starting[i+1]=json.loads(json.dumps(starting[i]))
            starting[i].append(0)
            starting[i].append(0)
        client.db.settype('kreski',n+'.json',[msg.author.id,args[0].slice(2,-1),0,starting,starting,'11']) #If I remember correctly it's the 5th time not semi-colon was used
        n = f"{int(n)+1}"
        client.db.set('kreskigames.txt',n)
        msg.reply(f"game started! id: {int(n)-1}\n{printgame(starting)}")
        return
    switch["start"] = case
    def case():
        if len(args) < 2:
            msg.reply("not enough arguments")
            return
        if len(args[1]) < 3:
            msg.reply('move is supposed to be (row)(start)(end)\nfor example b12')
            return
        game = json.loads(client.db.gettype('kreski',args[0]+'.json'))
        if not msg.author.id == game[game[2]]:
            msg.reply('not your turn!')
        try:
            x = 'abcdefghijklmno'.find(args[1][0])
            y = int(args[1][1])
            z = int(args[1][2])
        except:
            return
        allowed = True
        for i in game[3][x][y-1, z]:
            if i != 0:
                allowed = False
        if allowed:
            game[4] = json.loads(json.dumps(game[3]))
            for i in range(y, z, 1):
                game[3][x][i] = 1
            game[3][x][y - 1] = z-y+1
            game[2] = (game[2]+1)%2
        client.db.settype('kreski',args[0]+'.json',game) #6th ?
        cont = False
        for x in game[3]:
            for y in x:
                if not y:
                    cont = True
        if cont:
            msg.reply(printgame(game[3]))
        else:
            msg.reply(f"game ends, <@{game[(game[2]+1)%2]}> wins!")
        return
    switch["move"] = case
    def case():
        if (len(args)<1):
            msg.reply('not enough arguments')
        game = json.loads(client.db.gettype('kreski',args[0]+'.json'))
        if msg.author.id != game[(game[2]+1)%2]:
            msg.reply('not your turn!')
        if game[5][game[2]] == "0":
            msg.reply('you can only undo once')
            game[3] = game[4]
            game[2] = (game[2]+1)%2
            game[5][game[2]] = 0
            client.db.settype('kreski',args[0]+'.json',game)
    switch["undo"] = case
    del case
    switch[msg.content.split(' ')[0][2:].lower()]()
    del switch
