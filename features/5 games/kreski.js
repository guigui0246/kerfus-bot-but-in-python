const fs = require('fs');

function printgame(game){
  function printrow(row){
  let out = "";
  for(let i=0;i<row.length;i++){
    if(row[i]==0)out += '\\| ';
    else{
      out+= '~~' + '\\| '.repeat(row[i]-1) + '\\|' + '~~ ';
      i+=row[i]-1;
    }
  }
  return out;
}
  let out = '';
  for(let i in game){
    out += 'abcdefghijklmno'[i] + printrow(game[i]) + '\n';
  }
  return out;
}

exports.run = (msg,client) => {
  if(!msg.content.startsWith('k!'))return;
  let n = client.db.get('kreskigames.txt',0);
  let args = msg.content.split(' ').slice(1);
  switch(msg.content.split(' ')[0].slice(2).toLowerCase()){
    case 'help':{
      msg.reply('k!start @opponent to start a game\nk!move (gameid) (move) to move')
    break;}case 'start':{
      if(args[1]==undefined)args[1]=4;
      const starting = [[0]];
for(let i=0;i<args[1]-1;i++){
  starting[i+1]=JSON.parse(JSON.stringify(starting[i]));
  starting[i+1].push(0,0);
}
      client.db.settype('kreski',n+'.json',[msg.author.id,args[0].slice(2,-1),0,starting,starting,'11'])
      n = `${parseInt(n)+1}`;
      client.db.set('kreskigames.txt',n);
      msg.reply(`game started! id: ${parseInt(n)-1}\n${printgame(starting)}`);
    break;}case 'move':{
      if(args.length<2){msg.reply('not enough arguments');break;}
      if(args[1].length<3){msg.reply('move is supposed to be (row)(start)(end)\nfor example b12');break;}
      let game = JSON.parse(client.db.gettype('kreski',args[0]+'.json'));
      if(msg.author.id!=game[game[2]]){msg.reply('not your turn!');break;}
      let x = 'abcdefghijklmno'.indexOf(args[1][0]);
      let y = parseInt(args[1][1]);
      let z = parseInt(args[1][2]);
      let allowed = true;
      for(let i of game[3][x].slice(y-1,z))if(i!=0)allowed = false;
      if(allowed){
        game[4] = JSON.parse(JSON.stringify(game[3]))
        for(let i=y;i<z;i++){game[3][x][i]=1;}
        game[3][x][y-1] = z-y+1;
        game[2] = (game[2]+1)%2;
      }
      client.db.settype('kreski',args[0]+'.json',game)
      let cont = false;
      for(let x of game[3])for(let y of x)if(!y)cont=true;
      if(cont)
        msg.reply(printgame(game[3]));
      else
        msg.reply(`game ends, <@${game[(game[2]+1)%2]}> wins!`)
    break;}case 'undo':{
      if(args.length<1){msg.reply('not enough arguments');break;}
      let game = JSON.parse(client.db.gettype('kreski',args[0]+'.json'));
      if(msg.author.id!=game[(game[2]+1)%2]){msg.reply('not your turn!');break;}
      if(game[5][game[2]]=='0'){msg.reply('you can only undo once');break;}
      game[3] = game[4];
      game[2] = (game[2]+1)%2;
      game[5][game[2]] = '0';
      client.db.settype('kreski',args[0]+'.json',game);
    break;}
  }
}