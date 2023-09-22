"What's reply for sudo ?"

async def run(msg, client):
    "use async to call the console"
    _run(msg, client)

def _run(msg, client):
    if not msg.content.startswith('!console '):
        return
    import json
    data = json.loads(client.db.v2getuser(f"console", msg.author.id, '{"dir":"/"}')) #Don't know why a formatted string fo console
    text = ' '.join(msg.content.split(" ")[1:])
    sudo = False
    if text.split(" ")[0] == 'sudo':
        if client.misg.hastag("admin", msg.author.id):
            sudo = True
            text = ' '.join(text.split(' ')[1:])
        else:
            msg.reply(reply+f"{msg.author.username} is not in the sudoers file. This incident will be reported.```")
            return
    out = "```root@win 10 ~]#" + text + '\n'

    def index(list, fun):
        val = -1
        for i, e in enumerate(list):
            if val != -1:
                return
            if fun(e,i):
                val = i
        return val

    def fixdir(dir):
        while "/./" in dir:
            dir = dir.replace("/./", "/")
        while "//" in dir:
            dir = dir.replace("//", "/")
        while "/../" in dir:
            import re
            dir = re.compile("^/../").sub(dir, "/")
            dir = re.compile("/[^/]+?/../").sub(dir, "/")
        return dir

    commands = {}
    def case(args):
        return " ".join(args)
    commands["echo"] = case
    def case(args):
        import os
        if not os.access(data.dir, 0):
            return f"directory not found" #Still don't know what is the need of formatted strings
        temp = os.listdir(data.dir)
        return "\n".join(temp)
    commands["dir"] = case
    def case(args):
        if args[0] == '..':
            if data.dir == '/':
                return f"you're at root you idiot" #...
            data.dir += "/../"
            data.dir = fixdir(data.dir)
            return ""
        temp = ' '.join(args) + "/"
        temp = temp.replace("~", "/home/runner/kerfus-bot")
        newdir = ("" if temp[0] == "/" else data.dir) + temp
        import os
        if not os.access(newdir,0):
            return f"directory not found" #...
        data.dir = newdir
        data.dir = fixdir(data.dir)
        return ""
    commands["cd"] = case
    def case(args):
        temp = ' '.join(args)
        temp = temp.replace("~", "/home/runner/kerfus-bot")
        temp = temp if temp[0] == "/" else (data.dir + temp)
        import os
        if not os.access(temp, 0):
            return f"file not found" #...
        try: #first try execpt I saw of 0lie
            with open(temp) as file:
                return file.read()
        except Exception as e:
            return str(e)									# Changed it for the right error name
            return "typeError: its a folder dumbass"		# in case it's another error
    commands["cat"] = case
    commands["none"] = lambda :""
    def case(args):
        temp = " ".join(args)
        temp = temp.replace("~","/home/runner/kerfus-bot")
        temp = temp if temp[0] == '/' else (data.dir + temp)
        if not sudo:
            msg.reply('access error')
            return 'access error'
        import os
        os.makedirs(temp)
        return ""
    commands["mkdir"] = case
    del case

    formatted = ""
    quotes = ""
    def findquotes(text):
        formatted = ""
        quotes = ""
        i = 0
        in_quotes = 0
        while i < len(text):
            char = text[i]
            if char == "\\":
                char = text[i+1]
                quotes += 1
                formatted += char
                i += 1
            elif char == "\"":
                in_quotes ^= True
            else:
                quotes += in_quotes
                formatted += char
            i += 1
        return formatted, quotes
    formatted, quotes = findquotes(text)

    def execute(text, quotes, newargs="", newquotes=""):
        ind = index(list(text), lambda e,i : e==">" and quotes[i]=="0")
        if ind != -1:
            out = execute(text[0:ind], quotes[0:ind], newargs, newquotes)
            file = ""
            append = False
            text_ = out
            if text[ind + 1] == '>':
                append = True
                file = '/'+data.dir+"/"+text[ind+2:].strip()
            else:
                file = '/'+data.dir+"/"+text[ind+1:].strip()
            file = fixdir(file)
            if sudo == False and not file.startswith(f"/home/runner/kerfus-bot/personal/{msg.author.id}"):
                msg.reply("access error")
                return 'access error'
            import os
            dir = os.path.dirname(file)
            if not os.access(dir, 0):
                return "not found error: directory doesnt exist"
            file = file.strip()
            if append:
                with open(file, 'a', encoding="utf8"):
                    file.write(text_)
            else:
                with open(file, 'w', encoding="utf8"):
                    file.write(text_)
            return ""
        ind = index(list(text), lambda e,i : (e=="|" or e==";") and quotes[i]=="0")
        if ind != -1:
            newargs = execute(text[0:ind], quotes[0:ind])
            nform = ""
            nq = ''
            if list(text)[ind] == "|":
                nform, nq = findquotes(newargs)
            return execute(text[ind+1:], quotes[ind+1], nform, nq)
        #actual commands here
        text = text+newargs
        quotes = quotes+newquotes
        while(text[0] == ' '):
            text = text[1:]
            quotes = quotes[1:]
        args= []
        curr =""
        i = 0
        while i < len(text):
            char = text[i]
            quo = quotes[i]
            if char == " " and quo == '0':
                args.append(curr)
                curr = ""
                while text[i] == " ":
                    i += 1
                i -= 1
            else:
                curr += char
            i += 1
        args.append(curr)
        if not args[0] in commands.keys:
            msg.channel.send("error: unexpected command " + ' '.join(args))
            return ''
        return commands[args[0]](args[1:])

    top_dir = data.dir.split("/")
    top_dir = top_dir[len(top_dir) - 2]
    top_dir = "/" if top_dir == "" else top_dir
    out = execute(formatted, quotes)
    reply = f"[root@win 10 {'~' if top_dir=='kerfus-bot' else top_dir}]# {text}\n"
    client.db.v2setuser(f"console", msg.author.id, json.dumps(data)) #You know I'm gonna asked why it's a fstring
    pages = client.misc.sliceby(out,1500)
    if len(pages) == 0:
        msg.channel.send("```"+reply+'```')
    for e in pages:
        msg.channel.send("```"+reply.replace('```','``\\`')+e.replace('```','``\\`')+'```')
