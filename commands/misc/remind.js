const { SlashCommandBuilder } = require('discord.js');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('remind')
		.setDescription('Reminds you!')
    .addStringOption(option =>
		  option.setName('time')
			.setDescription('time, either XhYmZs or X:Y:Z, unused can be skipped')
      .setRequired(true))
    .addStringOption(option =>
		  option.setName('text')
			.setDescription('text for the reminder')
      .setMaxLength(1000)
      .setRequired(false)),
	execute(client, interaction) {
	  interaction.reply({ content: 'will remind you (probably)', ephemeral: true }).catch(e=>{})
    let message = interaction.options.getString('text') ?? "Reminded!";
    let user = interaction.member;
    let timestring = interaction.options.getString('time');
    let time = 0;
    let temp;
    if(!/[hms]/.test(timestring)){  
      temp = timestring.split(':').slice(-3)
      let len =temp.length
      if(len==3)time+=3600*temp[0]+60*temp[1]+1*temp[2];
      else if(len==2)time+=60*temp[0]+1*temp[1];
      else if(len==1)time += 1*temp[0];
    }
    else{
      if(timestring.includes('h'))
        time+=3600*timestring.split('h')[0].split(/[sm]/).slice(-1);
      if(timestring.includes('m'))
        time+=60*timestring.split('m')[0].split(/[sh]/).slice(-1);
      if(timestring.includes('s'))
        time+=1*timestring.split('s')[0].split(/[mh]/).slice(-1);
    }
    client.misc.remind(time,user,message)
  }
};