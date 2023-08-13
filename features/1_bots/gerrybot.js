exports.run = (msg, client) => {
  return;
  const collectorFilter = (reaction, user) => {
    console.log(reaction,"abc",user);
	  return reaction.emoji.name == "gerald" && user.id === "1120441619720699905";
  };
  //console.log(msg)
  msg.awaitReactions({
      filter:collectorFilter,
      max: 1,
      time: 60000,
      errors:["time"]
  })
  .then(col=>{
    console.log(col);
    col.first().remove();
  })
  .catch(col=>{})
}