from funcs.pastas import Replies

pasta = Replies("copypastas.json")
reacts = Replies("reactions.json")

def run(comm, args, client):
    "at least there's comm in it (but idk what that is)"
    pasta.reload()
    reacts.reload()
    out = True
    switch = {}
    def case():
        print(args[0])
    switch["test"]=case
    def case():
        client.misc.addtag(args[0], args[1])
    switch["addtag"]=case
    def case():
        client.misc.removetag(args[0], args[1])
    switch["removetag"]=case
    def case():
        try:
            client.channels.fetch(args[0]).send(args[1])
        except:
            pass
    switch["channel"]=case
    def case():
        channel = client.get_channel(args[0])
        if channel is None:
            return
        channel.send(args[2])
        import time
        time.sleep(int(args[1]))
        try:
            last_message = (channel.history(limit=1).flatten())[0]
            last_message.delete()
        except Exception as e:
            pass
    switch["flash"]=case
    def case():
        pasta.add(args[0], args.slice(1, args.length))
    switch["addmessage"]=case
    def case():
        id = pasta.findid(args[0])
        if len(id) == 0:
            out = ["reply", "message not found :("]
        else:
            out = ["reply", ""]
            for x in id:
                out[1] += f"id:{x}\n\n{pasta.get(x)[0:500]}\n\n"
    switch["findmessage"]=case
    def case():
        pasta.addreact(args[0], args[1]) #yay, no ;
    switch["addreaction"]=case
    def case():
        reacts = pasta.getreact(args[0])
        out = ["reply", reacts.join('&')] #yay, no ;
    switch["seereactions"]=case
    def case():
        pasta.setmsg(args[0], args[1])
    switch["changemessage"]=case
    def case():
        pasta.setmsg(args[0], pasta.get(args[0]) + args[1])
    switch["appendmessage"]=case
    def case():
        pasta.delet(args[0])
        print(args[0])
    switch["deletemessage"]=case
    def case():
        channel = client.channels.fetch(args[0])
        if channel:
            msg = channel.messages.fetch(args[1])
            if msg:
                msg.delete()
    switch["delete"]=case
    del case
    if comm in switch.keys():
        switch[comm]()
    del switch
    return out
