from discord.ext import commands

class ErrorHandler(commands.Cog):
    
    # Add bot to the cog
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Error handler script ready")


    # Function runs on every exception
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Runs if a non existing member is used
        if isinstance(error, commands.errors.MemberNotFound):
            await ctx.send("Error:\nMember does not exist.\n||{}||".format(ctx.author.mention))

        # Runs if a command has a missing required argument
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Error:\nRequired argument missing.\n||{}||".format(ctx.author.mention))

        # Runs if an exception hasn't been handled
        else:
            await ctx.send(
                "Unhandled Error:\n"
                "{}\n"
                "||{}||".format(error, ctx.author.mention)
                )


def setup(bot):
    bot.add_cog(ErrorHandler(bot))