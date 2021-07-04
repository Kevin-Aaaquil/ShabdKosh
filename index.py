import os
import discord
import googletrans
from datetime import datetime
from google_speech import Speech  # for voice module
from gif import giffy
from discord.flags import Intents
import speech_recognition as spr
from googletrans import Translator
from discord.ext import commands
from gtts import gTTS



client = discord.Client()


translator = googletrans.Translator()


@client.event
async def on_ready():
    print('{0.user} is active now.'.format(client))
    await client.change_presence(activity=discord.Game('With Words'))


@client.event
async def on_guild_join(guild):
    channel = await guild.create_text_channel('shabdkosh')
    await channel.send(
        'Hello! Hola! Hallo! I am ShabdKosh, your personal word assistant!')


channel = ['shabdkosh']


@client.event
async def on_message(message):
    if str(message.channel) in channel:
        if message.author == client.user:
            return

        if message.content.startswith('*Hello'):
            await message.channel.send(await giffy())
            await message.channel.send(googletrans.LANGUAGES)

        if message.content.startswith('*tle'):
            msg = message.content.split("\"")
            print(msg)
            tle = translator.translate(msg[1], dest=msg[2].lstrip())
            await message.channel.send("`{}` -> `{}`".format(msg[1], tle.text))

        ldict = googletrans.LANGUAGES

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

        if message.content.startswith('*dict'):
            msg = message.content[6:]
            await message.channel.send(dictionary.meaning(msg))

        if message.content.startswith('*syn'):
            msg = message.content[5:]
            await message.channel.send(dictionary.synonym(msg))

        if message.content.startswith('*ant'):
            msg = message.content[5:]
            await message.channel.send(dictionary.antonym(msg))

#         if message.content.startswith('*help'):
#           async def help(ctx):
#             author = ctx.message.author
            
#             embed = discord.Embed(colour = discord.Colour.yellow())

#             embed.set_author(name='Help')
#             embed.add_field(name='*hello',value = 'Returns a hello!',inline = False)
          
      
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel, you must be in a voice channel to run this command")


@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


intents = discord.Intents.default()

client = commands.Bot(command_prefix = '*', intents=intents)



@client.event
async def on_message(message):
    if str(message.channel) in channel:
        if message.author == client.user:
            return
        
        recog1 = spr.Recognizer()
        recog2 = spr.Recognizer()

        mc = spr.Microphone(device_index=0)
        
        if message.content.startswith('*voice'):
          
          with mc as source:
            print("Speak 'Hello' to initiate the Translation!")
            print("----------------------------")
            audio = recog1.listen(source)
          if 'hello' in recog1.recognize_google(audio):
            recog1 = spr.Recognizer()
            translator = Translator()
            from_lang = 'en'
            to_lang = 'hi'
            with mc as source:
              print('Speak a sentence...')
              audio = recog2.listen(source)
              get_sentence = recog2.recognize_google(audio)
        
            try:
              get_sentence = recog2.recognize_google(audio)
              print('Phrase to be Tranlated: '+ get_sentence)
              text_to_translate = translator.translate(get_sentence,dest = to_lang, src = from_lang) 
              #print(text_to_translate.text)
              text = text_to_translate.text
              speak = gTTS(text=text, lang = to_lang, slow = False)
              speak.save("captured_voice.mp3")
              os.system("start captured_voice.mp3")
            except spr.UnknownValueError:
              print("Unable to understand the input")
            except spr.RequestError as e:
              print("Unable to provide required output".format(e))
          


keep_alive()

my_secret = os.environ['TOKEN']
client.run(my_secret)
