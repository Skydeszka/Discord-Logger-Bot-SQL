from discord.ext import commands
from discord import Member


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
            await ctx.send(error_message("Member does not exist", ctx.author))

        # Runs if a command has a missing required argument
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(error_message("Required argument missing", ctx.author))
 
        # Runs if an exception hasn't been handled
        else:
            await ctx.send(
                "Unhandled Error:\n"
                "{}\n"
                "||{}||".format(error, ctx.author.mention)
                )


def error_message(message:str, author: Member):
    return "Error:\n{}.\n||{}||".format(message, author.mention)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))