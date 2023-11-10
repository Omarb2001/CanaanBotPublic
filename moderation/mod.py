import nextcord
from nextcord.ext import commands
import datetime

class CogMod(commands.Cog): #class for all moderation commands
    def __init__(self,bot: commands): self.bot = bot
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Function that will gracefully handle the various errors we might encounter when using a command
        emb = nextcord.Embed(title='ERROR', description=f'{error}', color=0x00FFFF)
        await ctx.send(embed=emb)


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: nextcord.Member, *, reason=None):
        #kick a member of the server
        #format: -kick {ping user or user id}
        emb = None
        if ctx.author.id == member.id:
            emb = nextcord.Embed(title='ERROR', description='You can\'t kick yourself!', color=0x00FFFF)
            await ctx.send(embed=emb)
            return

        if reason is None:
            reason = 'No reason specified'
        if member in ctx.guild.members:
            await member.kick(reason=reason)
            emb = nextcord.Embed(title=f'User `{member}` has been kicked!',description=f'Reason: {reason}', color=0x00FFFF)
        else:
            emb = nextcord.Embed(title=f'User `{member}` not in guild.', color=0x00FFFF)

        await ctx.send(embed=emb)


    @staticmethod
    async def is_banned(guild: commands.Context.guild, user:nextcord.User):
        #check if user is banned. Supplementary function for the ban and unban commands
        try:
            entry = await guild.fetch_ban(user)
        except:
            return False
        return True


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, user: nextcord.User, *, reason=None):
        #bans a user (works whether they're in the server or not)
        #format: -ban {ping user or user id}
        emb = None

        if ctx.author.id == user.id:
            emb = nextcord.Embed(title='ERROR', description='You can\'t ban yourself!', color=0x00FFFF)
            await ctx.send(embed=emb)
            return
        if reason is None:
            reason = 'No reason specified'

        emb = None

        if CogMod.is_banned(ctx.guild, user):
            emb = nextcord.Embed(title=f'User {user} has already been banned!', description=f'Reason: {reason}', color=0x00FFFF)
        else:
            await ctx.guild.ban(user)
            emb = nextcord.Embed(title=f'User {user} has been banned!', color=0x00FFFF)

        await user.send(f'you have been banned from {ctx.guild.name}')
        await ctx.send(embed=emb)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: nextcord.User, *args):
        #unban a user
        #format: -unban {user id}
        emb = None
        if ctx.author.id == user.id:
            emb = nextcord.Embed(title='ERROR', description='You can\'t unban yourself!', color=0x00FFFF)
            await ctx.send(embed=emb)
            return

        if CogMod.is_banned(ctx.guild, user):
            await ctx.guild.unban(user)
            emb = nextcord.Embed(title=f'User {user} has been unbanned!',color=0x00FFFF)
        else:
            await ctx.guild.ban(user)
            emb = nextcord.Embed(title=f'User {user} is not banned!', color=0x00FFFF)

        await ctx.send(embed=emb)


    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx: commands.Context, member: nextcord.Member, time='10', *, reason=None):
        #mute a user
        #format: -mute {number}d(ays)/m(minutes)/h(ours) (default is minutes)
        #example: mute @user 2d mutes for two days, mute @user 2 mutes for 2 minutes
        #if time not mentioned, default to 10 minutes
        emb = None
        time_desc = None
        if ctx.author.id == member.id:
            emb = nextcord.Embed(title='ERROR', description='You can\'t mute yourself!', color=0x00FFFF)
            await ctx.send(embed=emb)
            return

        if 'd' in time:
            time = time.replace('d', '')
            duration = datetime.timedelta(days=int(time))
            time_desc = f'{time} days'
        elif 'm' in time:
            time = time.replace('m', '')
            duration = datetime.timedelta(minutes=int(time))
            time_desc = f'{time} minutes'
        elif 'h' in time:
            time = time.replace('h', '')
            duration = datetime.timedelta(hours=int(time))
            time_desc = f'{time} hours'
        elif time.isnumeric():
            duration = datetime.timedelta(minutes=int(time))
            time_desc = f'Duration: {time} minutes'
        else:
            emb = nextcord.Embed(title='ERROR', description='Invalid time format')
            await ctx.send(embed=emb)
            return

        await member.timeout(duration)
        emb = nextcord.Embed(title=f'member {member} was muted!', description=time_desc)
        await ctx.send(embed=emb)


    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx: commands.Context, member: nextcord.Member, *, reason=None):
        #unmute a user
        #format:-unmute {ping user or id}
        emb = None
        if ctx.author.id == member.id:
            emb = nextcord.Embed(title='ERROR', description='You can\'t unmute yourself!', color=0x00FFFF)
            await ctx.send(embed=emb)
            return

        muted = member.communication_disabled_until

        if muted is not None:
            await member.timeout(None)
            emb = nextcord.Embed(title=f'{member} has been unmuted!', color=0x00FFFF)
        else:
            emb = nextcord.Embed(title=f'{member} is not muted!', color=0x00FFFF)
        await ctx.send(embed=emb)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, member: nextcord.Member, *args):
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
    async def removerole(self, ctx: commands.Context, member: nextcord.Member, *args):
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

        await ctx.send(embed=emb)







def setup(bot):
    bot.add_cog(CogMod(bot))