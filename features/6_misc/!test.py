"""=================


ALL TEST CODE HERE


================="""

from ...funcs import misc
import discord

def run(msg, client):
    "test run"
    _pass = "test123among"
    if not misc.hashtag('admin',msg.author.id):
        return
    if not msg.content.startswith(_pass):
        return
    

    """
    exampleEmbed = discord.embeds.Embed(color=0x0099FF, title='Test', url='https://discord.js.org/', description='Some description here')
    exampleEmbed.set_author(name= msg.author.username + '#' + msg.author.discriminator, icon_url= 'https://cdn.discordapp.com/avatars/'+msg.author.id+'/'+msg.author.avatar+'.webp?size=32')
    exampleEmbed.set_thumbnail('https://i.imgur.com/AfFp7pu.png')
    exampleEmbed.add_field(**{"name":'Regular field title', "value":'</ping:1130506515757936660>'}).add_field(**{"name":'\u200B', "value":'\u200B'}).add_field(**{"name":'Inline field title', "value":'Some value here', "inline":True}).add_field(**{"name":'Inline field title', "value":'Some value here', "inline":True})
    exampleEmbed.add_field(**{"name": 'Inline field title', "value": 'Some value here', "inline": True })
    exampleEmbed.set_footer(**{"text": 'Some footer text here', "iconURL": 'https://i.imgur.com/AfFp7pu.png'})
    msg.channel.send({"embeds":[exampleEmbed]})
    """

    #async def send():
    #    import asyncio
    #    while True:
    #        await msg.channel.send("test")
    #        await asyncio.sleep(60)
    #send()
    #del send
    #msg.guild.members.fetch()

    """for member in msg.guild.members.cache:
        print(member.user.username)
        #try:
        #    member.kick()
        #except:
        #    pass
    """
    """
    async def send():
        import asyncio
        while True:
            await msg.channel.send(msg.content.split(_pass)[1])
            await asyncio.sleep(1)
    send()
    del send
    """
