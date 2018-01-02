import discord
import asyncio
from src.fortnite import get_squad_stats, build_string_for_squad_stats


symbol='!'
token='Mzk3NDI2MjM0MDI1NDQzMzMw.DSv0VA.edPUD214IyWDdRxZ65azoZkc1ss'


print('init')
client = discord.Client()
print('done init')

async def call_fortnite(name, message):
  username = name # Here your username.
  
  platform = 'pc' # Here your platform: psn, xbox, pc.
  squad_data = get_squad_stats(username, platform)
  if len(squad_data) == 0:
    await client.send_message(message.channel, "Wrong username")
    return
  squad_data = squad_data[0]
  await client.send_message(message.channel, (build_string_for_squad_stats(squad_data)))

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
      if len(mess) != 2:
        await client.send_message(message.channel, 'fortstat takes 1 argument')
      await call_fortnite(mess[1], message)
    if mess[0] == 'play':
      chan = client.get_server('272379096640520193').get_channel('395021485099450369')
      print(chan)
      voice = await client.join_voice_channel(chan)
      player = await voice.create_ytdl_player(mess[1])
      player.start()


client.run(token)

