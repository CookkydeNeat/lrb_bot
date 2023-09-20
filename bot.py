# ----------------------------------------- import modules -----------------------------------------#

from discord import *
from insta import *
from setup import *
from dotenv import *
import time
import discord
import sys
import asyncio
import threading
import nest_asyncio
import math
import os
nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# ----------------------------------------- global variables -----------------------------------------#

at = '@'
an = '&'
load_dotenv()
token = os.getenv("TOKEN")

# async def slash3(interaction: discord.Interaction, number: int):

# ----------------------------------------- slash commands -----------------------------------------#

# hello command -----------------------------------------


@tree.command(name="hello", description="Say you hello", guild=discord.Object(id=server_id))
async def hello_command(interaction):
    await interaction.response.send_message(f"hello <{at}{interaction.user.id}>")
    print(f'/hello =====> "hello" sent to {interaction.user}')


# uwu command -----------------------------------------
@tree.command(name="uwu", description="Say you uwu", guild=discord.Object(id=server_id))
async def uwu_command(interaction):
    await interaction.response.send_message("UwU!")
    print(f'/uwu =====> "uwu" sent to {interaction.user}')


# shutdown command -----------------------------------------
@tree.command(name="shutdown", description="kill da bot", guild=discord.Object(id=server_id))
async def shutdown_command(interaction):
    await interaction.response.send_message('Goodbye, sir !')
    sys.exit()


# info command -----------------------------------------
@tree.command(name="info", description="get some infos about the bot", guild=discord.Object(id=server_id))
async def info_command(interaction):
    await interaction.response.send_message(f'Hello <{at}{interaction.user.id}>, Im active. My ping is {math.floor(bot.latency*1000)} ms. Have a nice day !')
    print(f'/info =====> infos sent with {round(bot.latency,6)*1000} ms')


# start command -----------------------------------------
@tree.command(name="start", description="start the lookup tool", guild=discord.Object(id=server_id))
async def start_command(interaction):
    await interaction.response.send_message('Look-up tool is now active.')
    print(f'/start =====> lookup tool started')
    asyncio.run(periodic_task())


# avatar command -----------------------------------------
@tree.command(name="avatar", description="Return your avatar", guild=discord.Object(id=server_id))
async def avatar_command(interaction: discord.Interaction, account: str):
    await interaction.response.send_message(interaction.user.avatar.url)
    print(f'/avatar =====> avatar sent to {interaction.user}')


# insta command -----------------------------------------
@tree.command(name="insta", description="Return any account's post number", guild=discord.Object(id=server_id))
async def insta_command(interaction: discord.Interaction, account: str):
    target = get_info(account)
    if target == None:
        await interaction.response.send_message("This account does not exist, please try again.")
    else:
        await interaction.response.send_message(f'{account} a fait {target} posts.')
    print(f'/insta =====> Posts sent for account {account}')


# test command -----------------------------------------
@tree.command(name="test", description="start the lookup tool", guild=discord.Object(id=server_id))
async def test_command(interaction: discord.Interaction, lenght: int):
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
        print(
            f'/test =====> test finished with an avarage of {math.floor(average)} ms')
    else:
        await interaction.response.send_message(f'The value must be beetween 1 and 100.')


# setup command -----------------------------------------
@tree.command(name="setup", description="setup the targets of instagram detection", guild=discord.Object(id=server_id))
async def setup_command(interaction):
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

# ----------------------------------------- bot functions -----------------------------------------#


@bot.event
async def on_ready():
    print(f'{bot.user} is online !')
    await bot.change_presence(activity=discord.Game(name="being coded"))
    await tree.sync(guild=discord.Object(id=server_id))
    # PLEASE DON'T LOG THE TOKEN FOR OBVIOUS SECURITY REASONS


async def lookup_refresh(interval, stop_event):
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)

    try:
        while not stop_event.is_set():
            for i, target_account in enumerate(accounts):
                target_counter = counters[i]
                print(f'lookup tool =====> user = {target_account}, counter = {target_counter}')
                
                posts = get_info(target_account)

                if posts is None:
                    await channel.send(f"This account does not exist or is innaccessible: {target_account}")
                    continue
                
                if posts > counters[i]:
                    new_post = await get_post(target_account)

                    if new_post.startswith("An error"):
                        await channel.send(f"An error occurred while accessing the account {target_account}...")
                        continue
                    else:
                        print(f'lookup tool =====> {target_account} have a new post {new_post}')
                        await channel.send(f'{target_account} has a new post! \n {new_post}')
                    
                    counters[i] = posts
                elif posts < counters[i]:
                    counters[i] = posts
                await asyncio.sleep(interval)

            print(f'lookup tool =====> Turn has been completed. Going back to 0.')

    except asyncio.CancelledError:
        print("Lookup tool has been canceled.")
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping the task...")
        stop_event.set()  # Set the stop event to stop the task
    except Exception as e:
        print("Something went wrong:", e)
        await channel.send("Something went wrong:"+repr(e))
        await channel.send("Lookup tool stopped")



async def periodic_task():
    interval = 60*5  # Run the task every 5 minutes
    stop_event = asyncio.Event()
    
    # Create a task for the periodic task
    task = asyncio.create_task(lookup_refresh(interval, stop_event))
    
    try:
        await task  # Wait for the task to complete (Ctrl+C to stop)
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping the task...")
        stop_event.set()  # Set the stop event to stop the task
        await task  # Wait for the task to be canceled

# ----------------------------------------- important utilities -----------------------------------------#

async def delete_after(msg):
    asyncio.sleep(10)
    await msg.delete()

def obfuscate_token(token):
    obfuscated_token = list(token)
    for index, _ in enumerate(obfuscated_token):
        if index > len(obfuscated_token)/2:
            obfuscated_token[index] = "*"
    if obfuscated_token == "":
        obfuscated_token = "EMPTY"
    if obfuscated_token == None:
        obfuscated_token = "NONE"
    obfuscated_token = ''.join(obfuscated_token)
    return obfuscated_token


# Try to log
try:
    bot.run(token)
except:
    obfuscated_token = obfuscate_token(token)
    # PLEASE DON'T LOG THE TOKEN FOR OBVIOUS SECURITY REASONS
    print(f"Could not connect with: {obfuscated_token}")
