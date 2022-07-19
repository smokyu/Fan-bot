import discord
import json
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand
from cogs import economy

os.chdir('D:\\DEVELOPPEMENT\\FanBot')
load_dotenv(dotenv_path='config')

class FanBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

    async def on_ready(self):
        print(f"{self.user.display_name} est connecté au serveur.")


fanbot = FanBot()

slash = SlashCommand(fanbot, sync_commands=True, sync_on_cog_reload=True)

fanbot.remove_command("help")

fanbot.load_extension('cogs.economy')
fanbot.load_extension('cogs.others')

fanbot.run(os.getenv("TOKEN"))