//Deleted by 0lie
const fs = require('fs');

function wordAt(word,at){
  let start = at, end = at;
  if(/[a-zA-Z0-9_]/.test(word[at])){
    while(start>0&&/[a-zA-Z0-9_]/.test(word[start-1]))
      start--;
    while(end<word.length&&/[a-zA-Z0-9_]/.test(word[end]))
      end++;
  }
  if(end-start==0)
    return [word.slice(start,end+1),start,end];
  return [word.slice(start,end),start,end];
  
}

function findVars(code){
  let vars = code;
  let keywords = fs.readFileSync('data/keywords.txt', 'utf-8').split('\n');
  for(let x in keywords)keywords[x]=keywords[x].trim();
  vars = vars.split('\n').filter(e=>!/^#/.test(e)).join(' ');
  let instr = false;
  let strstart = 0;
  for(let x in vars){
    if(vars[x]!='"')continue;
    if(!instr)
      strstart = x;
    else{
      vars = vars.slice(0,strstart)+vars.slice(x,Infinity);
      x = strstart;
    }
    instr = !instr;
  }
  for(let x in vars){
    let wa = wordAt(vars,x)[0];
    if(keywords.includes(wa))
      vars=vars.replace(wa,' ');
  }
  vars = [...new Set(vars.trim().replace(/([\t\r\n]|  )/g,' ').split(' '))];
  for(let x in vars)
    while(/^[0-9]+(.[0-9]+)?$/.test(vars[x]))
      vars.splice(x,1);
  vars = vars.filter(e=>e!="");
  return vars;
}

function randName(rander){
  let seed = new (require('./seed.js'))(rander + new Date());
  let x = seed.randomInt(0,2);
  let abc = "qwertyuiopasdfghjklzxcvbnm";
  abc = abc + abc.toUpperCase();
  let name = abc[seed.randomInt(0,abc.length-1)];
  abc += "0123456789";
  for(let i =0;i<x;i++)
    name+= abc[seed.randomInt(0,abc.length-1)];
  return name;
}

exports.anon = (code) => {
  let temp = code.split('\n');
  let org = "";
  // removing comments 
  for(let x of temp)
    if(!/^\/\//.test(x))
       org+= x + '\n';
  
  // generating new var names
  let vars = findVars(org);
  let newnames = [];
  for(let x = 0;x<vars.length;){
    let temp=randName(x);
    if(!newnames.includes(temp)){
      newnames.push(temp);
      x++;
    }
  }

  //replacing variables with new names
  for(let x = 0;x<code.length;x++){
    let wa = wordAt(code,x);
    let index = vars.indexOf(wa[0]);
    if(index!=-1){
      code = code.slice(0,wa[1]) + newnames[index] + code.slice(wa[2],Infinity);
    }
  }
  
  //splitting fors into multiple lines
  const seed = new (require('./seed.js'))(""+new Date())
  code = code.replace(/\n([ \t]*)for\((.*);(.*);(.*)\)/g,(match,p1,p2,p3,p4,offset,string,groups) => {
    if(!seed.randomInt(0,4)){
      return `\n${p1}for(\n\t${p1+p2};\n\t${p1+p3};\n\t${p1+p4}\n${p1})`;
    }
    return match;
  });

  //doubling line breaks
  code = code.replace(/\n/g,(match,p1,offset,string,groups)=>{
    if(!seed.randomInt(0,2))
      return "\n\n";
    return "\n";
  });
  
  return code;
}


exports.test = () => {
}