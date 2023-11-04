import nextcord
from nextcord.ext import commands
import datetime

class CogMod(commands.Cog):
    def __init__(self,bot: commands):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        #kick a member of the server
        #format: -kick {ping user or user id}

        emb =  None
        if reason is None:
            reason = 'No reason specified'
        if member in ctx.guild.members:
            await member.kick(reason=reason)
            emb = nextcord.Embed(title=f'User {member} has been kicked!',description=f'Reason: {reason}', color=0x00FFFF)
        else:
            emb = nextcord.Embed(title=f'User {member} not in guild.', color=0x00FFFF)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: nextcord.User, *, reason=None):
        #bans a user (works whether they're in the server or not)
        #format: -ban {ping user or user id}


        emb = None
        if reason is None:
            reason = 'No reason specified'
        if user:
            await user.name.
            emb = nextcord.Embed(title=f'User {user} has been banned!',description=f'Reason: {reason}', color=0x00FFFF)
        else:
            emb = nextcord.Embed(description=f'User {user} doesn\'t exist.', color=0x00FFFF)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: nextcord.Member, *args):
        #unban a user
        #format: -unban {user id}

        emb = None
        await member.unban()
        await ctx.send(f'User {member} has been unbanned.')

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: nextcord.Member, time, *, reason=None):
        #mute a user
        #format: -mute {number}d(ays)/m(minutes)/h(ours) (default is minutes)
        #example: mute @user 2d mutes for two days, mute @user 2 mutes for 2 minutes
        if 'd' in time:
            time = time.replace('d', '')
            duration = datetime.timedelta(days=int(time))
        elif 'm' in time:
            time = time.replace('m', '')
            duration = datetime.timedelta(minutes=int(time))
        elif 'h' in time:
            time = time.replace('h', '')
            duration = datetime.timedelta(hours=int(time))
        elif time.isnumeric():
            duration = datetime.timedelta(minutes=int(time))
        else:
            ctx.send('invalid')
            return

        await member.timeout(duration)
        await ctx.send(f'User {member} has been muted.')

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: nextcord.Member, *, reason=None):
        #unmute a user
        #format:-unmute {ping user or id}
        await member.timeout(None)
        await ctx.send(f'User {member} has been unmuted.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: nextcord.Member, *args):
        role = ' '.join(args)
        role = nextcord.utils.get(ctx.guild.roles, name=role)
        emb = None
        if role is not None:
            if role not in member.roles:
                await member.add_roles(role)
                emb = nextcord.Embed(description=f'{member.name} was given role `{role}`!', color=0x00FFFF)
            else:
                await member.add_roles(role)
                emb = nextcord.Embed(description=f'{member.name} already has role `{role}`!', color=0x00FFFF)
        else:
            emb = nextcord.Embed(description=f'role `{role}` doesn\'t exist!', color=0x00FFFF)

        await ctx.send(embed=emb)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: nextcord.Member, *args):
        #removes a role from user
        #format: -removerole {ping user or id} {name of role}
        role = ' '.join(args)
        role = nextcord.utils.get(ctx.guild.roles, name=role)
        emb = None
        if role is not None:
            if role not in member.roles:
                await member.remove_roles(role)
                emb = nextcord.Embed(description=f'{member.name} already doesn\'t have role `{role}`!', color=0x00FFFF)
            else:
                await member.remove_roles(role)
                emb = nextcord.Embed(description=f'Removed role `{role}` from {member.name}!', color=0x00FFFF)

        else:
            emb = nextcord.Embed(description=f'role `{role}` doesn\'t exist!', color=0x00FFFF)

        await ctx.send(embed = emb)

def setup(bot):
    bot.add_cog(CogMod(bot))