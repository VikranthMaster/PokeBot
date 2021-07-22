import discord
from discord.ext import commands
import pypokedex
import urllib3
from io import BytesIO
import PIL.Image, PIL.ImageTk
import sys
import os.path
from PIL import Image
import random
import asyncio

client = commands.Bot(command_prefix=".")

def randnum(fname):
	lines=open(fname).read().splitlines()
	return random.choice(lines)

@client.event
async def on_ready():
    print("Bot ready")

#make the check for pokemon_name

@client.command(aliases=["poke","pokemon","p","about"])
async def start(ctx):
    pokemon_name = randnum('pokemon.txt')
    print(f"{pokemon_name}")
    pokemon = pypokedex.get(name=pokemon_name)
    http = urllib3.PoolManager()
    response = http.request('GET', pokemon.sprites.front.get('default'))
    image = PIL.Image.open(BytesIO(response.data))
    img = image.save("pokemon.png")
    with open("pokemon.png","rb") as fp:
        print("All is working good")
        await ctx.send(file = discord.File(fp, "pokemon.png"))
    
    await ctx.channel.send("Whos that pokemon")
    try:
        msg = await client.wait_for(
            "message",
            timeout=10,
            check=lambda m : m.author == ctx.author and m.channel == ctx.channel
        )
        if msg.content.lower() == pokemon_name:
            await ctx.send("You guessed it correct! :partying_face:")
    except asyncio.TimeoutError:
        await ctx.send("Ouch! that pokemon name is {}".format(pokemon_name))
        embed = discord.Embed(color = discord.Color.blue())
        embed.add_field(name = f"**{pokemon.name}**", value = f"Showing Stats for {pokemon.name}", inline=False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

@client.command()
async def test(ctx):
    embed = discord.Embed(color = discord.Color.blue())
    embed.add_field(name = "Something", value= "Someone",inline = False)
    embed.set_thumbnail(url= ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

# @client.event
# async def on_message(message):
#     if message.content.startswith('hello'):
#         await message.channel.send("Hello there")        
#         def check(m):
#             return m.content == "hello" and m.channel == message.channel
#         msg = await client.wait_for('message',check=check)

#         await message.channel.send(f"Hello {msg}")
#     await client.process_commands(message)

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

client.run('TOKEN')
