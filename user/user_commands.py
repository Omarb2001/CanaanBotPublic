import nextcord
from nextcord.ext import commands
import re
import datetime

class CogUser(commands.Cog): #class for all user commands
    def __init__(self,bot: commands): self.bot = bot
    '''@commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        #Function that will gracefully handle the various errors we might encounter when using a command
        #error will be sent to console (discord chat)
        emb = nextcord.Embed(title='ERROR', description=f'{error}', color=0x00FFFF)
        await ctx.send(embed=emb)'''

    @commands.command()
    async def avatar(self, ctx: commands.Context, member: nextcord.Member = None):
        #shows the specified user's avatar/pfp, if no member mentioned, the author's avatar is shown
        #format: -avatar user, or just -avatar for yourself
        emb = nextcord.Embed(color=0x00FFFF, title='Avatar')
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        if member is None:
            avatar = ctx.author.avatar
            emb.set_image(avatar)
        else:
            avatar = member.avatar
            emb.set_image(avatar)

        await ctx.send(embed=emb)

    @staticmethod
    async def checkregex(pll: str):
        #supplementary function to poll
        #makes sure that the poll is in the correct format, using regex
        #format: basically as there are at least 2 statements and at least the second one onwards must be enclosed in parentheses
        #if correct format, process into a question and options list
        newstring = re.search(r'^(\w|\W)+("(\w|\W)+")', pll).string
        options = []
        question = None
        if newstring == pll:
            temp = re.search(r'\s+"(\w|\W)+"(\w|\W)+$', pll).string
            options = temp.split('"')
            for i in range(0, len(options)):
                options[i] = options[i].strip()
            while '' in options:
                options.remove('')
            question = options[0]
            options.remove(options[0])
            print(question, options)
            return True, question, options
        return False, None, None


    @commands.command(pass_context=True)
    async def poll(self, ctx: commands.Context, *, pll: str):
        #command to make an interactive poll
        #based on user-given question and answew-options
        #each option is represented by a clickable reaction to the poll
        #format: -poll question "option1" "option2"...
        #limited to 10 options
        emb = None
        pll = pll.strip()

        result, question, options = await CogUser.checkregex(pll=pll)
        if not result:
            emb = nextcord.Embed(color=0x00FFFF, description='Wrong format!', title='ERROR')
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=emb)
            return

        if len(options) < 2 or len(options) > 10:
            emb = nextcord.Embed(color=0x00FFFF, description='You can only have between 2-9 options!', title= 'ERROR')
            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            await ctx.send(embed=emb)
            return

        description = []
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for x, option in enumerate(options):
            description += '\n{} {}\n'.format(reactions[x], option)

        emb = nextcord.Embed(title=question, description=''.join(description), color=0x00FFFF)
        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        react_message = await ctx.send(embed=emb)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)



def setup(bot):
    bot.add_cog(CogUser(bot))