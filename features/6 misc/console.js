const fs = require('fs');

exports.run = async (msg, client) => {
  run(msg,client);
}

function run(msg,client){
if (!msg.content.startsWith('!console ')) return;
let data = JSON.parse(client.db.v2getuser(`console`,msg.author.id, '{"dir":"/"}'));

let text = msg.content.split(' ').slice(1).join(' ');
let sudo = false;
if(text.split(' ')[0]=='sudo'){
  if(client.misc.hastag("admin",msg.author.id)){
    sudo = true;
    text = text.split(' ').slice(1).join(' ');
  }else{
    msg.reply(reply+`${msg.author.username} is not in the sudoers file. This incident will be reported.\`\`\``);
    return;
  }
}

out = "```root@win 10 ~]#" + text + '\n';

function index(list,fun){
  let val = -1;
  list.forEach((e,i)=>{
    if(val!=-1)return;
    if(fun(e,i)) val=i;
  })
  return val;
}

function fixdir(dir){
	while(dir.includes("/./"))
      dir = dir.replaceAll("/./","/")
    
    while(dir.includes("//"))
      dir = dir.replaceAll("//","/");
    while(dir.includes("/../")){
      dir = dir.replace(/^\/..\//,"/")
      dir = dir.replace(/\/[^\/]+?\/\.\.\//,"/")
    }
	return dir;
}

const commands = {
  echo:(args)=>{
    return args.join(" ")
  },
  dir:(args)=>{
    if (!fs.existsSync(data.dir)) {
        return `directory not found`;
    }
    temp = fs.readdirSync(data.dir);
    return temp.join('\n');
  },
  cd:(args)=>{
    if (args[0] == '..') {
      if (data.dir == '/')
        return `you're at root, idiot`;
      data.dir += "/../";
      data.dir = fixdir(data.dir);
      return "";
    }
    temp = args.join(" ")+"/";
    temp = temp.replace("~","/home/runner/kerfus-bot")
    var newdir = (temp[0]=="/"?"":data.dir)+temp;  
    if (!fs.existsSync(newdir))
      return `directory not found`;
    data.dir = newdir;
    data.dir = fixdir(data.dir);
    return "";
  },
  cat:(args)=>{
    var temp = args.join(" ");
    temp = temp.replace("~","/home/runner/kerfus-bot")
    temp = (temp[0]=="/"?temp:(data.dir+temp));
    if (!fs.existsSync(temp))
      return `file not found`;
    try{
      temp = ""+fs.readFileSync(temp);
      return temp;
    }
    catch(err){
      return 'typeError: its a folder dumbass';
    }
  },
  none:(args)=>"",
  mkdir:(args)=>{
    var temp = args.join(" ");
    temp = temp.replace("~","/home/runner/kerfus-bot")
    temp = (temp[0]=="/"?temp:(data.dir+temp));
    if(!sudo&&!temp.startsWith(`/home/runner/kerfus-bot/personal/${msg.author.id}`)){
      msg.reply('access error')
      return 'access error';
    }
    fs.mkdirSync(temp,{recursive:true});
    return "";
  }
}



let formatted = ""
let quotes=""
function findquotes(text){
  let formatted = ""
  let quotes=""
  let i=0
  let in_quotes=0;
  while(i<text.length){
    let char = text[i];
    if(char=='\\'){
      char=text[i+1];
      quotes+=1;
      formatted+=char;
      i++;
    }else
    if(char=='"'){
      in_quotes^=true;
    }
    else{
      quotes+=in_quotes;
      formatted+=char;
    }
    i++;
  }
  return [formatted,quotes]
}
[formatted,quotes]=findquotes(text);


function execute(text,quotes,newargs="",newquotes=""){
  let ind = index(text.split(""),(e,i)=>{return e==">"&&quotes[i]=="0"});
  if(ind!=-1){
    let out = execute(text.slice(0,ind),quotes.slice(0,ind),newargs,newquotes)
    let file = "";
    let append = false;
    let text_ = out
    if(text[ind+1]==">"){
      append = true;
      file = '/'+data.dir+"/"+text.slice(ind+2).trim();
    }else
      file = '/'+data.dir+"/"+text.slice(ind+1).trim();
    file = fixdir(file);
    if(sudo==false&&!file.startsWith(`/home/runner/kerfus-bot/personal/${msg.author.id}`)){
      msg.reply('access error')
      return 'access error';
    }
    let dir = file.split('/').slice(0,-1).join('/');
    if(!fs.existsSync(dir))
      return "not found error: directory doesnt exist";
    fs.closeSync(fs.openSync(file, 'w'));
    console.log(append,text_)
    if(append){
      text_ = fs.readFileSync(file.trim()) + text_;
      console.log(fs.readFileSync(file.trim()),text_);
      console.log("."+file.trim()+".")
      fs.writeFileSync(file,text_);
    }else
      fs.writeFileSync(file,text_);
    return "";
  }
  ind=index(text.split(""),(e,i)=>{return e=="|"&&quotes[i]=="0"});
  if(ind!=-1){
    let newargs = execute(text.slice(0,ind),quotes.slice(0,ind));
    let [nform,nq]=findquotes(newargs);
    return execute(text.slice(ind+1),quotes.slice(ind+1),nform,nq);
  }
  //actual commands here
  text = text+newargs;
  quotes = quotes+newquotes;
  while(text[0]==" "){
    text = text.slice(1);
    quotes = quotes.slice(1);
  }
  let args=[];
  let curr="";
  for(let i=0;i<text.length;i++){
    let char = text[i];
    let quo = quotes[i];
    if(char==" "&&quo=="0"){
      args.push(curr);
      curr="";
      while(text[i]==" ")
        i++;
      i--;
    }else{
      curr+=char;
    }
  }
  args.push(curr)
  if(!(args[0] in commands)){
    msg.channel.send("error: unexpected command "+args.join(' '));
    return '';
  }
  return commands[args[0]](args.slice(1))
}

  
let top_dir = data.dir.split("/");
top_dir = top_dir[top_dir.length-2];
top_dir = top_dir==""?"/":top_dir;

out = execute(formatted,quotes);
let reply = `[root@win 10 ${top_dir=="kerfus-bot"?"~":top_dir}]# ${text}\n`;
client.db.v2setuser(`console`,msg.author.id,JSON.stringify(data));
let pages = client.misc.sliceby(out,1500);
if(pages.length==0)msg.channel.send("```"+reply+'```')
pages.forEach(e=>{
  msg.channel.send("```"+reply.replace('```','\\```')+e.replace('```','\\```')+'```')
})
}