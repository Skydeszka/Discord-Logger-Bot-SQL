import discord
from discord.ext import commands
from datetime import datetime as dt
from bot import conn


# The maximum amount of LIMIT parameter
lookback_maxamount = 100

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands cog ready")


    # Prints last {amount} of messages from a specified user
    @commands.group(invoke_without_command=True, aliases=['message'])
    async def messages(self, ctx, user: discord.Member, amount:int = 10):
        if amount <= lookback_maxamount:
            data = conn.execute(
                "SELECT * FROM messages WHERE AuthorID = ? LIMIT ?", (int(user.id), amount) 
            )

            message = log_to_message(data)

            await ctx.send(message)

    
    # Prints last {amount} of messages between the two given dates
    @messages.command()
    async def between(self, ctx, raw_date1: str, raw_date2: str, amount:int = 10):
        if amount <= lookback_maxamount:
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
            

    # Prints last {amount} of messages between the given dates from a specified user
    @messages.command()
    async def betweenfrom(self, ctx, raw_date1: str, raw_date2: str, user: discord.Member, amount:int = 10):
        if amount <= lookback_maxamount:
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


    # Prints last {amount} of messages which contains the given keyword
    @messages.command()
    async def contains(self, ctx, keyword: str, amount: int = 10):
        if amount <= lookback_maxamount:
            data = conn.execute(
                "SELECT * FROM messages WHERE Content LIKE ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(amount))
            )

            message = log_to_message(data)

            await ctx.send(message)


    # Prints last {amount} of messages which contains the given keyword sent by a specified user
    @messages.command()
    async def containsfrom(self, ctx, keyword: str, user: discord.Member, amount: int = 10):
        if amount <= lookback_maxamount:
            data = conn.execute(
                "SELECT * FROM messages WHERE Content LIKE ? AND AuthorID = ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(user.id), int(amount))
            )

            message = log_to_message(data)

            await ctx.send(message)


    # Prints last {amount} of messages which contains the given keyword between the two given dates
    @messages.command()
    async def containsbetween(self, ctx, keyword: str, raw_date1: str, raw_date2: str, amount: int = 10):
        if amount <= lookback_maxamount:
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


    # Prints last {amount} of messages which contains the given keyword sent by a specified user between the two given dates
    @messages.command()
    async def containsfrombetween(self, ctx, keyword: str, user: discord.Member, raw_date1: str, raw_date2: str, amount: int = 10):
        if amount <= lookback_maxamount:
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


    # Changes the maximum amount of messages that can be looked back at the same time
    @commands.command()
    async def lookbacklimit(self, ctx, limit: int):
        if limit > 1:
            message = "Update:\n"
            pastLimit = lookback_maxamount
            lookback_maxamount = limit
            if pastLimit < lookback_maxamount:
                message += "Lookback limit increased from {} to {}".format(pastLimit, lookback_maxamount)
            elif pastLimit > lookback_maxamount:
                message += "Lookback limit decreased from {} to {}".format(pastLimit, lookback_maxamount)
            else:
                message += "Attention: New limit equals to old limit."

            await ctx.send(message)


# Functions

# Convers the "messages" table data into a sendable text
def log_to_message(data):
    message = ""
    i = 1
    for row in data.fetchall():
        placeholder = "{}`{}.{}({})[{}]: {}`\n".format(message, i, row[1], str(row[2]), row[3][:-7], row[4])
        if len(placeholder) <= 2000:
            message = placeholder
            i += 1

    if len(message) == 0:
        return "No records found."
    else:
        return message


# Convers the "edits" table data into a sendable text
def log_to_edit(data):
    message = ""
    i = 1
    for row in data.fetchall():
        placeholder = "{}```{}.{}({})[{} - {}]\nOrginal: {}\nEdit: {}```\n".format(message, i, row[1], str(row[2]), row[3][:-7], row[4][:-7], row[4], row[5])
        if len(placeholder) <= 2000:
            message = placeholder
            i += 1

    if len(message) == 0:
        return "No records found."
    else:
        return message


def setup(bot):
    bot.add_cog(UserCommands(bot))