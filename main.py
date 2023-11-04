import nextcord
from nextcord.ext import commands
import os
import nextwave

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix='-', intents=intents)
@bot.event
async def on_ready():
    print('deployed')
    bot.loop.create_task(on_node())

async def on_node():
    node: nextwave.Node = await nextwave.NodePool.create_node(host='lavalink.clxud.pro',password="youshallnotpass", bot = bot, port = 2333)

if __name__ == '__main__':
    '''for filename in os.listdir("music"):
        if filename.endswith(".py"):
            bot.load_extension(f"music.{filename[:-3]}")'''
    bot.load_extension(f"music.play")
    bot.load_extension(f"music.joinleave")
    bot.load_extension(f"moderation.mod")

# fun commands that just manipulate the strings in the discord message
@bot.command()
async def hot(ctx, *args):
    string = "🥵".join(args)
    emb = nextcord.Embed(description=string, color=0x00FFFF)
    await ctx.send(embed=emb)

@bot.command()
async def fire(ctx, *args):
    string = "🔥".join(args)
    emb = nextcord.Embed(description=string, color = 0x00FFFF)
    await ctx.send(embed = emb)

@bot.command()
async def mock(ctx, *args):
    original_message = " ".join(args).lower()
    mocking_message = ''

    i = True
    for letter in original_message:
        if i:
            mocking_message += letter.upper()
        else:
            mocking_message += letter
        i = not i
    emb = nextcord.Embed(description=mocking_message, color=0x00FFFF)
    await ctx.send(embed=emb)

bot.run('insert token here')
