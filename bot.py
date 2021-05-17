# Import discord.py modules
import discord
from discord.ext import commands


# Import other modules
import sqlite3
import io
import os


# Read token from token.secret file
# .secret files are inside .gitignore
token = io.open("./database/token.secret", mode="r").read()


# Create bot and give default intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!log ", intents=intents)


# Connect to database
conn = sqlite3.connect("./database/logs.db3")


# Executes function when bot is ready
@bot.event
async def on_ready():
    print("Logger Bot Online")


# Executes function on every message that the bot sees
@bot.event
async def on_message(message):
    add_message(message)


# Executes function on every message edit that the bot sees
@bot.event
async def on_message_edit(before, after):
    add_edit(before, after)


# Functions
def build_database():
    with open(file="./scripts/start.sql", mode="r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()


def add_message(msg: discord.Message):
    conn.execute(
        "INSERT INTO messages VALUES(?, ?, ?, ?)",
        (int(msg.id), str(msg.author), msg.created_at, str(msg.content))
    )

    conn.commit()


def add_edit(bef: discord.Message, aft: discord.Message):
    conn.execute(
        "INSERT INTO edits VALUES(?, ? ,?, ?, ?, ?)",
        (int(aft.id), str(aft.author), bef.created_at, aft.edited_at, str(bef.content), str(aft.content))
    )

    conn.commit()


# Creates database
if __name__ == "__main__":
    try:
        build_database()
    except sqlite3.OperationalError as err:
        print(err)


# Search for cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Starts the bot
bot.run(token)
