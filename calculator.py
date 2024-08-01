import discord
from discord.ext import commands
from colorama import Fore
import json

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())
    
    async def on_ready(self):
        print("Logged in as " + Fore.RED + self.user.name + Fore.RESET)
        synced = await self.tree.sync()
        print("Slash CMDs synced " + Fore.RED + str(len(synced)) + " Commands" + Fore.RESET)

with open('config.json','r') as file:
    TOKEN = json.load(file)['token']


class Buttons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.expression = ""

    async def add(self, interaction: discord.Interaction, symbol):
        if(self.expression == "Cleared!"):
            self.expression = ""
        self.expression += symbol
        await self.update(interaction)

    async def update(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.message.edit(content=f"```{self.expression}```")

    async def solve(self, interaction: discord.Interaction):
        pi = 3.14159
        try:
            self.expression = str(eval(self.expression))
        except:
            await interaction.response.send_message("This expression is invalid", ephemeral=True)
        await self.update(interaction)
        #self.expression = ""

    async def cleared(self, interaction: discord.Interaction):
        self.expression = "Cleared!"
        await self.update(interaction)

    async def back(self, interaction: discord.Interaction):
        self.expression = self.expression[:-1]
        await self.update(interaction)

    @discord.ui.button(label="x", style=discord.ButtonStyle.blurple, row=0)
    async def multisym(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"*")

    @discord.ui.button(label="÷", style=discord.ButtonStyle.blurple, row=0)
    async def divisym(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction, "/")

    @discord.ui.button(label="+", style=discord.ButtonStyle.blurple, row=0)
    async def plussym(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction, "+")

    @discord.ui.button(label="-", style=discord.ButtonStyle.blurple, row=0)
    async def minussym(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"-")

    @discord.ui.button(label="7", style=discord.ButtonStyle.grey, row=1)
    async def num7(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"7")

    @discord.ui.button(label="8", style=discord.ButtonStyle.grey, row=1)
    async def num8(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"8")

    @discord.ui.button(label="9", style=discord.ButtonStyle.grey, row=1)
    async def num9(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"9")

    @discord.ui.button(label="π", style=discord.ButtonStyle.blurple, row=1)
    async def pisym(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"pi")

    @discord.ui.button(label="4", style=discord.ButtonStyle.grey, row=2)
    async def num4(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"4")
    
    @discord.ui.button(label="5", style=discord.ButtonStyle.grey, row=2)
    async def num5(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"5")

    @discord.ui.button(label="6", style=discord.ButtonStyle.grey, row=2)
    async def num6(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"6")

    @discord.ui.button(label="Clear", style=discord.ButtonStyle.red, row=2)
    async def clear(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.cleared(interaction)
    
    @discord.ui.button(label="1", style=discord.ButtonStyle.grey, row=3)
    async def num1(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"1")
    
    @discord.ui.button(label="2", style=discord.ButtonStyle.grey, row=3)
    async def num2(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"2")

    @discord.ui.button(label="3", style=discord.ButtonStyle.grey, row=3)
    async def num3(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"3")
    
    @discord.ui.button(label="←", style=discord.ButtonStyle.red, row=3)
    async def backspace(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.back(interaction)
    
    @discord.ui.button(label="00", style=discord.ButtonStyle.grey, row=4)
    async def num00(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"00")

    @discord.ui.button(label="0", style=discord.ButtonStyle.grey, row=4)
    async def num0(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,"0")

    @discord.ui.button(label=".", style=discord.ButtonStyle.grey, row=4)
    async def pointsym(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.add(interaction,".")

    @discord.ui.button(label="=", style=discord.ButtonStyle.green, row=4)
    async def equal(self, interaction:discord.Integration, Button: discord.ui.Button):
        await self.solve(interaction)


bot = Client()


@bot.tree.command(name="calculator", description="Sends an interactive calculator")
async def calculator(interaction: discord.Interaction):
    await interaction.response.send_message("```Begin Calculating...```", view=Buttons())


bot.run(TOKEN)
