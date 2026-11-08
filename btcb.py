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

import time
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
	'id': 'botId'
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
	embed.add_field(name='**Уровни** (платно)', value='``levels [прикрепите гифку/фото, отправляемое при повышении уровня]`` если фото не прикрепленно, то при повышении уровня будет только текст')
	embed.add_field(name='**Магазин** (платно)', value='``shop``')
	embed.add_field(name='**Статусы** (платно)', value='``status``')
	embed.add_field(name='**Окончание создания бота**', value='``finish``')
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

	c.execute('SELECT bot_name FROM bots WHERE member_name=?', (interaction.user.display_name, ))
	check_bot = c.fetchone()
	print(check_bot)
	if check_bot is None:
		pass
	else:
		await sentMsg.edit(content=f'Можно создавать только одного бота одновременно!')
		return

	request_url = 'https://discord.com/api/v10/users/@me'
	headers = {
		'Authorization': f'Bot {token}',
		'Content-Type': 'application/json'
	}
	response = requests.get(url=request_url, headers=headers)
	if response:
		pass
	else:
		await sentMsg.edit(content=f'Бота с таким токеном не существует!')
		return

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
import random

from discord.ext import commands

import asyncio
from asyncio import sleep

import sqlite3
conn_lvl = sqlite3.connect('database.db')
c_lvl = conn_lvl.cursor()
c_lvl.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, level INTEGER, experience INTEGER)')

conn_bios = sqlite3.connect('bios.db')
c_bios = conn_bios.cursor()
c_bios.execute('CREATE TABLE IF NOT EXISTS bios (user_id INTEGER PRIMARY KEY, bio TEXT)')

conn_eco = sqlite3.connect('economic.db')
c_eco = conn_eco.cursor()
c_eco.execute('CREATE TABLE IF NOT EXISTS economic (user_id INTEGER PRIMARY KEY, mon INTEGER)')

conn_shop = sqlite3.connect('shop.db')
c_shop = conn_shop.cursor()
c_shop.execute('CREATE TABLE IF NOT EXISTS shop (name TEXT PRIMARY KEY, cost INTEGER, role_id INTEGER)')

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
	return perms.send_messages and perms.embed_links and perms.view_channel

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

	docs = codecs.open('Документация ' + bot_name + ' ' + interaction.user.display_name + '.html', 'a', 'utf-8')
	docs.write(u'<h1>Документация по боту %s от %s</h1>\nПрефикс бота: !help\n<h2>Команды</h2>\n' % (bot_name, interaction.user.display_name))

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	docs.close()
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

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Очистка чата</h3>\n!clear [количество-сообщений]\n')
	docs.close()

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

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'''<h3>Муты</h3>\n!mute [пользователь] [объем-времени] [единица-измерения] [причина] <strong>Причмечание:</strong> единицы измерения указываются через пробел после объема и перед причиной и с помощью ключ-букв: s(секунды); m(минуты); h(часы); d(дни)
		!unmute [пользователь]\n''')
	docs.close()

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

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Баны</h3>\n!ban [пользователь] [причина]\n!unmute [пользователь]\n')
	docs.close()

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

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Кик</h3>\n!kick [пользователь] [причина]\n')
	docs.close()

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

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Кастомные войсы</h3>\n!voice_to_create [айди-войса]\n')
	docs.close()

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="levels", description="Настроить систему уровней")
async def levels(interaction: discord.Interaction, attachment: discord.Attachment = None):
	await interaction.response.defer()
	progress_bar = tqdm(total=3)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	mySrv = bot.get_guild(1540981782977970188)
	prem_role = mySrv.get_role(1541064093203435560)
	if interaction.user not in prem_role.members:
		embed = discord.Embed(color=discord.Color.red())
		embed.add_field(name='**Ошибка!**', value='У вас нет премиума! Чтобы его получить, зайдите на сервер и напишите разработчику в личные сообщения\nhttps://discord.gg/5PzDUgV8sm\n<@949821041566445608>')
		await interaction.followup.send(embed=embed, ephemeral=True)
		return

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду ``create``!', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	url = None
	if attachment == None:
		url = ' '
	else:
		url = f'''embed.set_image(url='{attachment.url}')'''

	botFile.write(u'''

@bot.command()
async def level(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.message.author
	c_lvl.execute('SELECT * FROM users WHERE user_id=?', (member.id,))
	result = c_lvl.fetchone()
	if result is None:
		await ctx.reply('Пользователь не найден в базе')
	else:
		await ctx.reply(f'{member.mention} уровень: {result[1]}, опыт: {result[2]}')

@bot.command(description='Выдать опыт пользователю')
@commands.has_permissions(manage_roles=True)
async def exp(ctx, member: discord.Member, amount: int):
	c_lvl.execute('UPDATE users SET experience=experience+? WHERE user_id=?', (amount, member.id))
	conn_lvl.commit()
	c_lvl.execute('SELECT experience FROM users WHERE user_id=?', (member.id,))
	exp = c_lvl.fetchone()
	embed = discord.Embed(color=discord.Color.green())
	embed.add_field(name='Успешно!', value=f'К {member.display_name} добавлено {amount} опыта, теперь у него {exp[0]} опыта')
	await ctx.reply(embed=embed)

@bot.command()
async def leaderboard(ctx):
	c_lvl.execute('SELECT * FROM users ORDER BY experience DESC')
	all_users = c_lvl.fetchall()
	if not all_users:
		await ctx.reply('В базе пока нет данных.')
		return

	view = LeaderboardView(all_users, ctx.message.guild)
	embed = view.get_embed()
	await ctx.reply(embed=embed, view=view)

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if message.author.bot == True:
		return

	c_lvl.execute('SELECT * FROM users WHERE user_id=?', (message.author.id,))
	user = c_lvl.fetchone()

	if user is None:
		c_lvl.execute('INSERT INTO users VALUES (?, ?, ?)', (message.author.id, 0, 1))
		conn_lvl.commit()
	
	else:
		c_lvl.execute('UPDATE users SET experience=experience+1 WHERE user_id=?', (message.author.id,))
		conn_lvl.commit()

	if user[2] >= user[1]  * 50:
		c_lvl.execute('UPDATE users SET level=level+1 WHERE user_id=?', (message.author.id,))
		conn_lvl.commit()
		embed=discord.Embed(color=discord.Color.yellow())
		embed.add_field(name=f' ', value=f'{message.author.mention} повысил уровень до {user[1] + 1}')
		%s
		await message.channel.send(embed=embed)

	await bot.process_commands(message)

class LeaderboardView(discord.ui.View):
	def __init__(self, entries, guild, per_page=10, page=1):
		super().__init__(timeout=120)  # таймаут 2 минуты
		self.entries = entries
		self.guild = guild
		self.per_page = per_page
		self.page = page
		self.total_pages = (len(entries) + per_page - 1) // per_page
		self.update_buttons()

	def update_buttons(self):
		# Изменяем состояние кнопок в зависимости от страницы
		self.children[0].disabled = (self.page <= 1)		  # кнопка "Назад"
		self.children[1].disabled = (self.page >= self.total_pages)  # "Вперёд"

	def get_embed(self):
		start = (self.page - 1) * self.per_page
		end = start + self.per_page
		page_entries = self.entries[start:end]

		embed = discord.Embed(
			color=discord.Color.green(),
			title=f'🏆 Таблица лидеров (стр. {self.page}/{self.total_pages})'
		)
		pos = start + 1
		for data in page_entries:
			mem = self.guild.get_member(data[0])
			if mem:
				embed.add_field(
					name=' ',
					value=f'**#{pos}** {mem.mention}\\n**Уровень**: {data[1]}\\n**Опыт**: {data[2]}',
					inline=False
				)
			pos += 1
		return embed

	@discord.ui.button(label='◀', style=discord.ButtonStyle.secondary)
	async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		if self.page > 1:
			self.page -= 1
			self.update_buttons()
			embed = self.get_embed()
			await interaction.response.edit_message(embed=embed, view=self)

	@discord.ui.button(label='▶', style=discord.ButtonStyle.secondary)
	async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		if self.page < self.total_pages:
			self.page += 1
			self.update_buttons()
			embed = self.get_embed()
			await interaction.response.edit_message(embed=embed, view=self)

	@discord.ui.button(label='Закрыть', style=discord.ButtonStyle.red)
	async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.edit_message(content='Таблица лидеров закрыта.', embed=None, view=None)''' % (url))

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Уровни</h3>\n!level [пользователь]\n!exp [пользователь] [количество-опыта]\n!leaderboard\n')
	docs.close()

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="shop", description="Настроить систему экономики")
async def shop(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=3)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	mySrv = bot.get_guild(1540981782977970188)
	prem_role = mySrv.get_role(1541064093203435560)
	if interaction.user not in prem_role.members:
		embed = discord.Embed(color=discord.Color.red())
		embed.add_field(name='**Ошибка!**', value='У вас нет премиума! Чтобы его получить, зайдите на сервер и напишите разработчику в личные сообщения\nhttps://discord.gg/5PzDUgV8sm\n<@949821041566445608>')
		await interaction.followup.send(embed=embed, ephemeral=True)
		return

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду ``create``!', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.command(description="Добавить товар в магазин (требуется manage_roles)")
@commands.has_permissions(manage_roles=True)
async def add_item(ctx, cost: int, role: discord.Role, *, name: str):
	c_shop.execute('INSERT INTO shop VALUES (?, ?, ?)', (name, cost, role.id))
	conn_shop.commit()
	embed = discord.Embed(color=discord.Color.green())
	embed.add_field(name='Успешно', value=f'Добавлено: **{name}**, стоимость **{cost}**, выдаёт роль {role.mention}')
	await ctx.reply(embed=embed)

@bot.command()
async def balance(ctx, member: discord.Member = None):
	if member is None:
		member = ctx.message.author
	c_eco.execute('SELECT mon FROM economic WHERE user_id = ?', (member.id,))
	bal = c_eco.fetchone()
	if bal is None:
		await ctx.reply('У пользователя нет счета')
		return
	embed = discord.Embed(color=discord.Color.purple())
	embed.add_field(name=f'Баланс **{member.display_name}**', value=f'**{bal[0]}** монет')
	await ctx.reply(embed=embed)

@bot.command()
async def buy(ctx, item: str):
	c_eco.execute('SELECT * FROM economic WHERE user_id=?', (ctx.message.author.id,))
	user = c_eco.fetchone()
	if user is None:
		c_eco.execute('INSERT INTO economic VALUES (?, ?)', (ctx.message.author.id, 0))
		conn_eco.commit()
		await ctx.reply('Недостаточно средств!')
		return
	c_shop.execute('SELECT cost, role_id FROM shop WHERE name=?', (item,))
	shop_item = c_shop.fetchone()
	if shop_item is None:
		await ctx.reply('Такого предмета нет в магазине')
		return
	cost, role_id = shop_item
	c_eco.execute('SELECT mon FROM economic WHERE user_id = ?', (ctx.message.author.id,))
	balance = c_eco.fetchone()
	if balance[0] < cost:
		await ctx.reply('Недостаточно средств!')
		return
	c_eco.execute('UPDATE economic SET mon = mon-? WHERE user_id=?', (cost, ctx.message.author.id))
	conn_eco.commit()
	role = ctx.message.guild.get_role(role_id)
	if role:
		await ctx.message.author.add_roles(role)
	await ctx.reply('Покупка успешно совершена!')

@bot.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def work(ctx):
	c_eco.execute('SELECT * FROM economic WHERE user_id=?', (ctx.message.author.id,))
	user = c_eco.fetchone()
	if user is None:
		c_eco.execute('INSERT INTO economic VALUES (?, ?)', (ctx.message.author.id, 0))
		conn_eco.commit()
	zarplata = random.randrange(100, 500)
	c_eco.execute('UPDATE economic SET mon = mon+? WHERE user_id=?', (zarplata, ctx.message.author.id))
	conn_eco.commit()
	await ctx.reply(f'Вы получили зарплату **{zarplata}** монет!')
@bot.command()
async def shop(ctx):
	c_shop.execute('SELECT * FROM shop')
	items = c_shop.fetchall()
	embed = discord.Embed(color=discord.Color.purple())
	if items == []:
		embed.add_field(name='Магазин', value=f'Магазин пуст', inline=False)
	else:
		for data in items:
			embed.add_field(name=data[0], value=f'Стоимость: {data[1]}\nВыдаёт: <@&{data[2]}>', inline=False)
	await ctx.reply(embed=embed)''')

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Экономика</h3>\n!work\n!balance [пользователь]\n!shop\n!add_item [цена] [роль] [название]\n')
	docs.close()

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.tree.command(name="status", description="Настроить систему статусов")
async def status(interaction: discord.Interaction):
	await interaction.response.defer()
	progress_bar = tqdm(total=3)
	sentMsg = await interaction.followup.send(f'Прогресс: {progress_bar}')

	mySrv = bot.get_guild(1540981782977970188)
	prem_role = mySrv.get_role(1541064093203435560)
	if interaction.user not in prem_role.members:
		embed = discord.Embed(color=discord.Color.red())
		embed.add_field(name='**Ошибка!**', value='У вас нет премиума! Чтобы его получить, зайдите на сервер и напишите разработчику в личные сообщения\nhttps://discord.gg/5PzDUgV8sm\n<@949821041566445608>')
		await interaction.followup.send(embed=embed, ephemeral=True)
		return

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (interaction.user.display_name,))
	bot_name = c.fetchone()
	if bot_name is None:
		await sentMsg.edit(content=f'Ошибка!')
		await interaction.followup.send(f'Вы еще не создали своего бота! Используйте команду ``create``!', ephemeral=True)
		return

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0] + '.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write(u'''

@bot.command()
async def bio(ctx, *, txt=None):
	c_bios.execute('SELECT * FROM bios WHERE user_id=?', (ctx.message.author.id,))
	user = c_bios.fetchone()

	if user is None:
		if txt != None:
			c_bios.execute('INSERT INTO bios VALUES (?, ?)', (ctx.message.author.id, txt))
			conn_bios.commit()
			embed = discord.Embed(color=discord.Color.green())
			embed.set_thumbnail(url=ctx.message.author.avatar)
			embed.add_field(name=f'Информация **{ctx.message.author.display_name}** изменена', value=txt)
			await ctx.send(embed=embed)
			return
		else:
			await ctx.send(f'Напишите команду ещё раз с информацией которую вы хотите вставить!')
			return
	if txt != None:	
		c_bios.execute('UPDATE bios SET bio = ? WHERE user_id = ?', (txt, ctx.message.author.id))
		conn_bios.commit()
		embed = discord.Embed(color=discord.Color.green())
		embed.set_thumbnail(url=ctx.message.author.avatar)
		embed.add_field(name=f'Информация **{ctx.message.author.display_name}** изменена', value=txt)
		await ctx.send(embed=embed)
	else:
		await ctx.send(f'Напишите команду ещё раз с информацией которую вы хотите вставить!')
@bot.command()
async def user(ctx, member: discord.Member = None):
	if member == None:
		member = ctx.message.author

	c_bios.execute('SELECT * FROM bios WHERE user_id=?', (member.id,))
	user = c_bios.fetchone()

	if user is None:
		await ctx.reply(f'Пользователя **{member.display_name}** нет в базе данных!')
		return
	
	embed = discord.Embed(color=discord.Color.green())
	embed.set_thumbnail(url=member.avatar)
	embed.add_field(name=f'Информация о **{member.display_name}**', value=user[1])
	await ctx.send(embed=embed)''')

	docs = codecs.open('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html', 'a', "utf-8")
	docs.write(f'<h3>Статусы</h3>\n!bio [пользователь] [текст]\n!user [пользователь]\n')
	docs.close()

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

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
		"Примечание: \n"
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

	botFile.write('''
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.RoleNotFound):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты не ввёл название роли либо такой роли попросту не существует!", color=discord.Color.red())
		await ctx.send(embed=em)
		return
	elif isinstance(error, commands.ChannelNotFound):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты не ввёл название канала либо такого канала попросту не существует!", color=discord.Color.red())
		await ctx.send(embed=em)
		return
	elif isinstance(error, commands.CommandNotFound):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты допустил ошибку в команде либо такой команды попросту не существует!", color=discord.Color.red())
		await ctx.send(embed=em)
		return
	elif isinstance(error, commands.CommandOnCooldown):
		em = discord.Embed(title=f"Подожди!У тебя стоит кулдаун!", description=f"У тебя не закончился куладун на команде. Приходи ещё через {round(error.retry_after) // 60} минут", color=discord.Color.red())
		await ctx.send(embed=em)
	else:
		em = discord.Embed(title=f"Ошибка!", description=error, color=discord.Color.red())
		await ctx.send(embed=em)
		return
bot.run(config['token'])''')
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
		discord.File(bot_name[0] + '_start.bat'),
		discord.File('Документация ' + bot_name[0] + ' ' + interaction.user.display_name + '.html')
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