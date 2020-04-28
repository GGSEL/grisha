import discord 
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio


client = commands.Bot(command_prefix = '.')

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
	
	

token = os.environ.get('BOT_TOKEN')
client.run(str(token))
