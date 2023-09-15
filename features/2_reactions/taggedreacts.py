import random

async def run(msg, client):
    "react to tag"
    if client.misc.hastag("woman", msg.author.id):
        try:
            msg.react('☕')
        except:
            pass
    if client.misc.hastag("delikot", msg.author.id):
        try:
            msg.react('🐱')
        except:
            pass
    if client.misc.hastag("littlehawk", msg.author.id):
        try:
            msg.react('🦅')
        except:
            pass
    if client.misc.hastag("🐢", msg.author.id):
        try:
            msg.react('🐢')
        except:
            pass
        try:
            msg.react('1129926033768988724')
        except:
            pass
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
    if client.misc.hastag("weirdcat", msg.author.id):
        try:
            msg.react('1129116659194531930')
        except:
            pass
