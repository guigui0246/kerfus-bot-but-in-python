import re

async def run(msg, client):
    "Mathbot but it does nothing"
    return
    if msg.author.id != 1119928094418018354:
        return
    reg = re.compile("^You're on", re.I) #Wait you're gonna check that it's not a dungeon and not that it's a symbol get ?
    if reg.search(msg.content):
        return
    client.misc.remind(10*60, msg.interaction.user, f"reminder for your symbol get") #Why the heck ?