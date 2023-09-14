#https://openai.com/dall-e-2
import discord

#Just so you know it was hard to find how to do this correctly, all tutorials are for text commands
@discord.app_commands.command(name="art-gen", description='Generates artwork using the latest AI tech')
@discord.app_commands.describe(prompt="whats the art about", nsfw="Should the art be *spicy*?")
async def art_gen(interaction: discord.Interaction, prompt:str, nsfw:bool):
    await interaction.response.defer()
    await interaction.response.edit_message("https://openai.com/dall-e-2")
