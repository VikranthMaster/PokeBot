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
from pprint import pprint
from discord.ext import tasks
import typing


def randnum(fname):
	lines=open(fname).read().splitlines()
	return random.choice(lines)

seq = [1,3,5,6]

class Pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._cd = commands.CooldownMapping.from_cooldown(1, 6.0, commands.BucketType.member)

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Pokemon Cog ready!")

    @commands.command(aliases = ["find"])
    async def search(self, ctx, pokemon, special=None):
        try:
            p = pypokedex.get(name=pokemon)
        except TypeError:
            await ctx.send("That pokemon Does not exist.")
        if special == None:
            embed = discord.Embed(title = f"**__Showing stats for {pokemon}__**", url = f"https://pokemondb.net/pokedex/{pokemon}", color = discord.Color.blue())
            embed.add_field(name="Pokemon Dex Index : ", value = f"{p.dex}", inline= False)
            embed.add_field(name="Pokemon Weight : ", value = f"``{p.weight/10}``", inline = False)
            embed.add_field(name="Pokemon Height : ", value = f"``{p.height*10}``", inline = False)
            embed.set_thumbnail(icon_url=ctx.author.avatar_url)
            # embed.add_field(name = "Something", value = (discord.File('pokemon.png')), inline=False)
            embed.set_image(url="pokemon.png")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        ratelimit = self.get_ratelimit(message)
        if (message.author.bot) or ratelimit is None:
            return
        else:
            pokemon_name = randnum('Coding Files/Python/PokeBot/pokemon.txt')
            print(f"Pokemon Name : {pokemon_name}")
            pokemon = pypokedex.get(name=pokemon_name)
            http = urllib3.PoolManager()
            response = http.request('GET', pokemon.sprites.front.get('default'))
            image = PIL.Image.open(BytesIO(response.data))
            img = image.save("pokemon.png")
            with open("pokemon.png","rb") as fp:
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

def setup(client):
    client.add_cog(Pokemon(client))
