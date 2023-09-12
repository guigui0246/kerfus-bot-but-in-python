from typing import Any
from typing import SupportsIndex
import json
import time
import asyncio
import re

def setup (a) -> dict[str, Any]:
    global client
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

def addhtmls(data, document) -> str:
    with open("web/generic.html") as file:
        gen = file.read()
    doc = str(document).split("##")
    out = gen.replace("#DATA#",json.dumps(data))
    for x in range(0, len(doc), 2):
        out = out.replace(f"#{doc[x]}#", doc[x+1])
    return out

def hashtag (tag:SupportsIndex, id) -> bool:
    with open("data/tags.json", encoding="utf-8") as file:
        tagged:list[list] = json.load(file)
    if not tag in tagged:
        return False
    return id in tagged[tag]

def addtag(tag:SupportsIndex, id):
    with open("data/tags.json", encoding="utf-8") as file:
        tagged:list[list] = json.load(file)
    if tag in tagged:
        if not id in tagged[tag]:
            tagged[tag].append(id)
    else:
        tagged[tag] = [id]
    with open("data/tags.json", "w", encoding="utf-8") as file:
        json.dump(tagged, file)

def removetag(tag:SupportsIndex, id):
    with open("data/tags.json", encoding="utf-8") as file:
        tagged:list[list] = json.load(file)
    if tag in tagged:
        if id in tagged[tag]:
            tagged[tag].remove(id)
            with open("data/tags.json", "w", encoding="utf-8") as file:
                json.dump(tagged, file)

def log(text:str, filepath:str="logs.txt"):
    with open(filepath, "a") as file:
        file.write(text.replace("\n", " ") + "\n")

def polishchars(text:str) -> str:
    copy = text
    polish = "ęóąśłżźćń"
    fixed = "eoaslzzcn"
    for i in range(len(fixed)):
        copy = copy.replace(polish[i], fixed[i])
    return copy

def sliceby (text:str, spacing:SupportsIndex) -> list:
    out = []
    for i in range(0, len(text), spacing):
        out.append(text[i:i+spacing])
    return out

def replace4html(inp):
    text = inp
    if isinstance(text, (str, int, float)):
        text = str(text)
        text.replace("<", "&lt;")
        text.replace(">", "&gt;")
        text = re.compile("\r?\n\r?").sub("<br>", text)
    else:
        for i in range(len(text)):
            text[i] = replace4html(text[i])
    return text

async def remind(timer, user, message:str):
    numb = int(await client.db.nget('other/remindercount', 0))
    await client.db.nset('other/remindercount', str(numb + 1))
    timeend = timer * 1000 + int(time.time() * 1000)
    await client.db.nset(f'reminder/{numb}', json.dumps([user.id, timeend, message]))
    async def send_reminder():
        await asyncio.sleep(timer)
        try:
            await user.send(message)
        except:
            pass
        await client.db.ndel(f'reminder/{numb}')
    asyncio.create_task(send_reminder())
