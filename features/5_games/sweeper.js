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
        if(real=='0')
          out += '`'+" ".repeat(outsize)+'` ';
        else
          out +="`"+real.slice(0,outsize)+" ".repeat(outsize-real.length)+"` ";
        if(imag=='0')
          outt += '`'+" ".repeat(math.floor(outsize))+'` ';
        else 
          outt+="`"+imag.slice(0,outsize)+" ".repeat(math.floor(outsize-imag.length))+"` ";
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
  
  let player = {"board":games[msg.author.id],"mta":mta[msg.author.id]};
  let player = JSON.parse(client.db.v2getuser("sweeper",msg.author.id))
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
      player = {};
      player.board = board;
      player.mta = args[0];
      msg.reply('started probably idk')
    break}
    case 'sweep':{
      if(!player){msg.reply('you have to start a game!');break}
      if(args.length<2){msg.reply('too few agruments');break;}
      if(!isNumeric(args[0])||!isNumeric(args[1])){msg.reply('expected 2 intigers');break}
      let [x,y] = args;
      if(player.board[x][y]>0){
        msg.reply('you clicked a mine!')
        delete player.board;
        delete player.mta;
      }else{
        player.board[x][y] = -1;
        msg.reply(printboard(player.board,player.mta))
      }
    break}
    case 'help':{
      msg.reply('welcome to the complex minesweeper!\nin this minesweeper, there are N different mine types\neach mine\'s value is one of the Nths roots of unity\nthe values on the cells are the sum of values of the neighbouring 8 cells(empty=0)\ntop is the real part, bottom is the imaginary part\n\ncommands:\n[]-> optional,\n> m!start mine_type_amount [board_size=5]\n\n> m!sweep x y\nnote: 0-indexed, so for a 5x5 board the possibilities are 0,1,2,3,4')
    break}
  };
  if(player=={}) client.db.v2deluser("sweeper",msg.author.id);
  else client.db.v2setuser("sweeper",msg.author.id,JSON.stringify(player))
}