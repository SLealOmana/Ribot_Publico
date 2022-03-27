import os
from discord.ext import commands as commands
from urllib import parse, request
import re
import discord
import youtube_dl

token = os.environ['Token']
bot = commands.Bot(command_prefix ='ribot ')
queue = []
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
YDL_OPTIONS =  {'format':"bestaudio"}

#Comandos
# comandos varios
def check_queue(ctx,arg):
  if len(queue)!=0 and arg == 1:
    vc=ctx.voice_client
    source=queue.pop(0)
    vc.play(source)
  elif len(queue)!=0 and arg == 0:
    return len(queue)
    
def youtube(search):
  query_string = parse.urlencode({'search_query':search})
  html_content = request.urlopen('http://www.youtube.com/results?'+ query_string)
  search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
  return "https://www.youtube.com/watch?v="+search_results[0]
@bot.command()
async def ping(ctx):
  print("pong")
  await ctx.send('pong')
# comandos de voz
@bot.command()
async def entre(ctx):
  if(ctx.author.voice is None):
    await ctx.send("Primero unase a un canal de voz sapohijueputa")
    return
  voice_channel = ctx.author.voice.channel
  if(ctx.voice_client is None):
    await voice_channel.connect()
  else:
    await ctx.voice_client.move_to(voice_channel)
@bot.command()
async def salgase(ctx):
  await ctx.voice_client.disconnect()



@bot.command()
async def coloque(ctx,*,url):
  vc = ctx.voice_client
  if vc is None:
    await ctx.send("Oiga animal no estoy en ningun canal de voz")
    return
  print(url)
  url = youtube(url)
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url,download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
    queue.append(source)
    try:
      vc.play(source, after = lambda x=None: check_queue(ctx,1))
    except:
      await ctx.send("La cancion sonara despues")
    
@bot.command()
async def callese(ctx):
  ctx.voice_client.stop()
@bot.command()
async def espere(ctx):
  ctx.voice_client.pause()
@bot.command()
async def siga(ctx):
  ctx.voice_client.resume()

#Eventos
@bot.event
async def on_ready():
  print("Que paso perro hijueputa {0.user}".format(bot))
#@bot.event
#
#async def on_message(message):
  
  #if message.author == bot.user:
    #return
 #if message.content.startswith("ribot"):
  #  await message.channel.send("Que paso perro hijueputa?")
 #await bot.process_commands(message)

bot.run(token)

