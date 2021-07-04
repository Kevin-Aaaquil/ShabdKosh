import os
import discord
import googletrans
from datetime import datetime
#from google_speech import Speech
from gif import giffy 
#from discord.flags import Intents
#import speech_recognition as spr
#from googletrans import Translator
#from discord.ext import commands
#from gtts import gTTS


client = discord.Client()


translator = googletrans.Translator()


@client.event
async def on_ready():
    print('{0.user} is active now.'.format(client)) #logged in
    await client.change_presence(activity=discord.Game('With Words'))  #adds the status of the bot


@client.event
async def on_guild_join(guild):
    channel = await guild.create_text_channel('shabdkosh') #creates channel shabdkosh
    await channel.send(
        'Hello! Hola! Hallo! I am ShabdKosh, your personal word assistant!')


channel = ['shabdkosh']


@client.event
async def on_message(message):
    if str(message.channel) in channel: #allows users to interact only in shabdkosh channel
        if message.author == client.user:
            return
        
        #say hi!
        if message.content.startswith('*hello'): 
            await message.channel.send(await giffy())
        
       #translate function
        if message.content.startswith('*tle'):
            msg = message.content.split("\"")
            #print(msg)
            tle = translator.translate(msg[1], dest=msg[2].lstrip())
            await message.channel.send("`{}` -> `{}`".format(msg[1], tle.text))
       
        ldict = googletrans.LANGUAGES
           
        #detect function
        if message.content.startswith('*dt'):
            msg = message.content[4:]
            language = str(translator.detect(msg))
            l1 = language.split("=", 1)[1]
            print(l1)
            lcode = l1.split(",")[0]
            print(lcode)
            await message.channel.send("The message is in {}".format(
                ldict.get(lcode)))

        from PyDictionary import PyDictionary
        dictionary = PyDictionary()

        #dictionary function
        if message.content.startswith('*dict'):
            msg = message.content[6:]
            await message.channel.send(dictionary.meaning(msg))

        #synonyms function
        if message.content.startswith('*syn'):
            msg = message.content[5:]
            await message.channel.send(dictionary.synonym(msg))

        #antonyms function
        if message.content.startswith('*ant'):
            msg = message.content[5:]
            await message.channel.send(dictionary.antonym(msg))

        #gives list of languages supported by ShabdKosh
        if message.content.startswith('*lang'):
          dict = googletrans.LANGUAGES
          await message.channel.send("The languages available in ShabdKosh are:\n")
          ln = ""
          for i in dict.items():
            ln = ln + str(i) + "\n"
          await message.channel.send(ln)      
        
        #help command
        if message.content.startswith('*help'):
          await message.channel.send(" ```*help - Displays the commands of ShabdKosh📚 \n*hello- Pops in to say Hi!📘 \n*lang - Displays the languages in ShabdKosh's pocket!📖 \n*tle \"sentence\" lang_code- Translates words from 100+ languages📗 \n*dt sentence - Detects the language of the sentence📙 \n*dict word - Displays the meaning of the word in English✨ \n*syn word - Gives synonyms of the word in English🔖 \n*ant word - Gives antonyms of the word in English📑 ``` ")

my_secret = os.environ['TOKEN']
client.run(my_secret)
