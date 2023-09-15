from ...funcs import pastas as replies

async def run(msg, client):
    "Make the reactions using an object ?!!?!"
    if not msg.guild:
        return
    reacts = replies.Replies("reactions.json", client)
    for i in range(len(reacts)):
        if not reacts.includes(msg.formatted, i):
            continue
        if not reacts.allowed(i, msg.guild.id, msg.channel.id):
            continue
        reactions = reacts.get(i)
        for j in reactions:
            try:
                msg.react(j)
            except:
                pass
