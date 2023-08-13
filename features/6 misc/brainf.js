const brainf = require('/home/runner/kerfus-bot/funcs/brainf.js');
exports.run = (msg,client) => {
  
  if(!msg.content.startsWith('!brainf')) return;
  
  let instance = brainf.createinstance([msg.content[8]==1,msg.content[9]==1,msg.content[10]==1]);
  console.log(msg.content.split('&'))
  let runtime = msg.content.split('&')[1];
  let input = [msg.content.split('&')[2]];
  let code = msg.content.split('&')[3];
  client.misc.log(code);
  let cont = true;
  for(let x=0;(x<runtime||runtime==-1)&&cont;x++){
    cont = brainf.runframe(instance,code,input);
  }
  if(instance.output!="")
    msg.reply(instance.output);
  else
    msg.reply("no output");
}