exports.run = (client,res,req,data) => {
  if(!req.user||!req.user.tags.admin){
    data["popup"] = "Error: no access";
    data["popup type"] = "text";
    return;
  }
  data["send"] = 'admin';
}