import discord
import json

@discord.app_commands.command(name="autoremind", description='config the leaf claim autoreminding')
@discord.app_commands.describe(config="-1 for no reminding, otherwise reminds you x seconds before its avaliable (so 0 for no wait time)")
async def autoremind(interaction: discord.Interaction, config:int):
    if config < -1:
        return
    try:
        await interaction.response.send_message('settings changed', ephemeral=True)
    except:
        pass
    sett = json.loads(interaction.client.db.v2getuser("settings", interaction.user.id, str({"autoremind":{"time":300}})))
    sett.autoremind.time = config
    interaction.client.db.v2setuser("settings", interaction.user.id, json.dumps(sett))
