from discord.ext import commands
from bot import conn, setting_preset

# The maximum amount of LIMIT parameter
__lookback_maxamount:int = conn.execute(
                "SELECT LookbackMax FROM setting WHERE PresetID = ?", (setting_preset,) 
            ).fetchone()[0]


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        global lookback_maxamount
        lookback_maxamount = 100
        print("Functions script ready")


    # Only administrators can use
    # Changes the maximum limit of messages that can be looked back with a message
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def limit(self, ctx, limit: str):
        if limit.isnumeric():
            await ctx.send(_lookback_limit(int(limit)))
        else:
            await ctx.send("Error:\nGiven value not a number\n||{}||".format(ctx.author.mention))


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
        placeholder = "{}```{}.{}({})[{} - {}]\nOrginal: {}\nEdit: {}```\n".format(message, i, row[1], str(row[2]), row[3][:-7], row[4][:-7], row[5], row[6])
        if len(placeholder) <= 2000:
            message = placeholder
            i += 1

    if len(message) == 0:
        return "No records found."
    else:
        return message


# Changes the lookback limit
def _lookback_limit(limit: int):
    limit = 1 if limit <= 1 else limit

    global __lookback_maxamount

    msg = "Update:\n"
    if limit > __lookback_maxamount:
        msg += "Maximum lookback amount increased from {} to {}.".format(__lookback_maxamount, limit)
    elif limit < __lookback_maxamount:
        msg += "Maximum lookback amount decreased from {} to {}.".format(__lookback_maxamount, limit)
    else:
        msg += "Given amount and loopback amount are the same. No changes done."

    __lookback_maxamount = limit

    conn.execute(
        "UPDATE setting SET LookbackMax = ? WHERE PresetID = 4", (int(limit),)
    )

    conn.commit()

    return msg


def lookback():
    return __lookback_maxamount


def setup(bot):
    bot.add_cog(Functions(bot))