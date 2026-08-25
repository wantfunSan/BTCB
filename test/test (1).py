import discord
import requests
import time
import json
import datetime

from discord.ext import commands

import asyncio
from asyncio import sleep

config = {
	'token': 'token',
	'bot': 'test'
}

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

async def on_error(error):
	on_error_chat_id = 1234567890 #your_account_id
	on_error_chat = bot.get_user(on_error_chat_id)

	embed = discord.Embed(color = discord.Color.red())
	embed.add_field(name = '**❌ Ошибка**', value = error)
	await on_error_chat.send(embed=embed)
	return


def can_send_messages(channel: discord.TextChannel) -> bool:
	perms = channel.permissions_for(channel.guild.me)
	return perms.send_messages and perms.embed_links

def can_assign_role(guild: discord.Guild, role: discord.Role) -> bool:
	me = guild.me
	if not me.guild_permissions.manage_roles:
		return False
	if role.is_default():
		return False
	if role.position >= me.top_role.position:
		return False
	return True

def can_modder(guild: discord.Guild, author: discord.Member, member: discord.Member):
	me = guild.me
	if me.top_role.position <= member.top_role.position:
		return False
	if author.top_role.position <= member.top_role.position:
		return False
	if author.top_role.position > member.top_role.position and me.top_role.position > member.top_role.position:
		return True


@bot.event
async def on_ready():
	print('Спасибо, что воспользовались моим сервисом, если вам понравится, подайте автору на пропитание) https://www.donationalerts.com/r/petelinka')
	print('А также присоединяйся к нашему сообществу https://discord.gg/5PzDUgV8sm')
	await bot.change_presence(status=discord.Status.online, activity=discord.Game(name = "Bot created by BTCB"))


@bot.event
async def on_member_join(member):
	hello = 1234567890 #hello chat id
	channel = bot.get_channel(hello)

	if not can_send_messages(channel):
		await on_error(f'У меня нет доступа к каналу <#{hello}>!')
		return

	embed = discord.Embed(color = 0x00FF01)
	embed.add_field(name="Добро пожаловать!", value = f'qq {member.mention}')
	await channel.send(embed=embed)

	role = discord.utils.get(member.guild.roles, name = "тест")
	if not can_assign_role(member.guild, role):
		on_error(f'Роль <@&{role.id} находится выше меня, я не могу ее добавить!>!')
		return
	await member.add_roles(role)

@bot.event
async def on_member_remove(member):
	goodbye = 1234567890 #goodbye chat id
	channel = bot.get_channel(goodbye)

	if not can_send_messages(channel):
		await on_error(f'У меня нет доступа к каналу <#{goodbye}>!')
		return

	embed = discord.Embed(color = 0x00FF01)
	embed.add_field(name = "До встречи!", value = f'bb {member.mention}')
	await channel.send(embed=embed)

@bot.command()
async def clear(ctx, count: int = None):
	if not ctx.guild.me.guild_permissions.manage_messages:
		await on_error('У меня нет возможности удалять сообщения!')
		return

	print(count)

	if count == None:
		await ctx.reply(f'Пожалуйста, укажите число')
		await ctx.message.add_reaction('❌')
		return
	await ctx.message.add_reaction('✅')
	await ctx.channel.purge(limit=count+1)
	await ctx.send(f"Удалено **{count}** сообщений")

@bot.command()
@commands.has_permissions(moderate_members = True)
async def mute(ctx, member: discord.Member = None, tm: int=None, value ='s', *,reason = None):

	if not ctx.guild.me.guild_permissions.moderate_members:
		await on_error('У меня нет возможности мутить участников!')
		return

	if member == None:
		await ctx.reply(f'Укажите кого надо замьютить')
		await ctx.message.add_reaction('❌')
		return

	elif member == ctx.message.author:
		await ctx.reply(f'Самого себя нельзя мутить!')
		await ctx.message.add_reaction('❌')
		return

	else:

		if member.timed_out_until is not None:
			await ctx.reply(f'Пользователь уже замьючен!')
			await ctx.message.add_reaction('❌')
			return

		if not can_modder(ctx.guild, ctx.message.author, member):
			await ctx.reply(f'У меня либо у Вас недостаточно прав для мута этого человека!')
			await ctx.message.add_reaction('❌')
			return

		await ctx.message.add_reaction('✅')

		embed = discord.Embed(color = discord.Color.red(), title = f'Пользователь **{member.display_name}** замьючен')
		embed.add_field(name = 'Модератор:', value = ctx.message.author.mention)
		if reason == None:
			embed.add_field(name = 'Причина:', value = 'Причина не указана')
		else:
			embed.add_field(name = 'Причина:', value = reason)
		if tm == None:
			embed.add_field(name = "Срок", value = "Срок не указан")
		if tm != None:

			if value == 's':
				embed.add_field(name = "Срок", value = f'{tm} сек')
			elif value == 'm':
				embed.add_field(name = "Срок", value = f'{tm} минут')
			elif value == 'h':
				embed.add_field(name = "Срок", value = f'{tm} часов')
			elif value == 'd':
				embed.add_field(name = "Срок", value = f'{tm} дней')
			await ctx.send(embed=embed)
			
		if tm != None:
			if value == 's':
				tm = tm #секунды
			elif value == 'm':
				tm = tm *60 #минуты
			elif value == 'h':
				tm = tm *3600 #часы
			elif value == 'd':
				tm = tm *216000 #дней

		await member.timeout(datetime.timedelta(seconds=tm), reason = reason)

@bot.command()
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: discord.Member = None):
	if not ctx.guild.me.guild_permissions.moderate_members:
		await on_error('У меня нет возможности мутить участников!')
		return

	if member == None:
		await ctx.reply(f'Укажите кого надо размьютить')
		await ctx.message.add_reaction('❌')
		return
	else:

		if member.timed_out_until == None:
			await ctx.message.add_reaction('❌')
			await ctx.reply(f'У данного Вами пользователя раннее не было мута!')
			return

		if not can_modder(ctx.guild, ctx.message.author, member):
			await ctx.reply(f'У меня либо у Вас недостаточно прав для размута этого человека!')
			await ctx.message.add_reaction('❌')
			return

		else:
			await ctx.message.add_reaction('✅')
			embed = discord.Embed(color = discord.Color.green())
			embed.add_field(name='Модератор', value=ctx.message.author.mention)
			embed.add_field(name='Размьютил', value = member.mention)
			await member.edit(timed_out_until = None)
			await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, reason=None):
	if not ctx.guild.me.guild_permissions.kick_members:
		await on_error('У меня нет возможности кикать участников!')
		return

	if member == None:
		await ctx.reply(f'Укажите кого надо выгнать')
		await ctx.message.add_reaction('❌')
		return

	if not can_modder(ctx.guild, ctx.message.author, member):
		await ctx.reply(f'У меня либо у Вас недостаточно прав для кика этого человека!')
		await ctx.message.add_reaction('❌')
		return

	await member.kick(reason=reason)
	
	embed = discord.Embed(color = discord.Color.red(), title = f'Пользователь **{member.display_name}** выгнан')
	embed.add_field(name="Модератор", value=ctx.message.author.mention)
	embed.add_field(name="Выгнал", value=member.mention)
	if reason == None:
		embed.add_field(name="Причина", value="Причина не указана")
	else:
		embed.add_field(name="Причина", value=reason)
	await ctx.reply(embed=embed)

@bot.event
async def on_voice_state_update(member,before,after): #Создание войс комнат
	if not member.guild.me.guild_permissions.manage_channels or not member.guild.me.guild_permissions.move_members:
		await on_error('У меня нет возможности управлять каналами или перемещать участников!')
		return

	if after:
		if after.channel:
			if after.channel.id == 1234567890: # voice chat id
				for guild in bot.guilds:
					guild = member.guild

					maincategory = discord.utils.get(guild.categories, name=after.channel.category.name)
					channel2 = await guild.create_voice_channel(name=f'『{member.display_name}`s Channel』',category = maincategory)
					await member.move_to(channel2)
					def check(x,y,z):
						return len(channel2.members) == 0
		
					await bot.wait_for('voice_state_update',check=check)
					await channel2.delete()
bot.run(config['token'])