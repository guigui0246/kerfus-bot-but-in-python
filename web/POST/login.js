exports.run = (client,res,req,data) => {
  let inp = req.body; 
  if(!inp.password||!inp.username){
    res.send(false)
    return 'stop';
  }
  let newpass = require('js-sha512').sha512(inp.password)
  let usr = client.webdb.v2getuser("users",inp.username);
  if(usr==0){
    res.send(false);
    return 'stop';
  } 
  usr = JSON.parse(usr);
  if(newpass != usr.password){
    res.send(false);
    return 'stop';
  }
  res.cookie('username', inp.username);
  res.cookie('password', inp.password);
  res.send(true);
  return 'stop';
}