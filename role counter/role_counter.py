import os
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DIS_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

def read_json():
    with open('storage.json', 'r') as of:
        data = json.load(of)
        return data

def append_json(data):
    cdata = read_json()
    with open('storage.json', 'w') as of:
        cdata['users'].append(data)
        of.seek(0)
        json.dump(cdata, of, indent = 4)

def modify_json(data, user, entry, val):
    for e in data['users']:
        if(e['name'] == user):
            e[entry] += val
    with open('storage.json', 'w') as of:
        json.dump(data, of, indent = 4)

def set_json(data, user, entry, val):
    for e in data['users']:
        if(e['name'] == user):
            e[entry] = val
    with open('storage.json', 'w') as of:
        json.dump(data, of, indent = 4)

def list_data(user):
    d = read_json()
    for entry in d['users']:
        if(entry['name'] == user):
            s = 'Tank: ' + str(entry['t']) + ' Dps: ' + str(entry['d']) + ' Supp: ' + str(entry['s'])
            return s

@bot.command()
async def c(ctx):
    u = str(ctx.author);
    d = read_json()
    for entry in d['users']:
        if(entry['name'] == u):
            await ctx.reply("You have already created an account")
            return
    x = { "name": u, "t": 0, "d": 0, "s": 0 }
    append_json(x)
    await ctx.reply("Account created successfully")

@bot.command()
async def t(ctx):
    u = str(ctx.author)
    d = read_json()
    valid = False
    for entry in d['users']:
        if(entry['name'] == u):
            valid = True
    if(valid):
        await ctx.reply(list_data(str(ctx.author)))
    else:
        await ctx.reply('Please create an account with !c first')

@bot.command()
async def w(ctx, args):
    u = str(ctx.author)
    d = read_json()
    valid = False
    for entry in d['users']:
        if(entry['name'] == u):
            valid = True

    if(valid):
        if(args == 's'):
            modify_json(d, u, 's', 1)
            await ctx.reply(list_data(u))
        elif(args == 'd'):
            modify_json(d, u, 'd', 1)
            await ctx.reply(list_data(u))
        elif(args == 't'):
            modify_json(d, u, 't', 1)
            await ctx.reply(list_data(u))
        else:
            await ctx.reply('Invalid input')
    else:
        await ctx.reply('Please create an account with !c first')

@bot.command()
async def r(ctx):
    u = str(ctx.author)
    d = read_json()
    valid = False
    for entry in d['users']:
        if(entry['name'] == u):
            valid = True
    if(valid):
        set_json(d, u, 's', 0)
        set_json(d, u, 'd', 0)
        set_json(d, u, 't', 0)
        await ctx.reply(list_data(u))
    else:
        await ctx.reply('Please create an account with !c first')

bot.run(TOKEN)