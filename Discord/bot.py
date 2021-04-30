import discord
from discord.ext import commands
import sqlite3
import pypokedex
import urllib3
from io import BytesIO
import PIL.Image, PIL.ImageTk
import sys
import os.path
from PIL import Image

client = commands.Bot(command_prefix=".")

# conn = sqlite3.connect("main.db")

# c = conn.cursor()

# # c.execute("""CREATE TABLE IF NOT EXISTS levels (
# #             guild_id text
# #             msg text
# #             channel_id TEXT
# # )""")


@client.event
async def on_ready():
    print("Bot ready")


# @client.event
# async def on_message(message):
#     if message.content.startswith('.hello'):
#         await message.channel.send('Hello!')

#     await client.process_commands(message)

# @client.command()
# async def welcome(ctx):
#     await ctx.send("Avaible Setup commands: \nwelcome channel <#channel>\nwelcome text <message>")

# @welcome.command
# async def channel(ctx, channel:discord.TextChannel):
#     if ctx.message.author.guild_permissions.manage_messages:
#         db = sqlite3.connect('main.db')        
#         cursor = db.cursor()
#         cursor.execute("SELECT channel_id FROM levels WHERE guild_id = {ctx.guild.id}")
#         result = cursor.fetchone()
#         if result is None:
#             sql = ("INSERT INTO levels(guild_id, channel_id) VALUES(?,?)")
#             val = (ctx.guild.id, channel.id)
#             await ctx.send(f"Channel has been set to {channel.mention}")
#         elif result is not None:
#             sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
#             val = (channel.id, ctx.guild.id)
#             await ctx.send(f"Channel has been updated to {channel.mention}") 
#         cursor.execute(sql, val)
#         db.commit()
#         cursor.close()
#         db.close()

# def load_pokemon(pokemon_name):
#     pokemon = pypokedex.get(name=pokemon_name)
#     http = urllib3.PoolManager()
#     response = http.request('GET', pokemon.sprites.front.get('default'))
#     image = PIL.Image.open(BytesIO(response.data))
#     # if os.path.exists("pokemon.png"):
#     #     os.remove("pokemon.png")
#     # else:
#     image.save("pokemon.png")

@client.command(aliases=["poke","pokemon","p","about"])
async def find(ctx,*,pokemon_name):
    await ctx.send(f"{pokemon_name} Detected!")
    pokemon = pypokedex.get(name=pokemon_name)
    http = urllib3.PoolManager()
    response = http.request('GET', pokemon.sprites.front.get('default'))
    image = PIL.Image.open(BytesIO(response.data))
    img = image.save("pokemon.png")
    with open("pokemon.png","rb") as fp:
        print("All is working good")
        await ctx.send(file = discord.File(fp, "pokemon.png"))

    embed = discord.Embed(color = discord.Color.blue())
    embed.add_field(name = f"**{pokemon.name}", value = f"Showing Stats for {pokemon.name}, inline=False")
    embed.set_thumbnail(url = image)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@client.command()
async def test(ctx):
    embed = discord.Embed(color = discord.Color.blue())
    embed.add_field(name = "Something", value= "Someone",inline = False)
    embed.set_thumbnail(url= ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

client.run('TOKEN')
