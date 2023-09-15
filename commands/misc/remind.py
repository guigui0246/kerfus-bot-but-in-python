import discord
import re

@discord.app_commands.command(name="remind", description='Reminds you!')
@discord.app_commands.describe(time="time, either XhYmZs or X:Y:Z, unused can be skipped", text='text for the reminder')
async def remind(interaction: discord.Interaction, time:str, text:str="Reminded!"):
    if len(text) > 1000:
        return
    try:
        await interaction.response.send_message(content='will remind you (probably)', ephemeral=True)
    except:
        pass
    message = text
    user = interaction.user
    timestring = time
    time = 0
    if not re.compile("[hms]").search(timestring):
        temp = timestring.split(':')[-3:]
        length = len(temp)
        if (length == 3):
            time += 3600*temp[0]+60*temp[1]+1*temp[2]
        elif (length == 2):
            time += 60*temp[0]+1*temp[1]
        elif (length == 1):
            time += 1*temp[0]
    else:
        if "h" in timestring:
            time+=3600*re.compile("[sm]").split(timestring.split('h')[0])[-1:]
        if "m" in timestring:
            time+=60*re.compile("[sh]").split(timestring.split('m')[0])[-1:]
        if "s" in timestring:
            time+=1*re.compile("[mh]").split(timestring.split('s')[0])[-1:]
    interaction.client.misc.remind(time, user, message)
