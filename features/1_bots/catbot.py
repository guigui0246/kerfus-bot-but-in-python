import re

async def run(msg, client):
    """get cat"""
    if (msg.author.id != 966695034340663367 and msg.author.id != 438767282328436737):
        return
    reg = re.compile("^<:.+?:\d+?> .* cat has ", re.I)
    if not reg.search(msg.content):
        return
    msg.channel.send("cat")