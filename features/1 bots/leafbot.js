let claims = {
  "swift_claim": [
    [8, ["mint_leaf", 4]],
    [8, ["mint_leaf", 3]],

    [7, ["bay_leaf", 3]],
    [7, ["bay_leaf", 2]],

    [6, ["aloe_leaf", 2]],
    [6, ["aloe_leaf", 1]],

    [2, ["jade_leaf", 2]],
    [8, ["jade_leaf", 1]],

    [5, ["monstera_leaf", 1]],

    [2, ["yucca_leaf", 1]],

    [1, ["sedum_leaf", 1]]
  ],
  "daily_claim": [
    [8, ["mint_leaf", 16]],
    [8, ["mint_leaf", 14]],
    [8, ["mint_leaf", 12]],

    [14, ["bay_leaf", 8]],
    [14, ["bay_leaf", 7]],

    [16, ["aloe_leaf", 5]],
    [16, ["aloe_leaf", 4]],

    [16, ["jade_leaf", 4]],
    [16, ["jade_leaf", 3]],
    [16, ["jade_leaf", 2]],

    [12, ["monstera_leaf", 3]],
    [12, ["monstera_leaf", 2]],
    [12, ["monstera_leaf", 1]],

    [10, ["yucca_leaf", 2]],
    [10, ["yucca_leaf", 1]],

    [2, ["sedum_leaf", 2]],
    [6, ["sedum_leaf", 1]],

    [3, ["heuchera_leaf", 1]],

    [1, ["maple_leaf", 1]]
  ],
  
  "turbo_claim":[
    [6, ["mint_leaf", 60]], // 75  6
    [12,["mint_leaf", 50]], // 62.5 7
    [6, ["mint_leaf", 40]], // 50  8
    
    [6, ["bay_leaf", 30]], // 75   6
    [3, ["bay_leaf", 25]], // 62.5 7
    
    [12,["aloe_leaf", 20]], // 100 5
    [6, ["aloe_leaf", 15]], // 75  6
    
    [8, ["yucca_leaf", 5]], // 250 4
    
    [4, ["sedum_leaf", 3]], // 300 3
    
    [4, ["maple_leaf", 1]], // 400 2
    [1, ["agave_leaf", 1]]  // 1600 1
  ]
};

let sum = {};
for (let x in claims) {
  sum[x] = 0;
  for (let y of claims[x]) sum[x] += y[0];
}

let ids = {
  "therealolie": '438767282328436737',
  "Olie | #TheRakers": '438767282328436737',
  "fake": '558979299177136164',
  "🐢": '704556927018991686',
  "guigui0246 | #TheRakers": '436178855104086037',
  "HeuchEnder08": '373266820792188928',
  "rotatable_cube": '877345121790730252',
  "calionreal": '576065759185338371',
  "milenakos": '553093932012011520',
  "k_lemon": '534806202698432514',
  "fernhalo": '614862278713409543',
  "blaumeise20": '646401965596868628',
  "morningstar37": '772501410092023852',
  "slashred": '872058344003739678',
  "baking leaves": '817212706355413052',
  "birdtree": '485716797706993705',
  "creepz1691": '690699296508739594',
  "itamar_nudge": '1043197880023928944',
  "the_rake_": '822431137544405022',
  "xfexel": '878298928582361120',
  "guigui0246": "436178855104086037",
  "Methman":"817212706355413052"
}
let times = {
  "swift": 120,
  "daily": 1440,
}
let leaves = "Mint Bay Aloe Jade Monstera Yucca Sedum Heuchera Maple Flapjack Agave Echeveria Licorice Tomentosa".split(" ");
let def = {};
leaves.forEach(e=>def[e]=0)

function otherpeople(msg, client){
  if(msg.content!="!togglebroadcastreminder")return;
  if(client.misc.hastag("broadcastremind",msg.author.id)) client.misc.removetag("broadcastremind",msg.author.id)
  else  client.misc.addtag("broadcastremind",msg.author.id)
  msg.reply('toggled')
}

exports.run = async (msg, client) => {
  if (msg.author.id != 1073619066272620666n){
    otherpeople(msg, client);
    return;
  }
  if(!msg.interaction)return;
  
  if (msg.interaction.commandName=="garden claim") {
    const reg = /^You found x([0-9]+?) \*\*(\w+?) Leaf\*\* in your (\w+?) package\!/gi;
    let temp = reg.exec(msg.content)
    if (temp === null) return;
    let claim = claims[`${temp[3]}_claim`];
    let weight = -1;
    for (let x of claim)
      if (x[1][0] == `${temp[2].toLowerCase()}_leaf` && x[1][1] == temp[1]) weight = x[0];
    msg.channel.send(`chance: ${weight / sum[`${temp[3]}_claim`] * 100}% (${weight}/${sum[`${temp[3]}_claim`]})`).catch()
    
    let user = JSON.parse(client.db.v2getuser("leafamount",msg.interaction.user.id,JSON.stringify(def)));
    user[temp[2]] = 1*temp[1] + 1*(user[temp[2]]);
    client.db.v2setuser("leafamount",msg.interaction.user.id,JSON.stringify(user));
    
    client.misc.log(`${msg.interaction.user.id} ${temp[3]} ${temp[1]} ${temp[2].toLowerCase()}`, 'leaflogs.txt');
    let time = times[temp[3]]
    if(!time) return;
    let settings = JSON.parse(client.db.v2getuser('settings', msg.interaction.user.id, '{ "autoremind": { "time": 300 } }'));
    if (settings.autoremind.time == -1) return;
    client.misc.remind(time*60 - settings.autoremind.time, msg.interaction.user, `reminder for your ${temp[3]} package`);
    return;
  }
  else if (msg.interaction.commandName=="garden gift") {
    const reg = /^You gave x([0-9]+?) \*\*(\w+?) Leaf\*\* to (.+?)\!/gi;
    let temp = reg.exec(msg.content);
    if (temp === null) return;
    let to_user = client.users.cache.find(u => u.username == temp[3]);
    let id = temp[3];
    if (temp[3] in ids) id = ids[temp[3]];
    else if (to_user != undefined) id = to_user.id;
    msg.channel.send(`logged transaction: ${msg.interaction.user.username} -> ${temp[3]}: ${temp[1]}x ${temp[2]}`).catch()
    
    let user = JSON.parse(client.db.v2getuser("leafamount",msg.interaction.user.id,JSON.stringify(def)));
    user[temp[2]] = 1*user[temp[2]] -1* temp[1];
    client.db.v2setuser("leafamount",msg.interaction.user.id,JSON.stringify(user));
    user = JSON.parse(client.db.v2getuser("leafamount",id,JSON.stringify(def)));
    user[temp[2]] = 1*(user[temp[2]]) + 1*temp[1];
    client.db.v2setuser("leafamount",id,JSON.stringify(user));
    
    client.misc.log(`${msg.interaction.user.id} ${id} ${temp[1]} ${temp[2].toLowerCase()}`, 'leaflogs2.txt')
  }
  else if (msg.interaction.commandName=="broadcast") {
    if (!msg.content.startsWith("Successfully broadcasted")) return;
    if (!client.misc.hastag("broadcastremind",msg.interaction.user.id)) return;
    client.misc.remind(60 * 5, msg.interaction.user, `reminder for broadcast`);
  }
  else if(msg.interaction.commandName=="garden inv"){
    let embed = msg.embeds[0];
    const reg = /^(.+?)'s collection:$/i;
    //console.log(embed)
    let temp = reg.exec(embed.title);
    if(temp===null)return;
    let user = client.users.cache.find(u => u.username == temp[3]);
    let id = temp[1];
    if (temp[1] in ids) id = ids[temp[1]];
    else if (user != undefined) id = user.id;
    if(id==temp[1])console.log(`not found: ${id}`)
    let amounts = {};
    leaves.forEach(e=>amounts[e]=0);
    embed.fields.forEach(e=>{
      const reg = /^.*? (.+)$/i;
      let temp = reg.exec(e.name);
      if(temp===null)return;
      amounts[temp[1]] = 1*e.value;
    })
    let out = `id:${id}\n\n`;
    for(let i in amounts)
      out += amounts[i]!=0?`${i}: ${amounts[i]}\n`:"";
    msg.channel.send(out);
    client.db.v2setuser("leafSyncTime",id,`${new Date()*1}`);
    client.db.v2setuser("leafamount",id,JSON.stringify(amounts))
  }
  else if(msg.interaction.commandName=="garden compost"){
    const reg = /^You created... x([0-9]+?) (\w+?) Leaf!/gi;
    let temp = reg.exec(msg.content)
    if (temp === null) return;
    let user = JSON.parse(client.db.v2getuser("leafamount",msg.interaction.user.id,JSON.stringify(def)));
    user[temp[2]] = 1*user[temp[2]] + 1*temp[1];
    let prev_leaf = leaves[leaves.indexOf(temp[2])-1];
    user[prev_leaf] = 1*user[prev_leaf] - 2*temp[1];
    client.db.v2setuser("leafamount",msg.interaction.user.id,JSON.stringify(user));
  }
}