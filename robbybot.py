import discord
from discord.ext import commands
import asyncio
import os

bot = commands.Bot(command_prefix='!')
bot.colors = [0xff00fd, 0xc040f0, 0x9a66f3, 0x8779f5, 0x5ea6f9, 0x15ecff]
bot.path = os.getcwd()

if not os.path.exists('./data'): os.mkdir('./data/')

if os.path.isfile('secrets.cfg'): 
    with open('secrets.cfg', 'r') as f: secrets = f.read()
else:
    with open('secrets.cfg', 'w') as f: f.write('##PUT BOT TOKEN HERE##')
    print("Please add your token to 'secrets.cfg' and run again.")
    raise SystemExit(0)

@bot.event
async def on_ready():
    print('[Robbybot] Online')
    i = 1
    for guild in bot.guilds:
        if os.path.exists('./data/' + str(guild.id)):
            print(f'[{guild.name}] data loaded ({i}/{len(bot.guilds)})')
            i += 1
        else:
            os.mkdir('./data/' + str(guild.id))
            with open('data.cfg', 'r') as f: r = f.read()
            with open('./data/' + str(guild.id) + '/data.cfg', 'w') as f:
                f.write(r)
            print(f'[{guild.name}] directory and main config created ({i}/{len(bot.guilds)})')
            i += 1

extensions = ['cogs.rb_mod', 'cogs.rb_admin', 'cogs.rb_autofaq', 'cogs.rb_poll', 'cogs.rb_reminder'] #, 'cogs.rb_ae'
for extension in extensions:
	bot.load_extension(extension)
bot.run(secrets)
