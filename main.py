import os
from discord.ext import commands as commands
from urllib import parse, request
import re
import discord
from discord import FFmpegPCMAudio
import youtube_dl

dir_frases="Frases/"
wav=".wav"
token = os.environ['Token']

bot = commands.Bot(command_prefix ='- ')

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
YDL_OPTIONS =  {'format':"bestaudio"}
queue = []

#Comandoss
# comandos varioss
def check_queue(ctx,arg):
  for i in queue:
    print(i)
  if len(queue)!=0 and arg == 1:
    vc=ctx.voice_client
    source=queue.pop(0)
    
    vc.play(source)
  elif len(queue)!=0 and arg == 0:
    return len(queue)
    
def youtube(search):
  query_string = parse.urlencode({'search_query':search})
  html_content = request.urlopen('https://www.youtube.com/results?'+ query_string)
  search_results = re.findall( r"watch\?v=(\S{11})", html_content.read().decode())
  return "https://www.youtube.com/watch?v="+search_results[0]

  
@bot.command()
async def ping(ctx):
  print("pong")
  await ctx.send('pong')
def filetowav(dir_frases,filename):
  actual_filename = filename[:-4]
  filename = dir_frases+filename
  if(filename.endswith(".mp4")):
      os.system('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}/{}.wav'.format(filename, dir_frases, actual_filename))
  else:
      pass

  
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
    ctx.author
    if(vc.is_playing() == False):
      await ctx.send("En estos momentos esta sonando "+url)
      vc.play(source, after = lambda x=None: check_queue(ctx,1))
    else:
      queue.append(source)
      await ctx.send("La cancion sonara despues")
@bot.command()
async def pase(ctx,*,args):
  try:
      from googlesearch import search
  except ImportError:
      print("No module named 'google' found")
  # to searcha
  query = args
  for j in search(query, num_results=5):
      await ctx.send(j)
@bot.command()
async def lulu(ctx):
  lulu = "https://www.lolhentai.net/index?/category/lulu"
  await ctx.send(lulu)
     
@bot.command()
async def callese(ctx):
  ctx.voice_client.stop()
@bot.command()
async def espere(ctx):
  ctx.voice_client.pause()
@bot.command()
async def siga(ctx): 
  ctx.voice_client.resume()
#Bareto comandosddd
@bot.command()
async def diga(ctx,*,args):
  vc = ctx.voice_client
  if vc is None:
    await ctx.send("Oiga animal no estoy en ningun canal de voz")
    return
  if 'plante' in args:
    source = FFmpegPCMAudio(dir_frases+"plante_perra"+wav)
  elif 'horario' in args:
    source = FFmpegPCMAudio(dir_frases+"horario_naujotil"+wav)
  elif 'aprenda a contar' in args:
    source = FFmpegPCMAudio(dir_frases+"aprenda_a_contar"+wav)
  elif '10 pendejadas' in args:
    source = FFmpegPCMAudio(dir_frases+"pendejadas"+wav)
  if(vc.is_playing() == False):
    vc.play(source, after = lambda x=None: check_queue(ctx,1))
  else:
    queue.append(source)
    await ctx.send("lo digo despues perro")

@bot.command()
async def uwu(ctx):
  vc = ctx.author.voice.channel
  if(ctx.voice_client is None):
    await vc.connect()
  else:
    await ctx.voice_client.move_to(vc)
  source = FFmpegPCMAudio(dir_frases+"uwu"+wav)
  if(vc.is_playing() == False):
    vc.play(source, after = lambda x=None: check_queue(ctx,1))
  await ctx.voice_client.disconnect()
#Eventos
@bot.event
async def on_ready():
  print("Que paso perro hijueputa {0.user}".format(bot))
@bot.event

async def on_message(message):
  if message.author == bot.user:
    return
  if "49" in message.author.name:
    await message.channel.send(message.author.name+" Haga silencio porfavor")
    #return
  if "uwu" in message.content:
    message.content="- uwu"
    await bot.process_commands(message)
    return
  if message.content.startswith("- "):
    #await message.channel.send("Que paso perro hijueputa?")
    await bot.process_commands(message)

bot.run(token)

