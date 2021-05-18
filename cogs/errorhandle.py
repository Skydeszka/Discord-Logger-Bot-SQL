import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Error handler cog ready")

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Error:\nMember does not exist.\n||{}||".format(ctx.author.mention))

def setup(bot):
    bot.add_cog(ErrorHandler(bot))