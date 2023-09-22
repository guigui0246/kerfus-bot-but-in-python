const fs = require('fs')
const math = require('math');
exports.setup = async (client)=>{
  const channel = await client.channels.fetch('1142562663361155103')
  //console.log(channel)
  //channel.send('test')
  const files = fs.readdirSync('papieszaki');
  
  
let fun = async ()=>{
      let time = 1*new Date()-1000*(60*(37+19*60));
      let date = math.floor(time/(24*60*60*1000));
      //console.log(time,date)
      let newest = 1*client.db.v2get('other/papiesz.txt',`${date}`);
      //console.log(time,date,newest)
      while(newest<date){
        
        let random = Math.floor(Math.random()*files.length);
        //console.log(random,files[random])
        await  channel.send('https://kerfus-bot.0lie.repl.co/papiesz?file='+files[random]);
        newest+=1;
      }
      client.db.v2set('other/papiesz.txt',newest);
  }
  setInterval(fun,60*1000)//*/
  fun();
}
exports.run=()=>{}