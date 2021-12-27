#Modules
import datetime
import os
from typing import final
from discord import user
from discord import colour
from discord.colour import Color
from discord.embeds import Embed
import dotenv
from dotenv import load_dotenv
import discord
import json
from discord.ext import commands
import random
import asyncio
import logging
import time

# Client Delcaration and Events and Stuff ---------------------------------------------------------------------------------------------------------------------------------------------
os.chdir("D:\\CodingGames\Coding Files\\Python\\Bot maybe")
prefix = "k."
Intents = discord.Intents().all()
client = commands.Bot(command_prefix = prefix, help_command= None, intent = Intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'Server name: {guild.name}\nServer id: {guild.id}\nMember count: {guild.member_count}')
        print('----------------')
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Conquering the Hell of {str(len(client.guilds))} servers! │ k.help"))

@client.event
async def on_member_join(member):
  with open('users.json', 'r') as f:                
    users = json.load(f)

  await update_data(users, member)

  with open('users.json', 'w') as f:
    json.dump(users, f, indent=4)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the permission to do that. :eyes:")

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Conquering the Hell of {str(len(client.guilds))} servers! │ k.help"))

@client.event
async def on_guild_remove(guild):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Conquering the Hell of {str(len(client.guilds))} servers! │ k.help"))
#-#===== Welcomer ====================================================================================================================

# @client.event
# async def on_member_join(member, ):

#     channel = await client.get_channel(welchannel)

#     embed = discord.Embed(title = f"🎊Welcome {member} To The Server!", description= f"A new Wild {member} just joined the server.🎊\n🎉We hope u will have a great time here.🎉")
#     embed.set_footer("Made By Someone who cares for you.")
#     embed.timestamp()
#     embed.thumbnail(url = member.avatar_url)

#     await channel.send(embed=embed)

#-#===================================================================================================================================
@client.event
async def on_message(message):
  if message.author.bot == False:
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 3)
    await level_up(users, message.author, message )

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    await client.process_commands(message)

# Command -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
            "no?????",
            "When will manage you grow a braincell, yes",
            "You stoopid!, of course not",
            "lol no",
            "nope!",
            "Absolutely!",
            "As I see it, yes.",
            "Most likely.",
            "Yes.",
            "Idfk",
            "Try again",
            "Not today.",
            "I\'m not very sure, but I think the answer is no.",
            "I\'m not very sure, but I think the answer is yes!",
            "brain.exe stopped responding.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is nopee.",
            "My sources say n o.",
            "Outlook not so good.",
            "Its a secret >:]",
            "Yare Yare Daze",
            "Drink your Milk and Ask Again"
    ]
    ballEmbed = discord.Embed(title=f':8ball: {question}', description=f'{random.choice(responses)}')
    await ctx.send(embed=ballEmbed)

@client.command()
async def ping(ctx):
        ping = random.randrange(40324, 3291423040)
        await ctx.send(f'Bot Ping/Latency is {ping}ms')
        time.sleep(3)
        await ctx.send(f'Just kidding Latency is {round(client.latency * 1000)}ms')

@client.command()
async def avatar(ctx, member: discord.Member= None):
    if member == None:
        member = ctx.author

    icon_url = member.avatar_url

    avatarEmbed = discord.Embed(title= f"{member}'s Avatar", color= discord.Color.blurple())
    avatarEmbed.set_image(url = f"{icon_url}")

    await ctx.send(embed = avatarEmbed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked successfully.')

@client.command(pass_context=True, aliases=['purge'])
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send('Cleared by {}'.format(ctx.author.mention))
    await ctx.message.delete()
@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can not do that!")


@client.command(aliases =["bal"])
async def balance(ctx):
    await open_account(ctx.author) 

    users = await get_bank_data()
    
    user = ctx.author

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"] 

    em = discord.Embed(title = f"{ctx.author.name}'s Balance", Color = discord.Color.gold)
    em.add_field( name = "wallet", value = wallet_amt)
    em.add_field( name = "Bank Balance", value = bank_amt)

    await ctx.send(embed = em)

@client.command()
async def say(ctx, *, message = ''):
    if message == '':
        await ctx.send("Say Something!")
    else:
        await ctx.message.delete()
        await ctx.send(f'{message}')
    
@client.command()
async def beg(ctx):
    await open_account(ctx.author) 

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(140)
    personlist= ["Kaneo", "Noihachi", "Kurutse", "Kamari", "Mameko"]
    person = random.choice(personlist)

    em2 = discord.Embed(title = f"{user} Wanting Coins", Color = discord.Color.blurple)
    em2.add_field(name = f"{person} Being Kind", value = f"Hey! {person} Gave you {earnings} coins.")

    await ctx.send(embed = em2)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@client.command(aliases =["with"])
async def withdraw(ctx, amount = None,):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the Amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("U dont have That Much Money")
        return

    if amount<0:
        await ctx.send("Amount must be Positive")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "bank")

    await ctx.send(f"U withdrew {amount} coins!")

@client.command(aliases =["dep"])
async def deposit(ctx, amount = None,):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the Amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("U dont have That Much Money")
        return

    if amount<0:
        await ctx.send("Amount must be Positive")
        return

    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, "bank")

    await ctx.send(f"U deposited {amount} coins!")

@client.command()
async def send(ctx,member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter the Amount")
        return

    bal = await update_bank(ctx.author)
    if amount == "all":
            amount = bal[0]

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("U dont have That Much Money")
        return

    if amount<0:
        await ctx.send("Amount must be Positive")
        return

    await update_bank(ctx.author, -1 * amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"Transaction Complete! \nU Sent {amount} coins to {member}!")

@client.command()
async def slots(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the Amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("U dont have That Much Money")
        return

    if amount<0:
        await ctx.send("Amount must be Positive")
        return

    final = []
    for i in range(3):
        a = random.choice(["X", "T", "O"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_bank(ctx.author, 2 * amount)  
        await ctx.send("You Won!")   
    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send("You Lost!")        

@client.command()
async def help(ctx):

    emhelp = discord.Embed(title = "Kamaje || Commands ◈ Support ",
    description="This message Contains all the Command present in the bot.",
    color=discord.Color.blurple() )
    emhelp.add_field(name= f"{prefix}help", value="Shows this message", inline= False)
    emhelp.add_field(name= "Economy", value= f"{prefix}eco", inline= True)
    emhelp.add_field(name= "Fun Commands", value= f"{prefix}fun", inline= True)
    emhelp.add_field(name= "Leveling", value= f"{prefix}lvl", inline= True)
    emhelp.add_field(name= "Moderation", value= f"{prefix}mod", inline= True)
    await ctx.send(embed = emhelp)

@client.command(aliases=["mod"])
async def moderation(ctx):
    emmod = discord.Embed(title = "Kamaje || Commands ◈ Support", description = "Moderation Commands", color=discord.Color.blurple())
    emmod.add_field( name = f"{prefix}kick <user>", value = "Kick the ||ass|| of the user out of the server.", inline= False)

    await ctx.send(embed = emmod)

@client.command(aliases=["lvl"])
async def leveling(ctx):
    emlvl = discord.Embed(title = "Kamaje || Commands ◈ Support", description = "Leveling Commands", color=discord.Color.blurple())
    emlvl.add_field( name = f"{prefix}level", value = "Shows your current Level and Exp", inline= False)
    emlvl.add_field( name = f"{prefix}rank <user>", value = "Shows the mentioned user's current Level and Exp", inline= False)

    await ctx.send(embed = emlvl)

@client.command(aliases=["eco"])
async def economy(ctx):
    emeco = discord.Embed(title = "Kamaje || Commands ◈ Support", value = "Economy Commands", color=discord.Color.blurple())
    emeco.add_field( name = "k.bal", value = "shows your current wallet balance and bank balance.", inline= False)
    emeco.add_field( name = "k.rob <member>", value = "Robs Some coins from their wallet and add to your. If you are Lucky u will rob their whole wallet!", inline= False)
    emeco.add_field( name = "k.with <amount>", value = "Withdraws the amount of coins from your bank", inline= False)
    emeco.add_field( name = "k.dep <amount>", value = "Deposits the amount of coins to your bank", inline= False)
    emeco.add_field( name = "k.slots <amount>", value = "a minigame within the bot which can either add the double the coins amount to your bank or rmeove the amount of coins from your bank. Depends on your Luck!", inline= False)
    emeco.add_field( name = "k.beg", value = "Gives your Some Coins", inline= False)

    await ctx.send(embed = emeco)

@client.command(aliases=["sed"])
async def sad(ctx):
    emmod = discord.Embed(title = f"{ctx.author.name} Is sed😢!", description = "Dude Dont be Sed. If No one cares for You then I am here. \nAlso U dOnT kNoW wHaT kArLsOn Is?", color=discord.Color.blurple())
    emmod.add_field( name = "Useful Tip 1", value = "Drink **m i l k**🥛")
    emmod.add_field( name = "Useful Tip 2", value = "Add me to your Server [Click here To Invite!(●ˇ∀ˇ●)](https://rb.gy/1hlww4)")
    await ctx.send(embed = emmod)

@client.command(aliases = ['rank'])
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        exp = users[str(id)]['experience']
        await ctx.send(f'You are at **Level {lvl} and Exp : {exp}**')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        exp = users[str(id)]['experience']
        await ctx.send(f'{member.mention} is on **Level {lvl} and Exp : {exp}!**')

@client.command(aliases = ['steal'])
async def rob(ctx,member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(member)

    if bal[0] < 1000:
        await ctx.send("They dont have That Much Money! \nAnd Not worth it too!")
        return

    if member == ctx.author:
        await ctx.send("If cant rob yourself dumbass!!")
        return

    earned = random.randrange(0, bal[0])

    await update_bank(ctx.author, earned)
    await update_bank(member, -1 * earned)

    await ctx.send(f"U Robbed {earned} coins from {member}")


# Helper Functions --------------------------------------------------------------------------------------------------------------------------------------------------------------------

async def open_account(user):
    
    users = await get_bank_data()

    if str(user.id) in users:
        return False    
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user,change = 0,mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']    
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has reached level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

# Getting Token -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client.run(TOKEN)
