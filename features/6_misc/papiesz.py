import os
import asyncio

async def setup(client):
    channel = await client.channels.fetch('1142562663361155103')
    #print(channel)
    #channel.send('test')
    files = os.listdir('papieszaki')


    async def fun():
        import time
        import math
        import random
        time = time.time() - 1000*(60*(37+16*60))
        date = math.floor(time/(24*60*60*1000))
        #print(time, date)
        newest = 1*client.db.v2get("other/papiesz.txt", f"{date}")
        #print(time, date, newest)
        while (newest < date):
            rand = math.floor(random.random() * len(files))
            print(rand, files[rand])
            await channel.send('https://kerfus-bot.0lie.repl.co/papiesz?file='+files[random])
            newest += 1
        client.db.v2set('other/papiesz.txt',newest)

    async def fun_loop():
        while True:
            await fun()
            await asyncio.sleep(60)
    await fun()
    await fun_loop()
