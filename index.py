# import discord dependencies from pip
import discord

client = discord.Client()

@client.event
async def on_ready():
  print('{0.user} is active now.'.format(client))
  await client.change_presence(activity = discord.Game('with words'))

@client.event
async def on_guild_join(guild):
  channel = await guild.create_text_channel('shabdkosh')
  await channel.send("Hello! I'm ShabdKosh, your personal word assistant!")

channels = ['shabdkosh']

@client.event
async def on_message(message):
  if str(message.channel) in channels:
    if message.author == client.user:
      return

    if message.content.startswith('Hello'):
      await message.channel.send('Hi')
      
    if message.content.startswith('!tle'):
      msg = message.content.split("\"")
      print(msg)
      tle = translator.translate(msg[1], dest=msg[2].lstrip())
      await message.channel.send("`{}` -> `{}`".format(msg[1], tle.text))
    
    if message.content.startswith('!dt'):
      msg = message.content[8:]
      await message.channel.send("The message is in {}".format({translator.detect(msg)}))
      
      
