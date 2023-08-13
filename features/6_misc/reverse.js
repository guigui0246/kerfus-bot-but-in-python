exports.run = (msg, client) => {
  if (msg.formatted.includes('reverse'))
    msg.reply(msg.content.split('').reverse().join(''));
}