from discord.ext import commands

# The maximum amount of LIMIT parameter
lookback_maxamount = 100


class Functions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Functions script ready")


    # Only administrators can use
    # Changes the maximum limit of messages that can be looked back with a message
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def limit(self, ctx, limit:int):
        await ctx.send(lookback_limit(limit, ctx))


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
def lookback_limit(limit: int):
    limit = 1 if limit <= 1 else limit

    msg = "Update:\n"
    if limit > lookback_maxamount:
        msg += "Maximum lookback amount increased from {} to {}.".format(lookback_maxamount, limit)
    elif limit < lookback_maxamount:
        msg += "Maximum lookback amount decreased from {} to {}.".format(lookback_maxamount, limit)
    else:
        msg += "Given amount and loopback amount are the same. No changes done."

    lookback_maxamount = limit
    
    return msg


def setup(bot):
    bot.add_cog(Functions(bot))