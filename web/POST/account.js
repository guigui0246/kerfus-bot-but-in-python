 exports.run = (client,res,req,data) => {
  if(!req.user){
    res.send(false);
    return 'stop';
  }
  let usr = JSON.parse(client.webdb.v2getuser("users",req.cookies.username));
  let newpass = require('js-sha512').sha512(req.body.newpass);
  usr.password = newpass;
  client.webdb.v2setuser("users",req.cookies.username,usr);
  res.send(true);
  return 'stop';
}