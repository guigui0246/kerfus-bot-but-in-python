
def run(msg, client):
    "reverse the string"
    if "reverse" in msg.formatted:
        msg.reply(msg.content[::-1])