#!/usr/bin/python3
import discord
import asyncio
import copy
import random
import requests
import math
import re

symbol = '!'
dic = {
	0: 'zero',
	1: 'one',
	2: 'two',
	3: 'three',
	4: 'four',
	5: 'five',
	6: 'six',
	7: 'seven',
	8: 'eight',
	9: 'nine'
}
print('init')
client = discord.Client()
random.seed()
print('done init')


async def come_and_play_sound(url, message):
	if message.author.voice.voice_channel is None:
		await client.send_message(message.channel, "User not in voice channel")
	chan = message.author.voice.voice_channel
	print(url)
	voice = await client.join_voice_channel(chan)
	client.join_voice_channel(chan)
	print(url)
	player = await voice.create_ytdl_player(url)
	voice.create_ytdl_player(url)
	player.start()


async def check_args(mess, neededNbArgs, message):
	if len(mess) - 1 != neededNbArgs:
		await client.send_message(message.channel, mess[0] + ' takes ' + str(neededNbArgs) + ' argument(s). Given: ' + str(len(mess) - 1))
		return False
	return True


async def move_chan_to_chan(mess, message):
	if not message.author.permissions_in(message.channel).move_members:
		await client.send_message(message.channel, message.author.name + ' is not authorized to move members')
		return
	mess[1] = mess[1].replace('_', ' ')
	mess[2] = mess[2].replace('_', ' ')
	previous = None

	new = None
	for server in client.servers:
		if new == None and previous == None:
			for channel in server.channels:
				if mess[1] == channel.name:
					previous = channel
					if (new != None):
						break;
				elif mess[2] == channel.name:
					new = channel
					if previous != None:
						break;
	print(len(previous.voice_members))
	if previous is not None and new is not None:
		mems = copy.deepcopy(previous.voice_members)
	for user in mems:
		await client.move_member(user, new)
		await client.send_message(message.channel, 'moving ' + user.name + ' to ' + mess[2])
		print(user.name)
	else:
		if (previous == None):
			await client.send_message(message.channel, mess[1] + ' channel not found')
		if (new == None):
			await client.send_message(message.channel, mess[2] + ' channel not found')


async def get_help(message):
	await client.send_message(message.channel, "The commands: \n\
	```\
	!fortstat <account name> \n\
	!play <youtube link>\n\
	!move <channel from> <channel to>\
	!random <arguments> <to> <chose> <from>\
	!yon Answer the question mostly just say no\
	!makecall ask people to play a game\
	```")


async def chose_random(mess, message):
	mess.pop(0)
	if len(mess) == 0:
		await client.send_message(message.channel, "please add something to chose from")
		return
	random.seed()
	a = random.randomint(0, len(mess) - 1)
	await client.send_message(message.channel, 'I picked: ' + mess[a])




async def YouMakeTheCall(phrase, message):
	chan = client.get_channel('486632170446782465')
	print(chan)
	phrase.pop(0)
	s = ' '.join(phrase)

	print(message.author, ' made the call', s)
	await client.send_message(chan, ':loudspeaker: :wavy_dash: :wavy_dash: ' + \
	                          s + ' :wavy_dash: :wavy_dash:')


async def randomMovie(message):
	url = 'http://www.omdbapi.com/?i=tt'
	r = math.floor(random.random() * 2155529)
	movie = str(r).rjust(7, '0')
	key = '&apikey=d7aa1e97'
	resp = requests.get(url + movie + key)
	if not resp:
		randomMovie(message)
		return
	resp = resp.json()
	print(resp['Title'])
	Title = resp['Title']
	Gresp = requests.get('http://www.google.com/search?start=0&num=10&as_q=' + \
	                     Title + ' allocine')
	test = re.search('Note : \d,\d', Gresp.text)
	note = ':question::question:'
	print(Gresp.text)
	if test:
		print(test.group(0))
		print('wtf')
		note = ''
		for i in range(int(re.search(r'\d+', test.group(0)).group())):
			note += ':star:'
		note += ':white_small_square:'
		small = int(re.search(r',\d+', test.group(0)).group(0)[1])
		note += ':' + dic[small] + ':'

	reqalo = re.search('http\:\/\/www\.allocine\.fr\/film\/fichefilm_gen_cfilm\%3D\d*\.html', Gresp.text)
	synopsis = 'No synopsis found'
	if reqalo:
		alourl = reqalo.group()
		alourl = alourl.replace('%3D', '=')
		print(alourl)
		reqalo = requests.get(alourl)
		synmatch = re.search('\<div class=\"content-txt\" itemprop=\"description\"\>(.*?)\<\/div\>', reqalo.text,
		                     re.DOTALL)
		if synmatch:
			synopsis = synmatch.group()
			synopsis = synopsis.replace('<br>', '\n')
			synopsis = synopsis.split("\n", 2)[2];
			synopsis = '```' + synopsis[:synopsis.rfind('\n')] + '```'
	await client.send_message(message.channel, ':projector: ' + Title + ' ' + note + '\n' + synopsis)


@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')


@client.event
async def on_message(message):
	if message.channel.is_private and not message.author.bot:
		if message.content[0] == symbol:
			message.content = message.content[1:]
			mess = message.content.split()
			if len(mess) > 0:
				if mess[0] == 'makecall':
					await YouMakeTheCall(mess, message)
		else:
			await get_help(message)
		return
	if not (len(message.content) and message.content[0] == symbol):
		return
	print(1)
	message.content = message.content[1:]
	mess = message.content.split()
	if len(mess) > 0:
		if mess[0] == 'play':
			if await check_args(mess, 1, message):
				await come_and_play_sound(mess[1], message)
		if mess[0] == 'move':
			if await check_args(mess, 2, message):
				await move_chan_to_chan(mess, message)
		if mess[0] == 'random':
			await chose_random(mess, message)
		if mess[0] == 'adrien,':
			await YesOrNo(mess, message)
		if mess[0] == 'film':
			print('film')
			await randomMovie(message)


client.run(token)
