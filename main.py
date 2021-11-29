import os
import discord
from discord.ext import commands
import json
import requests

token = os.environ['TOKEN']
auth = os.environ['AUTH']

activity = discord.Activity(type=discord.ActivityType.listening, name="+help")

bot = commands.Bot(command_prefix="+", activity=activity)
bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
  embed=discord.Embed(color=0x5662f6)
  embed.add_field(name="Commands Help", value="+gamertag (or +gt) \"gamertag\" - sets your gamertag\n+mcc - checks your MCC progress\n+infinite - checks your Halo Infinite progress\n+legacy - checks your Legacy Master progress\n+pc - checks your PC Master Progress\n+xbox - checks your Modern Xbox Master progress\n+hc - checks your Halo Completionist progress", inline=True)
  await ctx.send(embed=embed)

#@bot.command(pass_context=True)
#async def init(ctx):
#  d={}
#  d['Aido#9354'] = 2533274882190382
#  djson = json.dumps(d)
#  print(djson)
#  f=open("database.json", "w+")
#  json.dump(djson, f)
#  f.close()

#@bot.command(pass_context=True)
#async def init2(ctx):
#  f=open("database.json")
#  d=json.load(f)
#  f.close()
#  print(d)

@bot.command(pass_context=True)
async def mcc(ctx):
  role = discord.utils.get(ctx.guild.roles, id=913709746098429964)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already checked and finished MCC.')
     return
  user = str(ctx.message.author.id)
  f=open("database.json")
  db=json.load(f)
  f.close()
  if user not in db.keys():
    await ctx.reply('Please set your gamertag first.')
    return
  await ctx.message.add_reaction("1️⃣")
  xuid = db[user]
  url = "https://xbl.io/api/v2/achievements/player/"
  url+=xuid
  r=requests.get(url, headers={"X-Authorization":auth})
  x=r.json()
  await ctx.message.add_reaction('2️⃣')
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  for game in x['titles']:
     if game['name'] == 'Halo: The Master Chief Collection':
             if game['achievement']['progressPercentage'] == 100:
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('✅')
                     await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished MCC! Congrats!")
                     await ctx.message.author.add_roles(role)
                     return
             else:
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('❌')
                     await ctx.reply("Sorry, you haven\'t finished MCC yet. You\'re currently **" + str(game['achievement']['progressPercentage']) + "%** finished.")
                     return
  await ctx.message.add_reaction('3️⃣')
  await ctx.message.add_reaction('❌')
  await ctx.reply("You haven't played MCC before.")
  return

@bot.command(pass_context=True)
async def infinite(ctx):
  role = discord.utils.get(ctx.guild.roles, id=914441618591989801)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already checked and finished Halo Infinite.')
     return
  user = str(ctx.message.author.id)
  f=open("database.json")
  db=json.load(f)
  f.close()
  if user not in db.keys():
    await ctx.reply('Please set your gamertag first.')
    return
  await ctx.message.add_reaction("1️⃣")
  xuid = db[user]
  url = "https://xbl.io/api/v2/achievements/player/"
  url+=xuid
  r=requests.get(url, headers={"X-Authorization":auth})
  x=r.json()
  await ctx.message.add_reaction('2️⃣')
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  for game in x['titles']:
     if game['name'] == 'Halo Infinite':
             if game['achievement']['progressPercentage'] == 100:
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('✅')
                     await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Halo Infinite! Congrats!")
                     await ctx.message.author.add_roles(role)
                     return
             else:
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('❌')
                     await ctx.reply("Sorry, you haven\'t finished Halo Infinite yet. You\'re currently **" + str(game['achievement']['progressPercentage']) + "%** finished.")
                     return
  await ctx.message.add_reaction('3️⃣')
  await ctx.message.add_reaction('❌')
  await ctx.reply("You haven't played Halo Infinite before.")
  return

@bot.command(pass_context=True, aliases=['gamertag'])
async def gt(ctx, *args):
  if len(args) == 0:
    #await ctx.message.add_reaction("1️⃣")
    #await ctx.message.add_reaction('2️⃣')
    #await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("Please write your gamertag after the command.")
    return
  await ctx.message.add_reaction("1️⃣")
  user = ctx.message.author.id
  tag = ' '.join(args)
  gtag = tag
  tag = tag.replace(' ', "%20")
  url = "https://xbl.io/api/v2/friends/search?gt="
  url+=tag
  await ctx.message.add_reaction('2️⃣')
  db={}
  try:
    f=open("database.json")
    db=json.load(f)
    f.close()
  except:
    pass
  try:
    r=requests.get(url, headers={"X-Authorization":auth})
    x=r.json()
    xuid=x['profileUsers'][0]['id']
    db[str(user)] = xuid
    f=open("database.json", "w")
    json.dump(db, f)
    f.close()
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    await ctx.reply("Gamertag set to \"" + gtag +"\".")
    return
  except:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("Hmm, that gamertag didn't work. For names using the new gamertag system, please do not put a hashtag before the numbers.")
    return

@bot.command(pass_context=True)
async def legacy(ctx):
  role = discord.utils.get(ctx.guild.roles, id=914444710939074560)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Legacy Master.')
     return
  user = str(ctx.message.author.id)
  f=open("database.json")
  db=json.load(f)
  f.close()
  if user not in db.keys():
    await ctx.reply('Please set your gamertag first.')
    return
  await ctx.message.add_reaction("1️⃣")
  xuid = db[user]
  url = "https://xbl.io/api/v2/achievements/player/"
  url+=xuid
  r=requests.get(url, headers={"X-Authorization":auth})
  x=r.json()
  await ctx.message.add_reaction('2️⃣')
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  ce = 0
  h3 = 0
  odst = 0
  hr = 0
  h4 = 0
  hw = 0
  for game in x['titles']:
     if game['name'] == 'Halo: Combat Evolved Anniversary':
             if game['achievement']['progressPercentage'] == 100:
                     ce = 100
             else:
                     ce = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars':
             if game['achievement']['progressPercentage'] == 100:
                     hw = 100
             else:
                     hw = game['achievement']['progressPercentage']
     if game['name'] == 'Halo 3':
             if game['achievement']['progressPercentage'] == 100:
                     h3 = 100
             else:
                     h3 = game['achievement']['progressPercentage']
     if game['name'] == 'Halo: Reach':
             if game['achievement']['progressPercentage'] == 100:
                     hr = 100
             else:
                     hr = game['achievement']['progressPercentage']
     if game['name'] == 'Halo 4':
             if game['achievement']['progressPercentage'] == 100:
                     h4 = 100
             else:
                     h4 = game['achievement']['progressPercentage']
     if game['name'] == 'Halo 3: ODST Campaign Edition':
             if game['achievement']['progressPercentage'] == 100:
                     odst = 100
             else:
                     odst = game['achievement']['progressPercentage']
  if h3 == 100 and h4 == 100 and odst == 100 and hr == 100 and ce == 100 and hw == 100:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Legacy Master! Congrats!")
    await ctx.message.author.add_roles(role)
    return
  else:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("Here\'s your progress on the legacy games:\nHalo 3 :   **" + str(h3) + "%**\nHalo Wars :   **" + str(hw) + "%**\nHalo 3: ODST :   **" + str(odst) + "%**\nHalo: Reach :   **" + str(hr) +"%**\nHalo: Combat Evolved Anniversary :   **" + str(ce) + "%**\nHalo 4 :   **" + str(h4) + "%**")
    return

bot.run(token)