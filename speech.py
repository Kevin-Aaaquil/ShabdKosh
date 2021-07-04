from discord.flags import Intents
import speech_recognition as spr
import discord
from googletrans import Translator
from discord.ext import commands
from gtts import gTTS
import os

intents = discord.Intents.default()

client = commands.Bot(command_prefix = '*', intents=intents)



recog1 = spr.Recognizer()
recog2 = spr.Recognizer()

mc = spr.Microphone(device_index=0)


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
