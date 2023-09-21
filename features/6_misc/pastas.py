from ...funcs import pastas

def run(msg, client):
    """run the pastas"""
    if msg.guild==1121125014096318615:
        return
    if msg.content.startswith("!") :
        return
    pasta = pastas.Replies("copypastas.json", client)
    pasta.reload()
    for i in range(len(pasta)):
        if not pasta.includes(msg.formatted, i):
            continue
        if not pasta.allowed(i, msg.guild.id, msg.channel.id):
            continue
        reply = client.misc.sliceby(pasta.get(i), 2000)
        for j in reply:
            msg.reply(j)
