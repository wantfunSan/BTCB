#!/usr/bin/python
# -*- coding: utf-8 -*-

import discord
from discord import app_commands
import requests
import time
import json
import codecs

from discord.ext import commands

import asyncio
from asyncio import sleep


import sqlite3

import os

import functools 
import operator

from tqdm import tqdm

conn = sqlite3.connect('bots.db')
c = conn.cursor()

#Создание таблицы для хранения данных пользователей
c.execute('''CREATE TABLE IF NOT EXISTS bots (
				member_name TEXT PRIMARY KEY,
				bot_name TEXT
			)''')

config = {
	'token': 'token',
	'bot': 'BTCB',
	'id': '3457'
}

bot = commands.Bot(command_prefix = '-', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
	
	print('ERRORS ARE SUCK!(maybe) )')
	await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name = '''/help \nBot created by wF#2016'''))
	await bot.tree.sync()
	print("Слэш-команды синхронизированы!")

# -------------------- СЛЭШ-КОМАНДЫ (все с ephemeral=True) --------------------

@bot.tree.command(name="help", description="Показать справку по боту")
async def help(interaction: discord.Interaction):
	await interaction.response.defer()
	embed = discord.Embed(color=discord.Color.blurple())
	embed.add_field(name='**Создание бота**', value='``create [имя-вашего-бота] [токен-бота]``')
	embed.add_field(name='**Отправка сообщения при заходе нового участника**', value='``hello [упоминание-роли-которую-будут-выдавать] [упоминание-канала-для-сообщений]  [текст-сообщения]`` (для упоминания человека, просто напишите в нужном месте "@m")')
	embed.add_field(name='**Отправка сообщения при выходе участника**', value='``goodbye [упоминание-канала-для-отправки] [текст-сообщения]`` (для упоминания человека, просто напишите в нужном месте @m)')
	embed.add_field(name='**Команда очистки чата**', value='``clear``')
	embed.add_field(name='**Система мьюта**', value='``mute`` - отправит участника в таймаут (у людей, которые будут использовать эту команду, должно быть право таймаутить участников)')
	embed.add_field(name='**Команда "кик"**', value='``kick`` у людей, которые будут использовать эту команду, должно быть право кикать участников)')
	embed.add_field(name='**Команда "бан"**', value='``ban`` у людей, которые будут использовать эту команду, должно быть право банить участников)')
	embed.add_field(name='**Приватные войсы**', value='``voice_to_create [айди-войс-чата]``')
	#embed.add_field(name='**Оставить на сервере**', value='``to_server`` (данная команда не является бесплатной, стоимость: 50руб, все подробности при вызове команды)')
	embed.add_field(name='**Окончание создания бота**', value='``finish`` (это бесплатная функция, все подробности также, при вызове команды)')
	embed.add_field(name='**Больше информации**', value="http://vlahouse.ru/documentation/btcb")
	embed.add_field(name='**Ошибки**', value="При наличии ошибок, например, BTCB не отвечает на запросы, созданный бот некоректно работает, то вы можете создать топик на сервере поддержки: https://discord.gg/rwjr5WnNW7")
	embed.add_field(name='**Рабочие дни**', value='Время, в которое создатель может ответить: любое время')
	embed.set_footer(text='''Created by wantfun. Support author you can at https://www.donationalerts.com/r/petelinka''')
	await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="create", description="Создать нового бота")
@app_commands.describe(bot_name="Имя вашего бота", token="Токен вашего бота")
async def create(interaction: discord.Interaction, bot_name: str, token: str):
	await interaction.response.defer(ephemeral=True)
	progress_bar = tqdm(total=4)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}', ephemeral=True)

	c.execute('INSERT INTO bots VALUES (?,?)', (interaction.user.display_name, bot_name))
	conn.commit()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''import discord
import requests
import time
import json
import datetime

from discord.ext import commands

import asyncio
from asyncio import sleep

config = {
	'token': '%s',
	'bot': '%s'
}

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

async def on_error(error):
	on_error_chat_id = %s
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
''' % (token, bot_name, interaction.user.id))

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="hello", description="Настроить приветствие новых участников")
@app_commands.describe(role="Роль, которая будет выдаваться", channel="Канал для отправки приветствия", message="Текст приветствия (используйте @m для упоминания участника)")
async def hello(interaction: discord.Interaction, role: discord.Role, channel: discord.TextChannel, message: str):
	await interaction.response.defer()
	progress_bar = tqdm(total=5)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду /create !', ephemeral=True)
		return
	if role.is_default():
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Нельзя использовать everyone!', ephemeral=True)
		return

	check_role = interaction.guild.get_role(role.id)
	if check_role is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Роль `{role}` не существует на этом сервере.', ephemeral=True)
		return

	check_channel = interaction.guild.get_channel(channel.id)
	if check_channel is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Чат `{channel}` не существует на этом сервере.', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	if '@m' in message:
		message = message.replace("@m", '{member.mention}')

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.event
async def on_member_join(member):
	hello = %s
	channel = bot.get_channel(hello)

	if not can_send_messages(channel):
		await on_error(f'У меня нет доступа к каналу <#{hello}>!')
		return

	embed = discord.Embed(color = 0x00FF01)
	embed.add_field(name="Добро пожаловать!", value = f'%s')
	await channel.send(embed=embed)

	role = discord.utils.get(member.guild.roles, name = "%s")
	if not can_assign_role(member.guild, role):
		on_error(f'Роль <@&{role.id} находится выше меня, я не могу ее добавить!>!')
		return
	await member.add_roles(role)''' % (channel.id, message, role.name))

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="goodbye", description="Настроить прощание при выходе участника")
@app_commands.describe(channel="Канал для отправки сообщения", message="Текст прощания (используйте @m для упоминания участника)")
async def goodbye(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
	await interaction.response.defer()
	progress_bar = tqdm(total=5)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	check_channel = interaction.guild.get_channel(channel.id)
	if check_channel is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Чат `{channel}` не существует на этом сервере.', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	if '@m' in message:
		message = message.replace("@m", '{member.mention}')

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.event
async def on_member_remove(member):
	goodbye = %s
	channel = bot.get_channel(goodbye)

	if not can_send_messages(channel):
		await on_error(f'У меня нет доступа к каналу <#{goodbye}>!')
		return

	embed = discord.Embed(color = 0x00FF01)
	embed.add_field(name = "До встречи!", value = f'%s')
	await channel.send(embed=embed)''' % (channel.id, message))

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="clear", description="Добавить команду очистки чата в вашего бота")
async def clear(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=4)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.command()
async def clear(ctx, count: int = None):
	if not ctx.guild.me.guild_permissions.manage_messages:
		await on_error('У меня нет возможности удалять сообщения!')
		return

	if count == None:
		await ctx.reply(f'Пожалуйста, укажите число')
		await ctx.message.add_reaction('❌')
		return
	await ctx.message.add_reaction('✅')
	await ctx.channel.purge(limit=count+1)
	await ctx.send(f"Удалено **{count}** сообщений")''')

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="mute", description="Добавить систему мьюта в вашего бота")
async def mute(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=4)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

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
			await ctx.send(embed=embed)''')

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')
@bot.tree.command(name="ban", description="Добавить систему банов в вашего бота")
async def ban(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=4)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member = None, *, reason: str = None):
	if not ctx.guild.me.guild_permissions.ban_members:
		await on_error('У меня нет возможности банить участников!')
		return

	if member == None:
		await ctx.reply(f'Укажите кого надо забанить')
		await ctx.message.add_reaction('❌')
		return

	elif member == ctx.message.author:
		await ctx.reply(f'Самого себя нельзя забанить!')
		await ctx.message.add_reaction('❌')
		return

	elif not can_modder(ctx.guild, ctx.message.author, member):
		await ctx.reply(f'У меня либо у Вас недостаточно прав для бана этого человека!')
		await ctx.message.add_reaction('❌')
		return

	else:
		await ctx.message.add_reaction('✅')
		embed = discord.Embed(color = discord.Color.green())
		embed.add_field(name='Модератор', value=ctx.message.author.mention)
		embed.add_field(name='Забанил', value = member.mention)
		if reason == None:
			embed.add_field(name = 'Причина:', value = 'Причина не указана')
		else:
			embed.add_field(name = 'Причина:', value = reason)
		await member.ban(reason=reason)
		await ctx.send(embed=embed)
@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, member: int = None):
	if not ctx.guild.me.guild_permissions.ban_members:
		await on_error('У меня нет возможности банить участников!')
		return

	if member == None:
		await ctx.reply(f'Укажите кого надо забанить')
		await ctx.message.add_reaction('❌')
		return

	elif member == ctx.message.author:
		await ctx.reply(f'Самого себя банить нельзя!')
		await ctx.message.add_reaction('❌')
		return

	elif not can_modder(ctx.guild, ctx.message.author, member):
		await ctx.reply(f'У меня либо у Вас недостаточно прав для бана этого человека!')
		await ctx.message.add_reaction('❌')
		return

	else:
		await ctx.message.add_reaction('✅')
		embed = discord.Embed(color = discord.Color.green())
		embed.add_field(name='Модератор', value=ctx.message.author.mention)
		embed.add_field(name='Разбанил', value = f'<@{member}>')
		member = await bot.fetch_user(member)
		await ctx.guild.unban(member)
		await ctx.send(embed=embed)''')

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно! Чтобы разбанить участника нужен будет его ID')

@bot.tree.command(name="kick", description="Добавить команду кика в вашего бота")
async def kick(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=4)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

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
	await ctx.reply(embed=embed)''')

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="voice_to_create", description="Настроить создание приватных войс-комнат")
@app_commands.describe(voice_channel_id="ID голосового канала, при входе в который будет создаваться приватная комната")
async def voice_to_create(interaction: discord.Interaction, voice_channel_id: str):
	await interaction.response.defer()
	progress_bar = tqdm(total=3)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	try:
		vcId = int(voice_channel_id)
	except ValueError:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send("❌ ID должен быть числом!", ephemeral=True)
		return

	voice_channel = interaction.guild.get_channel(vcId)
	if voice_channel is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Голосовой канал с ID `{vcId}` не существует на этом сервере.', ephemeral=True)
		return
	if not isinstance(voice_channel, discord.VoiceChannel):
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Канал с ID `{vcId}` не является голосовым каналом.', ephemeral=True)
		return

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.event
async def on_voice_state_update(member,before,after): #Создание войс комнат
	if not member.guild.me.guild_permissions.manage_channels or not member.guild.me.guild_permissions.move_members:
		await on_error('У меня нет возможности управлять каналами или перемещать участников!')
		return

	if after:
		if after.channel:
			if after.channel.id == %s:
				for guild in bot.guilds:
					guild = member.guild

					maincategory = discord.utils.get(guild.categories, name=after.channel.category.name)
					channel2 = await guild.create_voice_channel(name=f'『{member.display_name}`s Channel』',category = maincategory)
					await member.move_to(channel2)
					def check(x,y,z):
						return len(channel2.members) == 0
		
					await bot.wait_for('voice_state_update',check=check)
					await channel2.delete()''' % (vcId))

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

'''@bot.tree.command(name="to_server", description="Информация о платной функции оставления бота на сервере")
async def to_server(interaction: discord.Interaction):
	await interaction.response.defer()
	await interaction.followup.send(
		"Прости, но это платная функция! Она стоит 50 рублей. Если ты уже переслал деньги, то ожидай пока мой создатель это увидит.\n"
		"Форма сообщения: В форме сообщения Donation Alerts ты должен указать своё имя и на что ты скинул деньги. Далее пишешь в личку создателя ник, указанный в донате Donation Alerts и ожидаешь ответа.\n"
		"Личные сообщения создателя: ggvp3869(Discord) или @w4n7fun(Telegram)\n"
		"Ссылка на донэйшн алёртс: https://www.donationalerts.com/r/petelinka\n"
		"Все деньги пойдут на продвижение функционала бота, программистических способностей создателя, а также на покушац)\n"
		"Рабочие дни: любой день",
		ephemeral=True
	)'''

@bot.tree.command(name="finish", description="Завершить создание бота и получить файлы для запуска")
async def finish(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=9)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду create !', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	await interaction.followup.send(
		"Ты воспользовался бесплатной функцией! Примечание: \n"
		"1. С помощью этой функции ты сможешь запускать бота, и **он будет функционировать пока ты не выключишь компьютер**(!)\n"
		"2. Я напишу как использовать этого бота только на Windows и Linux, как её использовать на macOS ты сможешь увидеть в интернете!",
		ephemeral=True
	)

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	c.execute('DELETE FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	conn.commit()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', 'utf-8')
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write('''\nbot.run(config['token'])''')
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	batFile = codecs.open(bot_name[0] + '_start.bat', 'a', 'utf-8')
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	batFile.write(u'''@echo off
"C:\\Program Files\\Pythonтут-твоя-версия\\python.exe" "%s.py"
pause''' % (bot_name[0]))

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	batFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

	files = [
		discord.File(bot_name[0] + '.py'),
		discord.File(bot_name[0] + '_start.bat')
	]

	await interaction.followup.send(
		"Итак, чтобы запустить свего бота на Windows, ты должен: \n"
		"1. Cкачать Python любой версии и установить его в такой путь: C:\Program Files\Python (в конце поставь свою версию без точек и другого, только цифры)\n"
		"2. Зайди в .bat файл который я тебе скинул и измени там где написано 'тут-твоя-версия' на версию, которую ты указал в конце пункта 1\n"
		"3. Нажми Win+R и напиши в открывшеемся окошке 'cmd'\n"
		"4. Далее у тебя откроется командная строка, в которую ты должен вбить '```pip install discord.py requests time```'\n"
		"5. Если у тебе напишет что-то вроде ''pip' команда не найдена', то вбей в поисковик 'активация pip в переменных средах'",
		files=files,
		ephemeral=True
	)

	await interaction.followup.send(
		"Если же у тебя Linux, то скачай Python любой версии через терминал 'sudo apt install python3'\n"
		"2. Не выходя из терминала напиши команду 'pip3 install discord.py requests time'\n"
		"3. Далее скачай .py файл, который я скинул в предыдущем сообщении\n"
		"4. Далее перейди в терминале в ту папку, где у тебя скрипт (это можно сделать через 'cd /путь-к-папке')\n"
		"5. Далее напиши 'python3 название-твоего-бота.py'",
		ephemeral=True
	)

	os.remove(bot_name[0] + '.py')
	os.remove(bot_name[0] + '_start.bat')

@bot.tree.error
async def on_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
	if isinstance(error, commands.RoleNotFound):
		em = discord.Embed(title=f"Подожди! Ты допустил ошибку в команде!", description=f"Ты не ввёл название роли либо такой роли попросту не существует!", color=discord.Color.red())
		await interaction.response.send_message(embed=em, ephemeral=True)
		return
	if isinstance(error, commands.ChannelNotFound):
		em = discord.Embed(title=f"Подожди! Ты допустил ошибку в команде!", description=f"Ты не ввёл название канала либо такого канала попросту не существует!", color=discord.Color.red())
		await interaction.response.send_message(embed=em, ephemeral=True)
		return
	if isinstance(error, commands.errors.CommandInvokeError):
		em = discord.Embed(title=f"Подожди! Ты допустил ошибку в команде!", description=f"Ты не ввёл какие-то важные аргументы команды!", color=discord.Color.red())
		await interaction.response.send_message(embed=em, ephemeral=True)
		return

@bot.command()
async def servers(ctx):
	servers = list(bot.guilds)
	await ctx.send(', '.join([guild.name for guild in servers]))

bot.run(config['token'])
