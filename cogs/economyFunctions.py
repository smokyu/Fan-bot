import discord
import json
import os
from discord.ext import commands

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