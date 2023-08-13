const math = require('math')

let team_ids = [
  '438767282328436737',
  '558979299177136164',
  '704556927018991686',
  '436178855104086037',
  '373266820792188928',
  '877345121790730252',
  '576065759185338371',
  '553093932012011520',
  '534806202698432514',
  '614862278713409543',
  '646401965596868628',
  '772501410092023852',
  '872058344003739678',
  '817212706355413052',
  '485716797706993705',
  '690699296508739594',
  '1043197880023928944',
  '822431137544405022',
  '878298928582361120'
]

exports.run = (msg, client) => {
  if (!msg.content.startsWith("!syncinvs")) return;
  if (!team_ids.includes(msg.author.id)) {
    msg.reply("no permission");
    return;
  }
  let ids = team_ids;
  let sync_time = msg.content.split(" ")[1] ?? 24;
  sync_time = +sync_time;
  let synced = true;
  ids.forEach(e => {
    let time = client.db.v2getuser("leafSyncTime", e);
    if (time && new Date() * 1 - time * 1 < sync_time * 3600 * 1000) return;
    synced = false;
    client.users.fetch(e).then(user => {
      msg.channel.send(`${user.username}'s inventory not synced`)
    })
  })
  if (synced) {
    msg.channel.send(`all synced`)
  }
}