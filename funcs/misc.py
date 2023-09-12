import json
import time
import asyncio

def setup (a):
    client = a
    n = 1*client.db.nget('other/remindercount')
    reminders = []
    loop = asyncio.get_event_loop()
    async def process_reminder(client, x):
        temp = await client.db.nget(f"reminder/{x}")
        if temp:
            reminder_data = json.loads(temp)
            reminders.append(reminder_data)
            await asyncio.sleep((reminder_data[1] - (int(time.time() * 1000))) / 1000)
            user = await client.fetch_user(reminder_data[0])
            try:
                await user.send(reminder_data[2])
            except:
                pass
            await client.db.ndel(f"reminder/{reminder_data[3]}")
    for x in range(400, n):
        loop.create_task(process_reminder(client, x))
    loop.run_forever()
    return globals()



def test():
    return

"""
exports.addhtmls = (data,document) => {
    let gen = ""+fs.readFileSync("web/generic.html");
    let doc = (""+document).split('##');
    let out = gen.replace("#DATA#",JSON.stringify(data));
    for( let x = 0;x<doc.length;x+=2)
        out = out.replace(`#${doc[x]}#`,doc[x+1])
    return out;
}

exports.hastag = (tag,id) => {
    let tagged= JSON.parse(fs.readFileSync("data/tags.json", 'utf-8'));
    if(!(tag in tagged))return false;
    return tagged[tag].includes(id);
}

exports.addtag = (tag,id) => {
    let tagged = JSON.parse(fs.readFileSync("data/tags.json", 'utf-8'));
    if(tag in tagged){
        if(!(tagged[tag].includes(id)))tagged[tag].push(id);
    }
    else
        tagged[tag] = [id];
    fs.writeFileSync("data/tags.json", JSON.stringify(tagged));
}

exports.removetag = (tag,id) => {
    let tagged = JSON.parse(fs.readFileSync("data/tags.json", 'utf-8'));
    if(tag in tagged)
        if(tagged[tag].includes(id)){
            tagged[tag].splice(tagged[tag].indexOf(id),1);
            fs.writeFileSync("data/tags.json", JSON.stringify(tagged));
        }
}

exports.log = (text , file = 'logs.txt') => {
    fs.appendFileSync(file, text.replace(/\n/g,' ')+"\n");
}

exports.polishchars = (text) => {
    let copy = text;
    let polish = "ęóąśłżźćń";
    let fixed = "eoaslzzcn";
    for(let i in fixed)
        copy = copy.replaceAll(polish[i], fixed[i])
    return copy;
}

exports.sliceby = (text,spacing) => {
    out = [];
    for(var i = 0;i<text.length;i+=spacing){
        out.push(text.slice(i,i+spacing));
    }
    return out;
}

function replace4html(inp){
    let text = inp;
    if(typeof text=='string'||typeof text=='number'){
        text = text.replaceAll('<','&lt;')
        text = text.replaceAll('>','&gt;')
        text = text.replaceAll(/\r?\n\r?/g,'<br>') 
    }
    else
        text.forEach((e,i)=>text[i]=replace4html(e));
    return text;
}

exports.replace4html = replace4html;

exports.remind = (time, user, message)=>{
    let numb = 1*client.db.nget('other/remindercount',0);
    client.db.nset('other/remindercount',`${numb+1}`);
    let timeend = time*1000+1*new Date();
    client.db.nset(`reminder/${numb}`,JSON.stringify([user.id,timeend,message]))
    setTimeout(()=>{
        user.send(message).catch(err=>{});
        client.db.ndel(`reminder/${numb}`)
    },time*1000);
}"""