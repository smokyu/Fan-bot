import discord
import json
import os
import cogs.shops
from discord.ext import commands
from cogs.economyFunctions import open_account, get_bank_data, update_bank


mainshop = [
    {"name": "Montre", "price": 100, "description": "pour connaitre l'heure"},
    {"name": "Ordi", "price": 1000, "description": "surfer sur le web"},
    {"name": "Console", "price": 10000, "description": "jouer aux jeux-vidéos"},
]


def setup(bot):
    bot.add_cog(Balance(bot))


class Balance(commands.Cog):
    def __init__(self, fanbot):
        self.fanbot = fanbot

    @commands.command()
    async def money(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)

        await open_account(member)
        user = member
        users = await get_bank_data()

        wallet_amount = users[str(user.id)]["wallet"]
        bank_amount = users[str(user.id)]["bank"]

        embed = discord.Embed(title=f"Compte en banque de {user.display_name}")
        embed.add_field(name="Porte-monnaie", value=wallet_amount)
        embed.add_field(name="Banque", value=bank_amount)
        await ctx.send(embed=embed)

    @commands.command()
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
        if int(amount) == 0:
            await ctx.send("Le montant n'est pas valide.")

        await update_bank(ctx.author, -1 * int(amount), "wallet")
        await update_bank(ctx.author, int(amount), "bank")

        await ctx.send(f"Vous avez déposer {amount}$ sur votre compte en banque !")

    @commands.command()
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
        if int(amount) == 0:
            await ctx.send("Le montant n'est pas valide.")

        await update_bank(ctx.author, int(amount), "wallet")
        await update_bank(ctx.author, -1 * int(amount), "bank")

        await ctx.send(f"Vous avez retiré {amount}$ sur votre compte en banque !")

    @commands.command()
    async def pay(
        self,
        ctx,
        member: discord.Member,
        amount=None,
        *,
        reason="Aucune raison n'a été renseignée.",
    ):
        await ctx.channel.purge(limit=1)

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
        if int(amount) == 0:
            await ctx.send("Le montant n'est pas valide.")

        await update_bank(member, int(amount), "bank")
        await update_bank(ctx.author, -1 * int(amount), "bank")

        embed = discord.Embed()
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(
            name=f"{amount} :dollar:  a bien été donné à {member.display_name}",
            value=f"**Raison:** {reason}",
        )
        await ctx.send(embed=embed)

    @commands.command()
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

        await member.send(
            f"Bonjour, {ctx.author} vous demande de lui faire un virement de {amount}$."
        )

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Magasin")

        for item in cogs.shops.mainshop:
            name = item["name"]
            price = item["price"]
            description = item["description"]
            embed.add_field(
                name=f"{name} ({price} :dollar:)", value=f"{description}", inline=False
            )

        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, item, amount=1):
        await open_account(ctx.author)

        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("L'objet n'a pas été trouvé.")
                return
            if res[1] == 2:
                await ctx.send(f"Vous n'avez pas assez d'argent pour acheter {item}.")
                return

        await ctx.send(f"Vous avez acheté {amount} {item}.")

    @commands.command()
    async def inv(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title="Inventaire")
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name=name, value=amount)

        await ctx.send(embed=em)

    async def buy_this(self, user, item_name, amount):
        item_name = item_name.lower()
        name_ = None
        for item in mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
                price = item["price"]
                break

        if name_ == None:
            return [False, 1]

        cost = price * amount

        users = await get_bank_data()

        bal = await update_bank(user)

        if bal[0] < cost:
            return [False, 2]

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index += 1
            if t == None:
                obj = {"item": item_name, "amount": amount}
                users[str(user.id)]["bag"].append(obj)
        except:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"] = [obj]

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        await update_bank(user, cost * -1, "wallet")

        return [True, "Worked"]
