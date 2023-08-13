const Replies = require('/home/runner/kerfus-bot/funcs/pastas.js');

exports.run = async (msg,client) => {
  if(!msg.guild)return;
  const reacts = new Replies("reactions.json", client);
  for (var i =0;i< reacts.len(); i++){
    if (!reacts.includes(msg.formatted, i)) continue;
    if (!reacts.allowed(i, msg.guild.id, msg.channel.id)) continue;
    let reactions = reacts.get(i)
    for (const j of reactions)
      msg.react(j).catch(err=>{});
  }
}