let math = require('math');
let games = {};
const def_size = 5;
const mineamount = 0.2;
let mta = {}; //minetypaamount
const outsize = 5;

function isNumeric(n){return !isNaN(parseFloat(n)) && isFinite(n);}

function printboard(board,amount){
  let out = "";
  for(let x in board){
    let outt = "";
    for(let y in board[x]){
      if(board[x][y]==-1){
        let sum = [0,0];
        for(let x1 = -1;x1<2;x1++)
          for(let y1=-1;y1<2;y1++)
            if(x-x1>-1&&y-y1>-1&&x-x1<size&&y-y1<size)
            if(board[x-x1][y-y1]>0){
              sum[0] += math.cos(board[x-x1][y-y1]*6.283185/amount);
              sum[1] += math.sin(board[x-x1][y-y1]*6.283185/amount);
            }
        let real = (math.round(sum[0]*1000)/1000).toString();
        let imag = (math.round(sum[1]*1000)/1000).toString();
        if(real=='0')out += '`'+" ".repeat(outsize)+'` ';
        else
          out +="`"+real.slice(0,outsize)+" ".repeat(outsize-real.length)+"` ";
        if(imag=='0')outt += '`'+" ".repeat(math.floor(outsize))+'` ';
        else
          outt+="`"+imag.slice(0,outsize)+" ".repeat(math.floor(outsize-real.length))+"` ";
      }else{
        out += '`'+"#".repeat(outsize)+'` '
        outt += '`'+"#".repeat(outsize)+'` '
      }
    }
    out += "\n"+outt+"\n\n";
  }
  return out;
}

exports.run = (msg, client) => {
  if(!msg.content.toLowerCase().startsWith('m!')) return;
  let args = msg.content.split(' ').slice(1);
  switch(msg.content.split(' ')[0].slice(2).toLowerCase()){
    case 'start':{
      if(args.length<1){msg.reply('too little arguments');break}
      size = args[1]??def_size
      let board = [];
      for(let x=0;x<size;x++){
        board.push([])
        for(let y=0;y<size;y++)
          if(math.random()<mineamount)
            board[x].push(math.floor(math.random()*args[0])+1)
          else
            board[x].push(0)
      }
      games[msg.author.id] = board;
      mta[msg.author.id] = args[0];
    break}case 'sweep':{
      if(!(msg.author.id in games)){msg.reply('you have to start a game!');break}
      if(args.length<2){msg.reply('too few agruments');break;}
      if(!isNumeric(args[0])||!isNumeric(args[1])){msg.reply('expected 2 intigers');break}
      let board = games[msg.author.id];
      let [x,y] = args;
      if(board[x][y]>0){
        msg.reply('you clicked a mine!')
        delete games[msg.author.id];
      }else{
        board[x][y] = -1;
        msg.reply(printboard(games[msg.author.id] = board,mta[msg.author.id]))
      }
    break}
  }
}