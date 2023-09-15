def run(msg, client):
    """This remove every messgae from people 0lie is afraid of
    She's a little girl scared of ghosts or what ?"""
    if not client.misc.hastag("phobic", msg.author.id):
        return
    client.misc.log(msg.content)
    out = 'stop'
    try:
        msg.delete()
    except:
        pass
    return out