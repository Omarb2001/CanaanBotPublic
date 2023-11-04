import nextwave
from nextwave.ext import spotify
import nextcord
from nextcord.ext import commands
'''music commands implemented using the nexwave module,
which is a music wrap for the nextcord module, which is based on the discord.py API'''
'''only works with youtube so far'''


async def ytsearch(self, ctx, args):
    '''search for link on YouTube (default)'''
    query = nextwave.YouTubeTrack.search(args, return_first= True)


class CogPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def play(self, ctx, *args):
       if args is None: return

       await ctx.send("playing")
def setup(bot):
    bot.add_cog(CogPlay(bot))

