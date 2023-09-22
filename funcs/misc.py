from typing import Any
from typing import SupportsIndex
import json
import time
import asyncio
import re

def setup (a) -> dict[str, Any]:
    "Setup of a client"
    global client
    client = a
    n = 1*client.db.v2get('other/remindercount')
    reminders = []
    loop = asyncio.get_event_loop()
    async def process_reminder(client, x):
        temp = await client.db.v2get(f"reminder/{x}")
        if temp:
            reminder_data = json.loads(temp)
            reminders.append(reminder_data)
            await asyncio.sleep((reminder_data[1] - (int(time.time() * 1000))) / 1000)
            user = await client.fetch_user(reminder_data[0])
            try:
                await user.send(reminder_data[2])
            except:
                pass
            await client.db.v2del(f"reminder/{reminder_data[3]}")
    for x in range(400, n):
        loop.create_task(process_reminder(client, x))
    loop.run_forever()
    return globals()

def test():
    "I still don't know why 0lie put that"
    return

def addhtmls(data, document) -> str:
    "Add data to a html"
    with open("web/generic.html") as file:
        gen = file.read()
    doc = str(document).split("##")
    out = gen.replace("#DATA#",json.dumps(data))
    for x in range(0, len(doc), 2):
        out = out.replace(f"#{doc[x]}#", doc[x+1])
    return out

def hashtag (tag:SupportsIndex, id:SupportsIndex) -> bool:
    "Look is an id as a tag"
    with open("data/tags.json", encoding="utf-8") as file:
        tagged:list[list] = json.load(file)
    if not tag in tagged:
        return False
    return id in tagged[tag]

def addtag(tag:SupportsIndex, id:SupportsIndex):
    "Add a tag to an id"
    with open("data/tags.json", encoding="utf-8") as file:
        tagged:list[list] = json.load(file)
    if tag in tagged:
        if not id in tagged[tag]:
            tagged[tag].append(id)
    else:
        tagged[tag] = [id]
    with open("data/tags.json", "w", encoding="utf-8") as file:
        json.dump(tagged, file)

def removetag(tag:SupportsIndex, id:SupportsIndex):
    "Remove a tag from an id"
    with open("data/tags.json", encoding="utf-8") as file:
        tagged:list[list] = json.load(file)
    if tag in tagged:
        if id in tagged[tag]:
            tagged[tag].remove(id)
            with open("data/tags.json", "w", encoding="utf-8") as file:
                json.dump(tagged, file)

def log(text:str, filepath:str="logs.txt"):
    "log a text to a file"
    with open(filepath, "a") as file:
        file.write(text.replace("\n", " ") + "\n")

def polishchars(text:str) -> str:
    """Change strange char to other char\n
    Only affects : ęóąśłżźćń
    not ç or á because 0lie decided that"""
    copy = text
    polish = "ęóąśłżźćń"
    fixed = "eoaslzzcn"
    for i in range(len(fixed)):
        copy = copy.replace(polish[i], fixed[i])
    return copy

def sliceby (text:str, spacing:SupportsIndex) -> list:
    "Cut a string using a specific spacing"
    out = []
    for i in range(0, len(text), spacing):
        out.append(text[i:i+spacing])
    return out

def replace4html(inp):
    "Replace char for a string to be addapted to html"
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
    "Make a reminder after a certain time for a specific client"
    numb = int(await client.db.v2get('other/remindercount', 0))
    await client.db.v2set('other/remindercount', str(numb + 1))
    timeend = timer * 1000 + int(time.time() * 1000)
    await client.db.v2set(f'reminder/{numb}', json.dumps([user.id, f"{timeend}", message]))
    async def send_reminder():
        await asyncio.sleep(float(timer))
        try:
            await user.send(message)
        except:
            pass
        await client.db.v2del(f'reminder/{numb}')
    asyncio.create_task(send_reminder())
