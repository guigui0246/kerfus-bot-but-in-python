def run(msg, client) -> str | None:
    "Bans a server"
    if not msg.guild:
        return
    if msg.guild.id == 958367026269782096:
        return 'stop'
