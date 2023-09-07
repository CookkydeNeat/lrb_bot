import discord
from insta import*
import sys
import time
import os

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="uwu"))
    
class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
            @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
            async def button_callback(self, button, interaction):
                await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked

@bot.event
async def on_ready():
    print(f'{bot.user} is online !')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send(f'Hello {message.author.mention}')
        print("!hello triggered, message sent")

    if message.content.startswith('!zizi'):
        await message.channel.send(f'Hello {message.author.mention}')
        print("!hello triggered, message sent")
        
    if message.content.startswith('!stop'):
        await message.channel.send('Goodbye, sir !')
        print("!stop triggered, message sent, turning off")
        sys.exit()
    
    if message.content.startswith('!info') or bot.user.mentioned_in(message):
        await message.channel.send(f'Hello {message.author.mention}, Im active :green_circle:. My ping is {round(bot.latency,2)}ms. Have a nice day !')
        print(f"!info triggered, message sent with {bot.latency}")
        
    if message.content.startswith('!test'):
        rang = 30
        average = 0
        await message.channel.send(f'Hello {message.author.mention}, let`s start our test.')
        for i in range(rang):
            start_time = time.time()
            await message.channel.send(f'Pinging {i+1} on {rang}...')
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            time.sleep(1)
            print(latency)
            average = average + latency
        average = average / rang  
        await message.channel.send(f'The test is finished ! Your average ping is {round(average,3)}ms.')   
        print(f"!test triggered, test finished with an average of {round(average,3)}ms")
        
    if message.content.startswith('!ping'):
        start_time = time.time()
        await message.channel.send(f'Pinging...')
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        await message.channel.send(f'My ping is {round(latency,3)} ms.')
        print(f"!ping triggered, message sent with {round(latency,3)}")
        
    if message.content.startswith('!insta'):
        user = message.content
        user = user.split("!insta ")
        user = user[1]
        post = get_info(user)
        await message.channel.send(f'{user} made {post} post(s)')
        print('!insta triggered, last post sent')
        
    if message.content.startswith('!help'):
        await message.channel.send('This is my commands ! Check it out ! \n **!hello** > the bot answer "hello" \n **!stop** > kill da bot instantly \n **!info or bot mention** > get some infos about the bot \n **!test** > start a ping test \n **!ping** > return current ping')
        print('!help triggered, help message sent')
        
    

bot.run(os.getenv("TOKEN"))
