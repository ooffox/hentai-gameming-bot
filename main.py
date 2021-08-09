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
client = commands.Bot(command_prefix=prefixes,
                      case_insensitive=True,
                      intents=intent)

quotes = [
    'you focking gormless asshole',
    'you are a stupid weapon who lost the plot', 'chips? you mean crisps?',
    'you focking barmy plonker', 'arse licking gannet.', 'mate',
    'focking wanker', 'bloody hell tool',
    'oi bruv mate, you are looking very dishy today',
    'what an absolute spanner', 'you fucking wanker mate',
    'im absolutely fuming mate ill fucking murk you man i swear to god',
    'are you interested in some tea?'
]


@tasks.loop(seconds=1.0)
async def slow_count():
    server = client.get_guild(640270238868439071)
    mizo = server.get_channel(867867528231387146)
    link = "https://tenor.com/view/happynewyear-2017-gif-7464363"
    link2 = "https://tenor.com/view/flick-esfand-esfandtv-ricardo-milos-ricardo-flick-gif-13730968"
    while True:
        tz_Madrid = pytz.timezone('Europe/Madrid')
        datetime_Madrid = datetime.now(tz_Madrid)
        time = datetime_Madrid.strftime("%H:%M:%S")
        if time == "00:00:00":
            await mizo.send(link)

        if time == "22:15:00":
            await mizo.send(link2)

        if time == "21:37:00":
            await mizo.send("https://i.imgur.com/a5ZHBqq.gif")

        elif time == "21:38:00":
            await mizo.send("https://i.imgur.com/Tg1hp5N.gif")

        elif time.endswith("00") and not time.startswith("21:37"):
            chances = random.randint(1, 720)
            if chances == 1:
                await mizo.send(
                    "https://tenor.com/view/jp2gmd-polishpope-papaj-papiez-papiesz-gif-8449013"
                )


@client.event
async def on_ready():
    print('konfident mode on')


@client.command()
async def pis(ctx):
    await ctx.send(f'Czy ty lubić pis?')

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    response = await client.wait_for('message', check=check, timeout=10.0)
    if "tak" in response.content.lower():
        await ctx.send(
            f'Wyglądasz jakbyś językiem czyścił chodniki z psich gówien ty skurwysyński ośle. Zrobię ci z dupy nieskończoną fontannę gówna. Taplaj sie w kale jebany pedale przerżnięty patałachu wypatroszony przez stado goryli. Masz takiego garba że sznurówki zawiązujesz na stojąco ty łysy bezchuju z mongolii. Ty jebany przez stado goryli lumpie, pchaj wibrator niedomyty cepie!!!!!!! Ściśnij dupe bo ci kał wycieka i zasysaj stolca molestowany pawianie z bazaru. Zryty gerontofilu, dmuchany przez sparaliżowaną azerbejdżańską kurwe. Masz ryj jakby cię w dzieciństwie z procy karmili ty zawszony barani pendzlu z rozjebanej chaty szmaciarza z uzbekistanu :>. Zajebie ci w ten kurwa głupi ryj, aż się porzygasz komunijnym bigosem. Zrobie ci z mordy origami ty trędowaty złamasie :>.'
        )
    if "nie" in response.content.lower():
        await ctx.send(f'Szanuje cie kolego, pis to klucz i trzeba go jebac!')


@client.command()
async def pins(ctx, channel=None):
    if not channel:
        chanel = ctx.channel
    else:
        channel = find(lambda m: m.name.lower() == channel,
                       ctx.guild.text_channels
                       )  #finds channel with the name input by the user

    if channel:  #checks whether or not a channel with that name was found
        pins = await channel.pins()
    else:
        channel = ctx.channel
        pins = await channel.pins()
    await ctx.send(f'there are {len(pins)} pins in {channel.name}')


@client.command()
async def briish(ctx):
    await ctx.send(f'{random.choice(quotes)}')


@client.command(aliases=['chuj', 'pp', 'cock', 'penis'])
async def dick(ctx, user=None):
    if user == None:
        user = ctx.author.name
    else:
        res = client.get_user(
            int(re.search(r'\d+', user).group())
        )  #fetches all integers from "user", basically because when you mention someone discord takes it as <@(user_id)> so its basically to fetch the user id when its a mention

        if res != None:  #if a user was found
            user = res
    dick = f'8{"".join(["=" for i in range(random.randint(1, 25))])}D'
    em = discord.Embed(title=f'{user.nick} CHUJEM KURWA: {len(dick)}cm',
                       description=dick,
                       color=discord.Colour.green())
    await ctx.send(embed=em)


@client.command()
async def klucz(ctx, user=None):
    if user == None:
        user = ctx.author
    else:
        res = client.get_user(int(re.search(r'\d+', user).group()))
        if res != None:
            user = res  # makes it so when the user doesnt mention anyone it doesnt break and when the user does mention someone it shows the nickname
    percent = random.randint(1, 100)
    em = discord.Embed(
        title=f'klucz %',
        description=f'{user.nick} jest klucz w {percent}% KURWAAAAAAAAAA',
        color=discord.Colour.red())
    await ctx.send(embed=em)


async def fetch_bank(mode=None, userId=None):
    mode = mode.lower() if mode else None

    if mode == 'wallet':
        mode = 0
    elif mode == 'bank':
        mode = 1

    with open("bank.json", "r") as file:
        bank = json.load(file)

    if userId == None and mode == None:
        return bank

    if userId == None:
        return bank[mode]

    return bank[mode][str(userId)]


async def register_user(userId):
    wallet = await fetch_bank('wallet')
    bank = await fetch_bank('bank')
    with open("bank.json", 'w') as file:
        try:
            wallet[str(userId)]
            bank[str(userId)]
        except KeyError:
            wallet[userId] = 0
            bank[userId] = 0
        json.dump([wallet, bank], file)


async def change_bank(userId, mode, amount, debt = True):
    money = [await fetch_bank("wallet"), await fetch_bank("bank")]
    if mode == 'wallet':
        mode = 0
    elif mode == 'bank':
        mode = 1
    if mode == 1 and debt:
        amount = amount * 0.8
    with open("bank.json", "w") as file:
        coins = money[mode][str(userId)]
        money[mode][str(userId)] = coins + amount
        json.dump(money, file)
        return bank

async def below_debt_limit(userId):
    wallet = await fetch_bank('wallet', userId)
    if wallet < -10000:
        return True
    return False


@client.command(aliases = ['with'])
async def withdraw(ctx, amount = None):
    if amount == None or int(amount) <= 0:
        await ctx.send('kurwa give me an amount')
        return
    await register_user(ctx.author.id)
    amount = int(amount)
    bank = await fetch_bank('bank', ctx.author.id)
    if amount > bank:
        await ctx.send('kurwa dont try to withdraw more than the current money in your bank')
        return
    await change_bank(ctx.author.id, 'wallet', amount)
    await change_bank(ctx.author.id, 'bank', -amount)
    await ctx.send(f'succesfully withdrew **{amount}** coins')


@client.command(aliases = ['dep'])
async def deposit(ctx, amount = None):
    if amount == None or int(amount) <= 0:
        await ctx.send('kurwa give me an amount')
        return
    await register_user(ctx.author.id)
    amount = int(amount)
    wallet = await fetch_bank('wallet', ctx.author.id)
    if amount > wallet:
        await ctx.send('kurwa dont try to deposit more than the current money in your wallet')
        return
    await change_bank(ctx.author.id, 'bank', amount)
    await change_bank(ctx.author.id, 'wallet', -amount)
    await ctx.send(f'succesfully deposited {amount} coins')


@client.command(aliases=['wallet', 'money', 'bal', 'balance'])
async def bank(ctx, user=None):
    if user == None:
        user = ctx.author
    else:
        res = client.get_user(int(re.search(r'\d+', user).group()))
        if res != None:
            user = res
        else:
            user = find(lambda m: user in m.name.lower(), ctx.guild.members())
            if user == None:
                await ctx.send('kurwa that user doesnt exist')
                return  # this is all just a username check

    await register_user(user.id)

    bank = await fetch_bank("bank", user.id)
    wallet = await fetch_bank("wallet", user.id)

    em = discord.Embed(title=f'bank of {user.name} kurwa',
                       color=discord.Colour.blurple())

    em.add_field(name="wallet", value=int(wallet), inline=True)
    em.add_field(name="bank", value=bank, inline=True)

    await ctx.send(embed=em)


@commands.cooldown(1, 10, commands.BucketType.user)
@client.command()
async def beg(ctx):
    await register_user(ctx.author.id)
    people = [member.nick for member in ctx.guild.members]
    coins = random.randint(1, 50)
    await ctx.send(f'kurwa, {random.choice(people)} gave you {coins} coins')
    await change_bank(ctx.author.id, 'wallet', coins)


@beg.error
async def beg_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        em = discord.Embed(
            title="**KURWA COOLDOWN**. <:weirdchamp:643921489074061312>",
            description=
            'COOLDOWN KURRRRWA, CO SPANNER, WAIT **{:.0f}** SECONDS.'.format(
                error.retry_after),
            color=discord.Colour.dark_blue())
        await ctx.send(embed=em)
    else:
        raise error


@client.command(aliases=['gamble'])
async def bet(ctx, amount: int):
    await register_user(ctx.author.id)
    bank = await fetch_bank('bank', ctx.author.id)
    wallet = await fetch_bank('wallet', ctx.author.id)
    if amount <= 0:
        await ctx.send('kurwa stop pierdoling')
        return
    if amount > 1000:
        await ctx.send('dont bet more than 1000 coins kurwa')
        return

    chance = random.randint(1, 10)
    if chance <= 5:
        coins = -round(amount * 2.35)

        em = discord.Embed(
            title=f'kurwa {ctx.author.nick} lost bet :peeposad:',
            color=discord.Colour.red())

        em.add_field(name="amount bet", value=amount, inline=True)

        em.add_field(name="amount lost", value=coins, inline=True)

        em.add_field(name="current wallet + bank amount",
                     value=int(wallet + bank + coins),
                     inline=True)
    elif chance > 5:
        coins = round(amount * 2.35)

        em = discord.Embed(
            title=f'kurwa {ctx.author.nick} won bet :peepohappy:',
            color=discord.Colour.green())

        em.add_field(name="amount bet", value=amount, inline=True)

        em.add_field(name="amount won", value=coins, inline=True)

        em.add_field(name="current wallet + bank amount",
                     value=int(wallet + bank + coins),
                     inline=True)
    await ctx.send(embed=em)

    await change_bank(ctx.author.id, 'wallet', coins)
    below_debt = await below_debt_limit(ctx.author.id)
    if below_debt:
        await ctx.send('you went below the debt limit of 10000 kurwa, you lost all your coins and items')
        await change_bank(ctx.author.id, 'wallet', -wallet)
        await change_bank(ctx.author.id, 'bank', -bank)

token = os.environ['DISCORD_BOT_SECRET']

keep_alive.keep_alive()

client.run(token)
