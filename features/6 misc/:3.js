exports.run = (msg,client) => {
  if(msg.content==':sudo rm -rf /*'){
    msg.reply(`6396 files deleted (1.405 seconds)`)
    return;
  }
  let cont = msg.content.replace(/\s/g,'');
  if(!(/^:-?(\(-?)*(((\(-?)*[0-9]+(\.[0-9]+)?|NaN|Infinity)\)*(\+|\-|\*|\/|\*\*[-]?))*(\(-?)*([0-9]+(\.[0-9]+)?|NaN|Infinity)\)*$/.test(cont))) return;
  let depth = 0;
  for(let a in cont){
    if(a=='(')depth+=1;
    if(a==')')depth-=1;
    if(depth<0)return;
  }
  if(depth!=0)return;
  msg.reply(`:${1+eval(cont.slice(1))}`);
}