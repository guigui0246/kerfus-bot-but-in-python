const fs = require('fs')
exports.run = (client,res,req,data) => {
  if(!req.query.path){
    res.send({status:1,error:'filepath not specified'})
    return 'stop';
  }
  if(!fs.existsSync(req.query.path)){
    res.send({status:2,error:'file doesnt exist'})
    return 'stop';
  }
  res.send({status:0,file:fs.readFileSync(req.query.path,'utf-8')})
  return 'stop';
}