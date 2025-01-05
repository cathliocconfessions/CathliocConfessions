import json
import random
import re
from logging import exception, raiseExceptions

import dataset
import discord
import pafy
import requests
from discord import app_commands
from discord.ext import commands
import time

from discord.ext.commands import CommandOnCooldown
from sqlalchemy import except_

COOKIES_FILE = "cookies.txt"

queue = []
pafy.set_api_key("AIzaSyBoAgLxws6dGmxUjttZyWZ_RK75kA5LU4U")
onmessagedeletelist = ["bro forgot about digital footprint", "watch what you say next time!", "Your message cant be hidden from me", "yall screenshot this rq and post it to twitter.com", "nice try buddy boy", "you are gonna be haunted by this in the future", ]
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
db = dataset.connect('sqlite:///users.db')
table = db['users']

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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    try:
        synced = await bot.tree.sync()
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

@bot.tree.command(name="register", description="Register a user, Silver only")
@app_commands.commands.describe(user="The user to Register")
async def register(interaction: discord.Interaction, user: discord.User = None):
    if interaction.user.id == 970493985053356052:
        guild = interaction.guild
        username = user.name
        user_id = user.id
        displayname = user.display_name

        # Fetch member object and check for booster status
        member = guild.get_member(user.id)
        if member in guild.premium_subscribers:
            donated = True
        else:
            donated = False

        # Upsert or Update logic
        table.upsert(
            {'user_id': user_id, 'username': username, 'donated': donated, 'displayname': displayname, 'cusses': 0 },
            ['user_id']  # Use 'user_id' as the unique key
        )

        await interaction.response.send_message(f"User {username}'s database record has been or added!")

@bot.tree.command(name="lookup", description="Lookup a user. (silver only)")
@app_commands.commands.describe(user="The user to lookup")
async def lookup(interaction: discord.Interaction, user: discord.User = None):
    if interaction.user.id == 970493985053356052:
        user_id = interaction.user.id
        userdata = table.find_one(user_id=user.id)
        if not userdata:
            await interaction.response.send_message(f" {user.name} not found in the database!")
            return
        else:
            await interaction.response.send_message(f"User data: {userdata}")


@bot.tree.command(name="fix", description="Fixes someone's query in the database. This might lag, so silver only 😘")
@app_commands.describe(user="The user to fix")
async def fixdb(interaction: discord.Interaction, user: discord.User = None):
    if interaction.user.id == 970493985053356052:
        guild = interaction.guild
        username = user.name
        user_id = user.id
        displayname = user.display_name

        # Fetch member object and check for booster status
        member = guild.get_member(user.id)
        if member.bot:
            return

        if member in guild.premium_subscribers:
            donated = True
        else:
            donated = False

        # Upsert or Update logic
        table.upsert(
            {'user_id': user_id, 'username': username, 'donated': donated, 'displayname': displayname},
            ['user_id']  # Use 'user_id' as the unique key
        )

        await interaction.response.send_message(f"User {username}'s database record has been fixed (or added)!")
    else:
        await interaction.response.send_message(f"You are not allowed to use this command!")

@bot.tree.command(name="add_all_to_db", description="Adds all members of the guild to the database.")
async def add_all_to_db(interaction: discord.Interaction):
    if not interaction.user.id == 970493985053356052:
        await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
        return

    else:
        guild = interaction.guild

        for member in guild.members:
                username = member.name
                user_id = member.id
                balance = 0
                displayname = member.display_name
                if member in guild.premium_subscribers:
                    donated = True
                else:
                    donated = False

                table.upsert(
                    {'user_id': user_id, 'username': username, 'donated': donated, 'displayname': displayname, 'balance': balance },
                    ['user_id']  # Use 'user_id' as the unique key
                )

    await interaction.response.send_message("all of the users have been added to the db")

@bot.event
async def on_member_join(member):
    username = member.name
    user_id = member.id
    displayname = member.display_name
    donated = False
    table.upsert(
        {'user_id': user_id, 'username': username, 'donated': donated, 'displayname': displayname, 'balance': 0},
        ['user_id']  # Use 'user_id' as the unique key
    )

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

    await interaction.response.send_message(random.choice(fish_puns))

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

@bot.tree.command(name="message", description="makes the bot send a message ")
@commands.has_permissions(administrator=True)
@app_commands.describe(message="The message to send")
async def message(interaction: discord.Interaction, message: str = None):
    await interaction.response.send_message(message)

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
                table.upsert(
                    {'user_id': user_id, 'username': username, 'donated': donated, 'displayname': displayname},
                    ['user_id']  # Use 'user_id' as the unique key
                )
                await send_dm(user_id, "Thanks for Donating (: You now have access to all of the features in the cathlioc confessions bot! 💖")
                break

@bot.event
async def on_message_delete(message):
    channel = message.channel



    if channel and not message.author.bot:
        await channel.send(f"{random.choice(onmessagedeletelist)} \n Author: {message.author} \n Content: {message.content} \n {message.attachments}")

@bot.event
async def on_message_edit(before, after):

    if before.content == after.content:
        return

    channel = before.channel

    if before.content and not before.author.bot:
        await channel.send(f"{random.choice(onmessagedeletelist)} \n Author: {before.author} \n Before: {before.content} \n After: {after.content}")

@bot.tree.command(name="work", description="Work for some cash")
@app_commands.checks.cooldown(1, 120.5)
async def work(interaction: discord.Interaction):
    user = table.find_one(user_id=interaction.user.id)

    givingcash = random.randint(45, 136)
    user['balance'] += givingcash
    jobs = [f"You worked as a cashier employee and got {givingcash}", f"you ate some dudes ass and got {givingcash}", f"You scammed samartians by faking that you are poor, {givingcash}", f"You coded a discord bot for a server and they gave you {givingcash}", f"You drew a picture for someone and they gave you {givingcash}", f"You sold newspapers for {givingcash}", f"You became a Rent-a-bitch and got {givingcash} out of it"]

    if user:
        table.update(user, ['user_id'])

    await interaction.response.send_message(f"{random.choice(jobs)}")

@work.error
async def work_error(interaction: discord.Interaction, error):
    # Check if the error is caused by the cooldown
    if isinstance(error, app_commands.CommandOnCooldown):
        # Calculate retry time (human-readable)
        retry_after = round(error.retry_after, 2)  # Retry time in seconds (rounded to 2 decimal places)
        await interaction.response.send_message(
            f"You're on cooldown! Try again in **{retry_after} seconds**.",
            ephemeral=False   # Makes the message visible only to the user
        )
    else:
        raise error  # Re-raise unexpected errors for logging


@bot.tree.command(name="balance", description="Checks how much cash you have")
async def balance(interaction: discord.Interaction):
    # Get the user's Discord ID
    user = interaction.user.id

    # Fetch data from the database for this user
    user_data = table.find_one(user_id=user)

    # Check if the user exists in the database
    if user_data is None:
        await interaction.response.send_message("You don't have an account yet!")
        return

    # Extract the balance from the returned database record
    user_balance = str(user_data['balance'])  # Convert for indexing if necessary

    # Respond with the balance or the first digit, depending on your logic
    await interaction.response.send_message(f"You have {user_balance} dollars.")  # Full balance
    # OR if you only care about the first digit:
    # await interaction.response.send_message(f"You have {user_balance[0]} Dollars.")






bot.run('MTE0MzUxODAzMDMwMzg3MTA2Nw.GmWt4l.oMVrTCmJ0ksTR1KlG6GmMdALpWVdage9_hI8G4')