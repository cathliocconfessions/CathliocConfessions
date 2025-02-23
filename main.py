import json
import random
import re
import asyncio
from logging import exception, raiseExceptions

import aiohttp
import base64
import os
from supabase import create_client, Client
import dataset
import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import time
import os
import sys
from discord.ext.commands import CommandOnCooldown

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

COOKIES_FILE = "cookies.txt"

queue = []
onmessagedeletelist = ["bro forgot about digital footprint", "watch what you say next time!", "Your message cant be hidden from me", "yall screenshot this rq and post it to twitter.com", "nice try buddy boy", "you are gonna be haunted by this in the future", ]
intents = discord.Intents.all()
intents.members = True
load_dotenv()
bot = commands.Bot(command_prefix="!", intents=intents)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
# Connect to the Supabase database



def play_next(vc):
    if queue:
        # Get the next song from the queue
        next_song = queue.pop(0)  # Using the single queue
        print(f"Playing next song from queue: {next_song}")

        # Play the next song
        vc.play(
            discord.FFmpegPCMAudio(next_song),
            after=lambda e: play_next(vc),
        )
    else:
        # No more songs in the queue
        print("Queue is empty. No more songs to play.")
        return

def error(f):
    catrequest = requests.get('https://api.thecatapi.com/v1/images/search')
    catphoto = json.loads(catrequest.text)[0]
    print(catrequest.text)
    embed = discord.Embed(colour=0x313338, color=0x313338, title="Uh oh an error!", type='rich', url=None, description=f'This has been reported to the debugging server and will get fixed soon!', timestamp=None)
    embed.add_field(name="Error", value=f, inline=True)
    embed.add_field(name="You found a glitch! now have a cat 🐱", value='discord.py required me to have this lol so this is placeholder text LALALALA', inline=True)
    embed.set_image(url=catphoto['url'])
    return embed

async def send_dm(user_id: int, message: str):
    user = await bot.fetch_user(user_id)
    if user:
        await user.send(message)

presencelines = ["Hawk tuah on that thang", "im fuckin a cow doggystyle", "menoga GIVE ME YOUR FUCKING GITHUB USERNAME", "I love you", "i am a orange", "We are all made to die", "My name dont even have a point anymore", "More mouse bites please", "i suck ass", "owo bot got nothing on me", "Turbo masturbo best author", "I have minecraft youtuber levels of deviousness", "i dont know what to do anymore", "i made an essay on video games", "/balance lol", "mega is a cute gay gooner", "I am a cute gay gooner", "im tired boss", "Mega have you given my dad your github username yet?", "𓋴𓇋𓃭𓆯𓅂𓂋 𓇋𓋴 𓄿 𓎢𓅲𓏏𓅂 𓎼𓄿𓇌 𓎼𓅱𓅱𓈖𓅂𓂋", "Ozar is not a cute gay gooner"]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    try:
        synced = await bot.tree.sync()
        await bot.change_presence(activity=discord.Game(name=random.choice(presencelines)))
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="Pong!")
async def ping(interaction: discord.Interaction):
    ping = round(bot.latency * 1000)
    if ping > 100:
        embed = discord.Embed(colour=0x313338, color=0x313338, title="Bot may be having some problems", type='rich', url=None, description=f'The bot is having some latency issues.', timestamp=None)
        embed.add_field(name="Current ping ⛔", value=f'{ping}ms', inline=True)
        await interaction.response.send_mesesage(embed=embed)
    else:
        embed = discord.Embed(colour=0x313338, color=0x313338, title="The bot is working normally.", type='rich', url=None, description=f'The bot is working. Please check the discord server for announcements or downtime!', timestamp=None)
        embed.add_field(name="Current ping ✅", value=f'{ping}ms', inline=True)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="lookup", description="Lookup a user. (silver only)")
@app_commands.commands.describe(user="The user to lookup")
async def lookup(interaction: discord.Interaction, user: discord.User = None):
    if interaction.user.id == 970493985053356052:
        user_id = user.id
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if not response:
            await interaction.response.send_message(f" {user.name} not found in the database!")
            return
        else:
            await interaction.response.send_message(f"User data: {response}")


@bot.tree.command(name="add_all_to_db", description="Adds all members of the guild to the database.")
async def add_all_to_db(interaction: discord.Interaction):
    if not interaction.user.id == 970493985053356052:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
        return

    else:
        await interaction.response.defer()

        guild = interaction.guild

        for member in guild.members:
            username = member.name
            user_id = member.id
            balance = 0
            lvlxp = 0
            lvl = 0


            if member in guild.premium_subscribers:
                donated = True
            else:
                donated = False

            response = (supabase.table('users').insert([{'id': user_id, 'username': username, 'donated': donated, 'balance': balance, "lvlxp": lvlxp, "lvl": lvl}])).execute()


    await interaction.edit_original_response(content="All members have been added to the database!")

@bot.event
async def on_member_join(member):
    username = member.name
    user_id = member.id
    donated = False
    balance = 0
    lvlxp = 0
    lvl = 0
    response = (supabase.table('users').insert([{'id': user_id, 'username': username, 'donated': donated,
                                                 'balance': balance, "lvlxp": lvlxp, "lvl": lvl}])).execute()

@bot.tree.command(name="fishjoke", description="Generates a random fish pun.")
async def fishpun(interaction: discord.Interaction):
    fish_puns = [
        "Looks like you’re cod-ing something fishy here.",
        "You’re so fin-tastic for asking—I can tuna my response any way you’d like!",
        "Let’s not carp about it and dive straight in.",
        "I’m hooked on helping you out with puns; I’ll tackle this line by line!",
        "Gill-ty as charged, this is going to be a pun-filled response.",
        "I’m not clowning around—this is a reel opportunity to help.",
        "Don’t trout yourself, you’ve got this!",
        "Want me to bait some more ideas? Just ask.",
        "I’m here to sea things through for you.",
        "This whole conversation is finsane, but I’m still on board.",
        "If you’re feeling eel-y overwhelmed, I can lighten the load.",
        "Let minnow if you need more help—don’t just flounder around.",
        "Keep your friends close but your anemones closer!",
        "Whale, this is a whale-y fun conversation so far.",
        "I krill-ly appreciate you dropping by with such fin-teresting questions.",
        "I’ll scale down the puns if you start to feel the pressure.",
        "Are you squid-ding me here? These puns make the perfect catch!",
        "Let’s wrap this up before things get out of salmon-control!",
        "I’m not salty about making more puns—I’ll just go with the flow.",
        "Holy mackerel! This is an un-fish-ievably fun task.",
        "I’ll kelp you out as much as you need!",
        "You’re the sole reason why I’m swimming in puns right now.",
        "Don’t be koi—I know you’re loving these puns.",
        "Wave hello to a sea-riously great list of puns!",
        "I’m shore you can appreciate how punny this is.",
        "I need to scale back before these puns get too deep.",
        "Cod you believe how many fish jokes are out there?",
        "Let’s not clam up—I’ve got plenty more puns in my net.",
        "You’ve got me floundering for words with all these pun requests.",
        "Having shell much fun with this; I hope you are, too.",
        "You’re doing fintastic—don’t let anyone tell you otherwise.",
        "Just relax and seas the day!",
        "This conversation is o-fish-ally one of the best I’ve had today.",
        "Stop acting so crabby; I haven’t finished yet.",
        "You’re not quite at the fin-ish line for puns; there’s more!",
        "I’ve haddock-nough, but I’ll keep fishing for more.",
        "I have to say, these puns really give me porpoise.",
        "You're dolphinitely my favorite person to share puns with.",
        "If you’re still not satisfied, I sea what I can do next.",
        "Don’t reef me hanging—I’ve got more ideas!",
        "This is a whale of a conversation, don’t you think?",
        "I’m not squidding when I say, these puns will tide you over.",
        "These puns are shrimply the best!",
        "Cod be worse—you could have no puns at all!",
        "Sea-liously though, nautical nonsense is the best nonsense.",
        "Stop being shellfish and share these puns with your friends!",
        "If you’re angling for more, just let me know.",
        "This pun list just keeps rowing and rowing.",
        "Just for the halibut, here’s another pun!",
        "I’m feeling a little shell-shocked by all these puns.",
        "Don’t lobster hope, I believe in you!",
        "Let’s not slack off—this is a plaice for serious puns!",
        "I cod-n’t resist adding more jokes.",
        "I’m shore this joke will tide everyone over.",
        "Anchors aweigh! Let’s dive into another joke.",
        "This is kraken me up!",
        "Seal-iously, I have so many more puns for you.",
        "Don’t let the tide bring you down; keep laughing!",
        "Sardine-ly, you must enjoy these ocean puns!",
        "I'm not angling for compliments, but you keep coming back for more!",
        "I’ll kelp you be the best version of yourself!",
        "Halibut you go and achieve your goals?",
        "Let’s skate into the weekend with joy!",
        "You’re fintastic, don’t let anyone tell you otherwise.",
        "Shell we continue this delightful chat?",
        "Plaices like this make everything better!",
        "You make my heart skip a bream.",
        "Why be crabby when you can be cheerful?",
        "You're swimming into uncharted waters with confidence!",
        "Let's not make things ten-tackle—we've got this!",
        "Keep calm and avoid getting in deep water.",
        "Squidn't life be more fun with a few puns?",
        "You're reel-y inspiring!",
        "Fish puns always hook me, line, and sinker.",
        "Cray-sea times, but nothing we can't handle together!",
        "You're fin-tastic, and I'm not just fishing for compliments.",
        "We're definitely on the same wave-length!",
        "Don't tide yourself up in stress—go with the flow."
    ]

    embed = discord.Embed(color=0xd2e7ba,  title="Fish puns", type='rich', url=None, description=f'{random.choice(fish_puns)}', timestamp=None)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="chatrevive", description="Revives chat in the most inconvent way ")
@commands.has_permissions(administrator=True)
async def chatrevive(interaction: discord.Interaction):
    membercount = 0
    memberpinglist = []
    guild = interaction.guild
    await interaction.response.send_message("SHOOT THE BOMB CAPTIN! ")

    for member in guild.members:
        memberpinglist.append(member.mention)
        membercount = membercount + 1

        if membercount == 10:
            await interaction.followup.send(f"{' '.join(memberpinglist)} WAKE UP MATEY")
            memberpinglist.clear()
            membercount = 0

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # Check if roles have changed
    if len(before.roles) < len(after.roles):  # A role has been added
        added_roles = [role for role in after.roles if role not in before.roles]

        for role in added_roles:
            if role.is_premium_subscriber():
                user_id = after.id
                username = after.name
                displayname = after.display_name
                donated = True
                response = (
                    supabase.table("users")
                    .update({"donated": donated})
                    .eq("id", user_id)
                    .execute()
                )

                await send_dm(user_id, "Thanks for Donating (: You now have access to all of the features in the cathlioc confessions bot! 💖")
                break

@bot.event
async def on_message_delete(message):
    channel = message.channel

    if channel and not message.author.bot:
        embed = discord.Embed(
            title=f"{message.author} Tried to delete a message",
            description=f"{random.choice(onmessagedeletelist)}",
            colour=discord.Colour.red()
        )

        embed.add_field(name="Message:", value=message.content)

        await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):

    if before.content == after.content:
        return

    channel = before.channel

    if before.content and not before.author.bot:
        embed = discord.Embed(
            title=f"{before.author} Edited a message",
            description=f"{random.choice(onmessagedeletelist)}",
            colour=discord.Colour.yellow()
        )

        embed.add_field(name="Before:", value=before.content)
        embed.add_field(name="After:", value=after.content)

        await channel.send(embed=embed)

@bot.tree.command(name="work", description="Work for some cash")
@app_commands.checks.cooldown(1, 120.5)
async def work(interaction: discord.Interaction):
    user_id = interaction.user.id
    response = supabase.table('users').select('*').eq('id', user_id).execute()
    user = response.data[0] if response.data else None

    givingcash = random.randint(45, 136)
    user['balance'] += givingcash
    jobs = [f"You worked as a cashier employee and got {givingcash}", f"you ate some dudes ass and got {givingcash}", f"You scammed samartians by faking that you are poor, {givingcash}", f"You coded a discord bot for a server and they gave you {givingcash}", f"You drew a picture for someone and they gave you {givingcash}", f"You sold newspapers for {givingcash}", f"You became a Rent-a-bitch and got {givingcash} out of it"]

    embed = discord.Embed(
        title="You worked",
        description=f"{random.choice(jobs)}",
        colour=discord.Colour.green()
    )

    user_id = interaction.user.id

    response = supabase.table('users').select('balance').eq('id', user_id).execute()

    if response.data:
        user_balance = response.data[0]['balance']
        new_balance = user_balance + givingcash


    if user:
        response = (
            supabase.table("users")
            .update({"balance": new_balance})
            .eq("id", user_id)
            .execute()
        )

    await interaction.response.send_message(embed=embed)

@work.error
async def work_error(interaction: discord.Interaction, error):
    # Check if the error is caused by the cooldown
    if isinstance(error, app_commands.CommandOnCooldown):
        # Calculate retry time (human-readable)
        retry_after = round(error.retry_after, 2)  # Retry time in seconds (rounded to 2 decimal places)

        embed = discord.Embed(
            title="Cooldown!",
            description="You are on cooldown!",
            color=0xe36572
        )

        await interaction.response.send_message(
            embed=embed
        )
    else:
        raise error  # Re-raise unexpected errors for logging


@bot.tree.command(name="balance", description="Checks how much cash you have")
async def balance(interaction: discord.Interaction):
    # Get the user's Discord ID
    user = interaction.user.id

    # Fetch data from the database for this user

    response = supabase.table('users').select('balance').eq('id', user).execute()

    user_balance = response.data[0]['balance']


    user_balance_formatted = "{:,}".format(user_balance)

    # Check if the user exists in the database

    embed = discord.Embed(
        title="Balance",
        description=f"you have {user_balance_formatted} Dollars ",
        color=0x00ff00  # Green color
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="coinflip", description="lets flip a coin err awh dang it err awh dang it err awh dangit")
@app_commands.describe(money="How much money you gonna gamble??")
@app_commands.describe(coinsides="Pick your poison")
@app_commands.choices(
    coinsides=[
        app_commands.Choice(name="Head", value="Head"),
        app_commands.Choice(name="Tails", value="Tails"),
    ]
)
async def coinflip(interaction: discord.Interaction, money: int = None, coinsides: str = None):
    user = interaction.user.id

    silver = supabase.table('users').select('*').eq('user_id', 970493985053356052).execute().data[0]
    weired = supabase.table('users').select('*').eq('user_id', 1211101305607553116).execute().data[0]

    silver_balance = silver.get('balance', 0)
    weired_balance = weired.get('balance', 0)

    # Fetch data from the database for this user
    user_data = supabase.table('users').select('*').eq('user_id', user).execute().data[0]

    # Check if the user exists in the database
    if user_data is None:
        await interaction.response.send_message(
            "Uh oh, Looks like you werent found in our database. Please ping Silverstero for help")
        return

    user_balance = user_data.get('balance', 0)

    if money > user_balance:
        embed = discord.Embed(
            title="Uh oh",
            description="You dont have enough cash bucko",
            color=discord.Colour.red()
        )

        await interaction.response.send_message(embed=embed)

    coinside = random.choice(['Head', 'Tails'])

    if coinside == coinsides:
        embed = discord.Embed(
            title="You won zamn",
            description=f"you got {money} dollars",
            color=discord.Colour.green()
        )
        await interaction.response.send_message(embed=embed)
        user_balance += money
        supabase.table('users').update({'balance': user_balance}).eq('user_id', user).execute()

    else:

        embed = discord.Embed(
            title="You lost damn",
            description=f"you lost {money} dollars",
            color=discord.Colour.red()
        )

        await interaction.response.send_message(embed=embed)
        user_balance -= money
        supabase.table('users').update({'balance': user_balance}).eq('user_id', user).execute()
        split = money / 2

        silver_balance += split
        weired_balance += split

        supabase.table('users').update({'balance': silver_balance}).eq('user_id', 970493985053356052).execute()
        supabase.table('users').update({'balance': weired_balance}).eq('user_id', 1211101305607553116).execute()


@bot.tree.command(name="slots", description="lets go gambling err awh dang it err awh dang it err awh dangit")
@app_commands.describe(money="How much money you gonna gamble??")
async def slots(interaction: discord.Interaction, money: int = None,):
    user = interaction.user.id

    silver = supabase.table('users').select('*').eq('user_id', 970493985053356052).execute().data[0]
    weired = supabase.table('users').select('*').eq('user_id', 1211101305607553116).execute().data[0]

    silver_balance = silver.get('balance', 0)
    weired_balance = weired.get('balance', 0)

    # Fetch data from the database for this user
    user_data = supabase.table('users').select('*').eq('user_id', user).execute().data[0]

    # Check if the user exists in the database
    if user_data is None:
        await interaction.response.send_message("Uh oh, Looks like you werent found in our database. Please ping Silverstero for help")
        return

    user_balance = user_data.get('balance', 0)

    if money > user_balance:
        await interaction.response.send_message("You dont have enough cash bucko")
        return

    slotmachinenumber = random.randint(1, 10000)
    schlatt = discord.PartialEmoji(name="schlatt", id=1327471277866483834)
    spiningemoji = discord.PartialEmoji(name="spinning", id=1327471218814881813)
    moneyemoji = discord.PartialEmoji(name="monery", id=1327471227278856222)
    trollface = discord.PartialEmoji(name="trollface", id=1327471236619698227)
    bigface1 =  discord.PartialEmoji(name="bigface1", id=1327471248057565296)
    bigface2 =  discord.PartialEmoji(name="bigface2", id=1327471257142169622)
    bigface3 =  discord.PartialEmoji(name="bigface3", id=1327471268450013236)



    slotemoji1 = '<a:spinning:1327471218814881813>'
    slotemoji2 = '<a:spinning:1327471218814881813>'
    slotemoji3 = '<a:spinning:1327471218814881813>'

    slotemojis = ['<a:monery:1327471227278856222>', '<:trollface:1327471236619698227>', '<:bigface1:1327471248057565296>', '<:bigface2:1327471257142169622>', '<:bigface3:1327471268450013236>']

    def build_format():
        return (
            f"`| Silver and weired slot machine no: {slotmachinenumber}  |` \n"
            "`|`                                                                                             `|`\n"
            f"                                `|`{slotemoji1}`|`{slotemoji2}`|`{slotemoji3}`|` \n"
            "                                `|             |` \n"
            "                                `|             |` \n"
            "                                `|             |` \n"
        )
    format = build_format()
    weights = [1,1,1,1,1]


    moneryweight = weights[0]
    trollfaceweight = weights[1]
    bigface1weight = weights[2]
    bigface2weight = weights[3]
    bigface3weight = weights[4]


    await interaction.response.send_message(format)
    format = build_format()
    time.sleep(3)
    slotemoji1 = random.choices(slotemojis, weights=weights, k=1)[0]


    format = build_format()
    await interaction.edit_original_response(content=format)

    if slotemoji1 == '<a:monery:1327471227278856222>':
        moneryweight = moneryweight + 5

    elif slotemoji1 == '<:trollface:1327471236619698227>':
        trollfaceweight = trollfaceweight + 5

    elif slotemoji1 == '<:bigface1:1327471248057565296>':
        bigface2weight = bigface2weight + 5

    elif slotemoji1 == '<:bigface2:1327471257142169622>':
        bigface3weight = bigface3weight + 5

    weights = [moneryweight, trollfaceweight, bigface1weight, bigface2weight, bigface3weight]

    time.sleep(1)

    slotemoji2 = random.choices(slotemojis, weights=weights, k=1)[0]

    if slotemoji2 == '<a:monery:1327471227278856222>':
        moneryweight = moneryweight + 5

    elif slotemoji2 == '<:trollface:1327471236619698227>':
        trollfaceweight = trollfaceweight + 5

    elif slotemoji2 == '<:bigface1:1327471248057565296>':
        bigface2weight = bigface2weight + 5

    elif slotemoji2 == '<:bigface2:1327471257142169622>':
        bigface3weight = bigface3weight + 5

    weights = [moneryweight, trollfaceweight, bigface1weight, bigface2weight, bigface3weight]

    format = build_format()
    await interaction.edit_original_response(content=format)
    time.sleep(1)
    slotemoji3 = random.choices(slotemojis, weights=weights, k=1)[0]
    if slotemoji3 == '<a:monery:1327471227278856222>':
        moneryweight = moneryweight + 5

    elif slotemoji3 == '<:trollface:1327471236619698227>':
        trollfaceweight = trollfaceweight + 5

    elif slotemoji3 == '<:bigface1:1327471248057565296>':
        bigface2weight = bigface2weight + 5

    elif slotemoji3== '<:bigface2:1327471257142169622>':
        bigface3weight = bigface3weight + 5

    weights = [moneryweight, trollfaceweight, bigface1weight, bigface2weight, bigface3weight]

    format = build_format()
    await interaction.edit_original_response(content=format)

    if slotemoji1 == slotemoji2 == slotemoji3:
        user_balance += money
        supabase.table('users').update({'user_id': interaction.user.id, 'balance': user_balance}).eq('user_id', interaction.user.id).execute()
        await interaction.edit_original_response(content= format + f"you won {money} dollars")

    else:
        user_balance -= money
        supabase.table('users').update({'balance': user_balance}).eq('user_id', interaction.user.id).execute()
        split = money / 2
        silver_balance += split
        weired_balance += split
        supabase.table('users').update({'user_id': 970493985053356052, 'balance': silver_balance}).eq('user_id', 970493985053356052).execute()
        supabase.table('users').update({'user_id': 1211101305607553116, 'balance': weired_balance}).eq('user_id', 1211101305607553116).execute()
        await interaction.edit_original_response(content=format + f"you lost {money} dollars, we are not going to say who has your money now")

@bot.tree.command(name="mammaljokes", description="mammal jokes")
async def mamaljokes(interaction: discord.Interaction):
    mammal_jokes = [
        "Why don't elephants use computers? Because they're afraid of the mouse!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the cow go to space? To see the moooon!",
        "What do you get when you cross a dog and a computer? A lot of bites!",
        "Why did the rabbit bring a pencil to the party? Because he wanted to draw attention!",
        "Why can't you trust a lion at the zoo? Because they are always lion around!",
        "What do you call a sleeping bull? A bulldozer!",
        "Why do squirrels like to swim? Because they’re great at nut-diving!",
        "How do you catch a unique rabbit? Unique up on it!",
        "What’s a kangaroo’s favorite type of music? Hip-hop!",
        "Why did the zebra start a band? Because he was a natural on the stripes!",
        "What do you get when you cross a snowman and a dog? Frostbite!",
        "Why do dolphins always carry a towel? Because they love to have a whale of a time!",
        "What did the fox say to the owl? You’re looking hoot-iful today!",
        "Why are pigs so bad at sharing? Because they’re always hogging things!",
        "What do you call a fish who practices magic? A sturgeon!",
        "Why did the bat join the baseball team? Because it was a great hitter!",
        "What do you call an alligator in a vest? An investigator!",
        "Why don’t monkeys use cell phones? They prefer using bananas for calls!",
        "What’s a cat’s favorite color? Purr-ple!",
        "Why don’t cows tell secrets? Because the beans always get spilled!",
        "How does a lion like its coffee? With a little roar-milk!",
        "What’s an elephant’s favorite game? Squash!",
        "Why did the dog sit in the shade? Because it didn’t want to be a hot dog!",
        "What do you call a dog magician? A labracadabrador!",
        "Why did the horse go behind the tree? To change his jockeys!",
        "What do you get if you cross a cow and a duck? Milk and quackers!",
        "What do you call a bear that’s stuck in the rain? A drizzly bear!",
        "Why was the giraffe so good at basketball? Because he was always above the rim!",
        "Why don’t horses ever play poker? Because they don’t want to get stables!",
        "What did the lion say when he saw a group of mice? ‘Dinner time!’",
        "What do you get when you cross a dog with a calculator? A friend you can count on!",
        "What did the elephant say to the tiger? You’re purr-fect!",
        "Why did the squirrel break up with the chipmunk? They had too many issues with their relationship!",
        "What did the walrus say to the seal? ‘You’re just a seal of approval!’",
        "Why was the bat upset? It wasn’t feeling quite up to scratch!",
        "What do you call a group of singing cats? A meow-sic band!",
        "Why are kangaroos such bad musicians? Because they always jump to the wrong notes!",
        "What do you call a dog that loves indulging in pastries? A pup-cake!",
        "Why did the cow want to become an astronaut? To get a higher moo-n!",
        "Why are zebras so bad at playing cards? Because they always show their stripes!",
        "What do you call a mammal who likes to tell jokes? A comed-otter!",
        "What’s the most musical animal? The hum-bat!",
        "What did the otter say when he won a race? ‘I’m otterly awesome!’",
        "What did the cheetah say to the slow turtle? ‘Catch me if you can!’",
        "What do you call an elephant that knows how to play the trumpet? A trunk-eteer!",
        "Why did the bear wear a fur coat in the summer? He was too cool to not wear it!",
        "Why don’t rhinos ever use their smartphones? Because they’re too big for their hands!",
        "What did the giraffe say to the turtle at the bar? 'You’re way too slow to catch up with me!'",
        "What do you get when you cross an elephant with a rhinoceros? Elephino!",
        "What do you call a wolf who loves ice cream? A howlin' sundae!",
        "Why don’t zebras play hide and seek? Because they’re always spotted!",
        "What’s a cat’s favorite game? Catch the mouse!",
        "What do you call a sloth with a loud voice? A yawn-imal!",
        "Why did the wolf join a band? Because he was great at howling!",
        "How does a porcupine make friends? With sharp wit!",
        "What do you call a boar that’s always going to school? A learning hog!",
        "What do you call a dog that can do magic? A labracadabrador!",
        "What do you call a mammal who’s always gossiping? A bear-it-tale!",
        "Why are giraffes bad at basketball? Because they always miss the basket!",
        "What do you get when you cross a shark with a zebra? A striped bite!",
        "Why did the penguin break up with the seagull? Because it couldn’t handle the distance!",
        "Why don’t raccoons make good basketball players? They can’t keep their eyes on the ball!",
        "What do you call a lion who lost his roar? A kitten!",
        "What do you call a camel with three humps? Pregnant!",
        "What did the lion say after a meal? ‘I’m stuffed!’",
        "Why do bears make great comedians? Because they know how to bear a joke!",
        "What’s a whale’s favorite game? Whale-thy words!",
        "What do you get if you cross a giraffe and a skunk? A very tall smell!",
        "Why was the dog sitting next to the computer? Because it wanted to keep an eye on the mouse!",
        "Why did the kangaroo break up with his girlfriend? He was jumping to conclusions!",
        "What did the penguin say to the polar bear? ‘You’re ice-cold awesome!’",
        "What did the seal say after finishing his meal? ‘That was seal-icious!’",
        "What do you call a cat who loves to play cards? A poker face!",
        "What’s a monkey’s favorite exercise? Chimp-ing in the gym!",
        "Why did the rabbit wear a fur coat? It was feeling hoppy!",
        "What did the giraffe say when it went to the party? ‘I’m feeling tall today!’",
        "Why don’t bears ever get married? They don’t want to bear the commitment!",
        "What did the dog say to the cat? ‘Stop cat-astrophizing!’",
        "What do you call an animal that loves to drive? A road hog!",
        "What did the cow say to the horse? ‘You’re horsing around too much!’",
        "What do you call a nervous bison? A buffa-lone!",
        "Why do giraffes have long necks? Because their heads are so far from their bodies!",
        "What do you get if you cross a lion and a donkey? A very confusing roar!",
        "Why don’t squirrels make good bankers? They’re always going nuts with their money!",
        "Why did the dog join the circus? Because he was a great performer!",
        "What did the mouse say to the cat? ‘You’re paws-itively scary!’",
        "What do you call a bear who loves to play sports? A grizzly athlete!",
        "What did the zebra say to the lion? ‘Better luck next time, buddy!’",
        "Why did the squirrel always bring a pencil to the party? So he could draw some attention!",
        "Why are giraffes such terrible comedians? Because their jokes are way too high-brow!",
        "What did the bat say to the owl? ‘You’re looking fly tonight!’",
        "Why did the rabbit get a job? He needed to make some hare-raising cash!",
        "What do you call an angry rhino? A horn-tastic beast!",
        "What did the lion do at the computer store? He went to buy a roary!",
        "What do you call a bear in the rain? A drizzly bear!",
        "Why don’t pandas ever play cards? They’re always too busy munching bamboo!",
        "Why did the dog go to therapy? To work on his bark issues!",
        "What do you call a pig who likes doing yoga? A ham-maste!",
        "Why did the bat go to the party? To have a fang-tastic time!",
        "Why was the koala so relaxed? He was on a leaf break!",
        "What do you call a hippo who loves cooking? A hip-hop chef!"
    ]

    embed = discord.Embed(
        title="Your mammal joke 😆",
        description=f"{random.choice(mammal_jokes)}",
        colour=discord.Colour.green()
    )


    await interaction.response.send_message(embeds=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    userid = message.author.id
    response = supabase.table('users').select('*').eq('id', userid).execute()
    userquery = response.data[0] if response.data else None

    if userquery and userquery['lvlxp'] >= 350:
        userquery['lvl'] += 1
        userquery['lvlxp'] = 0
        userquery['balance'] += 10000
        supabase.table('users').update(userquery).eq('id', userid).execute()

        await message.channel.send(f"Congrats {message.author}! You've leveled up to level {userquery['lvl']}! You also got 10,000 dollars or maybe the code bugged 🤷")

    if userquery:
        userquery['lvlxp'] += 1
        supabase.table('users').update(userquery).eq('id', userid).execute()

@bot.tree.command(name="lvl", description="Check your level")
async def lvl(interaction: discord.Interaction):
    userid = interaction.user.id
    response = supabase.table('users').select('*').eq('user_id', userid).execute()
    userquery = response.data[0] if response.data else None

    if userquery:
        await interaction.response.send_message(f"Your level is {userquery['lvl']} and you have {userquery['lvlxp']} xp")

@bot.tree.command(name="leaderboard", description="Check the leaderboard")
async def leaderboard(interaction: discord.Interaction):
    response = supabase.table('users').select('*').execute()
    allusers = response.data if response.data else []

    # Filter out users with None values for 'lvl'
    allusers = [user for user in allusers if user['lvl'] is not None and user['lvl'] >= 1]

    # Sort the filtered users by 'lvl' in descending order
    allusers = sorted(allusers, key=lambda x: x['lvl'], reverse=True)

    leaderboard = []
    for user in allusers:
        leaderboard.append(f"{user['username']} - Level {user['lvl']}")

    await interaction.response.send_message("The level leaderboard\n" + "\n".join(leaderboard))

@bot.tree.command(name="givecash", description="give cash to someone")
@app_commands.describe(money="how much money are you gonna give?")
@app_commands.describe(user="The user you are gonna give money to")
async def givecash(interaction: discord.Interaction, money: int = None, user: discord.User = None):
    user_id = interaction.user.id
    target_id = user.id

    # Fetch user and target data from Supabase
    user_response = supabase.table('users').select('balance').eq('id', user_id).execute()
    target_response = supabase.table('users').select('balance').eq('id', target_id).execute()

    if not user_response.data or not target_response.data:
        await interaction.response.send_message("User or target not found in the database.")
        return

    user_balance = user_response.data[0]['balance']
    target_balance = target_response.data[0]['balance']

    if user_balance < money:
        await interaction.response.send_message("You don't have enough cash bucko")
        return

    # Update balances
    new_user_balance = user_balance - money
    new_target_balance = target_balance + money

    supabase.table('users').update({'balance': new_user_balance}).eq('id', user_id).execute()
    supabase.table('users').update({'balance': new_target_balance}).eq('id', target_id).execute()

    await interaction.response.send_message(f"You gave {money} to {user.name}")

@bot.tree.command(name="meme", description="Fetches a meme from the dailyshitpost.net")
async def meme(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.thedailyshitpost.net/random") as response:
            data = await response.json()

    await interaction.response.send_message(data['url'])

@bot.tree.command(name="givepremium", description="Gives a user premium (Silver only) ")
@app_commands.describe(user="The user you are gonna give premium to")
async def gpremium(interaction: discord.Interaction, user: discord.User = None):

    if not interaction.user.id == 970493985053356052:
        await interaction.response.send_message("you are not silverstero", ephemeral=True)
        return
    else:
        response = supabase.table('users').select('*').eq('user', user.id).execute()
        userquery = response.data[0] if response.data else None
        if userquery:
            userquery['donated'] = True
            supabase.table('users').update(userquery).eq('id', user.id).execute()
            await interaction.response.send_message(f"You have given premium to {user.name} ")
        else:
            await interaction.response.send_message(f"User {user.name} not found in the database.")

@bot.tree.command(name="removepremium", description="Removes a users premium (Silver only) ")
@app_commands.describe(user="The user you are gonna remove premium from")
async def rpremium(interaction: discord.Interaction, user: discord.User = None):

    if not interaction.user.id == 970493985053356052:
        await interaction.response.send_message("you are not silverstero", ephemeral=True)
        return
    else:
        response = supabase.table('users').select('*').eq('user', user.id).execute()
        userquery = response.data[0] if response.data else None
        if userquery:
            userquery['donated'] = False
            supabase.table('users').update(userquery).eq('id', user.id).execute()
            await interaction.response.send_message(f"You have removed premium from {user.name} ")
        else:
            await interaction.response.send_message(f"User {user.name} not found in the database.")

@bot.tree.command(name="fileupload", description="Upload a file")
@app_commands.describe(file="The file you are going to upload")
async def fileupload(interaction: discord.Interaction, file: discord.Attachment = None):
    await interaction.response.send_message("Uploading file...")

    # Define the bucket name prefix and the file limit per bucket
    bucket_prefix = "bucket_"
    file_limit = 198  # Define your file limit per bucket

    # Function to get the number of files in a bucket
    def get_file_count(bucket_name):
        response = supabase.storage.from_(bucket_name).list()
        if isinstance(response, list) and response and 'error' in response[0]:
            return -1
        return len(response)

    # Find the current bucket
    bucket_index = 1
    while True:
        current_bucket = f"{bucket_prefix}{bucket_index}"
        file_count = get_file_count(current_bucket)
        if file_count == -1:
            # Bucket does not exist, create it
            supabase.storage.create_bucket(current_bucket, public=True)
            break
        elif file_count < file_limit:
            # Found a bucket with space
            break
        else:
            # Move to the next bucket
            bucket_index += 1

    # Upload the file to the current bucket
    file_content = await file.read()
    file_name = file.filename
    response = supabase.storage.from_(current_bucket).upload(file_name, file_content)

    url = f"https://tajkzdkaeapyuvdjgtsm.supabase.co/storage/v1/object/public/{current_bucket}//{file_name}"

    await interaction.followup.send(f"File uploaded successfully {url}. Please keep the url safe you will not be able to find it again ")




DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(DISCORD_TOKEN)