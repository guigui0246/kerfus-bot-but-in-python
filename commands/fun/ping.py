import discord

@discord.app_commands.command(name="ping", description='Replies with Pong!')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')
