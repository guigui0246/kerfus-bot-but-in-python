// sha512(test) == ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff
exports.run = (client,res,req,data) => {
  
  let inp = req.body;
  if(!inp.password||!inp.name||!inp.code){
    res.send("no inputs");
    return 'stop';
  }
  
  if(!/[a-zA-Z0-9\-\_\.]+/.test(inp.name)){
    res.send("invalid characters in name");
    return 'stop';
  }
  
  let temp = client.webdb.v2getuser('account',inp.name);
  if(temp!=null){
    res.send("account exists");
    return 'stop';
  }
  
  let codes = JSON.parse(client.webdb.v2get('other/codes',"{}"));
  let code = require('js-sha512').sha512(inp.code);
  if(!codes[code]){
    res.send("wrong code");
    return 'stop';
  }
  
  let user = {
    username:inp.name,
    password:require('js-sha512').sha512(inp.password),
    tags:codes[code].tags
  };
  
  client.webdb.v2setuser('account',inp.name,JSON.stringify(user));
  if(codes[code].uses==1){
    delete codes[code];
  }else{
    codes[code].uses-=1;
  }
  client.webdb.v2set('other/codes',JSON.stringify(codes));
  return 'stop';
};