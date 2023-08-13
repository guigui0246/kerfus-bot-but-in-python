const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('autoremind')
		.setDescription('config the leaf claim autoreminding')
    .addIntegerOption(option =>
		  option.setName('config')
			.setDescription('-1 for no reminding, otherwise reminds you x seconds before its avaliable (so 0 for no wait time)')
      .setMinValue(-1)
      .setRequired(true)),
	execute(client, interaction) {
	  interaction.reply({ content: 'settings changed', ephemeral: true }).catch(e=>{})
    let config = interaction.options.getInteger('config');
    let sett = JSON.parse(client.db.v2getuser('settings',interaction.user.id,'{"autoremind":{"time":300}}'));
    sett.autoremind.time = config;
    client.db.v2setuser('settings',interaction.user.id,JSON.stringify(sett));
  }
};