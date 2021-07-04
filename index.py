import os
import sox
import discord
import asyncio
from discord.ext import commands
import googletrans
from datetime import datetime
from keep_alive import keep_alive
from google_speech import Speech # for voice module
from PyDictionary import PyDictionary


client = discord.Client()

translator = googletrans.Translator()

@client.event
async def on_ready():
  print('{0.user} is active now.'.format(client))
  await client.change_presence(activity = discord.Game('with words'))

@client.event
async def on_guild_join(guild):
  channel = await guild.create_text_channel('shabdkosh')
  guild = client.get_guild(#guildid)
  channel = guild.get_channel(#channelid)
  embed=discord.Embed(
        title="Hello! Hola! Namaste!",
        description="I am Shabdkosh! Your personal voice and text translator bot :nerd: ",
        color=0x0000FF,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Name", 
                    value=f'ShabdKosh', 
                    inline=True)
    embed.add_field(name="Who am I ?", 
                    value=f'lalalala ',
                    inline=False)
    embed.set_footer(text="                  ")
    embed.set_image(url="https://media.giphy.com/media/IgGcxqawkRc6y43Z6I/giphy.gif")
    await channel.send(embed=embed)

    
channels = ['shabdkosh']


@client.event
async def on_message(message):
  if str(message.channel) in channels:
    if message.author == client.user:
      return

    if message.content.startswith('*Hello'):
      await message.channel.send('https://tenor.com/view/hello-there-gif-9442662')
      print(googletrans.LANGUAGES)
      
    
    if message.content.startswith('*tle'):
      msg = message.content.split("\"")
      print(msg)
      tle = translator.translate(msg[1], dest=msg[2].lstrip())
      await message.channel.send("`{}` -> `{}`".format(msg[1], tle.text))

#     if message.content.startswith('*dt'):
#       msg = message.content[4:]
#       await message.channel.send("The message is in {}".format(translator.detect(msg)))
      
    ldict=googletrans.LANGUAGES

    if message.content.startswith('*dt'):
      msg = message.content[4:]
      language = str(translator.detect(msg))
      l1 = language.split("=",1)[1]
      print(l1)
      lcode = l1.split(",")[0]
    #   l = list(language)
    #   print(l)
    #   lang =l [14:16]
    #   s = ""
    #   lcode = s.join(lang)
      print(lcode)
      await message.channel.send("The message is in {}".format(ldict.get(lcode)))
   
    dictionary=PyDictionary()

    """if message.content.startswith('*th'):
      msg = message.content[4:]
      #print(msg)
      meaning = py_thesaurus.Thesaurus(msg)
      print(meaning.get_synonym())
      await message.channel.send(meaning.get_definition())"""
  
   if message.content.startswith('*dict'):
      msg = message.content[6:]
      #print(msg)
      await message.channel.send(dictionary.meaning(msg))

   if message.content.startswith('*syn'):
      msg = message.content[5:]
      #print(msg)
      await message.channel.send(dictionary.synonym(msg)) 

   if message.content.startswith('*ant'):
      msg = message.content[5:]
      #print(msg)
      await message.channel.send(dictionary.antonym(msg))

      
      
keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
