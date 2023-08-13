exports.run = async (msg, client) => {
  if (msg.author.id != 966695034340663367n && msg.author.id != 438767282328436737n) return;
  const reg = /^<:.+?:\d+?> .* cat has /i;
  if(!reg.test(msg.content))return;
  msg.channel.send("cat")
}