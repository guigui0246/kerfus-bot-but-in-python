var CryptoJS = require("crypto-js");

exports.run = (client,res,req,data) => {
  data['send'] = 'suggest';
  let suggestions = JSON.parse(client.db.get('suggestions',[]));
  // Encrypt
  let sug = req.body.sugg.toLowerCase();
  var ciphertext = CryptoJS.AES.encrypt(sug, process.env['ENCRYPTION']).toString();

  let added = suggestions.includes(ciphertext);
  if(!added){
    suggestions.push(ciphertext);
    client.db.set('suggestions',JSON.stringify(suggestions));
  }
  data["popup"] = added?"suggestion was already posted":"suggestion added!";
  data["popup type"] = "text";
}