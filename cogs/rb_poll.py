import discord
from discord.ext import commands
import json
import random

class PollCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		self.option_emojis = [
			"\N{REGIONAL INDICATOR SYMBOL LETTER A}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER B}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER C}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER D}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
			"\N{REGIONAL INDICATOR SYMBOL LETTER F}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER G}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER H}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER I}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER J}",
			"\N{REGIONAL INDICATOR SYMBOL LETTER K}"
		]

	@commands.command()
	async def poll(self, ctx):
		await ctx.message.delete()
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return

		content = ctx.message.content.split(';')
		question = content[0].replace('!poll', '')
		if question == '':
			await build_embed(self, ctx, '[RB Poll]', 'Creates a poll. If you don\'t provide options, it will default to ✅ and ❎. Automatically pings relevant role if it has been set with !pollrole.',['\u200b|**Syntax**\n`!poll [question]`\n`!poll [question]; [option]; [option]...`\n`!pollrole [role]`|true', '\u200b|\u200b\nStart yes/no poll\nStart poll with multiple options\nSelect role to ping|true'])
			return

		if len(content) == 1: #Reaction poll
			await build_embed(self, ctx, question, react=0)
		else: #Options poll
			del content[0]
			fields = []
			i = 0
			for option in content:
				fields.append(f'{self.option_emojis[i]}| {option}|false')
				i += 1
			await build_embed(self, ctx, question, fields=fields, react=len(content))

		role = ctx.guild.get_role(cfg['Poll']['Role'])
		print(role)
		ping = await ctx.channel.send(role.mention)
		await ping.delete()

	@commands.command()
	async def pollrole(self, ctx, role:discord.Role):
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		cfg['Poll']['Role'] = str(role.id)
		to_json = json.dumps(cfg, indent=4)
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: f.write(to_json)

async def check_perm(self, ctx, user_roles, mod_roles):
	allowed = False
	if ctx.message.author.guild_permissions.administrator: allowed = True
	for role in user_roles:
		if role.name in mod_roles: allowed = True
	if allowed == False: await build_embed(self, ctx, title=str(ctx.author)+' does not have permission.', delete=5)
	return allowed

async def build_embed(self, ctx, title='', desc='', fields=[], footer='', delete=0, channel=None, react=-1):
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
		else: msg = await ctx.channel.send(embed=embed)
	else:
		if delete > 0: await channel.send(embed=embed, delete_after=delete)
		else: msg = await channel.send(embed=embed)

	if react == -1: return
	elif react == 0:
		await msg.add_reaction('✅')
		await msg.add_reaction('❎')
	else:
		i = 0
		while i < react:
			await msg.add_reaction(self.option_emojis[i])
			i += 1

def setup(bot):
	bot.add_cog(PollCog(bot))