import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print("Bot ready")

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

client.run('ODAxMDEyODc4OTM2NzY4NTIy.YAafYA.lE5bR-fdduCm71lOgUla9bTScHo')
