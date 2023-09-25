import sys
import os
#SETUP
starttime = 0
features = {}
commands = []
command_handlers = {}
_dirname = os.path.abspath(os.path.curdir)
import discord
client = discord.Client(intents= 37377, partials= [1, 3])
import database
client.db = database.database(os.path.join(_dirname, "/database/"))
client.webdb = database.database(os.path.join(_dirname, "/web/database/"))
import funcs.misc
client.misc = misc = funcs.misc.setup(client)
def handle_uncaught_exception(exctype, value, traceback):
    print(f"Uncaught exception: {exctype.__name__}, {value}\n\Traceback:\n\t{traceback}")
sys.excepthook = handle_uncaught_exception
rest = client.run(os.environ.get('DISCORD_BOT_SECRET'))

def loader(x, y):
    for a in os.listdir(x):
        if os.path.isdir(a):
            for b in os.listdir(os.path.join(x, a)):
                with open(f"./{x}/{a}/{b}") as file:
                    y(a,b,file)

loader("features",lambda a,b,c : features.setdefault(a.split("_")[0], []).append(c))

def tmp(a,b,c) :
  commands.append(c.data.to_dict())
  command_handlers[b.replace(".py","")]=c
loader("commands", tmp)
del tmp

"""
// ===================================== WEB =====================================
const expr = require('express')
expr()
  .use(expr.urlencoded({extended:1}))
  .use(require('cors')({origin:'*'}))
  .use(require('cookie-parser')())
  .use(expr.json())
  .use(require('./web/firefox.js'))
  .use(require('./web/login.js')(client))
  .all(/.*/,(req,res)=>{
    let data = {
      "starttime":starttime,
      "popup":"",
      "popup type":"none",
      "send":"404"
    }
    page = req.url.split('?')[0].split('/')[1]
    if(fs.existsSync(`web/${req.method}/${page}.js`)){
      if(require(`./web/${req.method}/${page}.js`).run(client, res, req, data)) return
    }else
      if(req.method=='GET'&&fs.existsSync(`web/html/${page}.html`))
        data['send']=page
    data['popup'] = misc.replace4html(data['popup'])
    res.send(misc.addhtmls(data,fs.readFileSync(`web/html/${data['send']}.html`)))
  })
  .listen(3000, () => console.log('host working'));
// ===================================== BOT =====================================
client.on('ready', async () => {
    console.log('bot working')
    starttime = new Date().toUTCString()
    for(let a in features)
      for(let b of features[a])
        if("setup" in b)
          b.setup(client);
  client.db.v2get('other/servers.txt').split('\n').forEach(e=>
    rest.put(
      Routes.applicationGuildCommands(client.application.id,e),
      {body:commands}
    ))
  })
  .on("guildCreate", g => misc.log(`added to server id ${g.id}`))
  .on('messageCreate', msg => {
    for(let a in features)
      for(let b of features[a])
        if(b.run(msg,client)=='stop')
          return
  })
  .on('interactionCreate',inter=>{
    if(!inter.isChatInputCommand())return;
    command_handlers[inter.commandName].execute(client,inter)
  })
  .login(process.env['DISCORD_BOT_SECRET'])
// ==================================== TEST  ====================================
"""