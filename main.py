import discord
import json
import os
from dotenv import load_dotenv
from discord.ext import commands
from cogs import economy

os.chdir('D:\\DEVELOPPEMENT\\FanBot')
load_dotenv(dotenv_path='config')


class FanBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

    async def on_ready(self):
        print(f"{self.user.display_name} est connecté au serveur.")


fanbot = FanBot()
fanbot.add_cog(economy.Balance(FanBot))

fanbot.run(os.getenv("TOKEN"))
