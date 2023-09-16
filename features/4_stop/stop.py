def run(msg, client):
    "remove missing guild or being bot"
    if (not msg.guild) or msg.author.bot:
        return "stop"