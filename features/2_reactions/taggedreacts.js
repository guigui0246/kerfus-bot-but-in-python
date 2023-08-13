exports.run = async (msg,client) =>{
  if(client.misc.hastag("woman",msg.author.id))msg.react('☕').catch(err=>{});
  if (client.misc.hastag("delikot", msg.author.id)) msg.react('🐱').catch(err=>{});
  if (client.misc.hastag("littlehawk", msg.author.id)) msg.react('🦅').catch(err=>{});
  if (client.misc.hastag("🐢", msg.author.id)) {
    msg.react('🐢').catch(err=>{});
    msg.react('1129926033768988724').catch(err=>{});
  }
  if (msg.author.bot) msg.react('🐱').catch(err=>{});
  else if (Math.random() < 0.05) msg.react('🐱').catch(err=>{});
  if(client.misc.hastag("weirdcat",msg.author.id)) msg.react("1129116659194531930").catch(err=>{})
}