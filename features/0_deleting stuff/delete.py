import base64
import re

def run(msg, client):
    """Polish message for readability by the bot\n
    And then verify krzys isn't in it"""
    msg.formatted = re.compile("[\"\'*.]").sub(client.misc.polishchars(f"{msg.content}").lower(), "")
    #if not "krzys" in msg.formatted:										# Exchange the place of # to
    if not base64.b64decode('a3J6eXM=').decode('utf-8') in msg.formatted:	# change between slow and fast way
        return
    client.misc.log(msg.content)
    out = 'stop'
    try:
        msg.delete()
    except:
        pass
    return out