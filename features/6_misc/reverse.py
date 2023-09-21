
def run(msg, client):
    if "reverse" in msg.formatted:
        msg.reply(msg.content[::-1])