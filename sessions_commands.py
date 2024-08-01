from discord.ext import commands
import discord
from dataclasses import dataclass
import datetime
import json

CHANNEL_ID = 761095951255076944

with open('config.json','r') as file:
    TOKEN = json.load(file)['token']

#intents (means that the bot is ready to use all the features of discord)
intents = discord.Intents.all()

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=intents)
session = Session()

#@bot.command()
@commands.command(name="start")
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active.")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"New session started at {human_readable_time}")

#@bot.command()
@commands.command(name="end")
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active.")
        return

    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    await ctx.send(f"Session ended after {human_readable_duration}")


#@bot.command()
@commands.command(name="prefix")
async def prefix_command(ctx):
    await ctx.send("This is a prefix command response!")

#bot.load_extension('sessions_commands')

#def setup(bot):
    #bot.add_cog(bot)


#bot.run(BOT_TOKEN)


