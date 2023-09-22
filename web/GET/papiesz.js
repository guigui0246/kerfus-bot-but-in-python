const fs = require('fs')

exports.run = (client,res,req,data) => {
  let filepath = "/home/runner/kerfus-bot/papieszaki/"+req.query.file;
  if(fs.existsSync(filepath)){
    res.sendFile(filepath);
  }
  return 'stop';
}