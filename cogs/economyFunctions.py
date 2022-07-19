import discord
import json
import os
from discord.ext import commands
import cogs.shops

os.chdir('D:\\DEVELOPPEMENT\\FanBot')

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


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in cogs.shops.mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < int(cost):
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
            obj = {"item":item_name, "amount":amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name, "amount":amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as file:
        json.dump(users, file)

    await update_bank(user, cost*-1, "wallet")

    return [True, "Worked"]