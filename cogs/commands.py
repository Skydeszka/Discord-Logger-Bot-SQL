import discord
from discord import message
from discord.ext import commands
from datetime import datetime as dt
from bot import conn

lookback_maxamount = 100

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands cog ready")


    @commands.group(invoke_without_command=True, aliases=['message'])
    async def messages(self, ctx, user: discord.Member, amount:int = 10):
        if amount <= lookback_maxamount:
            add_fetch(ctx, "Message")
            data = conn.execute(
                "SELECT * FROM messages WHERE Author = ? LIMIT ?", (str(user), amount) 
            )

            message = log_to_message(data)

            await ctx.send(message)

    
    @messages.command()
    async def between(self, ctx, raw_date1: str, raw_date2: str, amount:int = 10):
        if amount <= lookback_maxamount:
            add_fetch(ctx, "Message")
            date1 = dt.strptime(raw_date1, "%y/%m/%d %H:%M:%S")
            date2 = dt.strptime(raw_date2, "%y/%m/%d %H:%M:%S")
            data = conn.execute(
                "SELECT * FROM messages WHERE DateOfMessage BETWEEN ? AND ? ORDER BY DateOfMessage",
                (date1, date2)
            )

            message = log_to_message(data)

            await ctx.send(message)
            

    @messages.command()
    async def contains(self, ctx, keyword: str, amount: int = 10):
        if amount <= lookback_maxamount:
            add_fetch(ctx, "Message")
            data = conn.execute(
                "SELECT * FROM messages WHERE Content LIKE ? LIMIT ?",
                ('%{}%'.format(str(keyword)), int(amount))
            )

            message = log_to_message(data)

            await ctx.send(message)


def log_to_message(data):
    message = ""
    i = 1
    for row in data.fetchall():
        placeholder = "{}\n`{}.{}[{}]: {}`".format(message, i, row[1], row[2][:-7], row[3])
        if len(placeholder) <= 2000:
            message = placeholder
            i += 1
    return message


def add_fetch(ctx, type):
    conn.execute(
        "INSERT INTO logfetches(FetchDate, Author, FetchType) VALUES(?, ?, ?)",
        (ctx.message.created_at, str(ctx.author), str(type))
    )

    conn.commit()


def setup(bot):
    bot.add_cog(UserCommands(bot))