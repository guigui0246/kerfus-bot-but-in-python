def run(msg, client):
    if client.misc.hastag("admin", msg.author.id) and '&' in msg.content:
        from ... import admin
        action = admin.run(msg.content.split('&')[0],msg.content.split('&')[1:], client)
        if action[0] == "reply":
            msg.reply(action[1])
        if action:
            return "stop"
