exports.run = (msg,client) => {
  if(client.misc.hastag("admin", msg.author.id) && msg.content.includes('&')) {
    let action=require('/home/runner/kerfus-bot/admin.js').run(msg.content.split('&')[0],msg.content.split('&').slice(1), client)
    if(action[0] == "reply")msg.reply(action[1])
    if(action) return "stop";
  }
}