import os
import discord 
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import random
from random import choice
import config
import time
import l_func

client = commands.Bot(command_prefix = '.')

# ready bot
@client.event
async def on_ready():
	print('BOT is ready')

#join server
@client.event
async def on_member_join(member):
	channel = client.get_channel( 704641109103476806 )
	role = discord.utils.get(member.guild.roles, id = 697031247095922689)

	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = random.choice(config.join_messages).format(member.name), color = 0x00FF00 ))

# disconnect users
@client.event
async def on_member_remove(member):
	channel = client.get_channel( 704641109103476806 )
	await channel.send(embed = discord.Embed(description = f'Пользователь ``{member.name}`` покинул сервер', color = 0xFF0000 ))

# messages
@client.event 
async def on_message(message):
	await client.process_commands( message )

	msg = message.content.lower()


	author  = message.author
	content = message.content
	channel = message.channel

	print(f'Message from {author}: {content}')

	if(message.channel.id == '696425233518821457'):
		await client.add_reaction(message, '🧠')

	#delete bad messages
	for i in config.delete_msg: 
		if i in msg:
			await message.delete()
			await channel.send(f'Ай-ай-ай, {author.mention},материться тут нельзя!')
			mute()


#on edit
@client.event
async def on_message_edit(before, after):

	msg = after.content.lower()

	for i in delete_msg:
		if i in msg:
			await after.delete()

#kick
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( 704643080036548618 )

	await member.kick()
	await channel.send(embed = discord.Embed(description = random.choice(config.kick_message).format(member.mention), color = 0x9c5c0c ))


#ban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	
	await member.ban()
	channel = client.get_channel( 704643080036548618 )
	await channel.send(embed = discord.Embed(description = random.choice(config.ban_message).format(member.mention), color = 0xc0c0fc ))

#unban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
	await ctx.channel.purge(limit = 1)

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user
		channel = client.get_channel( 704681348979359745 )

		await ctx.guild.unban(user)
		await channel.send(embed = discord.Embed(description = random.choice(config.unban_message).format(member.mention), color = 0x0c0c4c ))

		return

#mute
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, amount = 1):
	await ctx.channel.purge(limit = 1)

	delete_r = discord.utils.get(member.guild.roles, id = 697031247095922689)
	role     = discord.utils.get(member.guild.roles, id = 697456709651791973)

	channel = client.get_channel( 704643080036548618 )

	await member.remove_roles(delete_r)
	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = random.choice(config.mute_message).format(member.mention), color = 0x808080 ))

# unmute
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member, amount = 1):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( 704681348979359745 )

	role       = discord.utils.get(member.guild.roles, id = 697031247095922689)
	delete_r   = discord.utils.get(member.guild.roles, id = 697455208372109383)

	await member.remove_roles(delete_r)
	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = random.choice(config.unmute_message).format(member.mention), color = 0x887764 ))

#invite member to voice channel
@client.command(pass_context = True)
async def invite_vchat(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( 695630701114032223 )
	author = ctx.author

	await channel.send(embed = discord.Embed(description = random.choice(config.invite_vchat_message).format(member.mention), color = 0x00FF00 ))
	await member.send(f'{author}, приглашает Вас в голосовой чат!')




token = os.environ.get('BOT_TOKEN')
client.run(str(token))
