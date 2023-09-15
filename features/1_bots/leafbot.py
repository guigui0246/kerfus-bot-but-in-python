claims = {
  "swift_claim": [
    [8, ["mint_leaf", 4]],
    [8, ["mint_leaf", 3]],

    [7, ["bay_leaf", 3]],
    [7, ["bay_leaf", 2]],

    [6, ["aloe_leaf", 2]],
    [6, ["aloe_leaf", 1]],

    [2, ["jade_leaf", 2]],
    [8, ["jade_leaf", 1]],

    [5, ["monstera_leaf", 1]],

    [2, ["yucca_leaf", 1]],

    [1, ["sedum_leaf", 1]]
  ],
  "daily_claim": [
    [8, ["mint_leaf", 16]],
    [8, ["mint_leaf", 14]],
    [8, ["mint_leaf", 12]],

    [14, ["bay_leaf", 8]],
    [14, ["bay_leaf", 7]],

    [16, ["aloe_leaf", 5]],
    [16, ["aloe_leaf", 4]],

    [16, ["jade_leaf", 4]],
    [16, ["jade_leaf", 3]],
    [16, ["jade_leaf", 2]],

    [12, ["monstera_leaf", 3]],
    [12, ["monstera_leaf", 2]],
    [12, ["monstera_leaf", 1]],

    [10, ["yucca_leaf", 2]],
    [10, ["yucca_leaf", 1]],

    [2, ["sedum_leaf", 2]],
    [6, ["sedum_leaf", 1]],

    [3, ["heuchera_leaf", 1]],

    [1, ["maple_leaf", 1]]
  ],
  
  "turbo_claim":[
    [6, ["mint_leaf", 60]], # 75  6
    [12,["mint_leaf", 50]], # 62.5 7
    [6, ["mint_leaf", 40]], # 50  8
    
    [6, ["bay_leaf", 30]], # 75   6
    [3, ["bay_leaf", 25]], # 62.5 7
    
    [12,["aloe_leaf", 20]], # 100 5
    [6, ["aloe_leaf", 15]], # 75  6
    
    [8, ["yucca_leaf", 5]], # 250 4
    
    [4, ["sedum_leaf", 3]], # 300 3
    
    [4, ["maple_leaf", 1]], # 400 2
    [1, ["agave_leaf", 1]]  # 1600 1
  ]
}

sum = {}
for x in range(len(claims)):
    sum[x] = 0
    for y in claims[x]:
        sum[x] += y[0]

ids = {"therealolie": '438767282328436737',
  "Olie | #TheRakers": '438767282328436737',
  "fake": '558979299177136164',
  "🐢": '704556927018991686',
  "guigui0246 | #TheRakers": '436178855104086037',
  "HeuchEnder08": '373266820792188928',
  "rotatable_cube": '877345121790730252',
  "calionreal": '576065759185338371',
  "milenakos": '553093932012011520',
  "k_lemon": '534806202698432514',
  "fernhalo": '614862278713409543',
  "blaumeise20": '646401965596868628',
  "morningstar37": '772501410092023852',
  "slashred": '872058344003739678',
  "baking leaves": '817212706355413052',
  "birdtree": '485716797706993705',
  "creepz1691": '690699296508739594',
  "itamar_nudge": '1043197880023928944',
  "the_rake_": '822431137544405022',
  "xfexel": '878298928582361120',
  "guigui0246": "436178855104086037",
  "Methman":"817212706355413052"}

times = {
  "swift": 120,
  "daily": 1440,
}

leaves = "Mint Bay Aloe Jade Monstera Yucca Sedum Heuchera Maple Flapjack Agave Echeveria Licorice Tomentosa".split(" ")
defi = {}

for e in range(len(leaves)):
    defi[e] = 0

def otherpeople(msg, client):
    if msg.content != "!togglebroadcastreminder":
        return
    if client.misc.hastag("broadcastremind",msg.author.id):
        client.misc.removetag("broadcastremind",msg.author.id)
    else:
        client.misc.addtag("broadcastremind",msg.author.id)
    msg.reply('toggled')

async def run(msg, client):
    "Leafbot really hard program"
    if msg.author.id != 1073619066272620666:
        otherpeople(msg, client)
        return
    if not msg.interaction:
        return
    import re
    import json
    if msg.interaction.commandName == "garden claim":
        reg = re.compile("^You found x([0-9]+?) \*\*(\w+?) Leaf\*\* in your (\w+?) package\!", re.I)
        temp = reg.search(msg.content)
        if temp == None:
            return
        claim = claims[f"{temp[3]}_claim"]
        weight = -1
        for x in claim:
            if x[1][0] == f"{temp[2].lower()}_leaf" and x[1][1] == temp[1]:
                weight = x[0]
        try:
            msg.channel.send(f"chance: {weight / sum[f'{temp[3]}_claim'] * 100}% ({weight}/{sum[f'{temp[3]}_claim']})")
        except:
            pass
        user = json.loads(client.db.v2getuser("leafamount",msg.interaction.user.id,json.dumps(defi)))
        user[temp[2]] = 1*temp[1] + 1*(user[temp[2]])
        client.db.v2setuser("leafamount",msg.interaction.user.id,json.dumps(user))
        client.misc.log(f"{msg.interaction.user.id} {temp[3]} {temp[1]} {temp[2].lower()}", 'leaflogs.txt')
        try:
            time = times[temp[3]]
        except:
            return
        if not time:
            return
        settings = json.dumps(client.db.v2getuser('settings', msg.interaction.user.id, '{ "autoremind": { "time": 300 } }'))
        if settings["autoremind"]["time"] == -1:
            return
        client.misc.remind(time*60 - settings.autoremind.time, msg.interaction.user, f"reminder for your {temp[3]} package")
    elif msg.interaction.commandName=="garden gift":
        reg = re.compile("^You gave x([0-9]+?) \*\*(\w+?) Leaf\*\* to (.+?)\!", re.I)
        temp = reg.search(msg.content)
        if temp == None:
            return
        to_user = client.users.cache.find(lambda u : u.username == temp[3])
        id  = temp[3]
        if temp[3] in ids.keys():
            id = ids[temp[3]]
        elif to_user != None:
            id = to_user.id
        try:
            msg.channel.send(f"logged transaction: {msg.interaction.user.username} -> {temp[3]}: {temp[1]}x {temp[2]}")
        except:
            pass
        user = json.loads(client.db.v2getuser("leafamount",msg.interaction.user.id,json.dumps(defi)))
        user[temp[2]] = 1*user[temp[2]] -1* temp[1]
        client.db.v2setuser("leafamount",msg.interaction.user.id,json.dumps(user))
        user = json.loads(client.db.v2getuser("leafamount",id,json.dumps(defi)))
        user[temp[2]] = 1*user[temp[2]] + 1* temp[1]
        client.db.v2setuser("leafamount",id,json.dumps(user))
        client.misc.log(f"{msg.interaction.user.id} {id} {temp[1]} {temp[2].lower()}", 'leaflogs2.txt')
    elif msg.interaction.commandName == "broadcast":
        if not msg.content.startswith("Successfully broadcasted"):
            return
        if not client.misc.hastag("broadcastremind",msg.interaction.user.id):
            return
        client.misc.remind(60 * 5, msg.interaction.user, f"reminder for broadcast") #idk why she put it in `` (equivalent fstring) so I put in in a fstring
    elif msg.interaction.commandName=="garden inv":
        embed = msg.embeds[0]
        reg = re.compile("^(.+?)'s collection:$", re.I)
        #print(embed)
        temp = reg.search(embed.title)
        if temp == None:
            return
        user = client.users.cache.find(lambda u : u.username == temp[3])
        id = temp[1]
        if temp[1] in ids:
            id = ids[temp[1]]
        elif not user == None:
            id = user.id
        if id == temp[1]:
            print(f"not found: {id}")
        amounts = {}
        for e in leaves:
            amounts[e] = 0
        for e in embed.fields:
            reg = re.compile("^.*? (.+)$", re.I)
            temp = reg.search(e.name)
            if temp == None:
                return
            amounts[temp[1]] = 1*e.value
        out = f"if:{id}\n\n"
        for i in range(len(amounts)):
            out += f"{i}: {amounts[i]}\n" if amounts[i] != 0 else ""
        msg.channel.send(out)
        import datetime
        client.db.v2setuser("leafSyncTime",id,f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        client.db.v2setuser("leafamount",id,json.dumps(amounts))
    elif msg.interaction.commandName=="garden compost":
        reg = re.compile("^You created... x([0-9]+?) (\w+?) Leaf!", re.I)
        temp = reg.search(msg.content)
        if temp == None:
            return
        user = json.loads(client.db.v2getuser("leafamount",msg.interaction.user.id,json.dumps(defi)))
        user[temp[2]] = 1*user[temp[2]] + 1*temp[1]
        prev_leaf = leaves[leaves.indexOf(temp[2])-1]
        user[prev_leaf] = 1*user[prev_leaf] - 2*temp[1]
        client.db.v2setuser("leafamount",msg.interaction.user.id,json.dumps(user))
