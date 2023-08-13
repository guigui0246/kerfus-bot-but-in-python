exports.run = (msg,client) => {
  if(!client.misc.hastag("phobic",msg.author.id))return;
  client.misc.log(msg.content);
  let out = 'stop';
  msg.delete().catch(e=>{});
  return out;
}