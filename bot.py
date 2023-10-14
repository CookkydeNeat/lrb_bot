#----------------------------------------- import modules -----------------------------------------#

from discord import*
from insta import*
from setup import*
from random import*
import time, discord, sys, asyncio, threading, nest_asyncio, math, os

#----------------------------------------- initializing discord bridge -----------------------------------------#

nest_asyncio.apply()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

#----------------------------------------- global variables -----------------------------------------#

at = '@'
lookup = False
setup = False
logs = 1

#----------------------------------------- slash commands -----------------------------------------#
# hello command --------------------------------------------------------------

@tree.command(name="hello", description="Say you *hello*", guild=discord.Object(id=server_id))
async def hello_command(interaction):
  await interaction.response.send_message(f"hello <{at}{interaction.user.id}>")
  asyncio.run(logs_embed(f"Logs : /hello", f"====> \"hello\" sent to {interaction.user}"))


# uwu command --------------------------------------------------------------

@tree.command(name="uwu", description="Say you *uwu*", guild=discord.Object(id=server_id))
async def uwu_command(interaction):
  await interaction.response.send_message("UwU!")
  asyncio.run(logs_embed(f"Logs : /uwu", f"====> \"uwu\" sent to {interaction.user}"))


# shutdown command --------------------------------------------------------------

@tree.command(name="shutdown", description="Kill da bot", guild=discord.Object(id=server_id))
async def shutdown_command(interaction):
  await interaction.response.send_message('Goodbye, sir !')
  asyncio.run(logs_embed(f"Logs : /shutdown", f"====> bot is now offline"))
  sys.exit()


# info command --------------------------------------------------------------

@tree.command(name="info",  description="Get some infos about the bot", guild=discord.Object(id=server_id))
async def info_command(interaction):
  global lookup
  if lookup == False:
    await interaction.response.send_message(f'Hello <{at}{interaction.user.id}>, Im active. My ping is {math.floor(bot.latency*1000)} ms. \n Lookup tool is disabled \n Have a nice day !')
  else:
    await interaction.response.send_message(f'Hello <{at}{interaction.user.id}>, Im active. My ping is {math.floor(bot.latency*1000)} ms. \n Lookup tool is enabled \n Have a nice day !')
  asyncio.run(logs_embed(f"Logs : /info", f"====> infos sent with {round(bot.latency,6)*1000} ms"))


# start command --------------------------------------------------------------

@tree.command(name="start", description="Start the lookup tool", guild=discord.Object(id=server_id))
async def start_command(interaction):
  global lookup
  if setup == False:
    await interaction.response.send_message('Please setup targets before using the lookup tool.')
    asyncio.run(logs_embed(f"Logs : /start",f"====> lookup tool couldn\'t be started"))
  else:
    await interaction.response.send_message('Look-up tool is now active.')
    asyncio.run(logs_embed(f"Logs : /start", f"====> lookup tool started"))
    lookup = True
    asyncio.run(lookup_refresh())


# avatar command --------------------------------------------------------------

@tree.command(name="avatar", description="Return your avatar", guild=discord.Object(id=server_id))
async def avatar_command(interaction):
  await interaction.response.send_message(interaction.user.avatar.url)
  print(f'/avatar =====> avatar sent to {interaction.user}')
  asyncio.run(logs_embed(f"Logs : /avatar", f"====> avatar sent to {interaction.user}"))


# debug_command command -------------------------------------------------------------

@tree.command(name="debug", description="Debug the bot", guild=discord.Object(id=server_id))
async def debug_command(interaction):
  await interaction.response.send_message(f'**Debug report** \nlookup state = {lookup} \nsetup state = {setup} \npost counters = {counters}\nlogs stats = {logs}')


# logs_states command --------------------------------------------------------------

@tree.command(name="logs", description="Set the logs states", guild=discord.Object(id=server_id))
async def logs_states(interaction: discord.Interaction, state: int):
  global logs 
  if state == 0:
    await interaction.response.send_message(f'Logs are now : *off*')
    asyncio.run(logs_embed(f"Logs : /logs", f"====> Logs are now *off*"))
    logs = 0
    asyncio.run(logs_embed(f"Logs : /logs", f"====> Logs are now off"))
  elif state == 1:
    await interaction.response.send_message(f'Logs are now : *on*')
    logs = 1
    asyncio.run(logs_embed(f"Logs : /logs", f"====> Logs are now *on*"))
  else:
    await interaction.response.send_message(f'Please try again.')


# post command --------------------------------------------------------------

@tree.command(name="post", description="Get the last post of any instagram acount", guild=discord.Object(id=server_id))
async def post_command(interaction: discord.Interaction, account: str):
  await interaction.response.send_message("Recherche en cours...")
  last_post = get_post(account)
  await interaction.channel.send(f'Voici le dernier post de *{account}* : {last_post}')
  asyncio.run(logs_embed(f"Logs : /post", f"====> last post of {account} sent"))


# insta command --------------------------------------------------------------

@tree.command(name="insta", description="Return any account's post number", guild=discord.Object(id=server_id))
async def insta_command(interaction: discord.Interaction, account: str):
  await interaction.response.send_message(f'{account} a fait {get_info(account)} posts.')
  asyncio.run(logs_embed(f"Logs : /insta", f"====> posts sent for account *{account}*"))


# test command --------------------------------------------------------------

@tree.command(name="test",description="Start the ping test", guild=discord.Object(id=server_id))
async def test_command(interaction: discord.Interaction, lenght: int):
  average = 0
  if 0 < lenght <= 100:
    await interaction.response.send_message('Pinging...')
    asyncio.run(logs_embed(f"Logs : /test", f"====> test started with lenght {lenght}"))
    for i in range(lenght):
      start_time = time.time()
      await interaction.edit_original_response(content=f'Pinging {i+1} on {lenght}...')
      end_time = time.time()
      latency = (end_time - start_time) * 1000
      time.sleep(1)
      average = average + latency
    average = average / lenght
    await interaction.channel.send(f'The test is finished ! <{at}{interaction.user.id}>, our average ping is {math.floor(average)}ms.')
    asyncio.run(logs_embed(f"Logs : /test",f"====> test finished with an avarage of {math.floor(average)} ms"))
  else:
    await interaction.response.send_message(f'The value must be beetween 1 and 100.')


# setup command --------------------------------------------------------------

@tree.command(name="setup", description=">Setup the targets of instagram detection", guild=discord.Object(id=server_id))
async def setup_command(interaction):
  global setup
  await interaction.response.send_message('Setup started, please wait')
  asyncio.run(logs_embed(f"Logs : /setup", f"====> setup started ({len(accounts)} targets)"))
  for i in range(len(accounts)):
    post = get_info(str(accounts[i]))
    counters[i] = post
    time.sleep(1)
    await interaction.edit_original_response(content=f"Setup started, please wait ({i+1}/{len(accounts)})")
  await interaction.channel.send(f' <{at}{interaction.user.id}>, all targets have been setup.')
  setup = True
  asyncio.run(logs_embed(f"Logs : /setup", f"====> setup finished"))
    

#----------------------------------------- bot functions -----------------------------------------#

@bot.event
async def on_ready():
  print(f'{bot.user} is online !')
  await bot.change_presence(activity=discord.Game(name="En ligne"))
  await tree.sync(guild=discord.Object(id=server_id))
  channel_logs = log_channel_id
    
async def lookup_refresh():
  await bot.wait_until_ready()
  channel = bot.get_channel(notification_channel_id)
  while True:
    await asyncio.sleep(randint(counter_time_min, counter_time_max))
    for i in range(len(accounts)):
      asyncio.run(logs_embed(f"Logs : lookup tool", f"====> user = {accounts[i]}, counter = {counters[i]}"))
      post = get_info(accounts[i])
      await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{accounts[i]}"))
      if post > counters[i]:
        await channel.send(f' {accounts[i]} a une nouvelle publication ! \n {asyncio.run(get_post(accounts[i]))}')
        asyncio.run(logs_embed(f"Logs : lookup tool", f"====> {accounts[i]} posted a new photo !"))
        counters[i] += 1
      if post < counters[i]:
        counters[i] -= 1
      await asyncio.sleep(randint(counter_time_min/20, counter_time_max/20))

async def logs_embed(command, text):
  global logs
  if logs == 0:
    current_time = time.strftime("%H:%M:%S -- ", time.localtime())
    print (current_time + command, text)
  elif logs == 1:
    channel_logs = log_channel_id
    await bot.wait_until_ready()
    current_time = time.strftime("%H:%M:%S", time.localtime())
    log_channel = bot.get_channel(log_channel_id)
    embedVar = discord.Embed(title=command, description=text, color=0x5765f2)
    embedVar.set_footer(text=current_time, icon_url=bot.user.avatar.url)
    await log_channel.send(embed=embedVar)


#----------------------------------------- important utilities -----------------------------------------#
  
loop_thread = threading.Thread(target=lambda: asyncio.run(lookup_refresh()))
loop_thread.start()
token = os.getenv("TOKEN")
bot.run(token)