import discord
from discord.ext import commands
import json
import random
import asyncio

class ModCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def rb(self, ctx, x=None):
		await ctx.message.delete()
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return
		if x == None: 
			await build_embed(self, ctx, 'RB Panel', fields=['\u200b|**Admin Commands**\n!setmod [role]\n!removemod [role]\n!modlog\n\n**Mod Commands**\n!mute [member] [duration] [reason]\n!unmute [member]\n!ban [member] [reason]\n\n**Module Commands**\n!faq|true', '\u200b|\u200b\nGive role moderator perms\nRevoke moderator perms from role\nSet channel as mod log\n\n\nMute member\nUnmute member\nBan member\n\n\nAutoFAQ config panel|true'])
			return

	@commands.command()
	async def mute(self, ctx, member:discord.Member, x=None):
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)

		title = 'RB Mute'
		await ctx.message.delete()
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return
		channel = self.bot.get_channel(cfg['Main']['ModLog'])
		muted_role=discord.utils.get(ctx.guild.roles, name="Muted")
		if muted_role in member.roles:
			await build_embed(self, ctx, title, f'{member.mention} is already muted.', delete=5)
			return

		chunks = ctx.message.content.split(' ')
		if len(chunks) < 3: #both fields empty
			await build_embed(self, ctx, title, desc=f'Invalid syntax: !mute [member] [duration*] [reason].', footer='*optional parameter, leave blank for permanent mute', delete=5)
			return

		dur = None
		reason = None
		try: #check if first input after member is a duration input...
			time_convert = {"s":1, "m":60, "h":3600,"d":86400}
			time_units = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days"}
			dur = int(x[:-1]) * time_convert[x[-1]]
		except: #...else its a reason string
			reason =''
			for chunk in chunks[2:]: reason += chunk + ' '

		if dur != None:
			if len(chunks) < 4:
				await build_embed(self, ctx, title, desc=f'Please provide a reason.', delete=5)
				return
			reason =''
			for chunk in chunks[3:]: reason += chunk + ' '
			time_convert = {"s":1, "m":60, "h":3600,"d":86400}
			time_units = {"s":"seconds", "m":"minutes", "h":"hours", "d":"days"}
			dur = int(chunks[2][:-1]) * time_convert[chunks[2][-1]]
			await member.add_roles(muted_role)
			await build_embed(self, ctx, title, f'{member.mention} has been muted for {chunks[2][:-1]} {time_units[chunks[2][-1]]}.', delete=5)
			await build_embed(self, ctx, f'[MUTE] {member}', f'**Reason:** {reason}', [f'Issuing moderator:|{ctx.author.mention}|true', f'Mute recipient:|{member.mention}|true', f'Duration:|{x[:-1]} {time_units[x[-1]]}|false'], channel=channel)
			print(dur)
			await asyncio.sleep(dur)
			await member.remove_roles(muted_role)
		else:
			await member.add_roles(muted_role)
			await build_embed(self, ctx, title, f'{member.mention} has been permanently muted.', delete=5)
			await build_embed(self, ctx, f'[MUTE] {member}', f'**Reason:** {reason}', [f'Issuing moderator:|{ctx.author.mention}|true', f'Mute recipient:|{member.mention}|true', f'Duration:|**permanent**|false'], channel=channel)

	@commands.command()
	async def unmute(self, ctx, member:discord.Member):
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		await ctx.message.delete()
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return
		channel = self.bot.get_channel(cfg['Main']['ModLog'])
		muted_role=discord.utils.get(ctx.guild.roles, name="Muted")
		if muted_role not in member.roles:
			await build_embed(self, ctx, 'RB Unmute', f'{member.mention} is not muted.', delete=5)
			return
		await member.remove_roles(muted_role)
		await build_embed(self, ctx, 'RB Unmute', f'{member.mention} is no longer muted.', delete=5)
		await build_embed(self, ctx, f'[UNMUTE] {member}', fields=[f'Issuing moderator:|{ctx.author.mention}|true', f'Member:|{member.mention}|true'], channel=channel)
		return

	@commands.command()
	async def ban(self, ctx, member:discord.Member, x=None):
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		await ctx.message.delete()
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return
		if x == None:
			await build_embed(self, ctx, 'RB Ban', desc=f'Please provide a reason.', delete=5)
			return
		chunks = ctx.message.content.split(' ')
		reason =''
		for chunk in chunks[2:]: reason += chunk + ' '
		channel = self.bot.get_channel(cfg['Main']['ModLog'])
		await member.ban(reason=reason)
		await build_embed(self, ctx, f'[BAN] {member}', fields=[f'Issuing moderator:|{ctx.author.mention}|true', f'Member:|{member.mention}|true', f'Reason:|{reason}|true'], channel=channel)

	@commands.command(name='modlog')
	async def mod_log(self, ctx):
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		await ctx.message.delete()
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return
		cfg['Main']['ModLog'] = ctx.channel.id
		to_json = json.dumps(cfg, indent=4)
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f:
			f.write(to_json)
		await build_embed(self, ctx, 'RB Mod Log', f'{ctx.channel.name} will now store moderator logs.', delete=5)
		return

	@commands.command()
	async def faq(self, ctx, x=None, y=None):
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)
		if await check_perm(self, ctx, ctx.author.roles, cfg['Main']['ModRoles']) is False: return
			
		await ctx.message.delete()
		if x == None: await build_embed(self, ctx, 'RB FAQ Panel', 'Robbybot AutoFAQ works with 2 components: a key:response entry, and a confidence value. Keys are keywords that relate to their corresponding response. For example, the [keyword] \'version\' would have the [response] \'The server is version 1.18\'.\n\nWhether or not the bot responds to a message is decided based on confidence and whether or not a key was heard. If the bot thinks the message was a question *and* hears a keyword, it will respond with that keywords response.', ['!faq toggle|Toggles AutoFAQ on and off|false', '!faq days [n]|Only responds to players with less than n days on the server|false', '!faq keys|Show current list of keywords the bot looks for to respond to|false', '!faq add [key] [response]|Add a new key:response entry. If the bot sees the [keyword] and has confidence its a question worth responding to, it will respond with [response]|false', '!faq remove [key]|Removes key:response entry|false'])
		elif x == 'toggle':
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
			cfg = json.loads(r)
			if cfg['FAQ']['Toggle'] == 'on': 
				cfg['FAQ']['Toggle'] = 'off'
				await build_embed(self, ctx, 'RB FAQ', 'Autofaq disabled', delete=5)
			else:
				cfg['FAQ']['Toggle'] = 'on'
				await build_embed(self, ctx, 'RB FAQ', 'Autofaq enabled', delete=5)
			to_json = json.dumps(cfg, indent=4)
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: r = f.write(to_json)
		elif x == 'days':
			if y == None:
				await build_embed(self, ctx, 'RB FAQ', 'Invalid syntax: !faq days [1-n]', delete=5)
				return
			try: int(y)
			except:
				await build_embed(self, ctx, 'RB FAQ', 'Error: please supply a **number** of days', delete=5)
				return
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
			cfg = json.loads(r)
			cfg['FAQ']['MaxDays'] = y
			to_json = json.dumps(cfg, indent=4)
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: r = f.write(to_json)
			await build_embed(self, ctx, 'RB FAQ', f'Set max days joined to recieve FAQ tips to {y}.', delete=5)
		elif x == 'keys':
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
			cfg = json.loads(r)
			lst = []
			for key in cfg['FAQ']['KeyResponse'].keys():
				lst.append(key)
			await build_embed(self, ctx, 'RB FAQ', 'The following is a list of keywords the bot uses to identify questions, along with the related information sent when the word is recognized in a message.', [f'Keys|{lst}|true'])
		elif x == 'add':
			if y == None:
				await build_embed(self, ctx, 'RB FAQ', 'Invalid syntax: !faq add [key] [response]', delete=5)
				return
			chunks = ctx.message.content.split(' ')
			del chunks[:3]
			blob = ''
			for chunk in chunks: blob += chunk + ' '
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
			cfg = json.loads(r)
			cfg['FAQ']['KeyResponse'][y] = blob[:-1]
			to_json = json.dumps(cfg, indent=4)
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: r = f.write(to_json)
			await build_embed(self, ctx, 'RB FAQ', f'Added \'{y}\' to response keys with response:\n{blob[:-1]}', delete=5)
		elif x == 'remove':
			if y == None:
				await build_embed(self, ctx, 'RB FAQ', 'Invalid syntax: !faq remove [key]', delete=5)
				return
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
			cfg = json.loads(r)
			if y not in cfg['FAQ']['KeyResponse'].keys():
				await build_embed(self, ctx, 'RB FAQ', f'{y} not a saved keyword', delete=5)
				return
			del cfg['FAQ']['KeyResponse'][y]
			to_json = json.dumps(cfg, indent=4)
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: r = f.write(to_json)
			await build_embed(self, ctx, 'RB FAQ', f'{y} removed from list of recognized keywords', delete=5)

async def check_perm(self, ctx, user_roles, mod_roles):
	allowed = False
	if ctx.message.author.guild_permissions.administrator: allowed = True
	for role in user_roles:
		if role.name in mod_roles: allowed = True
	if allowed == False: await build_embed(self, ctx, title=str(ctx.author)+' does not have permission.', delete=5)
	return allowed

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
	bot.add_cog(ModCog(bot))