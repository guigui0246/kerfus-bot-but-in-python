//deleted by 0lie
exports.run = (client,res,req,data) => {
  data['send'] = 'codeanon';
  data['popup'] = require("/home/runner/kerfus-bot/funcs/anonymiser.js").anon(req.body.code);
  data["popup type"] = "text";
}