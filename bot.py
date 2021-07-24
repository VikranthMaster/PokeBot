import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot ready")

try:
    for filename in os.listdir("Coding Files/Python/PokeBot/cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

except FileNotFoundError:
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

client.run('TOKEn')
