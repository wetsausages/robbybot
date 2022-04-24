import discord
from discord.ext import commands
import json
import random
import datetime
from datetime import datetime as date

class FAQCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):		
		with open(self.bot.path + '/data/' + str(message.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		if cfg['FAQ']['Toggle'] == 'off': return
		keyword = cfg['FAQ']['KeyResponse']
		max_days = cfg['FAQ']['MaxDays']

		#Checks
		if message.author == self.bot.user: return #if bot
		member_for = date.today() - message.author.joined_at #if they author isnt new enough
		if member_for.days > int(max_days): return
		if len(message.content) > 0:
			if message.content[0] == self.bot.command_prefix: return #if command
		else: return #if image

		blocks = message.content.replace(',','.').replace(';','.').replace('-','.').split('.')
		for block in blocks:
			heard_key = None
			block = block.replace('?', '')
			chunks = block.split(' ')
			for chunk in chunks:
				chunk = chunk.lower()
				if chunk in keyword.keys(): 
					await build_embed(self, message, 'RB FAQ', desc=keyword.get(chunk), footer=f'You\'ll stop recieving these tips in {((message.author.joined_at + datetime.timedelta(days=(int(max_days)))) - date.today()).days} days!', delete=5)
					return

async def build_embed(self, message, title='', desc='', fields=[], footer='', delete=0):
	colors = self.bot.colors
	if colors != []:
		if title != '':
			if desc != '': embed = discord.Embed(title=title, description=desc, color=colors[random.randint(0,len(colors)-1)])
			else: embed = discord.Embed(title=title, color=colors[random.randint(0,len(colors)-1)])
		else:
			if desc != '':  embed = discord.Embed(description=desc, color=colors[random.randint(0,len(colors)-1)])
	else:
		if title != '':
			if desc != '': embed = discord.Embed(title=title, description=desc)
			else: embed = discord.Embed(title=title)
		else:
			if desc != '': embed = discord.Embed(description=desc)

	for field in fields:
		chunks = field.split('|')
		if chunks[2] == 'true': inline = True
		embed.add_field(name=chunks[0], value=chunks[1], inline=inline)

	if footer != '': embed.set_footer(text=footer)
	
	if delete > 0: await message.channel.send(embed=embed, delete_after=delete)
	else: await message.channel.send(embed=embed)

def setup(bot):
	bot.add_cog(FAQCog(bot))