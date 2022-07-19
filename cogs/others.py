import discord
from discord.ext import commands
from discord_slash import cog_ext
from main import fanbot


def setup(bot):
    bot.add_cog(CommandsSlash(bot))


class CommandsSlash(commands.Cog):
    def __init__(self, fanbot):
        self.fanbot = fanbot

    @cog_ext.cog_slash(name="help", description="Affiche toutes les commandes du serveur.")
    async def help(self, ctx):
        embed = discord.Embed(title="Commandes:")
        for command in fanbot.walk_commands():
            description = command.description
            if not description or description is None or description == "":
                description = "Aucune description n'a été donnée."
            embed.add_field(name=f"!{command.name}", value=description)
        await ctx.send(embed=embed)