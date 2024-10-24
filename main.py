import os
import io
import subprocess
import sys
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import requests
import json
import secrets
from tinydb import TinyDB, Query

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
banlist = TinyDB('banlist.json')
economy = TinyDB('economy.json')
User = Query()

def createuseraccount(userid, interaction):
        if not economy.search(User.userid == User.id):
            interaction.response.send_message("You do not have an account! creating one right now...", ephemeral=True)
            createuseraccount(User.id)
            interaction.followup.send("Account has been created. Granting you 1000 NRK dollars", ephemeral=True)
            economy.update({'balance': 1000}, User.userid == User.id)
            interaction.followup.send(f"Account created and you now have 1000 NRK dollars", ephemeral=True)

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
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(colour=0x313338, color=0x313338, title="The bot is working normally.", type='rich', url=None, description=f'The bot is working. Please check the discord server for announcements or downtime!', timestamp=None)
        embed.add_field(name="Current ping ✅", value=f'{ping}ms', inline=True)
        await interaction.response.send_message(embed=embed)



class ConfessionView(View):

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve_button(self, interaction: discord.Interaction, button: Button):
        moderator = interaction.user
        user = await bot.fetch_user(userid5)
        if user:
            await user.send("Your confession has been Approved! Check it out")
        
        channel_id = 1293598104175640617
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("Confession has been Approved")
            await channel.send(f"{interaction.user.name} Approved the confession")

        confesschannel = 1293597525785313320
        confesschannel = bot.get_channel(confesschannel)
        if confesschannel:  
            embed = discord.Embed(colour=0x313338, color=0x313338, title="New Confession!", type='rich', url=None, description=f'{confession}', timestamp=None)
            await confesschannel.send(embed=embed)
        
        # Disable buttons
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: Button):
        class RejectionModal(discord.ui.Modal):
            def __init__(self):
                super().__init__(title="Rejection Reason")
                self.reason = discord.ui.TextInput(label="Reason for rejection", placeholder="Enter the reason for rejection", min_length=1, max_length=1000)
                self.add_item(self.reason)

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.edit_message(view=None)
                moderator = interaction.user

                user = await bot.fetch_user(userid5)
                if user:
                    await user.send(f"Your confession has been rejected for the following reason: {self.reason.value}")
                
                channel_id = 1293598104175640617
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(f"Confession has been rejected for the following reason: {self.reason.value}")
                    await channel.send(f"{interaction.user.name} rejected the confession")

                # Disable buttons
                await interaction.message.edit(view=None)

        await interaction.response.send_modal(RejectionModal())

    @discord.ui.button(label="Reject & ban", style=discord.ButtonStyle.danger)
    async def reject_and_ban(self, interaction: discord.Interaction, button: Button):
        class RejectionAndBanModal(discord.ui.Modal):
            def __init__(self):
                super().__init__(title="Rejection Reason")
                self.reason = discord.ui.TextInput(label="Reason for rejection", placeholder="Enter the reason for rejection", min_length=1, max_length=1000)
                self.add_item(self.reason)

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.edit_message(view=None)
                moderator = interaction.user
                user = await bot.fetch_user(userid5)
                if user:
                    await user.send(f"Your confession has been rejected and you have been banned for the following reason: {self.reason.value}")
                
                channel_id = 1293598104175640617
                channel = bot.get_channel(channel_id)
                if channel:
                    banlist.insert({'userid': userid5})
                    await channel.send(f"Confession has been rejected and user has been banned for the following reason: {self.reason.value}")
                    await channel.send(f"{interaction.user.name} rejected the confession and banned the user")

                # Disable buttons
                await interaction.message.edit(view=None)

        await interaction.response.send_modal(RejectionAndBanModal())

class migratesuccess(discord.ui.View):
    @discord.ui.button(label="Approve", style=discord.ButtonStyle.danger)
    async def Approve(self, interaction: discord.Interaction, button: Button):
        class BalanceModal(discord.ui.Modal):
            def __init__(self):
                super().__init__(title="Enter the balance of the old user")
                self.balance = discord.ui.TextInput(label="Enter the balance of the old user", placeholder="Enter the balance of the old user", min_length=1, max_length=1000)
                self.add_item(self.balance)

            async def on_submit(self, interaction: discord.Interaction):
                economy.update({'balance': int(self.balance.value)}, User.userid == interaction.user.id)
                await interaction.response.edit_message(view=None)
                await interaction.followup.send(f"User has been migrated with a balance of {self.balance.value}", ephemeral=True)
                user = await bot.fetch_user(interaction.user.id)
                economy.update({'balance': int(self.balance.value)}, User.userid == interaction.user.id)
                await user.send(f"Your migration has been approved! You have been granted {self.balance.value} NRK bucks")

        await interaction.response.send_modal(BalanceModal())
    
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def Reject(self, interaction: discord.Interaction, button: Button):
        class RejectionModal(discord.ui.Modal):
            def __init__(self):
                super().__init__(title="Rejection Reason")
                self.reason = discord.ui.TextInput(label="Reason for rejection", placeholder="Enter the reason for rejection", min_length=1, max_length=1000)
                self.add_item(self.reason)

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.edit_message(view=None)
                await interaction.followup.send("Migration has been rejected", ephemeral=True)
                user = await bot.fetch_user(interaction.user.id)
                await user.send(f"Your migration has been rejected reason: {self.reason.value}")

        await interaction.response.send_modal(RejectionModal())


        

@bot.tree.command(name="confess", description="Confess something anonymously")
@app_commands.describe(message="The message you want to confess")
async def confess(interaction: discord.Interaction, message: str):
    global userid5
    userid5 = interaction.user.id

    if not banlist.search(Query().userid == interaction.user.id):
        username = interaction.user.name
        global confession
        confession = message
        channel_id = 1293598104175640617
        await interaction.response.send_message(f"Your confession has been sent for review. We will send you a DM if your confession gets approved or not. Thanks!", ephemeral=True)
        embed = discord.Embed(colour=0x313338, color=0x313338, title="New Confession!", type= 'rich', url=None, description=f'{confession}', timestamp=None)
        embed.add_field(name="User", value=f'{username}', inline=True)
        embed.add_field(name="User ID", value=f'{userid5}', inline=True)
        embed.add_field(name="Confession", value=f'{confession}', inline=False)
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed, view=ConfessionView())
    else:
        await interaction.response.send_message("You have been banned from using the confession command.", ephemeral=True)

@bot.tree.command(name="confessunban", description="Unban a user from using the confession command")
@app_commands.describe(user="The user you want to unban")
async def confessunban(interaction: discord.Interaction, user: discord.User):
    if discord.utils.get(interaction.user.roles, name="ADMIN"):
        userid = user.id
        if banlist.search(User.userid == userid):  # Corrected search query
            unbanneduser = banlist.get(User.userid == userid)
            banlist.remove(User.userid == userid)  # Corrected remove query

            await interaction.response.send_message(f"{unbanneduser} has been unbanned from using the confession command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"this user is not banned from using the confession command.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.tree.command(name="confessban", description="Ban a user from using the confession command")
@app_commands.describe(user="The user you want to ban")
async def confessban(interaction: discord.Interaction, user: discord.User):
    interaction.guild.get_member(interaction.user.id)
    if discord.utils.get(interaction.user.roles, name="ADMIN"):
        userid = user.id
        if not banlist.search(User.userid == user.id):
            banlist.insert({'userid': userid})

            await interaction.response.send_message(f"{userid} has been banned from using the confession command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"this user is already banned from using the confession command.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.tree.command(name="confessbanlist", description="List all banned users from using the confession command")
async def confessbanlist(interaction: discord.Interaction):
    interaction.guild.get_member(interaction.user.id)
    if discord.utils.get(interaction.user.roles, name="ADMIN"):
        bannedusers = banlist.all()
        if bannedusers:
            message = "List of all banned users from using the confession command:\n"
            for user in bannedusers:
                user_obj = await bot.fetch_user(user["userid"])
                message += f"- {user_obj.name}#{user_obj.discriminator} (ID: {user['userid']})\n"
            await interaction.response.send_message(message, ephemeral=True)
        else:
            await interaction.response.send_message("There are no banned users from using the confession command.", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.tree.command(name="pullupdate", description="Pulls an update from GitHub - Silver only")
async def pullupdate(interaction: discord.Interaction):
    if interaction.user.id == 970493985053356052:  # Replace with the actual ID
        await interaction.response.send_message("Pulling update from GitHub...", ephemeral=True)
        
        try:
            github_token = "your_github_token_here"  # Replace with your GitHub token
            if not github_token:
                raise ValueError("GitHub token not found in environment variables.")
            
            repo_url = f"https://{github_token}:x-oauth-basic@github.com/banana-man10/CathliocConfessions.git"
            repo_dir = "CathliocConfessions"  # Directory where the repo should be cloned
            
            # Check if the repo directory exists
            if not os.path.exists(repo_dir):
                # Clone the repository if it doesn't exist
                subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
            
            # Change to the repo directory
            os.chdir(repo_dir)
            
            # Set the remote URL
            subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)
            
            # Pull the latest changes
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            
            await interaction.followup.send("Update pulled successfully! Restarting the bot...", ephemeral=True)
            await bot.close()
            os.system('python main.py')
        except subprocess.CalledProcessError as e:
            await interaction.followup.send(f"Failed to pull update: {e}", ephemeral=True)
        except ValueError as e:
            await interaction.followup.send(str(e), ephemeral=True)
    else:
        await interaction.response.send_message("you arent silver bro", ephemeral=True)

@bot.tree.command(name="migrate", description="requests a migration from Your Currency in the old bot to this bot")
@app_commands.describe(img="A screenshot showing your old currency balance")
async def ecomigrate(interaction: discord.Interaction, img: discord.Attachment):
    await interaction.response.send_message("Dmed Silverstero with your info. He may take a bit to approve your request", ephemeral=True)
    user = await bot.fetch_user(970493985053356052)
    if user:
        await user.send(f"{interaction.user.name} has requested a migration. Please approve or reject it {img.url}", view=migratesuccess())
    economy.insert({'userid': interaction.user.id, 'balance': 0})


@bot.tree.command(name="balance", description="Check your balance")
async def ecobalance(interaction: discord.Interaction):
    balance = economy.get(User.userid == interaction.user.id)['balance']
    await interaction.response.send_message(f"Your balance is {balance}", ephemeral=True)

@bot.tree.command(name="give", description="gives a user some of your NRK bucks")
@app_commands.describe(user="the money you want user give")
@app_commands.describe(amount="the money of amount you give want")
async def ecogive(interaction: discord.Interaction, user: discord.User, amount: int):
    createuseraccount(interaction.user.id, interaction)
    createuseraccount(user, interaction)
    interactionusermoney = economy.get(User.userid == interaction.user.id)['balance']
    recievermoney = economy.get(User.userid == user.id)['balance']
    if interactionusermoney >= amount:
        economy.update({'balance': interactionusermoney - amount}, User.userid == interaction.user.id)
        economy.update({'balance': recievermoney + amount}, User.userid == user.id)
        await interaction.response.send_message(f"You gave {amount} NRK bucks to {user.name}", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have enough money to give", ephemeral=True)

@bot.tree.command(name="add", description="add NRK bucks to a user - silver only")
@app_commands.describe(user="the money you want user add")
@app_commands.describe(amount="the money of amount you add")
async def ecoadd(interaction: discord.Interaction, user: discord.User, amount: int):
    if interaction.user.id == 970493985053356052:
        createuseraccount(user, interaction)
        recievermoney = economy.get(User.userid == user.id)['balance']
        economy.update({'balance': recievermoney + amount}, User.userid == user.id)
        await interaction.response.send_message(f"You added {amount} NRK bucks to {user.name}", ephemeral=True)
    else:
        await interaction.response.send_message("You are not silver", ephemeral=True)

@bot.tree.command(name="work", description="work for money")
@commands.cooldown(1, 300, commands.BucketType.user)  
async def ecowork(interaction: discord.Interaction):
    createuseraccount(interaction.user.id, interaction)
    random_number = secrets.randbelow(301) + 200

    economy.update({'balance': economy.get(User.userid == interaction.user.id)['balance'] + random_number}, User.userid == interaction.user.id)
    await interaction.response.send_message(f"You worked and got {random_number} NRK bucks", ephemeral=True)

@ecowork.error
async def ecowork_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(f"You worked already! work after {int(error.retry_after)} seconds.", ephemeral=True)
    else:
        raise error

## @bot.tree.command(name="welfare", description="signup for welfare") work on later im going to bed




Testing = True 
if not Testing:
    bot.run('MTE0MzUxODAzMDMwMzg3MTA2Nw.Gkmvjs.ToKMnSd971stOR_d8I_OCAEYkV0dwvLmAzbZhY')
else:
    bot.run('MTE0MzUxOTM0MjQ5NjA1OTU3Mw.GLQ5Jg.MFDbGe6-m4jgyxp9f9gKJE8ei7YJZbI-sMiP6U')