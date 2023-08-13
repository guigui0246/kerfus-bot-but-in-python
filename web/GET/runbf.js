const misc = require('/home/runner/kerfus-bot/funcs/misc.js');

exports.run = (client,res,req,data) => {
  let output = require('/home/runner/kerfus-bot/funcs/brainf.js').wholesim(req.query.sett.split(''),req.query.runtime,[req.query.input],req.query.code)
  data["popup"] =[["output"],[output==""?"no output":output]];
  data["popup type"] = "table";
  data['send'] = 'brainf';
}