from discord.ext import commands

class ErrorHandler(commands.Cog):
    
    # Add bot to the cog
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Error handler cog ready")


    # Function runs on every update
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Error:\nMember does not exist.\n||{}||".format(ctx.author.mention))
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Error:\nRequired argument missing.\n||{}||".format(ctx.author.mention))
        else:
            await ctx.send(
                "Unhandled Error:\n"
                "{}\n"
                "||{}||".format(error, ctx.author.mention)
                )

def setup(bot):
    bot.add_cog(ErrorHandler(bot))