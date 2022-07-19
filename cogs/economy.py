import discord
import json
import os
from discord.ext import commands
from cogs.economyFunctions import open_account, get_bank_data, update_bank

def setup(bot):
  bot.add_cog(Balance(bot))

class Balance(commands.Cog):
    def __init__(self, fanbot):
        self.fanbot = fanbot

    @commands.command(name="money", description="Affiche l'argent d'un utilisateur.")
    async def money(self, ctx, member: discord.Member):
        await open_account(member)
        user = member
        users = await get_bank_data()

        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]

        embed = discord.Embed(title=f"Compte en banque de {user.display_name}")
        embed.add_field(name="Porte-monnaie", value=wallet_amount)
        embed.add_field(name="Banque", value=bank_amount)
        await ctx.send(embed=embed)


    @commands.command(name="deposit", description="Dépose de l'argent sur votre compte en banque.")
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Aucun montant n'a été spécifie.")
            return

        money = await update_bank(ctx.author)
        if int(amount) > money[0]:
            await ctx.send("Vous n'avez pas assez d'argent.")
            return
        if int(amount) < 0:
            await ctx.send("le montant n'est pas valide.")
            return

        await update_bank(ctx.author, -1 * int(amount), "wallet")
        await update_bank(ctx.author, int(amount), "bank")

        await ctx.send(f"Vous avez déposer {amount}$ sur votre compte en banque !")


    @commands.command(name="withdraw", description="Débite de l'argent sur votre compte en banque.")
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send("Aucun montant n'a été spécifié.")
            return

        money = await update_bank(ctx.author)
        if int(amount) > money[1]:
            await ctx.send("Vous n'avez pas assez d'argent.")
            return
        if int(amount) < 0:
            await ctx.send("le montant n'est pas valide.")
            return

        await update_bank(ctx.author, int(amount), "wallet")
        await update_bank(ctx.author, -1 * int(amount), "bank")

        await ctx.send(f"Vous avez retiré {amount}$ sur votre compte en banque !")


    @commands.command(name="pay", description="Effectue un transfert d'un joueur à un autre.")
    async def pay(self, ctx, member: discord.Member, amount=None):
        await open_account(ctx.author)
        await open_account(member)

        if amount == None:
            await ctx.send("Aucun montant n'a été spécifié.")
            return

        money = await update_bank(ctx.author)
        if int(amount) > money[1]:
            await ctx.send("Vous n'avez pas assez d'argent.")
            return
        if int(amount) < 0:
            await ctx.send("Le montant n'est pas valide.")
            return

        await update_bank(member, int(amount), "bank")
        await update_bank(ctx.author, -1 * int(amount), "bank")

        await ctx.send(f"Vous avez envoyé {amount}$ sur le compte en banque de {member.display_name}!")


    @commands.command(name="askmoney", description="Envoie un mp à une personne pour lui demander un virement.")
    async def askmoney(self, ctx, member: discord.Member, amount=None):
        if amount == None:
            await ctx.send("Aucun montant n'a été spécifié.")
            return
        if int(amount) < 0:
            await ctx.send("Le montant n'est pas valide.")
            return
        if int(amount) == 0:
            await ctx.send("Le montant n'est pas valide.")
            return

        await member.send(f"Bonjour, {ctx.author} vous demande de lui faire un virement de {amount}$.")