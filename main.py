#!/usr/bin/python3
import discord
import asyncio
import copy
from src.fortnite import get_stats, build_string_for_stats, get_all_stats, build_string_for_all_stats

symbol='!'
token='Mzk3NDI2MjM0MDI1NDQzMzMw.DSv0VA.edPUD214IyWDdRxZ65azoZkc1ss'


print('init')
client = discord.Client()
print('done init')

async def call_fortnite(name, message):
  username = name # Here your username.
  platform = 'pc' # Here your platform: psn, xbox, pc.
  data = get_all_stats(name, 'pc')
  if len(data) == 0:
    await client.send_message(message.channel, "Wrong username")
    return
  wow = build_string_for_all_stats(username, data)
  wow = '```python\n' + str(wow) + '```\n'
  await client.send_message(message.channel, wow)

async def come_and_play_sound(url, message):
  if (message.author.voice.voice_channel == None):
    await client.send_message(message.channel, "User not in voice channel")
    return
  chan = message.author.voice.voice_channel
  voice = await client.join_voice_channel(chan)
  player = await voice.create_ytdl_player(url)
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
        if (mess[1] == channel.name):
          previous = channel
          if (new != None):
            break;
        elif (mess[2] == channel.name):
          new = channel
          if (previous != None):
            break;
  print(len(previous.voice_members))
  if (previous != None and new != None):
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


@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print('------')
@client.event
async def on_message(message):
  if not(len(message.content) and message.content[0] == symbol):
    return
  message.content = message.content[1:]
  mess = message.content.split()
  if len(mess) > 0:
    if mess[0] == 'fortstat':
      if check_args(mess, 1, message):
        await call_fortnite(mess[1], message)
    if mess[0] == 'play':
      if await check_args(mess, 1, message):
        await come_and_play_sound(mess[1], message)
    if mess[0] == 'move':
      if await check_args(mess, 2, message):
        await move_chan_to_chan(mess, message)
client.run(token)
