import discord
import json
import os
from discord.ext import commands

os.chdir('C:\\Users\\smoky\\PycharmProjects\\FanBot')

client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print("Lancé")


@client.command()
async def money(ctx, member: discord.Member):
    await open_account(member)
    user = member
    users = await get_bank_data()

    wallet_amount = users[str(user.id)]["wallet"]
    bank_amount = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"Compte en banque de {user.display_name}")
    embed.add_field(name="Porte-monnaie", value=wallet_amount)
    embed.add_field(name="Banque", value=bank_amount)
    await ctx.send(embed=embed)


@client.command()
async def generate(ctx, amount):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    await ctx.send(f"Ajout de {amount}$ à votre compte en banque.")

    users[str(user.id)]["bank"] += int(amount)
    with open("bank.json", 'w') as file:
        json.dump(users, file)


@client.command()
async def deposit(ctx, amount=None):
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


@client.command()
async def withdraw(ctx, amount=None):
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


@client.command()
async def pay(ctx, member: discord.Member, amount=None):
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


@client.command()
async def askmoney(ctx, member: discord.Member, amount=None):
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


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("bank.json", 'w') as file:
        json.dump(users, file)
    return True


async def get_bank_data():
    with open("bank.json", 'r') as file:
        users = json.load(file)
    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("bank.json", 'w') as file:
        json.dump(users, file)

    money = [users[str(user.id)][mode], users[str(user.id)]["bank"]]
    return money


client.run('OTk3OTI0NDAzMzkwMjA2MDI1.GllS8v.JvLM20_IB0s-m-MuBX3gStyzdOZVkUBv0rCe6I')
