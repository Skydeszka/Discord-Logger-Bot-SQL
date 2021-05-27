# Import discord.py modules
import discord
from discord.ext import commands


# Import other modules
import sqlite3
import io
import os
from datetime import datetime as dt
from time import time


# Read token from token.secret file
# .secret files are inside .gitignore
token = None
try:
    token = io.open("./database/token.secret", mode="r").read()
except FileNotFoundError:
    print(
        "New error encountered: FileNotFound\n\tdatabase/token.secret\tnot found."
        "\nTo fix this error create a token.secret file with the token of the Discord bot inside it."
        )


# Create bot and give default intents
bot = commands.Bot(command_prefix="!log.")


# Connect to database
conn = sqlite3.connect("./database/logs.db3")


# Settings preset ID
# Change source to change preset
# Base presets:
#   1 - normal  - 100   lookback
#   2 - extreme - 1000  lookback
#   3 - low     - 10    lookback
#   4 - custom  - can be changed with !log.limit <limit> command
#!!CHANGING THE VALUE BESIDE THESE WILL CAUSE AN EXCEPTION!!
setting_preset = 4


# Executes function when bot is ready
@bot.event
async def on_ready():
    print("Logger Bot Online")


# Executes function on every message that the bot sees
@bot.event
async def on_message(message):
    if not message.author.bot:
        add_message(message)
    await bot.process_commands(message)


# Executes function on every message edit that the bot sees
@bot.event
async def on_message_edit(before, after):
    if not after.author.bot:
        add_edit(before, after)
    await bot.process_commands(after)


# Saves database, can be done by Administrator permission
@bot.command()
@commands.has_permissions(administrator = True)
async def commit(ctx):
    await ctx.send("Committing database...")

    conn.commit()

    await ctx.send("Commit complete")


# Functions
def build_database():
    with open(file="./scripts/start.sql", mode="r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()


def add_message(msg: discord.Message):
    conn.execute(
        "INSERT INTO messages VALUES(?, ?, ?, ?, ?, ?)",
        (
            str(msg.id),
            str(msg.author.name),
            str(msg.author.id),
            date_utc_to_local(msg.created_at),
            str(msg.content.replace("`", "")),
            str(msg.channel.id)
        )
    )

    conn.commit()


def add_edit(bef: discord.Message, aft: discord.Message):
    conn.execute(
        "INSERT INTO edits VALUES(?, ? ,?, ?, ?, ?, ?, ?)",
        (
            str(aft.id),
            str(aft.author.name),
            str(aft.author.id),
            date_utc_to_local(bef.created_at), date_utc_to_local(aft.edited_at),
            str(bef.content.replace("`", "")), str(aft.content.replace("`", "")),
            str(aft.channel.id)
        )
    )

    conn.commit()


def date_utc_to_local(utc_datetime):
    now_timestamp = time()
    offset = dt.fromtimestamp(now_timestamp) - dt.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


# Creates database
if __name__ == "__main__":
    try:
        build_database()
    except sqlite3.OperationalError as err:
        print(err)


# Starts the bot and loads cogs
if token is not None:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

    bot.run(token)
else:
    input("Press anything to continue")
