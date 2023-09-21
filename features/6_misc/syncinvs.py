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
    "sync invs"
    if not msg.content.startswith("!syncinvs"):
        return
    if not msg.author.id in team_ids:
        msg.reply('no permission')
        return
    ids = team_ids
    sync_time = msg.content.split(" ")[1] if len(msg.content.split(" ")) > 1 else 24
    sync_time = int(sync_time)
    synced = True
    import time as now
    for e in ids:
        time = client.db.v2getuser("leafSyncTime", e)
        if time and now.time() - time < sync_time * 3600 * 1000:
            continue
        synced = False
        try:
            user = client.users.fetch(e)
            msg.channel.send(f"{user.username}'s inventory not synced")
        except:
            pass
    if synced:
        msg.channel.send(f"all synced") #Let me say it again : Why a formatted string ???
