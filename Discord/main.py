import discord 
from discord.ext import commands
import os
import sqlite3
import typing
import random
import asyncio

client = commands.Bot(command_prefix=".")

# for filename in os.listdir("./cogs"):
#   if filename.endswith(".py"):
#     client.load_extenstion(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
  print("Bot is ready")

conn = sqlite3.connect("register.db")

c = conn.cursor()

# c.execute("""CREATE TABLE register(
#             username text
#             password text
#             retype_password text
#           )""")

conn.close()

@client.command()
async def start(ctx):
  embed = discord.Embed(color=discord.Color.blue())
  embed.add_field(name="**Register or Login**", value = "``Hello user welcome to master bot...first lets config your details...register your name``", inline=False)
  await ctx.send(embed=embed)

# @client.event
# async def on_message(message):
#   if message.content.startswith('$greet'):
#       channel = message.channel
#       await channel.send('Say hello!')

#       def check(m):
#           return m.content == 'hello' and m.channel == channel

#       msg = await client.wait_for('message', check=check)
#       await channel.send('Hello {.author}!'.format(msg))
  
#   await client.process_commands(message)


# @client.event
# async def on_message(message):
#   if message.content.startswith('$thumb'):
#       channel = message.channel
#       await channel.send('Send me that 👍 reaction, mate')

#       def check(reaction, user):
#           return user == message.author and str(reaction.emoji) == '👍'

#       try:
#           reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
#       except asyncio.TimeoutError:
#           await channel.send('👎')
#       else:
#           await channel.send('👍')

@client.command()
async def guess(ctx):
    # we do not want the bot to reply to itself
  if ctx.author.id == client.user:
      return

  await ctx.send("Guess a number between 1 and 10")

  def is_correct(m):
      return m.author == ctx.author and m.content.isdigit()

  answer = random.randint(1, 10)

  try:
      guess = await client.wait_for('message', check=is_correct, timeout=5.0)
  except asyncio.TimeoutError:
      return await ctx.channel.send(f'Sorry, you took too long it was {answer}.')

  if int(guess.content) == answer:
      await ctx.channel.send('You are right!')
  else:
      await ctx.channel.send(f'Oops. It is actually {answer}.')

  # client.process_commands(message)


@client.event
async def on_message(message):
  if message.author.id == client.user.id:
    return
  
  if message.author != message.author.bot:
    if not message.guild:
      embed = discord.Embed(color=discord.Color.blue())
      embed.add_field(name="**ModMail SUpport**", value=f"USer Mention:{message.author.mention}\nUsername: {message.author}\n User ID: {message.author.id}\n\n**_Content_**\n{message.content}")
      await client.get_guild(830233837119471637).get_channel(830383383783276564).send(embed=embed)
  
  await client.process_commands(message)

@client.command()
async def echo(ctx):
  message = "Hello this is something"
  sent = await ctx.send(message)

  try:
    msg = await client.wait_for('message',timeout=60, check=lambda message: message.author == ctx.author and message.channe)
  except asyncio.TimeoutError:
    await msg.delete()
    await ctx.send("Cancelling due to timeout", delete_after=10)

client.run('ODMwMjMzNTQ2MTY5Mzg0OTkw.YHDtPg.Wpkns7gLuqaFa1vm9xTCBbY6BN0')