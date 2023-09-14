import discord
import re
from ...funcs import seed
from ...funcs import misc

settings = {"actions": 0.025, "faces": 0.05, "stutters": 0.2}
settings["faces"] += settings["actions"]
settings["stutters"] += settings["faces"]

def uwuify(inp):
    patterns = [
        ["[rlv]", "w"],
        ["th", "f"],
        ["owe", "uv"],
        [":(\\]|\\))", ":3"],
        ["m+e+o+w", "nyaa~~"],
        ["n([aeiou])", "Ny$1"]
    ]
    faces = [
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
    ]
    actions = [
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
    ]
    exclamations = ["!?", "?!!", "?!?1", "!!11", "?!?!"]
    text = inp
    for e in patterns:
        text = re.compile(e[0], re.I | re.M).sub(text, e[1])
    text = text.split(" ")
    out = text[0]
    for x in text[1:]:
        out += " "
        seedd = seed.Seed(x)
        if (re.compile("^(http[s]:\/\/|<@|:[a-zA-Z_\-0-9]+:)").search(x)):
            out += x
            continue
        rand = seedd.random()
        if (rand < settings["faces"]):
            out += x + " " + faces[seedd.randomInt(0, len(faces) - 1)]
        elif (rand < settings["actions"]):
            out += x + " " + faces[seedd.randomInt(0, len(actions) - 1)]
        elif (rand < settings["stutters"]):
            out += (x[0] + "-") * seedd.randomInt(0, 2) + x
        else:
            out += x

    text = out.split(' ')
    out = ""
    for x in text:
        seedd = seed.Seed(x)
        out = out + " " + re.compile("[?!]+$").sub(x, exclamations[seedd.randomInt(0, exclamations.length - 1)])
    return out

@discord.app_commands.command(name="uwu", description='Uwuifies your message!')
@discord.app_commands.describe(text="text to uwuify")
async def art_gen(interaction: discord.Interaction, text:str):
    await interaction.response.defer()
    uwuified = uwuify(text)
    if (len(uwuified) < 2000):
        await interaction.response.edit_message(uwuified)
        return
    await interaction.response.edit_message(uwuified[0:2000])
    for a in misc.sliceby(uwuified, 2000)[1:]:
        interaction.followup.send(a)
