# Import discord.py modules
import discord
from discord import message
from discord.ext import commands


# Import other modules
import sqlite3
import io
import os


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


# Functions
def build_database():
    with open(file="./scripts/start.sql", mode="r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()


def add_message(msg: discord.Message):
    conn.execute(
        "INSERT INTO messages VALUES(?, ?, ?, ?, ?)",
        (int(msg.id), str(msg.author), int(msg.author.id), msg.created_at, str(msg.content))
    )

    conn.commit()


def add_edit(bef: discord.Message, aft: discord.Message):
    conn.execute(
        "INSERT INTO edits VALUES(?, ? ,?, ?, ?, ?, ?)",
        (int(aft.id), str(aft.author), int(aft.author.id), bef.created_at, aft.edited_at, str(bef.content), str(aft.content))
    )

    conn.commit()


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
