from discord.ext import commands
import discord
from discord import app_commands
from dataclasses import dataclass
import random
from typing import List
import datetime
from sessions_commands import start, end, prefix_command
import json
from colorama import Fore
 
#BOT_TOKEN = "Add your bot token here"
CHANNEL_ID = 761095951255076944

intents = discord.Intents.all()
#intents.message_content = True
#intents (means that the bot is ready to use all the features of discord)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())#intents)

with open('config.json','r') as file:
    TOKEN = json.load(file)['token']


@bot.event
#The keyword async is used in Python to define an asynchronous function or method.
async def on_ready(): 
    print("Logged in as " + Fore.RED + bot.user.name + Fore.RESET)
    channel = bot.get_channel(CHANNEL_ID)
    synced = await bot.tree.sync()
    print("Slash CMDs synced " + Fore.RED + str(len(synced)) + " Commands" + Fore.RESET)


@bot.tree.command(name="ping",description="Shows the bot's latency in ms. ")
async def ping(interaction: discord.Interaction):
    bot_latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Ping: {bot_latency}ms")


@bot.event
#An asynchronous function is a function that can run concurrently with other code, allowing it to perform tasks asynchronously without blocking the execution of the entire program.
async def on_message(message):
    if message.content.startswith('hello'):
        await message.channel.send('Hello!')
    await bot.process_commands(message)


@bot.tree.command(name="hello", description="Responds with a hello message.")
#ctx is an abbreviation for "context" and is commonly used as the parameter name for commands and event functions.
#It represents the context in which a command or event is executed.
#The ctx parameter provides access to various information and functionality related to the current command or event.
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")


@bot.tree.command(name="hey", description="Says hello.")
async def hey(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")


@bot.tree.command(name="choose", description="Chooses from a bunch of options.")
async def choose(interaction:discord.Interaction, args:str):
    arguments = args.split(" ")
    choice = random.choice(arguments)
    await interaction.response.send_message(choice)


@bot.tree.command(name="math", description="Solves the given math expression.")
async def math(interaction: discord.Interaction, expression:str):
    symbols = ['+','-','*','**','/','%']
    try:
        if any(s in expression for s in symbols):
            calculated = eval(expression)
            embed = discord.Embed(title="Math Expression",description=f"`Expression` {expression}\n`Answer` {calculated}", color=discord.Color.dark_gold())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Give a math expression to solve.")
    except Exception as e:
        print("Error Occured: ", str(e))
        await interaction.response.send_message("Enter a valid math expression.")

@bot.tree.command(name="8ball", description="Ask a question and get an answer.")
async def eightball(interaction:discord.Interaction, *,question: str):
    with open("responses.txt","r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)
    await interaction.response.send_message(response)

@bot.tree.command(name="userinfo", description="Shows information about an user.")
async def userinfo(interaction: discord.Integration, member: discord.Member=None):
    if member == None:
        member = interaction.user
    roles = [role for role in member.roles]
    embed = discord.Embed(title="User info", description=f"Here's the user info on the user {member.mention}", color=discord.Colour.dark_green(), timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name="ID",value=member.id)
    embed.add_field(name="Name", value=f"{member.name}#{member.discriminator}")
    embed.add_field(name="Nickname",value=member.display_name)
    embed.add_field(name="Created At", value=member.created_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.add_field(name="Joined At", value=member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p"))
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role", value=member.top_role.mention)
    embed.add_field(name="Messages",value="0")
    embed.add_field(name="Bot?", value=member.bot)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="shutdown",description="Shuts down the bot.")
async def shutdown(interaction:discord.Interaction):
    await interaction.response.send_message(content=":robot: Shutting down the bot.")
    await bot.close()

@bot.tree.command(name="randomnumber", description="Chooses a random number from the given range.")
async def random_number(interaction: discord.Integration, start_range: int, end_range: int):
    if start_range > end_range:
        await interaction.response.send_message("Invalid range. The start range should be less than the end range.")
        return

    chosen_number = random.randint(start_range, end_range)
    await interaction.response.send_message(f"The random number between {start_range} and {end_range} is: {chosen_number}")


bot.add_command(start)
bot.add_command(end)
bot.add_command(prefix_command)


bot.run(TOKEN)