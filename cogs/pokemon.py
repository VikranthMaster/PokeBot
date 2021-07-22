import discord
from discord.ext import commands
import pypokedex
import urllib3
from io import BytesIO
import PIL.Image, PIL.ImageTk
import sys
import os
import os.path
from PIL import Image
import random
import asyncio
import time

def randnum(fname):
	lines=open(fname).read().splitlines()
	return random.choice(lines)

seq = [12,30,45,60]

class Pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pokemon Cog ready!")

    # @commands.command()
    # async def start(self,ctx):
    #     pokemon_name = randnum('pokemon.txt')
    #     print(f"{pokemon_name}")
    #     pokemon = pypokedex.get(name=pokemon_name)
    #     http = urllib3.PoolManager()
    #     response = http.request('GET', pokemon.sprites.front.get('default'))
    #     image = PIL.Image.open(BytesIO(response.data))
    #     img = image.save("pokemon.png")
    #     with open("pokemon.png","rb") as fp:
    #         print("All is working good")
    #         await ctx.send(file = discord.File(fp, "pokemon.png"))
        
    #     await ctx.channel.send("Whos that pokemon")
    #     try:
    #         msg = await self.client.wait_for(
    #             "message",
    #             timeout=10,
    #             check=lambda m : m.author == ctx.author and m.channel == ctx.channel
    #         )
    #         if msg.content.lower() == pokemon_name:
    #             await ctx.send("You guessed it correct! :partying_face:")
    #     except asyncio.TimeoutError:
    #         await ctx.send("Ouch! that pokemon name is {}".format(pokemon_name))
    #         embed = discord.Embed(color = discord.Color.blue())
    #         embed.add_field(name = f"**{pokemon.name}**", value = f"Showing Stats for {pokemon.name}", inline=False)
    #         embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    #         await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        time.sleep(random.choice(seq))
        if (message.author.bot):
            return
        else:
            pokemon_name = randnum('pokemon.txt')
            print(f"{pokemon_name}")
            pokemon = pypokedex.get(name=pokemon_name)
            http = urllib3.PoolManager()
            response = http.request('GET', pokemon.sprites.front.get('default'))
            image = PIL.Image.open(BytesIO(response.data))
            img = image.save("pokemon.png")
            with open("pokemon.png","rb") as fp:
                print("All is working good")
                await message.channel.send(file = discord.File(fp, "pokemon.png"))
            
            await message.channel.send("Whos that pokemon")
            try:
                msg = await self.client.wait_for(
                    "message",
                    timeout=10,
                    check=lambda m : m.author == message.author and m.channel == message.channel
                )
                if msg.content.lower() == pokemon_name:
                    await message.channel.send("You guessed it correct! :partying_face:")
            except asyncio.TimeoutError:
                await message.channel.send("Ouch! that pokemon name is {}".format(pokemon_name))
                embed = discord.Embed(color = discord.Color.blue())
                embed.add_field(name = f"**{pokemon.name}**", value = f"Showing Stats for {pokemon.name}", inline=False)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
                await message.channel.send(embed=embed)



    @commands.command()
    async def test(self,ctx):
        embed = discord.Embed(color = discord.Color.blue())
        embed.add_field(name = "Something", value= "Someone",inline = False)
        embed.set_thumbnail(url= ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Pokemon(client))
