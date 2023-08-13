exports.run = async (msg, client) => {
  return;
  if (msg.author.id != 1119928094418018354n) return;
  const reg = /^You're on/i;
  if(reg.test(msg.content))return;
  
  client.misc.remind(10*60, msg.interaction.user, `reminder for your symbol get`);
}