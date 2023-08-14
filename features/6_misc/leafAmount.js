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
  '1043197880023928944',
  '822431137544405022',
  '878298928582361120'
]

exports.run = (msg, client) => {
  if(!msg.content.startsWith("!countleaves"))return;
  if(!team_ids.includes(msg.author.id)){
    msg.reply("no permission");
    return;
  }
  let ids;
  if(msg.content.split(" ").length>1)ids=msg.content.split(" ").slice(1);
  else ids = team_ids;
  let index = {};
  let amounts = [];
  "Mint Bay Aloe Jade Monstera Yucca Sedum Heuchera Maple Flapjack Agave Echeveria Licorice Tomentosa".split(" ").forEach((e,i)=>{
    index[e]=i;
    amounts.push(0);
  });
  ids.forEach(e=>{
    let temp = client.db.v2getuser("leafamount",e);
    temp = JSON.parse(temp);
    for(let i in temp){
      amounts[index[i]] += 1*temp[i];
    }
  })
  let power = 0;
  amounts.forEach((e,i)=>{
    power += e*("1 2 5 10 20 50 100 200 400 800 1600 3000 5500 10000".split(" ")[i])
  })
  let out = `total power: ${power}\nteam's total:\n`;
  for(let i in index)
    out += `${i}: ${amounts[index[i]]}\n`;
  for(let i=0;i+1<amounts.length;i++){
    amounts[i+1]+=math.floor(amounts[i]/2)
    amounts[i]%=2;
  }
  msg.channel.send(out);
  power = 0;
  amounts.forEach((e,i)=>{
    power+=e*2**i;
  })
  let mintgoal = 1;
  while(mintgoal<power)mintgoal*=2;
  out = `optimal power: ${power*1.5625}\nmint amount: ${power}/${mintgoal}\nafter compression:\n`;
  for(let i in index)
    out += `${i}: ${amounts[index[i]]}\n`;
  msg.channel.send(out);
  
}