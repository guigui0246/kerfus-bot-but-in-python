const Replies = require('./funcs/pastas.js');
const pasta = new Replies("copypastas.json");
const reacts = new Replies("reactions.json");

exports.run = (comm, args, client) => {
  pasta.reload();
  reacts.reload();
  let out = true;
  switch (comm) {
    case "test":
      console.log(args[0])
    break; case "addtag":
      client.misc.addtag(args[0], args[1])
    break; case "removetag":
      client.misc.removetag(args[0], args[1])
    break; case "channel":
      client.channels.fetch(args[0]).then(channel => { channel.send(args[1]) })
    break; case "flash":
      client.channels.fetch(args[0]).then(channel => {
        channel.send(args[2])
        setTimeout(() => channel.messages.fetch({ limit: 1 }).then(msgs => msgs.first().delete()), args[1]);
      })
    break; case "addmessage":
      pasta.add(args[0], args.slice(1, args.length));
    break; case "findmessage":
      let id = pasta.findid(args[0]);
      if (id.length == 0) out = ["reply", "message not found :("];
      else {
        out = ["reply", ""]
        id.forEach(x => out[1] += `id:${x}\n\n${pasta.get(x).slice(0, 500)}\n\n`)
      }
    break; case "addreaction":
      pasta.addreact(args[0], args[1])
    break; case "seereactions":
      let reacts = pasta.getreact(args[0]);
      out = ["reply", reacts.join('&')]
    break; case "changemessage":
      pasta.setmsg(args[0], args[1]);
    break; case "appendmessage":
      pasta.setmsg(args[0], pasta.get(args[0]) + args[1]);
    break; case "deletemessage":
      pasta.delet(args[0]);
      console.log(args[0]);
    break; case "delete":
      client.channels.fetch(args[0]).then(channel=>
        channel.messages.fetch(args[1]).then(msg=>msg.delete)
      )
    break; default:
      return false;
  }
  return out;
}