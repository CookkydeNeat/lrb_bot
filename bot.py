#----------------------------------------- import modules -----------------------------------------#

from discord import*
from insta import*
from setup import*
import requests, json, time, discord, sys, asyncio, threading, nest_asyncio, math
nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

#----------------------------------------- global variables -----------------------------------------#

at = '@'
an = '&'

# async def slash3(interaction: discord.Interaction, number: int):   

#----------------------------------------- slash commands -----------------------------------------#

#hello command
@tree.command(name = "hello", description = "Say you hello", guild=discord.Object(id=1026168999173697647))
async def first_command(interaction):
    await interaction.response.send_message(f"hello <{at}{interaction.user.id}>")
    print(f'/hello =====> "hello" sent to {interaction.user}')

#uwu command
@tree.command(name = "uwu", description = "Say you uwu", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction):
    await interaction.response.send_message("UwU!")
    print(f'/uwu =====> "uwu" sent to {interaction.user}')
    
#shutdown command
@tree.command(name = "shutdown", description = "kill da bot", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction):
    await interaction.response.send_message('Goodbye, sir !')
    sys.exit()
        
#info command
@tree.command(name = "info", description = "get some infos about the bot", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction):
    await interaction.response.send_message(f'Hello <{at}{interaction.user.id}>, Im active. My ping is {math.floor(bot.latency*1000)} ms. Have a nice day !')
    print(f'/info =====> infos sent with {round(bot.latency,6)*1000} ms')
    
#start command
@tree.command(name = "start", description = "start the lookup tool", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction):
    await interaction.response.send_message('Look-up tool is now active.')
    print(f'/start =====> lookup tool started')
    asyncio.run(lookup_refresh())

#avatar command
@tree.command(name = "avatar", description = "Return your avatar", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction):
    await interaction.response.send_message(interaction.user.avatar.url)
    print(f'/avatar =====> avatar sent to {interaction.user}')
    
#insta command
@tree.command(name = "insta", description = "Return any account's post number", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction: discord.Interaction, account: str):
    if target == None:
        await interaction.response.send_message("This account does not exist, please try again.")
    else:  
        await interaction.response.send_message(f'{account} a fait {target} posts.')
    print(f'/insta =====> Posts sent for account {account}')
    
#test command
@tree.command(name = "test", description = "start the lookup tool", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction: discord.Interaction, lenght: int):
    average = 0
    if 0 < lenght <= 100:
        await interaction.response.send_message('Pinging...')
        print(f'/test =====> test started with lenght {lenght}')
        for i in range(lenght):
            start_time = time.time()
            await interaction.edit_original_response(content=f'Pinging {i+1} on {lenght}...')
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            time.sleep(1)
            average = average + latency
        average = average / lenght  
        await interaction.channel.send(f'The test is finished ! <{at}{interaction.user.id}>, our average ping is {math.floor(average)}ms.')   
        print(f'/test =====> test finished with an avarage of {math.floor(average)} ms')
    else:
        await interaction.response.send_message(f'The value must be beetween 1 and 100.')
    
#setup command
@tree.command(name = "setup", description = "setup the targets of instagram detection", guild=discord.Object(id=1026168999173697647)) 
async def first_command(interaction):
    setup_started = await interaction.response.send_message('Setup started, please wait')
    print(f'/setup =====> setup started ({len(accounts)} targets)')
    loop = len(accounts)
    for i in range(loop):
        target_account = accounts[i]
        target_counter = counters[i]
        post = get_info(target_account)
        counters[i] = post
        await interaction.edit_original_response(content=f"Setup started, please wait ({i+1}/{loop})")
    await interaction.channel.send(f' <{at}{interaction.user.id}>, all targets have been setup.')
    print(f'/setup =====> setup finished')

#----------------------------------------- bot functions -----------------------------------------#

@bot.event
async def on_ready():
    print(f'{bot.user} is online !')
    await bot.change_presence(activity=discord.Game(name="being coded"))
    await tree.sync(guild=discord.Object(id=1026168999173697647))
    
async def lookup_refresh():
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    while True:
        for i in range(len(accounts)):
            target_account = accounts[i]
            target_counter = counters[i]
            print(f'lookup tool =====> user = {target_account}, counter = {target_counter}')
            post = get_info(target_account)
            if post > counters[i]:
                await channel.send(f' {target_account} a une nouvelle publication ! \n {asyncio.run(get_post(target_account))}')
                counters[i] += 1
            if post < counters[i]:
                counters[i] -= 1
                asyncio.run(lookup_refresh(i))
            await asyncio.sleep(180)
    print(f'lookup tool =====> Turn have been complete. Going back to 0.')

#----------------------------------------- important utilities -----------------------------------------#
  
loop_thread = threading.Thread(target=lambda: asyncio.run(lookup_refresh()))
loop_thread.start()
bot.run(token)