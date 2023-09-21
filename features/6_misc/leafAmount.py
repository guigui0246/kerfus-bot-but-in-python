team_ids = [
  '438767282328436737',
  '558979299177136164',
  '704556927018991686',
  '436178855104086037',
  '373266820792188928',
  '877345121790730252',
  '576065759185338371',
  '553093932012011520',
  '534806202698432514',
  '614862278713409543',
  '646401965596868628',
  '772501410092023852',
  '872058344003739678',
  '817212706355413052',
  '485716797706993705',
  '1043197880023928944',
  '822431137544405022',
  '878298928582361120'
]

def run(msg, client):
    "leafAmount (i don't know what that is yet)"
    if not msg.content.startswith("!countleaves"):
        return
    if msg.author.id not in team_ids:
        msg.reply("no permission")
        return
    if len(msg.content.split(" ")) > 1:
        ids = msg.content.split(" ")[1:]
    else:
        ids = team_ids
    index = {}
    amounts = []
    for e,i in enumerate("Mint Bay Aloe Jade Monstera Yucca Sedum Heuchera Maple Flapjack Agave Echeveria Licorice Tomentosa".split(" ")):
        index[e] = i
        amounts.append(0)
    import json
    for e in ids:
        temp = client.db.v2getuser("leafamount", e)
        temp = json.loads(temp)
        for i in range(len(temp)):
            amounts[index[i]] += int(temp[i]) # I put int because I don't think float would be useful
    power = 0
    for e, i in enumerate(amounts):
        power += e*int("1 2 5 10 20 50 100 200 400 800 1600 3000 5500 10000".split(" ")[i])
    out = f"total power: {power}\nteam's total:\n"
    for i in range(len(index)):
        out += f"{i}: {amounts[index[i]]}\n"
    import math
    for i in range(len(amounts)-1):
        amounts[i+1]+=math.floor(amounts[i]/2)
        amounts[i]%=2
    msg.channel.send(out)
    power = 0
    for e,i in enumerate(amounts):
        power += e*2**i
    mintgoal = 1
    while(mintgoal < power):
        mintgoal*2
    out = f"optimal power: {power*1.5625}\nmint amount: {power}/{mintgoal}\nafter compression:\n"
    for i in range(len(index)):
        out += f"{i}: {amounts[index[i]]}\n"
    msg.channel.send(out)
