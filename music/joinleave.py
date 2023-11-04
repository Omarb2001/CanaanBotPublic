import nextwave
from nextcord.ext import commands

'''commands for bot to join/leave a vc'''

class CogJoinLeave(commands.Cog):
    def __init__(self,bot: commands):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.author.voice.channel
        except:
            await ctx.send('User required to join a voice before issuing this command')
            return
        try:
            if ctx.guild.voice_client:
                await nextwave.Player.disconnect(ctx.guild.voice_client)
            vc: nextwave.Player = await channel.connect(cls=nextwave.Player)
        except:
            await ctx.send('Already in vc!')



    @commands.command()
    async def superleave(self, ctx):
        try:
            await nextwave.Player.disconnect(ctx.guild.voice_client)
        except:
            await ctx.send('not currently in a vc')

    @commands.command()
    async def leave(self, ctx):
        try:
            channel = ctx.author.voice.channel
        except:
            await ctx.send('User not in vc.')
            return
        if (
            (self.bot.user.id in ctx.author.voice.channel.voice_states) and
            (ctx.author.id in ctx.author.voice.channel.voice_states)
            ):
            await nextwave.Player.disconnect(ctx.guild.voice_client)
        else:
            await ctx.send('User and bot are not in the same vc.')
            return



def setup(bot):
    bot.add_cog(CogJoinLeave(bot))