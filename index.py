import discord
import os
import requests
import json
from keep_alive import keep_alive
import asyncio
import random
from replit import db
import googletrans
from gif import giffy


client = discord.Client()

translator = googletrans.Translator()
lang = []


sad_words = [
    "sad", "depressed", "depressing", "hopeless", "i'm feeling low", "unhappy",
    "angry", "frustrated", "miserable", "I'm feeling low", "im feeling low"
]

encouragement = [
    "Hang in there. Here's a joke for you!",
    "You got this. Here's a joke for you!",
    "I hope you feel better. Here's a joke for you!",
    "Cheer up! Better things will come your way. Like this joke -",
    "You're a great person! Here's a joke for you."
]

if "responding" not in db.keys():
    db["responding"] = True


def get_joke():
    response = requests.get(
        "https://official-joke-api.appspot.com/random_joke")
    json_data = json.loads(response.text)
    joke = json_data['setup'] + json_data['punchline']
    return (joke)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('With Words'))


@client.event
async def on_guild_join(guild):
    channel = await guild.create_text_channel('plus-bot')
    await channel.send("Make way for me. I'm here!")

channels = ['plus-bot']

@client.event
async def on_message(message):
    if str(message.channel) in channels:
        if message.author == client.user:
            return

        if message.content.startswith('+hello'):
            await message.channel.send('Hello!')
            await message.channel.send(await giffy())
            

        if message.content.startswith('+joke'):
            joke = get_joke()
            await message.channel.send(joke)

        if message.content.startswith('+forever'):

            async def hello():
                joke = get_joke()
                await message.channel.send(joke)
                await asyncio.sleep(3600)
                await hello()

            await hello()

        msg = message.content

      
        if message.content.startswith('*lang'):
          dict = googletrans.LANGUAGES
          await message.channel.send("The languages available in ShabdKosh are:\n")
          ln = ""
          for i in dict.items():
            #print (i)
            ln = ln + str(i) + "\n"
            #print(ln)
          await message.channel.send(ln)      
          #await message.channel.send(str(x,y))

        if message.content.startswith('*tle'):
          msg = message.content.split("\"")
          print(msg)
          tle = translator.translate(msg[1], dest=msg[2].lstrip())
          await message.channel.send("`{}` -> `{}`".format(msg[1], tle.text))

  # """if message.content.startswith('*dt'):
  #   msg = message.content[4:]
  #   await message.channel.send("The message is in {}".format(translator.detect(msg)))"""
    
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

        from PyDictionary import PyDictionary
        dictionary=PyDictionary()

#           if message.content.startswith('*th'):
#           msg = message.content[4:]
#           #print(msg)
#           meaning = py_thesaurus.Thesaurus(msg)
#           print(meaning.get_synonym())
#           await message.channel.send(meaning.get_definition())
        
        if message.content.startswith('*dict'):
          try:
            msg = message.content[6:]
            #print(msg)
            await message.channel.send(dictionary.meaning(msg))
          except:
            await message.channel.send("Meaning not found.")

        if message.content.startswith('*syn'):
          msg = message.content[5:]
          #print(msg)
          await message.channel.send(dictionary.synonym(msg)) 

        if message.content.startswith('*ant'):
          msg = message.content[5:]
          #print(msg)
          await message.channel.send(dictionary.antonym(msg)) 

        if db["responding"]:
            if any(word in msg for word in sad_words):
                await message.channel.send(random.choice(encouragement))
                joke = get_joke()
                await message.channel.send(joke)

        
        

keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
