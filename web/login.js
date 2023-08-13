let perms = [["admin"],["religia"]];
let client;
function use(req,res,next){
  if(!req.cookies.password||!req.cookies.username){next();return;}
  let newpass = require('js-sha512').sha512(req.cookies.password);
  let usr = client.webdb.getuser("users",req.cookies.username)
  if(!usr){next();return;}
  usr=JSON.parse(usr);
  if(newpass != usr.password){next();return;}
  req.user = usr;
  let level = -1;
  for(let i in perms){
    let a = false;
    for(let j of perms[i])if(usr.tags[j])a=true;
    if(a){
      level = i;
      break;
    }
  }
  if(level!=-1)
    for(let i of perms.slice(level+1))
      for(let j of i)
        usr.tags[j] = true;
  next();
}
module.exports = (c)=>{
  client = c;
  return use;
}