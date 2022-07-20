import discord
import json
import os
from dotenv import load_dotenv
from discord.ext import commands

os.chdir("D:\\DEVELOPPEMENT\\FanBot")
load_dotenv(dotenv_path="config")


class FanBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

    async def on_ready(self):
        print(f"{self.user.display_name} has started successfully!")


fanbot = FanBot()
fanbot.load_extension("cogs.economy")

fanbot.run(os.getenv("TOKEN"))
