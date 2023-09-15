def run(msg, client):
    """Does nothing because of this return\n
    Remove it to do something for gerry\n
    I didn't try to make it work because it's not used"""
    return
    def collectorFilter_f (reaction, user):
        print(reaction, "abc", user)
        return reaction.emoji.name == "gerald" and int(user.id) == 1120441619720699905
    collectorFilter = collectorFilter_f
    del collectorFilter_f
    #print(msg)
    def f(col):
        print(col)
        col.first().remove()
    try:
        f(msg.awaitReactions({"filter":collectorFilter,
        "max": 1,
        "time": 60000,
        "errors":["time"]}))
    except:
        pass