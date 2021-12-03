import os
import discord
from discord.ext import commands
from discord import Member
import json
import requests
import random
from dotenv import load_dotenv

load_dotenv() #get env variables

intents = discord.Intents.default()
intents.members = True

token = os.environ['TOKEN']
auth = os.environ['AUTH']
tenor = os.environ['TENOR']

activity = discord.Activity(type=discord.ActivityType.listening, name="+help") #create activity instance

bot = commands.Bot(command_prefix="+", activity=activity, intents=intents) #set prefix to '+' and set the activity 
bot.remove_command('help') #delete default help

@bot.command(pass_context=True) #help command, send info about the commands
async def help(ctx):
  print("help command used - " + str(ctx.message.author))
  embed=discord.Embed(color=0x5662f6)
  embed.add_field(name="Commands Help", value="+gamertag (or +gt) \"gamertag\" - sets your gamertag\n+count - shows number of users with corresponding completion role\n+mcc - checks your MCC progress\n+infinite - checks your Halo Infinite progress\n+legacy - checks your Legacy Master progress\n+pc - checks your PC Master Progress\n+xbox - checks your Modern Xbox Master progress\n+hc - checks your Halo Completionist progress", inline=True)
  await ctx.send(embed=embed)

@bot.command(pass_context=True) #staff help command, send info about the commands
@commands.has_permissions(ban_members=True)
async def staffhelp(ctx):
  print("staff help command used - " + str(ctx.message.author))
  embed=discord.Embed(color=0x5662f6)
  embed.add_field(name="Staff Commands Help", value="+warn \"user id\" reason - warns the user\n+warns \"user id\" - shows warnings for that user\n+rmwarn \"user id\" \"warning number\" - deletes specified warning for that user\n+kick \"user id\" \"reason\" - kicks specified user\n+ban \"user id\" \"reason\" - bans specfied user\n+unban \"user id\" - unbans specified user", inline=True)
  await ctx.send(embed=embed)

@bot.command(pass_context=True) #issue command, uses tenor api to find a random skill issue gif
async def issue(ctx):
    print("skill issue command used - " + str(ctx.message.author)) 
    search_term = "skill issue"
    lmt = 50
    pos = random.randint(0,140)
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, tenor, lmt, pos))
    if r.status_code == 200:
      gifs = json.loads(r.content)
      random.seed()
      random_index = random.randint(0,len(gifs['results'])-1)
      await ctx.send(gifs['results'][random_index]['url'])

@bot.command(pass_context=True) #count command, sends number of users with each completion role
async def count(ctx): 
    print("count command used - " + str(ctx.message.author))
    mcc = ctx.guild.get_role(764645825392803870) #get each role
    infinite = ctx.guild.get_role(914979273608138783)
    pc = ctx.guild.get_role(818247288610357268)
    xbox = ctx.guild.get_role(818247307069882409)
    legacy = ctx.guild.get_role(818246915304194058)
    hc = ctx.guild.get_role(818278553187385424)
    await ctx.send("Number of users with each role:\nMCC 100%:   **" + str(len(mcc.members)) + "**\nInfinite 100%:   **" + str(len(infinite.members)) + "**\nPC Master:   **" + str(len(pc.members)) + "**\nModern Xbox Master:   **" + str(len(xbox.members)) + "**\nLegacy Master:   **" + str(len(legacy.members)) + "**\nHalo Completionist:   **" + str(len(hc.members)) + "**") #send counts

@bot.command(pass_context=True) #mcc command
async def mcc(ctx):
  print("mcc command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247307069882409)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Modern Xbox Master.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247288610357268)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished PC Master.')
     return
  role = discord.utils.get(ctx.guild.roles, id=764645825392803870) #get mcc role
  if role in ctx.message.author.roles: #if user has role already, do nothing
     await ctx.reply('You\'ve already finished MCC.')
     return
  user = str(ctx.message.author.id) #get the id of user
  f=open("database.json") #open the database and get the dictionary 
  db=json.load(f)
  f.close()
  if user not in db.keys(): #check if the id is already stored, if not, tell them.
    await ctx.reply('Please set your gamertag first.') 
    return
  await ctx.message.add_reaction("1️⃣") #progress up
  xuid = db[user] #get the xbox id of user
  url = "https://xbl.io/api/v2/achievements/player/" #create link for achievement info
  url+=xuid
  r=requests.get(url, headers={"X-Authorization":auth}) #do the get request
  x=r.json() #convert output
  await ctx.message.add_reaction('2️⃣') #progress up 
  if len(x['titles']) == 0: #if the list is empty 
    await ctx.message.add_reaction('3️⃣') #there was an issue or they haven't played any games before
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  for game in x['titles']: #for each game in titles 
     if game['name'] == 'Halo: The Master Chief Collection': #if mcc
             if game['achievement']['progressPercentage'] == 100: #if complete 
                     await ctx.message.add_reaction('3️⃣') #give them the role and congratulate 
                     await ctx.message.add_reaction('✅')
                     await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished MCC! Congrats!")
                     await ctx.message.author.add_roles(role)
                     return
             else: #not done
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('❌') #give progress of game
                     await ctx.reply("Sorry, you haven\'t finished MCC yet. You\'re currently **" + str(game['achievement']['progressPercentage']) + "%** finished.")
                     return
  await ctx.message.add_reaction('3️⃣') #mcc not in games, they havent played
  await ctx.message.add_reaction('❌')
  await ctx.reply("You haven't played MCC before.")
  return

@bot.command(pass_context=True) #same as mcc but for halo infinite
async def infinite(ctx):
  print("infinite command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247307069882409)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Modern Xbox Master.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247288610357268)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished PC Master.')
     return
  role = discord.utils.get(ctx.guild.roles, id=914979273608138783)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Infinite.')
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

@bot.command(pass_context=True) #ban command, bans a user for given reason
@commands.has_permissions(ban_members=True)
async def ban(ctx, id: int, reason, *args):
 print("ban command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 if len(args) != 0:
  reason += ' '
  reason += ' '.join(args)
 if user.dm_channel == None:
      await user.create_dm()
 await user.dm_channel.send(content=f"You have been banned from {ctx.guild}.\nReason: {reason}\nYou can appeal here: <https://forms.gle/QP62ibaP8GvZMzbM8>")
 await user.ban(reason=reason)  

@ban.error #checks for issues with ban command
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+ban user reason**')

@bot.command(pass_context=True) #unban command, unbans specified user
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
 print("unban command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 if user.dm_channel == None:
      await user.create_dm()
 await user.dm_channel.send(content=f"You have been unbanned from {ctx.guild}.\nJoin back if you'd like: https://discord.gg/UHwtz8rQse")
 await ctx.guild.unban(user)

@unban.error #checks for issues with unban command
async def unban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+unban user**')

@bot.command(pass_context=True) #kick command
@commands.has_permissions(ban_members=True)
async def kick(ctx, id: int, reason, *args):
 print("kick command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 if len(args) != 0:
  reason += ' '
  reason += ' '.join(args)
 if user.dm_channel == None:
      await user.create_dm()
 await user.dm_channel.send(content=f"You have been kicked from {ctx.guild}.\nReason: {reason} ")
 await user.kick(reason=reason) 

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+kick user reason**')

@bot.command(pass_context=True) #warn command, puts warning in database
@commands.has_permissions(ban_members=True)
async def warn(ctx, id: int, reason, *args):
 print("warn command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 if len(args) != 0:
  reason += ' '
  reason += ' '.join(args)
 if user.dm_channel == None:
      await user.create_dm()
 await user.dm_channel.send(content=f"You have been warned in {ctx.guild}.\nReason: {reason} ")
 member = str(user.id)
 db={} #make empty database 
 try: #try loading something from the database
    f=open("warnings.json")
    db=json.load(f) #set dict to db
    f.close()
 except:
    pass #keep db as empty dict
 db.setdefault(member, []).append(reason)
 f=open("warnings.json", "w") #write to warnings.json
 json.dump(db, f)
 f.close()
 await ctx.reply("This user has been warned.")
 await user.warn(reason=reason) 

@warn.error
async def warn_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+warn user reason**')

@bot.command(pass_context=True) #warns command, gets warnings for specified user
@commands.has_permissions(ban_members=True)
async def warns(ctx, id: int):
 print("warns command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 member = str(user.id)
 db={} #make empty database 
 try: #try loading something from the database
    f=open("warnings.json")
    db=json.load(f) #set dict to db
    f.close()
 except:
    pass #keep db as empty dict
 if member in db.keys():
   if len(db[member]) == 0:
     await ctx.reply("This user has no warnings.")
   else:
     i=1
     response = ''
     for warning in db[member]:
       response += str(i) + '. ' + warning + '\n'
       i += 1
     await ctx.reply(response)
 else:
    await ctx.reply("This user has no warnings.")

@warns.error
async def warns_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+warns user**')

@bot.command(pass_context=True) #rmwarn command, removes specified warning
@commands.has_permissions(ban_members=True)
async def rmwarn(ctx, id: int, warnnum):
 print("rmwarn command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 member = str(user.id)
 warnnum = int(warnnum) - 1
 db={} #make empty database 
 try: #try loading something from the database
    f=open("warnings.json")
    db=json.load(f) #set dict to db
    f.close()
 except:
    pass #keep db as empty dict
 if member in db.keys():
   if len(db[member]) == 0:
     await ctx.reply("This user has no warnings to remove.")
   else:
     try:
      del db[member][warnnum]
      f=open("warnings.json", "w") #write to database.json
      json.dump(db, f)
      f.close()
     except:
      await ctx.reply("That warning number does not exist.")
      return
     await ctx.reply("The warning has been removed.")
 else:
    await ctx.reply("This user has no warnings to remove.")

@rmwarn.error
async def rmwarn_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+warns user warning#**')

@bot.command(pass_context=True, aliases=['gamertag']) #gamertag command, sets user's gamertag in database
async def gt(ctx, *args):
  print("gt command used - " + str(ctx.message.author))
  if len(args) == 0: #if no gamertag given, tell them
    await ctx.message.add_reaction('❌')
    await ctx.reply("Please write your gamertag after the command.")
    return
  await ctx.message.add_reaction("1️⃣") #progress up
  user = ctx.message.author.id #get user id
  tag = ' '.join(args) #check for multiple arguements and join them
  gtag = tag
  tag = tag.replace(' ', "%20") #replace whitespace with '%20'
  url = "https://xbl.io/api/v2/friends/search?gt=" #create url
  url+=tag 
  await ctx.message.add_reaction('2️⃣') #progress up
  db={} #make empty database 
  try: #try loading something from the database
    f=open("database.json")
    db=json.load(f) #set dict to db
    f.close()
  except:
    pass #keep db as empty dict
  try:
    r=requests.get(url, headers={"X-Authorization":auth}) #get user info
    x=r.json() #convert to dict
    xuid=x['profileUsers'][0]['id'] #get xbox id
    db[str(user)] = xuid #set discord id as key, xbox id as value
    f=open("database.json", "w") #write to database.json
    json.dump(db, f)
    f.close()
    await ctx.message.add_reaction('3️⃣') #tell them we've finished
    await ctx.message.add_reaction('✅')
    await ctx.reply("Gamertag set to \"" + gtag +"\".")
    return
  except:
    await ctx.message.add_reaction('3️⃣') #there was an exception, something went wrong
    await ctx.message.add_reaction('❌')
    await ctx.reply("Hmm, that gamertag didn't work. For names using the new gamertag system, please do not put a hashtag before the numbers.")
    return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
async def legacy(ctx):
  print("legacy command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818246915304194058)
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
  await ctx.message.add_reaction('2️⃣')
  x=r.json()
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  ce = 0 #progress variables, set default as 0
  h3 = 0
  odst = 0
  hr = 0
  h4 = 0
  hw = 0
  games = set(['Halo: Combat Evolved Anniversary', 'Halo Wars', 'Halo 3', 'Halo: Reach', 'Halo 4', 'Halo 3: ODST Campaign Edition']) #create set of names of games
  for game in x['titles']: #for each game in the data
    if game['name'] in games: #if the game is in the set
     if game['name'] == 'Halo: Combat Evolved Anniversary': #check for what game and set progress accordingly
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
  if h3 == 100 and h4 == 100 and odst == 100 and hr == 100 and ce == 100 and hw == 100: #if all 100, give role
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Legacy Master! Congrats!")
    await ctx.message.author.add_roles(role)
    return
  else:
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    await ctx.reply("Here\'s your progress on the legacy games:\nHalo 3 :   **" + str(h3) + "%**\nHalo Wars :   **" + str(hw) + "%**\nHalo 3: ODST :   **" + str(odst) + "%**\nHalo: Reach :   **" + str(hr) +"%**\nHalo: Combat Evolved Anniversary :   **" + str(ce) + "%**\nHalo 4 :   **" + str(h4) + "%**")
    return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
async def xbox(ctx):
  print("xbox command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247307069882409)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Modern Xbox Master.')
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
  await ctx.message.add_reaction('2️⃣')
  x=r.json()
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  sa = 0 #progress variables, set default as 0
  mcc = 0
  h5 = 0
  hw = 0
  hw2 = 0
  infinite = 0
  games = set(['Halo: The Master Chief Collection', 'Halo Wars: Definitive Edition (PC)', 'Halo Wars 2', 'Halo 5: Guardians', 'Halo: Spartan Assault', 'Halo Infinite']) #create set of names of games
  for game in x['titles']: #for each game in the data
    if game['name'] in games: #if the game is in the set
     if game['name'] == 'Halo: The Master Chief Collection': #check for what game and set progress accordingly
             if game['achievement']['progressPercentage'] == 100:
                     mcc = 100
             else:
               if game['achievement']['progressPercentage'] >= mcc:
                     mcc = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars: Definitive Edition (PC)':
             if game['achievement']['progressPercentage'] == 100:
                     hw = 100
             else:
               if game['achievement']['progressPercentage'] >= hw:
                     hw = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars 2':
             if game['achievement']['progressPercentage'] == 100:
                     hw2 = 100
             else:
               if game['achievement']['progressPercentage'] >= hw2:
                     hw2 = game['achievement']['progressPercentage']
     if game['name'] == 'Halo 5: Guardians':
             if game['achievement']['progressPercentage'] == 100:
                     h5 = 100
             else:
               if game['achievement']['progressPercentage'] >= h5:
                     h5 = game['achievement']['progressPercentage']
     if game['name'] == 'Halo: Spartan Assault':
             if game['achievement']['progressPercentage'] == 100:
                     sa = 100
             else:
               if game['achievement']['progressPercentage'] >= sa:
                     sa = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Infinite':
             if game['achievement']['progressPercentage'] == 100:
                     infinite = 100
             else:
               if game['achievement']['progressPercentage'] >= infinite:
                     infinite = game['achievement']['progressPercentage']
  if mcc == 100:
    mccrole = discord.utils.get(ctx.guild.roles, id=764645825392803870)
    await ctx.message.author.add_roles(mccrole)
  if infinite == 100:
    infiniterole = discord.utils.get(ctx.guild.roles, id=914979273608138783)
    await ctx.message.author.add_roles(infiniterole)
  if sa == 100 and h5 == 100 and hw == 100 and hw2 == 100 and mcc == 100 and infinite == 100: #if all 100, give role
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    mccrole = discord.utils.get(ctx.guild.roles, id=764645825392803870)
    await ctx.message.author.remove_roles(mccrole)
    infiniterole = discord.utils.get(ctx.guild.roles, id=914979273608138783)
    await ctx.message.author.remove_roles(infiniterole)
    await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Modern Xbox Master! Congrats!")
    await ctx.message.author.add_roles(role)
    return
  else:
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    await ctx.reply("Here\'s your progress on the Modern Xbox games:\nHalo Infinite :   **" + str(infinite) + "%**\nMCC :   **" + str(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + str(hw) + "%**\nHalo Wars 2 :   **" + str(hw2) + "%**\nHalo 5: Guardians :   **" + str(h5) +"%**\nHalo: Spartan Assault :   **" + str(sa) + "%**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
    return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
async def pc(ctx):
  print("pc command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247288610357268)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished PC Master.')
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
  await ctx.message.add_reaction('2️⃣')
  x=r.json()
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  sa = 0 #progress variables, set default as 0
  mcc = 0
  ss = 0
  hw = 0
  hw2 = 0
  infinite = 0
  games = set(['Halo: The Master Chief Collection', 'Halo Wars: Definitive Edition (PC)', 'Halo Wars 2', 'Halo: Spartan Strike', 'Halo: Spartan Assault', 'Halo Infinite']) #create set of names of games
  for game in x['titles']: #for each game in the data
    if game['name'] in games: #if the game is in the set
     if game['name'] == 'Halo: The Master Chief Collection': #check for what game and set progress accordingly
             if game['achievement']['progressPercentage'] == 100:
                     mcc = 100
             else:
               if game['achievement']['progressPercentage'] >= mcc:
                     mcc = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars: Definitive Edition (PC)':
             if game['achievement']['progressPercentage'] == 100:
                     hw = 100
             else:
               if game['achievement']['progressPercentage'] >= hw:
                     hw = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars 2':
             if game['achievement']['progressPercentage'] == 100:
                     hw2 = 100
             else:
               if game['achievement']['progressPercentage'] >= hw2:
                     hw2 = game['achievement']['progressPercentage']
     if game['name'] == 'Halo: Spartan Strike':
             if game['achievement']['progressPercentage'] == 100:
                     ss = 100
             else:
               if game['achievement']['progressPercentage'] >= ss:
                     ss = game['achievement']['progressPercentage']
     if game['name'] == 'Halo: Spartan Assault':
             if game['achievement']['progressPercentage'] == 100:
                     sa = 100
             else:
               if game['achievement']['progressPercentage'] >= sa:
                     sa = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Infinite':
             if game['achievement']['progressPercentage'] == 100:
                     infinite = 100
             else:
               if game['achievement']['progressPercentage'] >= infinite:
                     infinite = game['achievement']['progressPercentage']
  if mcc == 100:
    mccrole = discord.utils.get(ctx.guild.roles, id=764645825392803870)
    await ctx.message.author.add_roles(mccrole)
  if infinite == 100:
    infiniterole = discord.utils.get(ctx.guild.roles, id=914979273608138783)
    await ctx.message.author.add_roles(infiniterole)
  if sa == 100 and ss == 100 and hw == 100 and hw2 == 100 and mcc == 100 and infinite == 100: #if all 100, give role
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    mccrole = discord.utils.get(ctx.guild.roles, id=764645825392803870)
    await ctx.message.author.remove_roles(mccrole)
    infiniterole = discord.utils.get(ctx.guild.roles, id=914979273608138783)
    await ctx.message.author.remove_roles(infiniterole)
    await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished PC Master! Congrats!")
    await ctx.message.author.add_roles(role)
    return
  else:
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    await ctx.reply("Here\'s your progress on the PC games:\nHalo Infinite :   **" + str(infinite) + "%**\nMCC :   **" + str(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + str(hw) + "%**\nHalo Wars 2 :   **" + str(hw2) + "%**\nHalo: Spartan Assault :   **" + str(sa) +"%**\nHalo: Spartan Strike :   **" + str(ss) + "%**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.\n**Spartan Strike achievements are bugged and will always show as 0%, please post a screenshot of completion and ping staff.**")
    return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
async def hc(ctx):
  print("hc command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist.')
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
  await ctx.message.add_reaction('2️⃣')
  x=r.json()
  if len(x['titles']) == 0:
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('❌')
    await ctx.reply("You have either not played any games or your Xbox profile is private.")
    return
  sa = 0 #progress variables, set default as 0
  mcc = 0
  ss = 0
  hw = 0
  hw2 = 0
  infinite = 0
  h5 = 0
  games = set(['Halo: The Master Chief Collection', 'Halo Wars: Definitive Edition (PC)', 'Halo Wars 2', 'Halo: Spartan Strike', 'Halo: Spartan Assault', 'Halo Infinite', 'Halo 5: Guardians']) #create set of names of games
  for game in x['titles']: #for each game in the data
    if game['name'] in games: #if the game is in the set
     if game['name'] == 'Halo: The Master Chief Collection': #check for what game and set progress accordingly
             if game['achievement']['progressPercentage'] == 100:
                     mcc = 100
             else:
               if game['achievement']['progressPercentage'] >= mcc:
                     mcc = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars: Definitive Edition (PC)':
             if game['achievement']['progressPercentage'] == 100:
                     hw = 100
             else:
               if game['achievement']['progressPercentage'] >= hw:
                     hw = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Wars 2':
             if game['achievement']['progressPercentage'] == 100:
                     hw2 = 100
             else:
               if game['achievement']['progressPercentage'] >= hw2:
                     hw2 = game['achievement']['progressPercentage']
     if game['name'] == 'Halo: Spartan Strike':
             if game['achievement']['progressPercentage'] == 100:
                     ss = 100
             else:
               if game['achievement']['progressPercentage'] >= ss:
                     ss = game['achievement']['progressPercentage']
     if game['name'] == 'Halo: Spartan Assault':
             if game['achievement']['progressPercentage'] == 100:
                     sa = 100
             else:
               if game['achievement']['progressPercentage'] >= sa:
                     sa = game['achievement']['progressPercentage']
     if game['name'] == 'Halo Infinite':
             if game['achievement']['progressPercentage'] == 100:
                     infinite = 100
             else:
               if game['achievement']['progressPercentage'] >= infinite:
                     infinite = game['achievement']['progressPercentage']
     if game['name'] == 'Halo 5: Guardians':
             if game['achievement']['progressPercentage'] == 100:
                     h5 = 100
             else:
               if game['achievement']['progressPercentage'] >= h5:
                     h5 = game['achievement']['progressPercentage']
  if mcc == 100:
    mccrole = discord.utils.get(ctx.guild.roles, id=764645825392803870)
    await ctx.message.author.add_roles(mccrole)
  if infinite == 100:
    infiniterole = discord.utils.get(ctx.guild.roles, id=914979273608138783)
    await ctx.message.author.add_roles(infiniterole)
  if sa == 100 and ss == 100 and hw == 100 and hw2 == 100 and mcc == 100 and h5 == 100 and infinite == 100: #if all 100, give role
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    mccrole = discord.utils.get(ctx.guild.roles, id=764645825392803870)
    await ctx.message.author.remove_roles(mccrole)
    infiniterole = discord.utils.get(ctx.guild.roles, id=914979273608138783)
    await ctx.message.author.remove_roles(infiniterole)
    xboxrole = discord.utils.get(ctx.guild.roles, id=818247307069882409)
    await ctx.message.author.remove_roles(xboxrole)
    pcrole = discord.utils.get(ctx.guild.roles, id=818247288610357268)
    await ctx.message.author.remove_roles(pcrole)
    await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Halo Completionist! Congrats!")
    await ctx.message.author.add_roles(role)
    return
  else:
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    await ctx.reply("Here\'s your progress on the Halo games:\nHalo Infinite :   **" + str(infinite) + "%**\nMCC :   **" + str(mcc) + "%**\nHalo 5: Guardians :   **" + str(h5) + "%**\nHalo Wars: Definitive Edition :   **" + str(hw) + "%**\nHalo Wars 2 :   **" + str(hw2) + "%**\nHalo: Spartan Assault :   **" + str(sa) +"%**\nHalo: Spartan Strike :   **" + str(ss) + "%**\n\nNote: If you finished everything and did Halo Wars: Definitive Edition and/or Halo: Spartan Assault/Strike on a non-XBL platform, please post your in-game screenshots now and ping a staff member.\n**Spartan Strike achievements are bugged and will always show as 0%, please post a screenshot of completion and ping staff.**")
    return

bot.run(token) #run the bot with the token