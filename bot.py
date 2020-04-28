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

client = commands.Bot(command_prefix = '.')
channels_id = [704641109103476806, 704643080036548618, 704681348979359745]

@client.event
async def on_ready():
	print('Hi')

#join server
@client.event
async def on_member_join(member):
	channel = client.get_channel( channels_id[0] )
	role = discord.utils.get(member.guild.roles, id = 697031247095922689)

	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = random.choice(config.join_messages).format(member.name), color = 0x00FF00 ))

# disconnect users
@client.event
async def on_member_remove(member):
	channel = client.get_channel( channels_id[0] )
	await channel.send(embed = discord.Embed(description = f'**Ну, куда ты?**\n\nПользователь ``{member.name}`` покинул сервер', color = 0xFF0000 ))

# messages
@client.event 
async def on_message(message):
	await client.process_commands( message )

	msg = message.content.lower()


	author  = message.author
	content = message.content
	channel = message.channel

	print(f'Message from {author}: {content}')


	#delete bad messages
	for i in config.delete_msg: 
		if i in msg:
			await message.delete()
			await channel.send(f'Ай-ай-ай, {author.mention},материться тут нельзя!')


#on edit
@client.event
async def on_message_edit(before, after):

	msg = after.content.lower()

	for i in config.delete_msg:
		if i in msg:
			await after.delete()

#clear command
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 100):
	await ctx.channel.purge(limit = amount)

#say hello
@client.command(pass_context = True)
async def hello(ctx, amount = 1):
	await ctx.channel.purge(limit = amount)

	author = ctx.message.author
	await ctx.send(f'Привет, {author.mention}')

@client.command(pass_context = True)
async def bye(ctx, amount = 1):
	await ctx.channel.purge(limit = amount)

	author = ctx.message.author
	await ctx.send(f'Пока, {author.mention}')

@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def bye_adm(ctx, member: discord.Member, amount = 1):
	await ctx.channel.purge(limit = amount)

	await ctx.send(f'Пока, {member.mention}')

#privet message
@client.command(pass_context = True)
async def hello_prv(ctx, member: discord.Member, amount = 1):
	await ctx.channel.purge(limit = amount)

	author = ctx.author

	await member.send(f'{member.name}, тебе привет от {author}')

#say by bot
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def say_by_bot(ctx, message):
	await ctx.channel.purge(limit = 1)

	channel = ctx.channel

	await channel.send(message)

#kick
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( channels_id[1] )

	msg = random.choice(config.kick_message)

	await member.kick()
	await channel.send(embed = discord.Embed(description = msg.format(member.mention), color = 0x9c5c0c ))


#ban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( channels_id[1] )

	msg = random.choice(config.ban_message)

	await member.ban()
	await channel.send(embed = discord.Embed(description = msg.format(member.mention), color = 0xc0c0fc ))

	await member.send('Вы были забанены на сервере "Счасливы вместе"!')

#unban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, user):
	await ctx.channel.purge(limit = 1)

	channel = client.get_channel( channels_id[2] )
	msg = random.choice(config.unban_message)

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user
		await ctx.guild.unban(user)

		await channel.send(embed = discord.Embed(description = msg.format(user.mention), color = 0x0c0c4c ))
		await user.send('Вы были разбанены на сервере "Счасливы вместе"!')

		return 

#mute
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, amount = 1):
	await ctx.channel.purge(limit = 1)

	delete_r = discord.utils.get(member.guild.roles, id = 697031247095922689)
	role     = discord.utils.get(member.guild.roles, id = 697455208372109383)

	channel = client.get_channel( channels_id[1] )

	msg = random.choice(config.mute_message)

	await member.remove_roles(delete_r)
	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = msg.format(member.mention), color = 0x808080 ))

# unmute
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unmute(ctx, member: discord.Member, amount = 1):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( channels_id[2] )

	role       = discord.utils.get(member.guild.roles, id = 697031247095922689)
	delete_r   = discord.utils.get(member.guild.roles, id = 697455208372109383)

	msg = random.choice(config.unmute_message)

	await member.remove_roles(delete_r)
	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = msg.format(member.mention), color = 0x887764 ))

#invite member to voice channel
@client.command(pass_context = True)
async def invite_vchat(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	channel = client.get_channel( 695630701114032223 )
	author = ctx.author

	msg = random.choice(config.invite_vchat_message)

	await channel.send(embed = discord.Embed(description = msg.format(member.mention), color = 0x00FF00 ))
	await member.send(f'{author} приглашает Вас в голосовой чат!')





token = os.environ.get('BOT_TOKEN')
client.run(str(token))
