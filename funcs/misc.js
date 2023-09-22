const fs = require('fs');
let client;
exports.setup = (a) => {
  client = a;
  let n = 1*client.db.v2get('other/remindercount');
  let reminders = [];
  for(let x=400;x<n;x++){
    let temp=client.db.v2get(`reminder/${x}`);
    if(temp)reminders.push(JSON.parse(temp).concat(x))
  }
  reminders.forEach(e=>{
    setTimeout(()=>{
      client.users.fetch(e[0]).then(user=>user.send(e[2]).catch(err=>{}));
      client.db.v2del(`reminder/${e[3]}`)
    },Number(BigInt(e[1])-BigInt(1*new Date())))
  })
  return exports;
}

exports.test = () => {}

exports.addhtmls = (data,document) => {
  let gen = ""+fs.readFileSync("web/generic.html");
  let doc = (""+document).split('##');
  let out = gen.replace("#DATA#",JSON.stringify(data));
  for( let x = 0;x<doc.length;x+=2)
    out = out.replace(`#${doc[x]}#`,doc[x+1])
  return out;
}

exports.hastag = (tag,id) => {
  let tagged= JSON.parse(fs.readFileSync("data/tags.json", 'utf-8'));
  if(!(tag in tagged))return false;
  return tagged[tag].includes(id);
}

exports.addtag = (tag,id) => {
  let tagged = JSON.parse(fs.readFileSync("data/tags.json", 'utf-8'));
  if(tag in tagged){
    if(!(tagged[tag].includes(id)))tagged[tag].push(id);
  }
  else
    tagged[tag] = [id];
  fs.writeFileSync("data/tags.json", JSON.stringify(tagged));
}

exports.removetag = (tag,id) => {
  let tagged = JSON.parse(fs.readFileSync("data/tags.json", 'utf-8'));
  if(tag in tagged)
    if(tagged[tag].includes(id)){
      tagged[tag].splice(tagged[tag].indexOf(id),1);
      fs.writeFileSync("data/tags.json", JSON.stringify(tagged));
    }
}

exports.log = (text , file = 'logs.txt') => {
  fs.appendFileSync(file, text.replace(/\n/g,' ')+"\n");
}

exports.polishchars = (text) => {
  let copy = text;
  let polish = "ęóąśłżźćń";
  let fixed = "eoaslzzcn";
  for(let i in fixed)
    copy = copy.replaceAll(polish[i], fixed[i])
  return copy;
}

exports.sliceby = (text,spacing) => {
  out = [];
  for(var i = 0;i<text.length;i+=spacing){
    out.push(text.slice(i,i+spacing));
  }
  return out;
}

function replace4html(inp){
  let text = inp;
  if(typeof text=='string'||typeof text=='number'){
    text = text.replaceAll('<','&lt;')
    text = text.replaceAll('>','&gt;')
    text = text.replaceAll(/\r?\n\r?/g,'<br>') 
  }
  else
    text.forEach((e,i)=>text[i]=replace4html(e));
  return text;
}

exports.replace4html = replace4html;

exports.remind = (time, user, message)=>{
  let numb = 1*client.db.v2get('other/remindercount',0);
  client.db.v2set('other/remindercount',`${numb+1}`);
  let timeend = time*1000n+BigInt(+new Date());
  client.db.v2set(`reminder/${numb}`,JSON.stringify([user.id,`${timeend}`,message]))
  setTimeout(()=>{
    user.send(message).catch(err=>{});
    client.db.v2del(`reminder/${numb}`)
  },Number(time*1000n));
}