import random

async def run(msg, client):
    "react to tag"
    if client.misc.hastag('nopastas', msg.guild.id if msg.guild else 0) or client.misc.hastag('nopastas',msg.channel.id):
        return False
    if msg.author.bot:
        try:
            msg.react('🐱')
        except:
            pass
    elif (random.random() < 0.05):
        try:
            msg.react('🐱')
        except:
            pass
    for x in [
        ['woman','☕'],
        ['delikot','🐱'],
        ['littlehawk','🦅'],
        ['🐢','🐢','1129926033768988724'],
        ['weirdcat','1129116659194531930'],
        ['wiktoria','✨'],
        ['fart','🇫','🇦','🇷','🇹']
    ]:
        if client.misc.hastag(x[0],msg.author.id):
            for y in x[1:]:
                try:
                    msg.react(y)
                except:
                    pass
