/*=================


ALL TEST CODE HERE


=================*/
const misc = require('/home/runner/kerfus-bot/funcs/misc.js');
const { EmbedBuilder } = require('discord.js');


exports.run = (msg, client) => {
  let pass = 'test123among'
  if(!misc.hastag('admin',msg.author.id))return;
  if(!msg.content.startsWith(pass))return;

  /*
  const exampleEmbed = new EmbedBuilder()
	.setColor(0x0099FF)
	.setTitle('Test')
	.setURL('https://discord.js.org/')
	.setAuthor({ name: msg.author.username + '#' + msg.author.discriminator, iconURL: 'https://cdn.discordapp.com/avatars/'+msg.author.id+'/'+msg.author.avatar+'.webp?size=32'})
	.setDescription('Some description here')
	.setThumbnail('https://i.imgur.com/AfFp7pu.png')
	.addFields(
		{ name: 'Regular field title', value: '</ping:1130506515757936660>' },
		{ name: '\u200B', value: '\u200B' },
		{ name: 'Inline field title', value: 'Some value here', inline: true },
		{ name: 'Inline field title', value: 'Some value here', inline: true },
	)
	.addFields({ name: 'Inline field title', value: 'Some value here', inline: true })
	.setTimestamp()
	.setFooter({ text: 'Some footer text here', iconURL: 'https://i.imgur.com/AfFp7pu.png' });
  msg.channel.send({ embeds: [exampleEmbed] });
  //*/

  
  //setInterval(()=>msg.channel.send('test'),60000)
  //msg.guild.members.fetch();

  /*msg.guild.members.cache.each(member => {
    console.log(member.user.username);
    //member.kick().catch(err=>{})
  })*/
  /*
  setInterval(()=>{
    msg.channel.send(msg.content.split(pass)[1])
  },1000)
  //*/
}