const fs = require('fs');
const misc = require('./misc.js');

class replies {
  filename;
  data;
  client;
  
  reload(){
   this.data = JSON.parse(fs.readFileSync("data/" + this.filename, 'utf-8'));
  }
  
  constructor(name, client){
    this.filename = name;
    this.client = client;
    this.reload();
  }

  save() {
    fs.writeFileSync("data/"+ this.filename, JSON.stringify(this.data,null,2))
  }

  includes(msg, x) {
    let out = false;
    this.data[x].slice(2).forEach(e=>out|=msg.includes(e))
    return out;
  }

  allowed(x, servid, chanid) {
    let tags = this.data[x][0];
    for(let a of tags)
      if(this.client.misc.hastag('no'+a,servid))return false;
    if(this.client.misc.hastag('nopastas',servid)||this.client.misc.hastag('nopastas',chanid))return false;
    return true;
  }

  len() {
    return this.data.length
  }

  get(id) {
    return this.data[id][1];
  }

  add(msg, reactions) {
    this.data.push([[], msg].concat(reactions));
    this.save();
  }

  findid(msg) {
    let out = [];
    this.data.forEach((e,i)=>{if(this.includes(msg,i))out.push(i)})
    return out;
  }

  addreact(id, react) {
    this.data[id].push(react);
    this.save();
  }

  getreact(id) {
    return this.data[id].slice(2);
  }

  setmsg(id, msg) {
    this.data[id][1] = msg;
    this.save();
  }

  delet(id) {
    this.data.splice(id, 1);
    this.save();
  }
}

module.exports = replies;