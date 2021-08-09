import discord
import re
from discord.ext import commands
import keep_alive
import os
import random
from discord.utils import find
from discord.ext.commands import BucketType
import json
from discord.utils import find
from datetime import datetime
from time import sleep
import pytz
from discord.ext import tasks

prefixes = ['kurw ', 'konfident', 'Kurw ', 'kb ', 'Kb ', 'KB ']
intent = discord.Intents.all()
intent.reactions = True
client = commands.Bot(command_prefix=prefixes, case_insensitive=True, intents=intent)

@tasks.loop(seconds = 1.0)
async def slow_count():
	server = client.get_guild(640270238868439071)
	mizo = server.get_channel(867867528231387146)
	link = "https://tenor.com/view/happynewyear-2017-gif-7464363"
	while True:
		tz_Madrid = pytz.timezone('Europe/Madrid')
		datetime_Madrid = datetime.now(tz_Madrid)
		time = datetime_Madrid.strftime("%H:%M:%S")
		if time == "00:00:00":
			await mizo.send(link)

		if time == "21:37:00":
			await mizo.send("https://i.imgur.com/a5ZHBqq.gif")

		elif time == "21:38:00":
			await mizo.send("https://i.imgur.com/Tg1hp5N.gif")

		elif time.endswith("00") and not time.startswith("21:37"):
			chances = random.randint(1, 720)
			if chances == 1:
				await mizo.send("https://tenor.com/view/jp2gmd-polishpope-papaj-papiez-papiesz-gif-8449013")

@client.event
async def on_ready():
	print('konfident mode on')

@client.command()
async def pins(ctx, channel = None):
	if not channel:
		channel = ctx.channel
	else:
		channel = find(lambda m: m.name.lower() == channel, ctx.guild.text_channels) #finds channel with the name input by the user

	
	if channel: #checks whether or not a channel with that name was found
		pins = await channel.pins()
	else:
		channel = ctx.channel
		pins = await channel.pins()
	await ctx.send(f'there are {len(pins)} pins in {channel.name}')

@client.command(aliases = ['chuj', 'pp', 'cock', 'penis'])
async def dick(ctx, user = None):
	if user == None:
		user = ctx.author.name
	else:
		res = client.get_user(int(re.search(r'\d+', user).group()))#fetches all integers from "user", basically because when you mention someone discord takes it as <@(user_id)> so its basically to fetch the user id when its a mention
		
		if res != None: #if a user was found
			user = res
	dick = f'8{"".join(["=" for i in range(random.randint(1, 25))])}D'
	em =  discord.Embed(title = f'{user.nick} CHUJEM KURWA: {len(dick)}cm', description = dick, color = discord.Colour.green())
	await ctx.send(embed = em)

token = os.environ['DISCORD_BOT_SECRET']
keep_alive.keep_alive()

client.run(token)