const fs = require('fs');
const math = require('math');
const flowertime = [1, 3, 10];
const flowerprices = [10, 50, 500];
const flowerrewards = [15, 70, 600];
const flowers = ["dandelion","rose","weed"];
const stagesbefore=["",     "small ","growing ","!grown ","decayed "];
const stagesafter =[" seed","",        "",      "!",      ""        ];
const stagetime =  [5,      10,        30,      120,      Infinity ];
const needswater = [1,      1,         0,       0,        0        ];
const buildings = ["water wheel","grave"];
const buildings_prices = [100,500];
let client;
for(let x in stagetime.slice(1))
  stagetime[x+1]+=stagetime[x];
let maxlentemp;
{
  let temp1 = 0,temp2 = 0;
  for(let x in stagesbefore)
    temp1 = Math.max(temp1,(stagesbefore[x]+stagesafter[x]).length);
  for(let x of flowers)
    temp2 = Math.max(temp1,x.length);
  maxlentemp = temp1 + temp2;
  for(let x of buildings)
    maxlentemp = Math.max(maxlentemp,x.length);
}
const maxlen = maxlentemp + 1;
const starting = {"plot":
  [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]
  ], "money":10
};
let strid;

function neighbours(x,y){
  x = parseInt(x);
  y = parseInt(y);
  let out = [];
  if(x>0)out.push([x-1,y])
  if(x<4)out.push([x+1,y])
  if(y>0)out.push([x,y-1])
  if(y<4)out.push([x,y+1])
  return out
}

function water(plot,x,y,msg,client){
  let temp = plot["plot"][x][y];
  if(typeof temp==='number') return 0;
  
  let out = "flower not ready";
  if(readytime(plot["plot"],x,y)<new Date().getTime()/60000){
    temp[1]= Math.floor(new Date().getTime()/60000);
    temp[2]++;
    plot["plot"][x][y] = temp;
    out = "flower watered";
    if(needswater[temp[2]]){
      client.misc.remind(readyin(plot["plot"],x,y)*60n, msg.author, "you have a flower to water");
    }else if(temp[2]==2){
      client.misc.remind(readyin(plot["plot"],x,y)*60n, msg.author, "you have a flower to harvest");
    }
  }
  return out;
}

function isNumeric(n){return !isNaN(parseFloat(n)) && isFinite(n);}


function updateLB(id,mon,client){
  console.log(id,mon)
  let i;
  let baltop = JSON.parse(client.db.v2get('other/flowerLB.json'));
  
  if(baltop[1].includes(id)){
    i = baltop[1].indexOf(id);
    if(baltop[0][i]>mon) return;
    baltop[0][i] = mon;
  }else{
    baltop[0].push(mon)
    baltop[1].push(id)
    i = 10;
  }
  while(i>0&&baltop[0][i-1]<baltop[0][i]){
    temp = baltop[0][i-1];
    baltop[0][i-1] = baltop[0][i];
    baltop[0][i] = temp;
    temp = baltop[1][i-1];
    baltop[1][i-1] = baltop[1][i];
    baltop[1][i] = temp;
    i--;
  }
  baltop[0].splice(10,1);
  baltop[1].splice(10,1);
  client.db.v2set('other/flowerLB.json',JSON.stringify(baltop));
}

function printplot(plot){
  out = "";
  for(let x in plot){
    for(let y of plot[x]){ 
      if(y===0){
        out+="`"+" ".repeat(maxlen) + "` ";
      }else if(typeof y == 'number'){
        out+="`"+buildings[y-1]+" ".repeat(maxlen-buildings[y-1].length) + "` ";
      }else{
        let temp = stagesbefore[y[2]]+flowers[y[0]]+stagesafter[y[2]]
        out+="`"+temp+" ".repeat(maxlen-temp.length)+"` ";
      }
    }
    out+="\n";
    for(let y in plot[x]){
      if(y===0){
        out+="`"+ " ".repeat(maxlen)+"` ";
      }else if(typeof plot[x][y] == 'number'){
        out+="`"+ " ".repeat(maxlen) + "` ";
      }else{
        let time = readytime(plot,x,y);
        let remtime = readytime(plot,x,y) - new Date().getTime()/60000;
        let percent = maxlen-Math.floor(maxlen*remtime/readyin(plot,x,y));
        if(remtime!=Infinity&&remtime>0)
          out+="`"+"#".repeat(Math.min(percent,maxlen))+" ".repeat(Math.max(maxlen-percent,0))+"` ";
        else
          out+="`"+"#".repeat(maxlen)+"` ";
      }
    }
    out+="\n\n";
  }
  return out;
}

function readyin(plot,x,y){
  let flower = plot[x][y];
  if(typeof flower == 'number') return Infinity;
  if(flower[2]==4) return Infinity;
  let time = stagetime[flower[2]]*flowertime[flower[0]]
  {
    let temp = 1
    for(let i of neighbours(x,y)){
      if(plot[i[0]][i[1]] === 1)
        temp -= 0.1;
    }
    time *= temp;
  }
  return time;
}

function readytime(plot,x,y){
  let flower = plot[x][y];
  if(typeof flower == 'number') return Infinity;
  return flower[1]+readyin(plot,x,y);
}

function update(plot){
    for(let x in plot["plot"]){
    for(let y in plot["plot"][x]){
      let temp = plot["plot"][x][y];
      if(typeof temp=='number') continue;
      while(readytime(plot["plot"],x,y)<new Date().getTime()/60000&&!needswater[temp[2]]){
        temp[1]+=stagetime[temp[2]];
        temp[2]++;
      }
      plot["plot"][x][y] = temp;
    }
  }
}

function harvest(plot,x,y,cl,strid){
  client = cl;
  let flower = plot["plot"][x][y];
  if(typeof flower === 'number')
    return -2;
  if(flower[2]<3)
    return -1;
  plot["plot"][x][y] = 0;
  if(flower[2]==4){
    let get = 0;
    for(let a of neighbours(x,y)){
      if(plot["plot"][a[0]][a[1]]==2){
        get += 0.01*(new Date().getTime()/60000-flower[1]);
      }
    }
    plot["money"] += flowerrewards[flower[0]]*get;
    
    updateLB(strid,plot["money"],client);
    return flowerrewards[flower[0]]*get;
  }
  plot["money"] += flowerrewards[flower[0]];
  
  return flowerrewards[flower[0]];
}

exports.run = (msg, client) => {
  if(!msg.content.toLowerCase().startsWith('f!')) return;
  strid = `${msg.author.id}`;
  let plot = JSON.parse(client.db.v2getuser('flowers',strid,JSON.stringify(starting)));
  let args = msg.content.split(' ').slice(1)

  
  //update plot 
  update(plot);
  
  switch(msg.content.split(' ')[0].slice(2)){
    case 'top':{
      let out = "> LEADERBOARDS:\n";
      let baltop = JSON.parse(client.db.v2get('flowerLB.json'));
      for(let x in baltop)
        if(baltop[1][x]==0)break
        else out += `> ${1*x+1}. <@${baltop[1][x]}>: ${baltop[0][x]}\n`
      msg.reply(out)
    break;}case 'help':{
      msg.reply(`> **commands:**\n[] - optional\nf!shop - show flower prices\nf!plot [user] - show user's plot, [user] defaults to you\nf!plant (x) (y) (flower) - plants flower at coordinates, coords = {0...4}\nf!harvest (x) (y) - harvest flower at coords\nf!water (x) (y) - water the flower at xy, water is only needed when a seed, growing or small is ready to grow\nf!build (x) (y) (building) builds a building at xy\nf!info - some math data, not important\n\n> **DANGEROUS**\nf!remove (x) (y) removes building/flower at xy\nf!reset - resets everything about you`)
    break;}case 'info':{
      msg.reply(`> **info:**\n\n> growth stages are:\nseed\nsmall\ngrowing\ngrown (\\*harvest\\*)\ndecayed\n\n> growths times are:\nseed -> small: 5 minutes\nsmall -> growing: 10 minutes\ngrowing -> grown: 30 minutes\ngrown -> decayed: 2 hours\n\nadditionally, each time is multiplied depending on the flower:\ndandelion - 1x\nrose - 3x\nweed - 10x`)
    break;}case 'shop':{
      out = "> **shop:**\nyou have " + math.floor(plot.money) + " money";
      out += '\n\n> **flowers**:'
      for(let x in flowers){
        out+='\n\n> **' +flowers[x];
        out+='**\nprice: ' +flowerprices[x];
        out+='\nreward: ' + flowerrewards[x];
      }
      const buildings_desc = [
        "decreases growth time by 10% for 4 nearby flowers","decayed flowers give 1% of their value, per minute of being decayed"
      ];
      
      out += '\n\n> **buildings**:'
      for(let x in buildings){
        out+='\n\n> **' +buildings[x];
        out+='**\nprice: ' + buildings_prices[x];
        out+='\ninfo: ' + buildings_desc[x];
      }
      
      msg.reply(out)
    break;}case 'plot':{
      let id;
      if(args[0]==undefined)
        id = strid;
      else
       id = args[0].slice(2,-1);
      let temp = JSON.parse(client.db.v2getuser('flowers',id,JSON.stringify(starting)));
      if(args[0]!=undefined)update(temp);
      msg.channel.send(printplot(temp["plot"]))
      client.db.v2setuser('flowers',id,JSON.stringify(temp));
    break;}case 'plant':{
      if(args.length<3){msg.reply('too little arguments');break}
      let x,y,flo;
      if(isNumeric(args[0])) [x, y, flo] = args;
      else [flo, x, y] = args;
      
      if(!isNumeric(x)||!isNumeric(y)){msg.reply("x and y have to be numbers");break}
      x = parseInt(x);
      y = parseInt(y);
      if(x<0||x>4||y<0||y>4){msg.reply("wrong place");break}
      if(plot["plot"][x][y]!==0){msg.reply("space taken");break}
      
      let index = flowers.indexOf(flo.toLowerCase());
      
      if(index==-1){msg.reply("flower not found");break}
      if(plot["money"]<flowerprices[index]){msg.reply('not enough money');break}
      
      plot["money"]-=flowerprices[index]
      plot["plot"][x][y] = [index, Math.floor(new Date().getTime() /60000),0];
      client.misc.remind(flowertime[index]*300n, msg.author, "you have a flower to water");
      msg.channel.send(printplot(plot["plot"]))
    break;}case 'harvest':{
      if(args[0]=='all'){
        let out = 0;
        for(let x=0;x<5;x++){
          for(let y=0;y<5;y++){
            let t = harvest(plot,x,y,client);
            if(t>0)
              out+=t;
          }
        }
        if(out!==0)
          msg.channel.send(`flowers harvested, got ${math.floor(out)} money.\n\n` + printplot(plot["plot"]))
        else
          msg.channel.send(`no flowers to harvest!\n\n` + printplot(plot["plot"]))
        break;
      }
      if(args.length<2){msg.reply('too little arguments');break}
      let x = args[0],y = args[1];
      if(x<0||x>4||y<0||y>4){msg.reply("wrong place");break}
      let temp = harvest(plot,x,y,client);
      if(temp==-2){msg.reply("empty plot");break}
      if(temp==-1){msg.reply('flower not grown up');break}
      if(temp==0){msg.channel.send(`decayed flower removed\n\n` + printplot(plot["plot"]));break}
      msg.channel.send(`flower harvested, got ${temp} money.\n\n` + printplot(plot["plot"]))
    break;}case 'reset':{
      plot = starting;
    break;}case 'water':{
      if(args[0]=='all'){
        let out = 0;
        for(let x=0;x<5;x++){
          for(let y=0;y<5;y++){
            let t = water(plot,x,y,msg,client);
            if(t=="flower watered")
              out++;
          }
        }
        if(out!==0) msg.channel.send(`all flowers watered!\n\n` + printplot(plot["plot"]))
        else msg.channel.send(`no flowers to water!\n\n` + printplot(plot["plot"]))
        break;
      }
      if(args.length<2){msg.reply('too little arguments');break}
      let x = args[0],y= args[1];
      if(x<0||x>4||y<0||y>4){msg.reply('wrong coordinates');break}
      let out = water(plot,x,y,msg,client);
      if(typeof out == 'string') msg.channel.send(out+`\n\n` + printplot(plot["plot"]))
    break;}case 'build':{
      if(args.length<3){msg.reply('too little arguments');break}
      if(!isNumeric(args[0])||!isNumeric(args[1])){msg.reply("x and y have to be numbers");break}
      if(args[0]<0||args[0]>4||args[1]<0||args[1]>4){msg.reply("wrong place");break}
      if(plot["plot"][args[0]][args[1]]!==0){msg.reply("space taken");break}
      
      let index = buildings.indexOf((args.slice(2).join(' ')).toLowerCase());
      
      if(index==-1){msg.reply("building not found");break}
      
      if(plot["money"]<buildings_prices[index]){msg.reply('not enough money');break}
      
      plot["money"]-=buildings_prices[index]
      plot["plot"][args[0]][args[1]] = index+1;
      msg.channel.send(printplot(plot["plot"]))
    break;}case 'remove':{
      if(args.length<2){msg.reply('too little arguments');break}
      if(!isNumeric(args[0])||!isNumeric(args[1])){msg.reply("x and y have to be numbers");break}
      if(args[0]<0||args[0]>4||args[1]<0||args[1]>4){msg.reply("wrong place");break}
      plot["plot"][args[0]][args[1]] = 0;
    break;}
  }
  client.db.v2setuser('flowers',strid,JSON.stringify(plot))
}
