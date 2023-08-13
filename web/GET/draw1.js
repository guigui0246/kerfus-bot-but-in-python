let n=20,m=20;
let def = [];
for(let i=0;i<n;i++){
  def.push([]);
  for(let j=0;j<m;j++)
    def[i].push('000000')
}
exports.run = (client,res,req,data) => {
  if(req.query.type==-1){
    let ret = client.webdb.v2get('other/drawmap',def);
    res.send(ret);
  }else{
    if(req.query.type>n*m-1){res.send('ERR: wrong position');return 'stop';}
    let ret = JSON.parse(client.webdb.v2get('other/drawmap',JSON.stringify(def)));
    let allowed = /#?[a-zA-Z0-9]{6}/.test(req.query.col)
    let col = req.query.col;
    if(col[0]=="#")col=col.slice(1);
    if(allowed){
      let pos = parseInt(req.query.type);
      ret[pos/m-pos/m%1][pos%m] = col;
      client.webdb.v2set('other/drawmap',JSON.stringify(ret));
    }
    res.send(JSON.stringify(ret));
  }
  return 'stop';
}