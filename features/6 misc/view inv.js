const math = require('math')

let team_ids = [
  '438767282328436737',
  '558979299177136164',
  '704556927018991686',
  '436178855104086037',
  '373266820792188928',
  '877345121790730252',
  '576065759185338371',
  '553093932012011520',
  '534806202698432514',
  '614862278713409543',
  '646401965596868628',
  '772501410092023852',
  '872058344003739678',
  '817212706355413052',
  '485716797706993705',
  '690699296508739594',
  '1043197880023928944',
  '822431137544405022',
  '878298928582361120'
]

exports.run = (msg, client) => {
  if(!msg.content.startsWith("!viewinv"))return;
  if(!team_ids.includes(msg.author.id)){
    msg.reply("no permission");
    return;
  }
  let ids;
  if(msg.content.split(" ").length>1)ids=msg.content.split(" ").slice(1);
  else ids = team_ids;
  ids.forEach(e=>{
    let time = client.db.v2getuser("leafSyncTime",e);
    let textinv = client.db.v2getuser("leafamount",e)
    let inv = JSON.parse(textinv);
    let amount = 0;
    for(let a in inv)amount+=inv[a];
    if(amount==0) return;
    client.users.fetch(e).then(user=>{
      if(!time||new Date()*1-time*1>24*3600*1000){
         msg.channel.send(`> WARNING: user's inventory not synced: ${user.username}`)
      }
        msg.channel.send(`${user.username}:\n`+textinv)
    })
  })
}  