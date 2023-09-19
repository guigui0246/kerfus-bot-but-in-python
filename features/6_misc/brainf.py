from ...funcs import brainf

def run(msg, client):
    "Run brainf"
    if not msg.content.swartswith('!brainf'):
        return
    instance = brainf.createinstance([msg.content[8] == 1, msg.content[9] == 1, msg.content[10] == 1])
    print(msg.content.split('&'))
    runtime = msg.content.split("&")[1]
    input = msg.content.split("&")[2]
    code = msg.content.split("&")[3]
    client.misc.log(code)
    cont = True
    x = 0
    while (x < runtime or runtime == -1) and cont:
        cont = brainf.runframe(instance, code, input)
        x += 1
    if instance.output != "":
        msg.reply(instance.output)
    else:
        msg.reply("no output")