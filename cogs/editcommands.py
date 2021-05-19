import discord
from discord.ext import commands
from datetime import datetime as dt
from bot import conn
from cogs.functions import lookback_maxamount, log_to_edit



class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Message Commands cog ready")


    # Prints last {amount} of edits from a specified user
    @commands.group(invoke_without_command=True, aliases=["edit"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def edits(self, ctx, user: discord.Member, amount:int = 10):
        if amount <= lookback_maxamount:
            data = conn.execute(
                "SELECT * FROM edits WHERE AuthorID = ? LIMIT ?", (int(user.id), amount) 
            )

            message = log_to_edit(data)

            await ctx.send(message)


    # Prints last {amount} of edits between the two given dates
    @edits.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def between(self, ctx, raw_date1: str, raw_date2: str, amount:int = 10):
        if amount <= lookback_maxamount:
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM edits WHERE DateOfEdit BETWEEN ? AND ? ORDER BY DateOfEdit",
                    (date1, date2)
                )

                message = log_to_edit(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")


    # Prints last {amount} of edits between the given dates from a specified user
    @edits.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def betweenfrom(self, ctx, raw_date1: str, raw_date2: str, user: discord.Member, amount:int = 10):
        if amount <= lookback_maxamount:
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM edits WHERE AuthorID = ? AND DateOfEdit BETWEEN ? AND ? ORDER BY DateOfEdit",
                    (int(user.id), date1, date2)
                )

                message = log_to_edit(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")


    # Prints last {amount} of edits which contains the given keyword
    @edits.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def contains(self, ctx, keyword: str, amount: int = 10):
        if amount <= lookback_maxamount:
            data = conn.execute(
                "SELECT * FROM edits WHERE Content LIKE ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(amount))
            )

            message = log_to_edit(data)

            await ctx.send(message)


    # Prints last {amount} of edits which contains the given keyword sent by a specified user
    @edits.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def containsfrom(self, ctx, keyword: str, user: discord.Member, amount: int = 10):
        if amount <= lookback_maxamount:
            data = conn.execute(
                "SELECT * FROM edits WHERE Content LIKE ? AND AuthorID = ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(user.id), int(amount))
            )

            message = log_to_edit(data)

            await ctx.send(message)


    # Prints last {amount} of edits which contains the given keyword between the two given dates
    @edits.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def containsbetween(self, ctx, keyword: str, raw_date1: str, raw_date2: str, amount: int = 10):
        if amount <= lookback_maxamount:
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM edits WHERE Content LIKE ? AND DateOfEdit BETWEEN ? AND ? ORDER BY DateOfEdit",
                    ('%{}%'.format(str(keyword)), date1, date2)
                )

                message = log_to_edit(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")


    # Prints last {amount} of edits which contains the given keyword sent by a specified user between the two given dates
    @edits.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def containsfrombetween(self, ctx, keyword: str, user: discord.Member, raw_date1: str, raw_date2: str, amount: int = 10):
        if amount <= lookback_maxamount:
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM edits WHERE AuthorID = ? AND Content LIKE ? AND DateOfEdit BETWEEN ? AND ? ORDER BY DateOfEdit LIMIT ?",
                    (int(user.id), '%{}%'.format(str(keyword)), date1, date2, int(amount))
                )

                message = log_to_edit(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")


# Functions


def setup(bot):
    bot.add_cog(MessageCommands(bot))