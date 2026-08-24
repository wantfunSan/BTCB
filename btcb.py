#!/usr/bin/python
# -*- coding: utf-8 -*-

import discord
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
	'id': '3457'
}

bot = commands.Bot(command_prefix = '-', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
	
	print('ERRORS ARE SUCK!(maybe) )')
	await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name = '''Bot created by wF#2016'''))

@bot.command()
async def help(ctx):
	embed = discord.Embed(color = discord.Color.blurple())
	embed.add_field(name = '**Создание бота**', value = '``create [имя-вашего-бота] [токен-бота]``')
	embed.add_field(name = '**Отправка сообщения при заходе нового участника**', value = '``hello [упоминание-роли-которую-будут-выдавать] [упоминание-канала-для-сообщений]  [текст-сообщения]`` (для упоминания человека, просто напишите в нужном месте "@m")')
	embed.add_field(name = '**Отправка сообщения при выходе участника**', value = '``goodbye [упоминание-канала-для-отправки] [текст-сообщения]`` (для упоминания человека, просто напишите в нужном месте @m)')
	embed.add_field(name = '**Команда очистки чата**', value = '``clear``')
	embed.add_field(name = '**Система мьюта**', value = '``mute`` - отправит участника в таймаут (у людей, которые будут использовать эту команду, должно быть право таймаутировать участников)')
	embed.add_field(name = '**Команда "кик"**', value = '``kick`` у людей, которые будут использовать эту команду, должно быть право кикать участников)')
	embed.add_field(name = '**Приватные войсы**', value = '``voice_to_create [айди-войс-чата]``')
	embed.add_field(name = '**Оставить на сервере**', value = '``to_server`` (данная команда не является бесплатной, стоимость: 50руб, все подробности при вызове команды)')
	embed.add_field(name = '**Окончание создания бота**', value = '``finish`` (это бесплатная функция, все подробности также, при вызове команды)')
	embed.add_field(name = '**Больше информации**', value = "http://vlahouse.ru/documentation/btcb")
	embed.add_field(name = '**Ошибки**', value = "При наличии ошибок, например, BTCB не отвечает на запросы, созданный бот некоректно работает, то вы можете создать топик на сервере поддержки: https://discord.gg/rwjr5WnNW7")
	embed.add_field(name = '**Рабочие дни**', value = 'Время, в которое создатель может ответить: любое время')
	embed.set_footer(text='''Created by wantfun. Support author you can at https://www.donationalerts.com/r/petelinka''')
	await ctx.reply(embed = embed)

@bot.command()
async def create(ctx, botName: str = None, *, token: str = None):

	if botName is None or token is None:
		raise commands.errors.CommandInvokeError
		return

	if botName == None:
		await ctx.reply(f'Введите имя бота')
		return
	if token == None:
		await ctx.reply('Вы не указали токен! Вы можете посмотреть http://www.youtube.com/watch?v=VMV0176VbzM , чтобы узнать, как его получить. Не бойся, моему создателю твой токен ни к чему!')
		return
	
	progress_bar = tqdm(total=4)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	c.execute('INSERT INTO bots VALUES (?,?)', (ctx.author.display_name, botName))
	conn.commit()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile = codecs.open(botName+'.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.write(u'''import discord
import requests
import time
import json

from discord.ext import commands

import asyncio
from asyncio import sleep

config = {
	'token': '%s',
	'bot': '%s'
}

bot = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

@bot.event
async def on_ready():
	print('Спасибо, что воспользовались моим сервисом, если вам понравится, подайте автору на пропитание) https://www.donationalerts.com/r/petelinka')
	print('А также присоединяйся к нашему сообществу https://discord.gg/5PzDUgV8sm')
	await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name = "Bot created by BTCB"))
''' % (token, botName)) #строки первой необходимости
	
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно! Обязательно удали свое сообщение с токеном!')
@bot.command()
async def hello(ctx, roleToAdd: discord.Role = None, channelToSend:discord.channel.TextChannel = None, *, helloMsg = None):

	if roleToAdd is None or channelToSend is None or helloMsg is None:
		raise commands.errors.CommandInvokeError
		return

	progress_bar = tqdm(total=5)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	
	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name  is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду create !')
		return													  
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	if '@m' in helloMsg:
		helloMsg = helloMsg.replace("@m", '{member.mention}')
		print(helloMsg)

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
	embed = discord.Embed(color = 0x00FF01)
	embed.add_field(name = f'%s')
	await channel.send(embed=embed)

	role = discord.utils.get(member.guild.roles, name = "%s")
	await member.add_roles(role)''' % (channelToSend.id, helloMsg, roleToAdd))
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.command()
async def goodbye(ctx, channelToSend:discord.channel.TextChannel = None, *, goodbyeMsg = None):

	if channelToSend is None or goodbyeMsg is None:
		raise commands.errors.CommandInvokeError
		return

	progress_bar = tqdm(total=5)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	
	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду ``create`` !')
		return													  
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	if '@m' in goodbyeMsg:
		goodbyeMsg = goodbyeMsg.replace("@m", '{member.mention}')
		print(goodbyeMsg)

	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile = codecs.open(bot_name[0]+'.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.write(u'''

@bot.event
async def on_member_remove(member):
	goodbye = %s
	channel = bot.get_channel(hello)
	embed = discord.Embed(color = 0x00FF01)
	embed.add_field(name = f'%s')
	await channel.send(embed=embed)''' % (channelToSend.id, goodbyeMsg))
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

@bot.command()
async def clear(ctx):
	progress_bar = tqdm(total=4)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	
	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду create !')
		return													  
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0]+'.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.write(u'''

@bot.command
async def clear(ctx, count):
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

@bot.command()
async def mute(ctx):
	progress_bar = tqdm(total=4)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	
	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду create !')
		return													  
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0]+'.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.write(u'''

@bot.command()
@commands.has_permissions(moderate_members = True)
async def mute(ctx, member: discord.Member = None, tm: int=None, value ='s', *,reason = None):
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
	if member == None:
		await ctx.reply(f'Укажите кого надо размьютить')
		await ctx.message.add_reaction('❌')
		return
	else:

		if member.timed_out_until == None:
				await ctx.message.add_reaction('❌')
				await ctx.reply(f'У данного Вами пользователя раннее не было мута!')
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
			
@bot.command()
async def kick(ctx):
	progress_bar = tqdm(total=4)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	
	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду create !')
		return													  
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0]+'.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.write(u'''

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, reason=None):
	if member == None:
		await ctx.reply(f'Укажите кого надо выгнать')
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

@bot.command()
async def voice_to_create(ctx, vcId: int = None):

	if vcId is None:
		raise commands.errors.CommandInvokeError
		return

	progress_bar = tqdm(total=3)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')
	
	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду create !')
		return													  
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile = codecs.open(bot_name[0]+'.py', 'a', "utf-8")
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile.write(u'''

@bot.event
async def on_voice_state_update(member,before,after): #Создание войс комнат
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

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.RoleNotFound):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты не ввёл название роли либо такой роли попросту не существует!", color=discord.Color.red())
		await ctx.send(embed=em)
		return
	if isinstance(error, commands.ChannelNotFound):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты не ввёл название канала либо такого канала попросту не существует!", color=discord.Color.red())
		await ctx.send(embed=em)
		return
	'''if isinstance(error, commands.CommandNotFound):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты допустил ошибку в команде либо такой команды попросту не существует!", color=discord.Color.red())
		await ctx.send(embed=em)
		return'''
	if isinstance(error, commands.errors.CommandInvokeError):
		em = discord.Embed(title=f"Подожди!Ты допустил ошибку в команде!", description=f"Ты не ввёл какие-то важные аргументы команды!", color=discord.Color.red())
		await ctx.send(embed=em)
		return

@bot.command()
async def to_server(ctx):
	await ctx.reply(f'Прости, но это платная функция! Она стоит 50 рублей. Если ты уже переслал деньги, то ожидай пока мой создатель это увидит.')
	await ctx.send(f'Форма сообщения: В форме сообщения Donation Alerts ты должен указать своё имя и на что ты скинул деньги. Далее пишешь в личку создателя ник, указанный в донате Donation Alerts и ожидаешь ответа.')
	await ctx.send(f'Личные сообщения создателя: ggvp3869(Discord) или @w4n7fun(Telegram)')
	await ctx.send(f'Ссылка на донэйшн алёртс: https://www.donationalerts.com/r/petelinka')
	await ctx.send(f'Все деньги пойдут на продвижение функционала бота, программистических способностей создателя, а также на покушац)')
	await ctx.send(f'Рабочие дни: любой день')

@bot.command()
async def finish(ctx):
	progress_bar = tqdm(total=9)
	sentMsg = await ctx.send(f'Прогресс: {progress_bar}')

	c.execute('SELECT bot_name FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	bot_name = c.fetchone()
	if bot_name is None:
		sentMsg = await ctx.send(content=f'Ошибка!')
		await ctx.reply(f'Вы еще не создали своего бота! Используйте команду create !')
		return				 
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	await ctx.reply(f'Ты воспользовался бесплатной функцией! Примечание: \n1. С помощью этой функции ты сможешь запускать бота, и **он будет функционировать пока ты не выключишь компьютер**(!)\n2. Я напишу как использовать этого бота только на Windows и Linux, как её использовать на macOS ты сможешь увидеть в интернете!')
	
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	c.execute('DELETE FROM bots WHERE member_name = ?', (ctx.author.display_name, ))
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	conn.commit()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	
	botFile = codecs.open(bot_name[0]+'.py', 'a', 'utf-8')
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.write('''\nbot.run(config['token'])''')
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	botFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	batFile = codecs.open(bot_name[0]+'_start.bat', 'a', 'utf-8')
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	batFile.write(u'''@echo off
"C:\\Program Files\\Pythonтут-твоя-версия\\python.exe" "%s.py"
pause''' % (bot_name))
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')

	batFile.close()
	progress_bar.update(1)
	await sentMsg.edit(content=f'Прогресс: {progress_bar}')
	await sentMsg.edit(content=f'Успешно!')

	files = [
	discord.File(bot_name[0]+'.py'),
	discord.File(bot_name[0]+'_start.bat')
	]

	await ctx.send(f'Итак, чтобы запустить свего бота на Windows, ты должен: \n 1. Cкачать Python любой версии и установить его в такой путь: C:\Program Files\Python (в конце поставь свою версию без точек и другого, только цифры)\n2. Зайди в .bat файл который я тебе скинул и измени там где написано "тут-твоя-версия" на версию, которую ты указал в конце пункта 1\n 3. Нажми Win+R и напиши в открывшеемся окошке "cmd"4. Далее у тебя откроется командная строка, в которую ты должен вбить "pip install discord.py"\n5. Если у тебе напишет что-то вроде ""pip" команда не найдена", то вбей в поисковик "активация pip в переменных средах"', files = files)
	await ctx.send(f'Если же у тебя Linux, то скачай Python любой версии через терминал "sudo apt install python3"\n2. Не выходя из терминала напиши команду "pip3 install discord.py"\n3. Далее скачай .py файл, который я скинул в предыдущем сообщении\n4. Далее перейди в терминале в ту папку, где у тебя скрипт (это можно сделать через "cd /путь-к-папке")\n4. Далее напиши "python3 название-твоего-бота.py"')
	os.remove(bot_name[0]+'.py')
	os.remove(bot_name[0]+'_start.bat')

bot.run(config['token'])
