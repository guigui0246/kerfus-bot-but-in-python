exports.run = (msg,client) => {
  msg.formatted = client.misc.polishchars(` ${msg.content} `).toLowerCase().replace(/["'\*\.]/g,"");
  if(!msg.formatted.includes(atob('a3J6eXM=')))return;
  client.misc.log(msg.content);
  let out = 'stop';
  msg.delete().catch(e=>{});
  return out;
}