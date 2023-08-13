function create(sett = [0,0,0]){
  return {
    settings:sett,
    data:[0],
    pointer:0,
    command:0,
    output:""
  }
}
exports.createinstance = create;

function runframe(instance,commands,input){
  switch(commands[instance.command]){
    case '+':
      instance.data[instance.pointer] += 1;
      if(instance.settings[2]==0)
        instance.data[instance.pointer] %=256;
      break;
    case '-':
      instance.data[instance.pointer] -= 1;
      if(instance.settings[2]==0)
        instance.data[instance.pointer] %=256;
      break;
    case '>':
      instance.pointer += 1;
      if(instance.data.length <= instance.pointer)
        instance.data.push(0);
      break;
     case '<':
      instance.pointer -= 1;
      break;
    case ',':
      if(instance.settings[0]==1){
        instance.data[instance.pointer] = Number(input[0].split(' ')[0]);
        
        input[0] = input[0].slice(input[0].split(' ')[0].length+1);
      }else{
        instance.data[instance.pointer] = input[0].charCodeAt(0);
        input[0] = input[0].slice(1);
      }
      break;
    case '.':
      if(instance.settings[1]==1){
        instance.output += instance.data[instance.pointer] + " ";
      }else{
         instance.output += String.fromCharCode(instance.data[instance.pointer]);
      }
      break;
    case '[':
      if(!instance.data[instance.pointer]){
        let depth = 1;
        while(depth>0){
          instance.command+=1;
          depth += commands[instance.command]=='[';
          depth -= commands[instance.command]==']';
        }
      }
      break;
     case ']':
      if(instance.data[instance.pointer]){
        let depth = 1;
        while(depth>0){
          instance.command-=1;
          depth -= commands[instance.command]=='[';
          depth += commands[instance.command]==']';
        }
      }
      break;
  }
  //console.log(`${instance.data} ${instance.command} ${instance.pointer} `)
  instance.command+=1;
  return instance.command < commands.length;
}
exports.runframe = runframe;

exports.wholesim = (settings, runtime, input, code) => {
  let instance = create(settings);
  let cont = true;
  for(let x=0;(x<runtime||runtime==-1)&&cont;x++)
    runframe(instance,code,input);
  return instance.output;
}