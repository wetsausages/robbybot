import discord
from discord.ext import commands
import json
import random

class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='setmod')
	async def set_mod(self, ctx, role:discord.Role):
		if await check_perm(self, ctx) is False: return

		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)

		if str(role) in cfg['Main']['ModRoles']:
			await build_embed(self, ctx, 'RB Admin', f'{role.mention} already has moderator permissions.', delete=5)
			return
		cfg['Main']['ModRoles'].append(str(role))
		to_json = json.dumps(cfg, indent=4)
		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: f.write(to_json)
		await build_embed(self, ctx, 'RB Admin', f'Moderator permissions given to {role.mention}.', delete=5)

	@commands.command(name='removemod')
	async def remove_mod(self, ctx, role:discord.Role):
		if await check_perm(self, ctx) is False: return

		with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'r') as f: r = f.read()
		cfg = json.loads(r)

		if str(role) in cfg['Main']['ModRoles']:
			cfg['Main']['ModRoles'].remove(str(role))
			to_json = json.dumps(cfg, indent=4)
			with open(self.bot.path + '/data/' + str(ctx.guild.id) + '/data.cfg', 'w') as f: f.write(to_json)
			await build_embed(self, ctx, 'RB Admin', f'Moderator permissions removed from {role.mention}.', delete=5)
		else: await build_embed(self, ctx, 'RB Admin', f'{role.mention} does not have permissions to remove.', delete=5)

	# @commands.command()
	# async def module(self, ctx, name=''):
	# 	if await check_perm(self, ctx) is False: return
	# 	if name == '': 
	# 		mod_data = ['Modules|AutoFAQ\nAnarchy Essentials|true', 'Tag|faq\nae|true']
	# 		await build_embed(self, ctx, 'RB Module List', 'Below is a list of toggleable modules you can use with Robbybot. Some may require further authorization or set up for full functionality. None are required for the base admin and moderator functionality of Robbybot.\n\nTo add a module, do !load [tag]\nTo remove a module, do !unload [tag]\nFor more information on each module, do !modules [tag]', mod_data)
	# 	else:
	# 		mod_data= {'faq': ['Commands|!faq [0-n]|true','\u200b|Sets how many days a member has to have been joined to stop recieving FAQ responses|true'], 'ae':['Commands|!relay\n!top *[1-10]\n!pt [player name]\n!rank [n]|true','\u200b|Chat relay between Discord and the game server.\nShows top n players. If n is blank, it defaults to top 10.\nShows playtime and rank of player.\nShows player by playtime rank|true']}
	# 		if name == 'faq': await build_embed(self, ctx, 'AutoFAQ', 'Automatically answer frequently asked questions. Uses a confidence system and automatic deletion to minimize spam, but can also be configured to only tirgger for new enough members.', mod_data.get(name))
	# 		elif name == 'ae': await build_embed(self, ctx, 'Anarchy Essentials', 'Framework for anarchy Minecraft servers, providing lag and spam mitigation, anti-illegals, and more. Connecting this module requires FTP authorization to your server with /auth.', mod_data.get(name), footer='*Optional paramter')

	# @commands.command(name='load')
	# async def load_module(self, ctx, module:str):
	# 	if await check_perm(self, ctx) is False: return
	# 	mod_list = {"faq":"rb_autofaq", "ae":"rb_ae"}
	# 	cog = mod_list.get(module)

	# 	try:
	# 		self.bot.load_extension('cogs.'+cog)
	# 	except Exception as e:
	# 		await build_embed(self, ctx, 'Error adding module:', f'{type(e).__name__} - {e}', delete=5)
	# 	else:
	# 		await build_embed(self, ctx, f'Succesfully added module [{cog}]', delete=5)

	# @commands.command(name='unload')
	# async def unload_module(self, ctx, module: str):
	# 	if await check_perm(self, ctx) is False: return
	# 	mod_list = {"faq":"rb_autofaq", "ae":"rb_ae"}
	# 	cog = mod_list.get(module)

	# 	try:
	# 		self.bot.unload_extension('cogs.'+cog)
	# 	except Exception as e:
	# 		await build_embed(self, ctx, 'Error removing module:', f'{type(e).__name__} - {e}', delete=5)
	# 	else:
	# 		await build_embed(self, ctx, f'Succesfully removed module [{cog}]', delete=5)

	# @commands.command(name='reload')
	# async def reload_module(self, ctx, *, module: str):
	# 	if await check_perm(self, ctx) is False: return
	# 	mod_list = {"faq":"rb_autofaq", "ae":"rb_ae"}
	# 	cog = mod_list.get(module)

	# 	try:
	# 		self.bot.unload_extension('cogs.'+cog)
	# 		self.bot.load_extension('cogs.'+cog)
	# 	except Exception as e:
	# 		await build_embed(self, ctx, 'Error reloading module:', f'{type(e).__name__} - {e}', delete=5)
	# 	else:
	# 		await build_embed(self, ctx, f'Succesfully reloaded module [{cog}]', delete=5)


async def check_perm(self, ctx):
	allowed = False
	if ctx.message.author.guild_permissions.administrator: allowed = True
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
	bot.add_cog(AdminCog(bot))