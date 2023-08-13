exports.run = (client,res,req,data) => {
  res.redirect('/index');
  return 'stop';
}