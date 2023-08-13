exports.run = (client,res,req,data) => {
  if(!req.user){
    data["popup"] = "Error: not logged in";
    data["popup type"] = "text";
    return;
  }
  data["send"] = 'account';
}