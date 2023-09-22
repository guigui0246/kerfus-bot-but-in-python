const math = require('math')

exports.run = (client,res,req,data) => {
  data['send'] = 'admin';
  data["popup"] = "wrong password";
  data["popup type"] = "text";
  if(!req.user||!req.user.perms.admin)return;
  let out = false;
  switch(req.body.comm){
    case 'createcode':
      let codes = JSON.parse(client.webdb.get('codes',{}));
      let codechars = "";
      for(let a=0x61;a<=0x7a;a++)codechars+=String.fromCharCode(a);
      codechars+=codechars.toUpperCase()+"0123456789-=!@#$%^&*()_+[]{};'\\:\"|,./<>?";
      let code = "";
      for(let a=0;a<20;a++)
        code+= codechars[math.floor(math.random()*codechars.length)];
      let codedata = {
        "uses":Number(req.body.arg1),
        "tags":JSON.parse(req.body.arg2)
      };
      
      codes[require('js-sha512').sha512(code)] = codedata;
      client.webdb.set('codes',JSON.stringify(codes));
      out = ["reply",code];
    break; case 'removesuggestion':
      let sugg = JSON.parse(client.db.get('suggestions',[]));
      sugg.splice(req.body.arg1,1);
      client.db.set('suggestions',JSON.stringify(sugg));
      out = ["reply",code];
    break; default:
      out = require('/home/runner/kerfus-bot/admin.js').run(req.body.comm,[req.body.arg1,req.body.arg2,req.body.arg3],client);
  }
  if(out){
    if(out==true)data["popup"] = "action (probably) done!";
    switch(out[0]){
      case "reply":{
        data["popup"] =  out[1];
        break;
      }
    }
  }
  else data["popup"] = "command not found :(";
}