import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_ready():
        print("Commands cog ready")


def setup(bot):
    bot.add_cog(Commands(bot))