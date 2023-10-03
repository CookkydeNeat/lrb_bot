#----------------------------------------- import modules -----------------------------------------#

from discord import*
from insta import*
from setup import*
from random import*
import time, discord, sys, asyncio, threading, nest_asyncio, math, os
nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

#----------------------------------------- global variables -----------------------------------------#

at = '@'
an = '&'
lookup = False
setup = False

#----------------------------------------- slash commands -----------------------------------------#

#hello command --------------------------------------------------------------

@tree.command(name = "hello", description = "Say you hello", guild=discord.Object(id=server_id))
async def hello_command(interaction):
    await interaction.response.send_message(f"hello <{at}{interaction.user.id}>")
    print(f'/hello =====> "hello" sent to {interaction.user}')
    asyncio.run(logs_embed(f"Logs : /hello",f"====> \"hello\" sent to {interaction.user}"))


#uwu command --------------------------------------------------------------
    
@tree.command(name = "uwu", description = "Say you uwu", guild=discord.Object(id=server_id)) 
async def uwu_command(interaction):
    await interaction.response.send_message("UwU!")
    print(f'/uwu =====> "uwu" sent to {interaction.user}')
    asyncio.run(logs_embed(f"Logs : /uwu",f"====> \"uwu\" sent to {interaction.user}"))
    
    
#shutdown command --------------------------------------------------------------
    
@tree.command(name = "shutdown", description = "kill da bot", guild=discord.Object(id=server_id)) 
async def shutdown_command(interaction):
    await interaction.response.send_message('Goodbye, sir !')
    asyncio.run(logs_embed(f"Logs : /shutdown",f"====> bot is now offline"))
    sys.exit()
    
        
#info command --------------------------------------------------------------
    
@tree.command(name = "info", description = "get some infos about the bot", guild=discord.Object(id=server_id)) 
async def info_command(interaction):
    global lookup
    if lookup == False:
        await interaction.response.send_message(f'Hello <{at}{interaction.user.id}>, Im active. My ping is {math.floor(bot.latency*1000)} ms. \n Lookup tool is disabled \n Have a nice day !')
    else:
        await interaction.response.send_message(f'Hello <{at}{interaction.user.id}>, Im active. My ping is {math.floor(bot.latency*1000)} ms. \n Lookup tool is enabled \n Have a nice day !')
    print(f'/info =====> infos sent with {round(bot.latency,6)*1000} ms')
    asyncio.run(logs_embed(f"Logs : /info",f"====> infos sent with {round(bot.latency,6)*1000} ms"))
    
    
#start command --------------------------------------------------------------
    
@tree.command(name = "start", description = "start the lookup tool", guild=discord.Object(id=server_id)) 
async def test_command(interaction):
    global lookup
    global setup
    if setup == False:
        await interaction.response.send_message('Please setup targets before using the lookup tool.')
        print(f'/start =====> lookup tool couldn\'t be started')
        asyncio.run(logs_embed(f"Logs : /start",f"====> lookup tool couldn\'t be started"))
    else:
        await interaction.response.send_message('Look-up tool is now active.')
        print(f'/start =====> lookup tool started')
        asyncio.run(logs_embed(f"Logs : /start",f"====> lookup tool started"))
        lookup = True
        asyncio.run(lookup_refresh())
    

#avatar command --------------------------------------------------------------
    
@tree.command(name = "avatar", description = "Return your avatar", guild=discord.Object(id=server_id)) 
async def avatar_command(interaction): 
    await interaction.response.send_message(interaction.user.avatar.url)
    print(f'/avatar =====> avatar sent to {interaction.user}')
    asyncio.run(logs_embed(f"Logs : /avatar",f"====> avatar sent to {interaction.user}"))

    
#debug_command command --------------------------------------------------------------
    
@tree.command(name = "debug", description = "Debug the bot", guild=discord.Object(id=server_id)) 
async def debug_command(interaction):
    await interaction.response.send_message(f'**Debug report** \n lookup state = {lookup} \n setup state = {setup}')
    test_request = debug_request()
    await interaction.channel.send(test_request) 
    test_browser = asyncio.run(debug_pyppeteer())
    await interaction.channel.send(test_browser) 
        
    
#post command --------------------------------------------------------------
    
@tree.command(name = "post", description = "Get the last post of any instagram acount", guild=discord.Object(id=server_id)) 
async def post_command(interaction: discord.Interaction, account: str):
    await interaction.response.send_message("Recherche en cours...")
    last_post = asyncio.run(get_post(account))
    if last_post == "An error has occured, please retry in a few minutes.":
        await interaction.channel.send(f'Cet utilisateur n\'existe pas ou n\'a pas fait de post.')
    else:
        await interaction.channel.send(f'Voici le dernier post de *{account}* : {last_post}')
    print(f'/insta =====> Last post of {account} sent') 
    asyncio.run(logs_embed(f"Logs : /post",f"====> last post of {account} sent"))
    
    
#insta command --------------------------------------------------------------
    
@tree.command(name = "insta", description = "Return any account's post number", guild=discord.Object(id=server_id)) 
async def insta_command(interaction: discord.Interaction, account: str):
    get_posts = get_info(account)
    if get_posts == None:
        await interaction.response.send_message(f" \"{account}\" does not exist, please try again.")
    else:  
        await interaction.response.send_message(f'{account} a fait {get_posts} posts.')
    print(f'/insta =====> Posts sent for account {account}')
    asyncio.run(logs_embed(f"Logs : /insta",f"====> posts sent for account *{account}*"))
    
    
#test command --------------------------------------------------------------
    
@tree.command(name = "test", description = "start the lookup tool", guild=discord.Object(id=server_id)) 
async def test_command(interaction: discord.Interaction, lenght: int):
    average = 0
    if 0 < lenght <= 100:
        await interaction.response.send_message('Pinging...')
        print(f'/test =====> test started with lenght {lenght}')
        asyncio.run(logs_embed(f"Logs : /test",f"====> test started with lenght {lenght}"))
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
        asyncio.run(logs_embed(f"Logs : /test",f"====> test finished with an avarage of {math.floor(average)} ms"))
    else:
        await interaction.response.send_message(f'The value must be beetween 1 and 100.')
        
    
#setup command --------------------------------------------------------------
        
@tree.command(name = "setup", description = "setup the targets of instagram detection", guild=discord.Object(id=server_id)) 
async def setup_command(interaction):
    global setup
    setup_started = await interaction.response.send_message('Setup started, please wait')
    print(f'/setup =====> setup started ({len(accounts)} targets)')
    asyncio.run(logs_embed(f"Logs : /setup",f"====> setup started ({len(accounts)} targets)"))
    loop = len(accounts)
    for i in range(loop):
        target_account = accounts[i]
        target_counter = counters[i]
        post = get_info(target_account)
        counters[i] = post
        await interaction.edit_original_response(content=f"Setup started, please wait ({i+1}/{loop})")
    await interaction.channel.send(f' <{at}{interaction.user.id}>, all targets have been setup.')
    setup = True
    print(f'/setup =====> setup finished')
    asyncio.run(logs_embed(f"Logs : /setup",f"====> setup finished"))
    

#----------------------------------------- bot functions -----------------------------------------#

@bot.event
async def on_ready():
    print(f'{bot.user} is online !')
    await bot.change_presence(activity=discord.Game(name="being coded"))
    await tree.sync(guild=discord.Object(id=server_id))
    channel_logs = log_channel_id
    
async def lookup_refresh():
    await bot.wait_until_ready()
    channel = bot.get_channel(notification_channel_id)
    while True:
        for i in range(len(accounts)):
            target_account = accounts[i]
            target_counter = counters[i]
            print(f'lookup tool =====> user = {target_account}, counter = {target_counter}.')
            asyncio.run(logs_embed(f"Logs : lookup tool",f"====> user = {target_account}, counter = {target_counter}"))
            post = get_info(target_account)
            if post > counters[i]:
                await channel.send(f' {target_account} a une nouvelle publication ! \n {asyncio.run(get_post(target_account))}')
                asyncio.run(logs_embed(f"Logs : lookup tool",f"====> {target_account} a une nouvelle publication"))
                counters[i] += 1
            if post < counters[i]:
                counters[i] -= 1
            await asyncio.sleep(randint(counter_time_min, counter_time_max))
        print(f'lookup tool =====> Turn have been complete. Going back to 0.')
        asyncio.run(logs_embed(f"Logs : lookup tool",f"====> turn have been complete. Going back to 0."))
        
async def logs_embed(command,text):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        log_channel = bot.get_channel(log_channel_id)
        embedVar = discord.Embed(title=command, description=text, color=0x0000ff)
        embedVar.set_footer(text=current_time)
        await log_channel.send(embed=embedVar)
        return

#----------------------------------------- important utilities -----------------------------------------#
  
loop_thread = threading.Thread(target=lambda: asyncio.run(lookup_refresh()))
loop_thread.start()
token = os.getenv("TOKEN")
bot.run(token)