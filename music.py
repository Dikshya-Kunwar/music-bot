import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
import os
from dotenv import load_dotenv
load_dotenv()

intents= discord.Intents.all()
intents.members= True
client= commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is ready for use!")
    print("---------------")

#join the voice channel
@client.command(pass_context=True)
async def play(ctx, url:str):
    if(ctx.author.voice):
        try:
            channel = ctx.message.author.voice.channel
            voice = await channel.connect()
            ydl_opts={
                'format': 'bestaudio/best',
                'postprocessors':[{
                    'key':'FFmpegExtractAudio',
                    'preferredcodec':'mp3',
                    'preferredquality':'192',
                }],
            }
            os.remove("song.mp3")
            ffmpeg ={'options': '-vn'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file,"song.mp3")
            source= FFmpegPCMAudio("song.mp3")
            player= voice.play(source)
        except Exception as e:
                print(e)

    else:
        await ctx.send("User Must be in the voice channel to use this command")


#leave the voice channel
@client.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")

#pause a song
@client.command(pass_context=True)
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("There is no audio playing in the voice channel.")

# resume a song
@client.command(pass_context=True)
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("There is no audio paused in the voice channel.")


#stop a song
@client.command(pass_context=True)
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        os.remove("song.mp3")
        print(f"File 'song.mp3 deleted successfully.")
    else:
        await ctx.send("There is no audio playing in the voice channel.")


client.run('TOKEN')
