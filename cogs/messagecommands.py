import discord
from discord.ext import commands
from datetime import datetime as dt
from bot import conn
from cogs.functions import log_to_message, lookback


class MessageCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Message commands script ready")


    # Prints last {amount} of messages from a specified user
    @commands.group(invoke_without_command=True, aliases=['message'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def messages(self, ctx, user: discord.Member, amount:int = 10):
        if amount <= lookback():
            data = conn.execute(
                "SELECT * FROM messages WHERE AuthorID = ? LIMIT ?", (int(user.id), amount) 
            )

            message = log_to_message(data)

            await ctx.send(message)
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))

    
    # Prints last {amount} of messages between the two given dates
    @messages.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def between(self, ctx, raw_date1: str, raw_date2: str, amount:int = 10):
        if amount <= lookback():
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM messages WHERE DateOfMessage BETWEEN ? AND ? ORDER BY DateOfMessage",
                    (date1, date2)
                )

                message = log_to_message(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))
            

    # Prints last {amount} of messages between the given dates from a specified user
    @messages.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def betweenfrom(self, ctx, raw_date1: str, raw_date2: str, user: discord.Member, amount:int = 10):
        if amount <= lookback():
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM messages WHERE AuthorID = ? AND DateOfMessage BETWEEN ? AND ? ORDER BY DateOfMessage",
                    (int(user.id), date1, date2)
                )

                message = log_to_message(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))


    # Prints last {amount} of messages which contains the given keyword
    @messages.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def contains(self, ctx, keyword: str, amount: int = 10):
        if amount <= lookback():
            data = conn.execute(
                "SELECT * FROM messages WHERE Content LIKE ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(amount))
            )

            message = log_to_message(data)

            await ctx.send(message)
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))


    # Prints last {amount} of messages which contains the given keyword sent by a specified user
    @messages.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def containsfrom(self, ctx, keyword: str, user: discord.Member, amount: int = 10):
        if amount <= lookback():
            data = conn.execute(
                "SELECT * FROM messages WHERE Content LIKE ? AND AuthorID = ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(user.id), int(amount))
            )

            message = log_to_message(data)

            await ctx.send(message)
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))


    # Prints last {amount} of messages which contains the given keyword between the two given dates
    @messages.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def containsbetween(self, ctx, keyword: str, raw_date1: str, raw_date2: str, amount: int = 10):
        if amount <= lookback():
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM messages WHERE Content LIKE ? AND DateOfMessage BETWEEN ? AND ? ORDER BY DateOfMessage",
                    ('%{}%'.format(str(keyword)), date1, date2)
                )

                message = log_to_message(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))


    # Prints last {amount} of messages which contains the given keyword sent by a specified user between the two given dates
    @messages.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages = True)
    async def containsfrombetween(self, ctx, keyword: str, user: discord.Member, raw_date1: str, raw_date2: str, amount: int = 10):
        if amount <= lookback():
            try:
                date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
                date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
                data = conn.execute(
                    "SELECT * FROM messages WHERE AuthorID = ? AND Content LIKE ? AND DateOfMessage BETWEEN ? AND ? ORDER BY DateOfMessage LIMIT ?",
                    (int(user.id), '%{}%'.format(str(keyword)), date1, date2, int(amount))
                )

                message = log_to_message(data)

                await ctx.send(message)
            except ValueError:
                await ctx.send("Invalid date type.\nCorrect type: YY/MM/DD HH:MM:SS")
        else:
            await ctx.send("Error:\nMaximum lookback amount ({}) exceeded".format(lookback()))


def setup(bot):
    bot.add_cog(MessageCommands(bot))