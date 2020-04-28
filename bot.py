import os
import discord 
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio

delete_msg = [
'хуй', 
'ебанутся', 
'ебануться', 
'блять', 'бля', 
'блядь', 'ебать', 
'пизда', 
'пиздец',
'сука',
'поздабол',
'пиздабол',
'ебать',
'пизди']


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	print('BOT is ready')

#join server
@client.event
async def on_member_join(member):
	channel = client.get_channel( 695630701114032223 )
	role = discord.utils.get(member.guild.roles, id = 697031247095922689)

	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = f'Пользователь ``{member.name}`` присоеденился к нам!', color = 0x0c0c0c ))


@client.event
async def on_member_remove(member):
	channel = client.get_channel( 695630701114032223 )
	await channel.send(embed = discord.Embed(description = f'Пользователь ``{member.name}`` покинул сервер', color = 0xc05520 ))

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
	for i in delete_msg: 
		if i in msg:
			await message.delete()
			await channel.send(f'Ай-ай-ай, {author.mention},материться тут нельзя!')



@client.event
async def on_message_edit(before, after):

	msg = after.content.lower()

	for i in delete_msg:
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


#kick
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)

	await member.kick(reason = reason)
	await ctx.send(f'{member.mention} кикнут' + reason)

#ban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def ban(ctx, member: discord.Member, *, reason = None):
	await ctx.channel.purge(limit = 1)

	await member.ban(reason = reason)
	await ctx.send(f'Бот забанил пользователя {member.mention}' + reason)

	await member.send('Вы были забанены Ботом' + reason)

#unban
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
	await ctx.channel.purge(limit = 1)

	banned_users = await ctx.guild.bans()

	for ban_entry in banned_users:
		user = ban_entry.user

		await ctx.guild.unban(user)
		await ctx.send(f'Разбанен пользователь {user.mention}')

		return

#mute
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def mute(ctx, member: discord.Member, reason = None, amount = 1):
	await ctx.channel.purge(limit = 1)

	delete_r = discord.utils.get(member.guild.roles, id = 697464842805575731)
	role     = discord.utils.get(member.guild.roles, id = 697456709651791973)

	await member.remove_roles(delete_r)
	await member.add_roles(role)
	await ctx.send(f'Пользователь {member.mention} получил мут! Причина: ' + reason)

#invite member to voice channel
@client.command(pass_context = True)
async def invite_vs(ctx, member: discord.Member):
	await ctx.channel.purge(limit = 1)
	channel = ctx.channel
	author = ctx.author

	await channel.send(f'{member.mention} приглашаем тебя в голосовой чат!')
	await member.send(f'{author}, приглашает Вас в голосовой чат!')

#say by bot
@client.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def say_by_bot(ctx, message):
	await ctx.channel.purge(limit = 1)

	channel = ctx.channel

	await channel.send(message)




token = os.environ.get('BOT_TOKEN')
client.run(str(token))