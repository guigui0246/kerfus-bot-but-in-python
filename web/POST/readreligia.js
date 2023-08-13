var CryptoJS = require("crypto-js");

exports.run = (client,res,req,data) => {
  data['send'] = 'religia';
  data["popup type"] = "text";
  if(!req.user){data['popup'] = 'no access';return;}
  if(!req.user.tags.religia){data['popup'] = 'no access';return;}

  let a = client.webdb.get('religia');
  a = CryptoJS.AES.decrypt(a, process.env['ENCRYPTION']).toString(CryptoJS.enc.Utf8);
  a = JSON.parse(a);
  data['popup'] = [["zgłoszenia"]];
  a.forEach(e=>data['popup'].push([e]))
  data["popup type"] = "table";
}