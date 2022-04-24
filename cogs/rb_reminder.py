import discord
from discord.ext import commands
import random
import asyncio

class ReminderCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def remindme(self, ctx):
		content = ctx.message.content.split(" ")

		if len(content) < 3:
			await build_embed(self, ctx, '[RB Reminder]', 'Syntax:\n`!remindme [duration] [text]`\nEx: !remindme 12h ban noss', delete=5)
			return

		in_dur = content[1]
		del content[:2]
		text = ""
		for word in content: text += word + " "
		text = text.rstrip()
		
		dur = 0
		time_convert = {"s":1, "m":60, "h":3600,"d":86400}
		time_units = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days"}
		try: #check if first input is a duration
			dur = int(in_dur[:-1]) * time_convert[in_dur[-1]]
		except:
			await build_embed(self, ctx, '[RB Reminder]', 'Syntax:\n`!remindme [duration] [text]`\nEx: !remindme 12h ban noss', delete=5)
			return

		response_list = [f'Ok, I\'ll remind you about `{text}` in {in_dur[:-1]} {time_units[in_dur[-1]]}.']
		await build_embed(self, ctx, '[RB Reminder]', response_list[random.randint(0, len(response_list)-1)], delete=5)
		await asyncio.sleep(dur)
		await build_embed(self, ctx, '[RB Reminder]', f'Hey {ctx.author.mention}, {text}')

async def build_embed(self, ctx, title='', desc='', fields=[], footer='', delete=0, channel=None):
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
		inline = False
		if chunks[2] == 'true': inline = True
		embed.add_field(name=chunks[0], value=chunks[1], inline=inline)

	if footer != '': embed.set_footer(text=footer)
	
	if channel == None:
		if delete > 0: await ctx.channel.send(embed=embed, delete_after=delete)
		else: await ctx.channel.send(embed=embed)
	else:
		if delete > 0: await channel.send(embed=embed, delete_after=delete)
		else: await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(ReminderCog(bot))