import os
import discord
from discord import member
from discord.ext import commands
from discord.ext.commands import bot_has_permissions
from discord import Member
import json
import requests
import random
from dotenv import load_dotenv
import music

cogs = [music]

activity = discord.Activity(type=discord.ActivityType.listening, name="+help") #create activity instance

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="+", activity=activity, intents=intents, case_insensitive=True) #set prefix to '+' and set the activity 

for i in range(len(cogs)):
  cogs[i].setup(bot)

load_dotenv() #get env variables

token = os.environ['TOKEN']
auth = os.environ['AUTH']
tenor = os.environ['TENOR']

bot.remove_command('help') #delete default help

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.reply("That command doesn't exist! Try +help!")
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.reply(str(error) + ".")

@bot.command(pass_context=True) #help command, send info about the commands
@commands.cooldown(1, 10, commands.BucketType.user)
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

@bot.command(pass_context=True) #cope command, uses tenor api to find a random cope gif
async def cope(ctx):
    print("cope command used - " + str(ctx.message.author)) 
    search_term = "cope"
    lmt = 50
    pos = random.randint(0,140)
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, tenor, lmt, pos))
    if r.status_code == 200:
      gifs = json.loads(r.content)
      random.seed()
      random_index = random.randint(0,len(gifs['results'])-1)
      await ctx.send(gifs['results'][random_index]['url'])

@bot.command(pass_context=True) #based command, uses tenor api to find a random based gif
async def based(ctx):
    print("based command used - " + str(ctx.message.author)) 
    search_term = "based"
    lmt = 50
    pos = random.randint(0,140)
    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s&pos=%s" % (search_term, tenor, lmt, pos))
    if r.status_code == 200:
      gifs = json.loads(r.content)
      random.seed()
      random_index = random.randint(0,len(gifs['results'])-1)
      await ctx.send(gifs['results'][random_index]['url'])

@bot.command(pass_context=True) #count command, sends number of users with each completion role
@commands.cooldown(1, 60, commands.BucketType.user)
async def count(ctx): 
    print("count command used - " + str(ctx.message.author))
    mcc = ctx.guild.get_role(764645825392803870) #get each role
    infinite = ctx.guild.get_role(914979273608138783)
    pc = ctx.guild.get_role(818247288610357268)
    xbox = ctx.guild.get_role(818247307069882409)
    legacy = ctx.guild.get_role(818246915304194058)
    hc = ctx.guild.get_role(818278553187385424)
    await ctx.send("Number of users with each role:\nMCC 100%:   **" + str(len(mcc.members)) + "**\nInfinite 100%:   **" + str(len(infinite.members)) + "**\nPC Master:   **" + str(len(pc.members)) + "**\nModern Xbox Master:   **" + str(len(xbox.members)) + "**\nLegacy Master:   **" + str(len(legacy.members)) + "**\nHalo Completionist:   **" + str(len(hc.members)) + "**") #send counts

@bot.command(pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.user)
async def ce(ctx):
  print("ce command used - " + str(ctx.message.author))
  await ctx.message.add_reaction('🤡')
  await ctx.reply("CE sucks, play literally any other Halo.")

@bot.command(pass_context=True) #mcc command
@commands.cooldown(1, 20, commands.BucketType.user)
async def mcc(ctx):
  print("mcc command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist, which requires MCC.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247307069882409)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Modern Xbox Master, which requires MCC.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247288610357268)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished PC Master, which requires MCC.')
     return
  role = discord.utils.get(ctx.guild.roles, id=764645825392803870) #get mcc role
  role2 = discord.utils.get(ctx.guild.roles, id=764645814677012490)
  if role in ctx.message.author.roles or role2 in ctx.message.author.roles: #if user has role already, do nothing
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
     if game['modernTitleId'] == '1144039928': #if mcc
             if game['achievement']['currentGamerscore'] == 7000: #if complete 
                     await ctx.message.add_reaction('3️⃣') #give them the role and congratulate 
                     await ctx.message.add_reaction('✅')
                     await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished MCC! Congrats!")
                     await ctx.message.author.add_roles(role)
                     return
             else: #not done
                     if ctx.channel.id == 923801105874452580:
                      await ctx.message.delete()
                      return
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('❌') #give progress of game
                     await ctx.reply("Sorry, you haven\'t finished MCC yet. You\'re currently **" + '{:.4g}'.format((game['achievement']['currentGamerscore'])/(game['achievement']['totalGamerscore'])*100) + "%** finished.")
                     return
  await ctx.message.add_reaction('3️⃣') #mcc not in games, they havent played
  await ctx.message.add_reaction('❌')
  await ctx.reply("You haven't played MCC before.")
  return

@bot.command(pass_context=True) #same as mcc but for halo infinite
@commands.cooldown(1, 20, commands.BucketType.user)
async def infinite(ctx):
  print("infinite command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Halo Completionist, which requires Halo Infinite.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247307069882409)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished Modern Xbox Master, which requires Halo Infinite.')
     return
  role = discord.utils.get(ctx.guild.roles, id=818247288610357268)
  if role in ctx.message.author.roles:
     await ctx.reply('You\'ve already finished PC Master, which requires Halo Infinite.')
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
     if game['modernTitleId'] == '2043073184':
             if game['achievement']['currentGamerscore'] == 1600:
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('✅')
                     await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Halo Infinite! Congrats!")
                     await ctx.message.author.add_roles(role)
                     return
             else:
                     if ctx.channel.id == 923801105874452580:
                      await ctx.message.delete()
                      return
                     await ctx.message.add_reaction('3️⃣')
                     await ctx.message.add_reaction('❌')
                     await ctx.reply("Sorry, you haven\'t finished Halo Infinite yet. You\'re currently **" + '{:.4g}'.format((game['achievement']['currentGamerscore'])/(game['achievement']['totalGamerscore'])*100) + "%** finished.")
                     return
  await ctx.message.add_reaction('3️⃣')
  await ctx.message.add_reaction('❌')
  await ctx.reply("You haven't played Halo Infinite before.")
  return

@bot.command(pass_context=True) #ban command, bans a user for given reason
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason, *args):
 print("ban command used - " + str(ctx.message.author))
 user = await bot.fetch_user(member.id)
 if len(args) != 0:
  reason += ' '
  reason += ' '.join(args)
 try:
    await member.send(content=f"You have been banned from {ctx.guild}.\nReason: {reason}\nYou can appeal here: <https://forms.gle/QP62ibaP8GvZMzbM8>")
    await member.ban(reason=reason)
    await ctx.message.add_reaction('✅')
    await ctx.reply("This user has been banned.")
 except Exception:
    await member.ban(reason=reason)
    await ctx.message.add_reaction('✅')
    await ctx.reply("This user has been banned, but we couldn't dm the reason.")  

@ban.error #checks for issues with ban command
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+ban user reason**')

@bot.command(pass_context=True) #unban command, unbans specified user
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
 print("unban command used - " + str(ctx.message.author))
 user = await bot.fetch_user(id)
 try:
   await user.send(content=f"You have been unbanned from {ctx.guild}.\nJoin back if you'd like: https://discord.gg/UHwtz8rQse")
   await ctx.message.add_reaction('✅')
   await ctx.reply("This user has been unbanned.")
   await ctx.guild.unban(user)
 except:
   await ctx.message.add_reaction('✅')
   await ctx.reply("This user has been unbanned, but we couldn't let them know.")
   await ctx.guild.unban(user)

@unban.error #checks for issues with unban command
async def unban_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+unban user**')

@bot.command(pass_context=True) #kick command
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason, *args):
 print("kick command used - " + str(ctx.message.author))
 user = await bot.fetch_user(member.id)
 if len(args) != 0:
  reason += ' '
  reason += ' '.join(args)
 try:
    await member.send(content=f"You have been kicked from {ctx.guild}.\nReason: {reason}")
    await member.kick(reason=reason)
    await ctx.message.add_reaction('✅')
    await ctx.reply("This user has been kicked.")
 except:
    await member.kick(reason=reason)
    await ctx.message.add_reaction('✅')
    await ctx.reply("This user has been kicked, but we couldn't dm the reason.")  

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+kick user reason**')

@bot.command(pass_context=True) #warn command, puts warning in database
@commands.has_permissions(ban_members=True)
async def warn(ctx, member: discord.Member, reason, *args):
 print("warn command used - " + str(ctx.message.author))
 user = await bot.fetch_user(member.id)
 if len(args) != 0:
  reason += ' '
  reason += ' '.join(args)
 idstring = str(user.id)
 db={} #make empty database 
 try: #try loading something from the database
    f=open("warnings.json")
    db=json.load(f) #set dict to db
    f.close()
 except:
    pass #keep db as empty dict
 db.setdefault(idstring, []).append(reason)
 f=open("warnings.json", "w") #write to warnings.json
 json.dump(db, f)
 f.close()
 try:
   await user.send(content=f"You have been warned in {ctx.guild}.\nReason: {reason} ")
   await ctx.message.add_reaction('✅')
   await ctx.reply("This user has been warned.")
 except:
   await ctx.message.add_reaction('✅')
   await ctx.reply("This user has their direct messages off, but the warning has been added to their history.")

@warn.error
async def warn_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply('Incorrect arguments entered | **+warn user reason**')

@bot.command(pass_context=True) #warns command, gets warnings for specified user
@commands.has_permissions(ban_members=True)
async def warns(ctx, member: discord.Member):
 print("warns command used - " + str(ctx.message.author))
 user = await bot.fetch_user(member.id)
 idstring = str(user.id)
 db={} #make empty database 
 try: #try loading something from the database
    f=open("warnings.json")
    db=json.load(f) #set dict to db
    f.close()
 except:
    pass #keep db as empty dict
 if idstring in db.keys():
   if len(db[idstring]) == 0:
     await ctx.reply("This user has no warnings.")
   else:
     i=1
     response = ''
     for warning in db[idstring]:
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
async def rmwarn(ctx, member: discord.Member, warnnum):
 print("rmwarn command used - " + str(ctx.message.author))
 user = await bot.fetch_user(member.id)
 idstring = str(user.id)
 warnnum = int(warnnum) - 1
 db={} #make empty database 
 try: #try loading something from the database
    f=open("warnings.json")
    db=json.load(f) #set dict to db
    f.close()
 except:
    pass #keep db as empty dict
 if idstring in db.keys():
   if len(db[idstring]) == 0:
     await ctx.reply("This user has no warnings to remove.")
   else:
     try:
      del db[idstring][warnnum]
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
@commands.cooldown(1, 10, commands.BucketType.user)
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
@commands.cooldown(1, 20, commands.BucketType.user)
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
      ce = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo Wars':
      hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo 3':
      h3 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo: Reach':
       hr = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo 4':
       h4 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo 3: ODST Campaign Edition':
       odst = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
  if h3 == 100 and h4 == 100 and odst == 100 and hr == 100 and ce == 100 and hw == 100: #if all 100, give role
    await ctx.message.add_reaction('3️⃣')
    await ctx.message.add_reaction('✅')
    await ctx.reply("Hey everyone! " + str(ctx.message.author.display_name) + " finished Legacy Master! Congrats!")
    await ctx.message.author.add_roles(role)
    return
  else:
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    await ctx.reply("Here\'s your progress on the legacy games:\n\nHalo 3 :   **" + '{:.4g}'.format(h3) + "%**\nHalo Wars :   **" + '{:.4g}'.format(hw) + "%**\nHalo 3: ODST :   **" + '{:.4g}'.format(odst) + "%**\nHalo: Reach :   **" + '{:.4g}'.format(hr) +"%**\nHalo: Combat Evolved Anniversary :   **" + '{:.4g}'.format(ce) + "%**\nHalo 4 :   **" + '{:.4g}'.format(h4) + "%**")
    return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
@commands.cooldown(1, 20, commands.BucketType.user)
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
             if game['achievement']['currentGamerscore'] == 7000:
                     mcc = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= mcc:
                     mcc = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo Wars: Definitive Edition (PC)':
             if game['achievement']['currentGamerscore'] == 1500:
                     hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= hw:
                     hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo Wars 2':
             if game['achievement']['currentGamerscore'] == 1750:
                     hw2 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= hw2:
                     hw2 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo 5: Guardians':
             if game['achievement']['currentGamerscore'] == 1250:
                     h5 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= h5:
                     h5 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo: Spartan Assault':
             if game['achievement']['progressPercentage'] == 100 and game['achievement']['totalGamerscore'] != 0:
                     sa = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             elif game['achievement']['totalGamerscore'] != 0:
               if game['achievement']['progressPercentage'] >= sa:
                     sa = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               sa = -1
     if game['name'] == 'Halo Infinite':
             if game['achievement']['currentGamerscore'] == 1600:
                     infinite = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= infinite:
                     infinite = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
  role2 = discord.utils.get(ctx.guild.roles, id=764645814677012490)
  if mcc == 100 and role2 not in ctx.message.author.roles:
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
    if sa == -1:
      sa = "Your SA achievements are bugged. Please post an in-game screenshot and ping staff."
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    if type(sa) is not str:
      await ctx.reply("Here\'s your progress on the Modern Xbox games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo 5: Guardians :   **" + '{:.4g}'.format(h5) +"%**\nHalo: Spartan Assault :   **" + '{:.4g}'.format(sa) + "%**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return
    else:
      await ctx.reply("Here\'s your progress on the Modern Xbox games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo 5: Guardians :   **" + '{:.4g}'.format(h5) +"%**\nHalo: Spartan Assault :   **" + sa + "%**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
@commands.cooldown(1, 20, commands.BucketType.user)
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
                     mcc = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= mcc:
                     mcc = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo Wars: Definitive Edition (PC)':
             if game['achievement']['progressPercentage'] == 100:
                     hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= hw:
                     hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo Wars 2':
             if game['achievement']['progressPercentage'] == 100:
                     hw2 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= hw2:
                     hw2 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
     if game['name'] == 'Halo: Spartan Strike':
             if game['achievement']['progressPercentage'] == 100 and game['achievement']['totalGamerscore'] != 0:
                     ss = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             elif game['achievement']['totalGamerscore'] != 0:
               if game['achievement']['progressPercentage'] >= ss:
                     ss = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               ss = -1
     if game['name'] == 'Halo: Spartan Assault':
             if game['achievement']['progressPercentage'] == 100 and game['achievement']['totalGamerscore'] != 0:
                     sa = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             elif game['achievement']['totalGamerscore'] != 0:
               if game['achievement']['progressPercentage'] >= sa:
                     sa = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               sa = -1
     if game['name'] == 'Halo Infinite':
             if game['achievement']['progressPercentage'] == 100:
                     infinite = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
             else:
               if game['achievement']['progressPercentage'] >= infinite:
                     infinite = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
  role2 = discord.utils.get(ctx.guild.roles, id=764645814677012490)
  if mcc == 100 and role2 not in ctx.message.author.roles:
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
    if sa == -1:
      sa = "Your SA achievements are bugged. Please post an in-game screenshot and ping staff."
    if ss == -1:
      ss = "Your SS achievements are bugged. Please post an in-game screenshot and ping staff."
    await ctx.message.add_reaction('3️⃣') #not all 100, give stats
    await ctx.message.add_reaction('❌')
    if type(ss) is not str and type(sa) is not str:
      await ctx.reply("Here\'s your progress on the PC games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo: Spartan Assault :   **" + '{:.4g}'.format(sa) +"%**\nHalo: Spartan Strike :   **" + '{:.4g}'.format(ss) + "%**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return
    if type(sa) is str and type(ss) is not str:
      await ctx.reply("Here\'s your progress on the PC games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo: Spartan Assault :   **" + sa +"%**\nHalo: Spartan Strike :   **" + '{:.4g}'.format(ss) + "%**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return
    else:
      await ctx.reply("Here\'s your progress on the PC games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo: Spartan Assault :   **" + '{:.4g}'.format(sa) +"%**\nHalo: Spartan Strike :   **" + ss + "**\n\nNote: If you finished everything and played any game on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return

@bot.command(pass_context=True) #legacy command, same as mcc but has to check multiple games
@commands.cooldown(1, 20, commands.BucketType.user)
async def hc(ctx):
  print("hc command used - " + str(ctx.message.author))
  role = discord.utils.get(ctx.guild.roles, id=818278553187385424)
  if role in ctx.message.author.roles:
    await ctx.reply('You\'ve already finished Halo Completionist.')
    return
  role2 = discord.utils.get(ctx.guild.roles, id=818247288610357268)
  role3 = discord.utils.get(ctx.guild.roles, id=818247307069882409)
  if role2 in ctx.message.author.roles and role3 in ctx.message.author.roles:
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
                      mcc = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                if game['achievement']['progressPercentage'] >= mcc:
                      mcc = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
      if game['name'] == 'Halo Wars: Definitive Edition (PC)':
              if game['achievement']['progressPercentage'] == 100:
                      hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                if game['achievement']['progressPercentage'] >= hw:
                      hw = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
      if game['name'] == 'Halo Wars 2':
              if game['achievement']['progressPercentage'] == 100:
                      hw2 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                if game['achievement']['progressPercentage'] >= hw2:
                      hw2 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
      if game['name'] == 'Halo: Spartan Strike':
              if game['achievement']['progressPercentage'] == 100 and game['achievement']['totalGamerscore'] != 0:
                      ss = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              elif game['achievement']['totalGamerscore'] != 0:
                if game['achievement']['progressPercentage'] >= ss:
                      ss = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                ss = -1
      if game['name'] == 'Halo: Spartan Assault':
              if game['achievement']['progressPercentage'] == 100 and game['achievement']['totalGamerscore'] != 0:
                      sa = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              elif game['achievement']['totalGamerscore'] != 0:
                if game['achievement']['progressPercentage'] >= sa:
                      sa = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                sa = -1
      if game['name'] == 'Halo Infinite':
              if game['achievement']['progressPercentage'] == 100:
                      infinite = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                if game['achievement']['progressPercentage'] >= infinite:
                      infinite = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
      if game['name'] == 'Halo 5: Guardians':
              if game['achievement']['progressPercentage'] == 100:
                      h5 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
              else:
                if game['achievement']['progressPercentage'] >= h5:
                      h5 = (game['achievement']['currentGamerscore']/game['achievement']['totalGamerscore'])*100
  role2 = discord.utils.get(ctx.guild.roles, id=764645814677012490)
  if mcc == 100 and role2 not in ctx.message.author.roles:
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
    if sa == -1:
      sa = "Your SA achievements are bugged. Please post an in-game screenshot and ping staff."
    if ss == -1:
      ss = "Your SS achievements are bugged. Please post an in-game screenshot and ping staff."
    if type(ss) is not str and type(sa) is not str:
      await ctx.reply("Here\'s your progress on the Halo games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo 5: Guardians :   **" + '{:.4g}'.format(h5) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo: Spartan Assault :   **" + '{:.4g}'.format(sa) +"%**\nHalo: Spartan Strike :   **" + '{:.4g}'.format(ss) + "%**\n\nNote: If you finished everything and did Halo Wars: Definitive Edition and/or Halo: Spartan Assault/Strike on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return
    if type(sa) is str and type(ss) is not str:
      await ctx.reply("Here\'s your progress on the Halo games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo 5: Guardians :   **" + '{:.4g}'.format(h5) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo: Spartan Assault :   **" + sa +"%**\nHalo: Spartan Strike :   **" + '{:.4g}'.format(ss) + "**\n\nNote: If you finished everything and did Halo Wars: Definitive Edition and/or Halo: Spartan Assault/Strike on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return
    else:
      await ctx.reply("Here\'s your progress on the Halo games:\n\nHalo Infinite :   **" + '{:.4g}'.format(infinite) + "%**\nMCC :   **" + '{:.4g}'.format(mcc) + "%**\nHalo 5: Guardians :   **" + '{:.4g}'.format(h5) + "%**\nHalo Wars: Definitive Edition :   **" + '{:.4g}'.format(hw) + "%**\nHalo Wars 2 :   **" + '{:.4g}'.format(hw2) + "%**\nHalo: Spartan Assault :   **" + '{:.4g}'.format(sa) +"%**\nHalo: Spartan Strike :   **" + ss + "**\n\nNote: If you finished everything and did Halo Wars: Definitive Edition and/or Halo: Spartan Assault/Strike on a non-XBL platform, please post your in-game screenshots now and ping a staff member.")
      return

bot.run(token) #run the bot with the token