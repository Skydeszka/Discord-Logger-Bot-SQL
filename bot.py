# Imoprt Discord.py modules
import discord
from discord.ext import commands
import sqlite3

# Import IO for working with files
import io
from datetime import date, datetime as dt

# Read token from token.secret file
# .secret files are inside .gitignore
token = io.open("./database/token.secret", mode="r").read()

# Create bot and give default intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!log", intents=intents)


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
    pass


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


# Creates database
if __name__ == "__main__":
    try:
        build_database()
    except sqlite3.OperationalError as err:
        print(err)


# Starts the bot
bot.run(token)
