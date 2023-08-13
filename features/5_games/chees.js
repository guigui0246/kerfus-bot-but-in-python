const meth = require('math');

const startingpos = [
  ["+rook","+horse","+bishop","+queen","+king","+bishop","+horse","+rook"],
  ["+pawn","+pawn","+pawn","+pawn","+pawn","+pawn","+pawn","+pawn"],
  ["","","","","","","",""],
  ["","","","","","","",""],
  ["","","","","","","",""],
  ["","","","","","","",""],
  ["-pawn","-pawn","-pawn","-pawn","-pawn","-pawn","-pawn","-pawn"],
  ["-rook","-horse","-bishop","-queen","-king","-bishop","-horse","-rook"]
]

function isNumeric(n){return !isNaN(parseFloat(n)) && isFinite(n);}

function printgame(board){
  if(!board){return 'game not found';}
  out = ""
  for(var i=8;i--;){
    for(let j of board[i])
      if(j==""||j[2]=="g") out+="` ` "
      else out+=j[0]=="+"?"*":""+`*\`${j[1].toUpperCase()}\`*`+j[0]=="+"?"* ":" ";
    out += "\n"
  }
  return out;
}

function isempty(board, move){
  let mov = [meth.min(move[0],move[2]),
             meth.min(move[1],move[3]),
             meth.max(move[0],move[2]),
             meth.max(move[1],move[3])
          ];
  let dir = [(mov[0]==move[0])*2-1,(mov[1]==move[1])*2-1];
  let out = true;
  if(mov[0]==mov[2]){
    board[mov[0]].slice(mov[1]+1,mov[3]).forEach(e=>{out&=e==""||e[2]=="g"});
    return out?"rook":false;
  }else if(mov[1]==mov[3]){
    board.slice(mov[0]+1,mov[2]).forEach(e=>{out&=e[mov[1]]==""||e[mov[1]][2]=="g"});
    return out?"rook":false;
  }
  else if(mov[2]-mov[0]==mov[3]-mov[1]){
    let j=move[1];
    for(let i=move[0];i!=move[2];i+=dir[0]){
      if(game[3][i][j]!=""&&game[3][i][j][1]!="g")return false;
      j+=dir[1];
    }
    return "vbishop";
  }
  return false;
}

exports.run = (msg,client) => {
  if (!msg.content.startsWith('c!')) return;
  var content = msg.content.split(" ");
  var id = msg.author.id;
  let temp,amount,game;
  switch(content[0]){
    case "c!see":
      temp = client.db.v2get(`chess/${content[1]}.json`);
      msg.reply(printgame(temp[3]));
    break; case "c!help":
      msg.reply(`command list:\n> !start <opponent>\n\n> !move <gameid> <move>\n example: !move 69 a1b1\n\n> !cleargames (only for me)\n\n`);
    break; case "c!start":
      amount = parseInt(client.db.v2get('other/chessgames.txt',0));
      client.db.v2set('other/chessgames.txt',amount+1)
      client.db.v2set(`chess/${amount}.json`,JSON.stringify([id,content[1].slice(2,-1),"+",startingpos,"1111"]))
      msg.reply(`game started! id:${amount}`)
      msg.reply(printgame(startingpos));
    break; case "c!move":
      amount = client.db.v2get('other/chessgames.txt',0);
      if(!isNumeric(content[1])||content[1]>=amount){
        msg.reply(`game id ${content[1]} not found :(`)
        return;
      }
      
      game = JSON.parse(client.db.v2get(`chess/${content[1]}.json`));
      if(!(game[2]=="+"&&game[0]==id||game[2]=="-"&&game[1]==id)) return;
      
      move = [content[2][1]-1,"abcdefgh".indexOf(content[2][0]),content[2][3]-1,"abcdefgh".indexOf(content[2][2])];
      for(x of move) if(x<0||x>7){msg.reply('moves outside the board :(');return;}
      from = game[3][move[0]][move[1]];
      to = game[3][move[2]][move[3]];
      
      if(move[0]==move[2]&&move[1]==move[3]){msg.reply("you cant skip a turn!");return;}
      if(from==""){msg.reply("This spot is empty!");return;}
      if(!from.startsWith(game[2])){msg.reply("not your figure");return;}
      if(to.startsWith(game[2])){msg.reply("you cant take your figure");return;}
      let a = move[3] - move[1];
      let b = move[2] - move[0];
      a = meth.abs(a);
      b = meth.abs(b);
      
      switch(from.slice(1)){
        case "pawn":
          if(move[3]==move[1]){
            if(b==1||(b==2&&(move[0]==1||move[0]==6)&&game[3][(move[2]+move[0])/2][move[1]]=="")&&to==""){
                game[3][move[2]][move[3]] = game[3][move[0]][move[1]];
                game[3][move[0]][move[1]] = "";
                if(b==2) game[3][(move[2]+move[0])/2][move[1]] = game[2] + "ghostpawn.";
            }else return;
          }else if(b==1&&a==1){
            if(to.slice(1)=="ghostpawn") game[3][move[0]][move[3]] = "";
            game[3][move[2]][move[3]] = game[3][move[0]][move[1]];
            game[3][move[0]][move[1]] = "";
          }else return;
          if(move[2]==0||move[2]==7) game[3][move[2]][move[3]] = game[3][move[2]][move[3]][0] + "queen";
        break; case "rook":
          if(isempty(game[3],move)=="rook"){
            game[3][move[2]][move[3]] = game[3][move[0]][move[1]];
            game[3][move[0]][move[1]] = "";
          }else return;
        break; case "horse":
          if(a*b==2){
            game[3][move[2]][move[3]] = game[3][move[0]][move[1]];
            game[3][move[0]][move[1]] = "";
          }else return;
        break; case "bishop":
          if(isempty(game[3],move)=="bishop"){
            game[3][move[2]][move[3]] = from;
            game[3][move[0]][move[1]] = "";
          }else return;
        break; case "queen":
          if(isempty(game[3],move)){
            game[3][move[2]][move[3]] = game[3][move[0]][move[1]];
            game[3][move[0]][move[1]] = "";
          }else return;
        break; case "king":
          if(a<2&&b<2){
            game[3][move[2]][move[3]] = game[3][move[0]][move[1]];
            game[3][move[0]][move[1]] = "";
            break;
          }
          if(!(a==2&&b==0)) return;
          if(!isempty(game[3],move)) return;
          if(move.join('')=="0402"&&game[4][0]=="1"){
            game[3][0][0]="";
            game[3][0][2]="+king";
            game[3][0][3]="+rook";
            game[3][0][4]="";
          }else if(move.join('')=="0406"&&game[4][1]=="1"){
            game[3][0][4]="";
            game[3][0][5]="+rook";
            game[3][0][6]="+king";
            game[3][0][7]="";
          }else if(move.join('')=="7472"&&game[4][2]=="1"){
            game[3][7][0]="";
            game[3][7][2]="-king";
            game[3][7][3]="-rook";
            game[3][7][4]="";
          }else if(move.join('')=="7476"&&game[4][3]=="1"){
            game[3][7][4]="";
            game[3][7][5]="-rook";
            game[3][7][6]="-king";
            game[3][7][7]="";
          }else return;
        break;
      }
      for(let i in game[3]) for(let j in game[3][i]) if(game[3][i][j].slice(1)=="ghostpawn")game[3][i][j]="";
      for(let i in game[3]) for(let j in game[3][i]) if(game[3][i][j].slice(1)=="ghostpawn.")game[3][i][j]=game[3][i][j][0]+"ghostpawn";
      if(from=="+king")game[4] = "00"+game[4].slice(2);
      if(from=="-king")game[4] = game[4].slice(0,2)+"00";
      temp = [[0,0],[0,7],[7,0],[7,7]];
      for(let i in temp) if([move[0],move[1]]==temp[i]||[move[2],move[3]]==temp[i])game[4][i] = "0";
      msg.reply(printgame(game[3]));
      if(game[2]=="+")game[2]="-";
      else game[2]="+";
      client.db.v2set(`chess/${content[1]}.json`,JSON.stringify(game));
    break; case "c!cleargames":
      if(id != 438767282328436737n) return;
      amount = client.db.v2get('other/chessgames.txt',0);
      for(let x in amount)
        client.db.v2set(`chess/${x}.json`,'[]');
      client.db.v2set('otherchessgames.txt',0)
    break; case "c!delgame":
      game = client.db.v2get(`chess/${content[1]}.json`);
      if([game[0],game[1],438767282328436737n].includes(id)) return;
      client.db.v2del(`chess/${content[1]}.json`);
    break;
  }
}
