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
    "view invs"
    if not msg.content.startswith("!viewinv"):
        return
    if not msg.author.id in team_ids:
        msg.reply('no permission')
        return
    if len(msg.content.split(" ")) > 1:
        ids = msg.content.split(" ")[1:]
    else:
        ids = team_ids
    import json
    for e in ids:
        time = client.db.v2getuser("leafSyncTime",e)
        textinv = client.db.v2getuser("leafamount",e) #Yay a new no useless ;
        inv = json.loads(textinv)
        amount = 0
        for a in range(len(inv)):
            amount += inv[a]
            if amount == 0:
                return
            try:
                import time as now
                user = client.users.fetch(e)
                if not time or now.time() - time > 24 * 3600:
                    msg.channel.send(f"WARNING: user's inventory not synced: {user.username}")
                msg.channel.send(f"{user.username}:\n"+textinv)
            except:
                pass

