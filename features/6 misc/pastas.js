const Replies = require('/home/runner/kerfus-bot/funcs/pastas.js');


exports.run = (msg,client) => {
  if(msg.guild==1121125014096318615n)return;
  if(msg.content.startsWith("!"))return;
  const pasta = new Replies("copypastas.json", client);
  pasta.reload();
  for (i = 0; i < pasta.len(); i++) {
    if (!pasta.includes(msg.formatted, i)) continue;
    if (!pasta.allowed(i, msg.guild.id, msg.channel.id)) continue;
    reply = client.misc.sliceby(pasta.get(i), 2000);
    for (const j of reply)
      msg.reply(j)
  }
}