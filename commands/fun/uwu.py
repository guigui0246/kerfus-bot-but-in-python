


"""const { SlashCommandBuilder } = require('discord.js');
const Seed = require("/home/runner/kerfus-bot/funcs/seed.js");

let settings = {
  actions: 0.025,
  faces: 0.05,
  stutters: 0.2
};
settings.faces += settings.actions;
settings.stutters += settings.faces;

function uwuify(inp) {
  const patterns = [
    ["[rlv]", "w"],
    ["th", "f"],
    ["owe", "uv"],
    [":(\\]|\\))", ":3"],
    ["m+e+o+w+", "nyaa~~"],
    ["n([aeiou])", "Ny$1"]
  ];
  const faces = [
    "(・\\`ω\\´・)",
    ";;w;;",
    "OwO",
    "UwU",
    ">w<",
    "^w^",
    "ÚwÚ",
    "^-^",
    ":3",
    "x3"
  ];
  const actions = [
    "*blushes*",
    "*whispers to self*",
    "*cries*",
    "*screams*",
    "*sweats*",
    "*twerks*",
    "*runs away*",
    "*screeches*",
    "*walks away*",
    "*sees bulge*",
    "*looks at you*",
    "*notices buldge*",
    "*starts twerking*",
    "*huggles tightly*",
    "*boops your nose*"
  ];
  const exclamations = ["!?", "?!!", "?!?1", "!!11", "?!?!"];
  let text = inp;
  patterns.forEach(pattern => text = text.replace(new RegExp(pattern[0], "gmi"), pattern[1]))
  text = text.split(' ');
  let out = text[0];
  for (let x of text.slice(1)) {
    out += " ";
    const seed = new Seed(x);
    if (/^(http[s]:\/\/|<@|:[a-zA-Z_\-0-9]+:)/.test(x)) {
      out += x;
      continue;
    }

    rand = seed.random()
    if (rand < settings.faces)
      out += x + " " + faces[seed.randomInt(0, faces.length - 1)];
    else if (rand < settings.actions)
      out += x + " " + actions[seed.randomInt(0, actions.length - 1)];
    else if (rand < settings.stutters)
      out += (x[0] + "-").repeat(seed.randomInt(0, 2)) + x;
    else
      out += x;
  }

  text = out.split(' ')
  out = "";
  text.forEach(x => {
    const seed = new Seed(x);
    out = out + " " + x.replace(/[?!]+$/, exclamations[seed.randomInt(0, exclamations.length - 1)])
  })
  return out;
}

module.exports = {
  data: new SlashCommandBuilder()
    .setName('uwu')
    .setDescription('Uwuifies your message!')
    .addStringOption(option =>
      option.setName('text')
        .setDescription('text to uwuify')
        .setRequired(true)),
  execute(client, interaction) {
    interaction.deferReply().then(() => {
      let uwuified = uwuify(interaction.options.getString('text'));
      if (uwuified.length < 2000) {
        interaction.editReply(uwuified);
        return;
      }
      interaction.editReply(uwuified.slice(0, 2000));
      for (let a of client.misc.sliceby(uwuified, 2000).slice(1)) {
        interaction.followUp(a);
      }
    })
  }
};"""