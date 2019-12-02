import discord
# this is the bot
import datetime as dt
from discord.ext import commands
from collections import defaultdict
import json
client = commands.Bot(command_prefix="$")
TOKEN = "Insert Token Here"
userdictionary = defaultdict(int)
usertime = {}
uservoiceduration = defaultdict(float)

# class Member_info:
#     "A class object to hold the information of members such as voice duration, message count, etc"
#     # init statement register member with a member id


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # list out all the guilds and channels
    print("Guild Listings")
    for guild in client.guilds:
        print(str(guild).format(client))
        for category in guild.categories:
            print("|-->" + str(category))
            for channel in category.channels:
                print("    |--->" + str(channel.type) + ' ' + str(channel))
    print("Bot is ready".format(client))


@client.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

        await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        with open('users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, message.author)
        await add_count(users, message.author)
        # count each message when sent
        with open('users.json', 'w') as f:
            json.dump(users, f)
    await client.process_commands(message)

async def update_data(users, user):
    userid = str(user.id)
    if not (userid in users):
        users[userid] = {}
        users[userid]['Message Count'] = 0
        users[userid]["Voice Duration"] = 0

async def add_count(users, user):
    userid = str(user.id)
    users[userid]['Message Count'] += 1

async def add_duration(users, user, duration):
    userid = str(user.id)
    users[userid]["Voice Duration"] += int(duration)


@client.event
async def on_voice_state_update(member, before, after):
    # store the current time when a user joins voice call if the user joins
    # the call
    if(before.channel == None):
        # store the current time in the dictionary
        usertime[member.id] = dt.datetime.now()
    # check if the user leaves the call
    if(before.channel != None and after.channel == None):
        with open('users.json', 'r') as f:
            users = json.load(f)
        duration = (dt.datetime.now() - usertime[member.id]).total_seconds()
        await update_data(users, member)
        await add_duration(users, member, duration)
        # count each message when sent
        with open('users.json', 'w') as f:
            json.dump(users, f)
    # store the duration in a variable


@client.command()
async def count(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    bot_message = await ctx.channel.send(users[str(ctx.message.author.id)]['Message Count'])
    await bot_message.delete(delay=10)
    await ctx.message.delete()


@client.command()
async def exit(ctx):
    await ctx.message.delete()
    await ctx.bot.close()


@client.command()
async def duration(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    users[str(ctx.message.author.id)]
    bot_message = await ctx.channel.send(str(users[str(ctx.message.author.id)]['Voice Duration']) + "Seconds")
    await bot_message.delete(delay=10)
    await ctx.message.delete()


@client.command()
async def info(ctx):
    # create an embed for discord
    embed = discord.Embed(title='User Statistics',
                          description=str(ctx.message.author), colour=0xe67e22)
    with open('users.json', 'r') as f:
        users = json.load(f)
    userid = str(ctx.message.author.id)
    embed.add_field(name="Voice Duration:",
                    value=str(users[userid]["Voice Duration"] // 3600) + " Hours\n" + str((users[userid]["Voice Duration"] % 3600) // 60) + " Minutes\n" + str(users[userid]["Voice Duration"] % 60) + " Seconds\n")
    embed.add_field(name="Message Count:",
                    value=users[userid]["Message Count"])
    bot_message = await ctx.channel.send(embed=embed)
    await bot_message.delete(delay=10)
    await ctx.message.delete()


@client.command()
async def react(ctx, message_id, emoji):
    await ctx.message.delete()
    message = await ctx.channel.fetch_message(message_id)
    if(isinstance(emoji, str)):
        emoji = emoji[1:-1]
        for emojis in client.emojis:
            if(emojis.name == emoji):
                await message.add_reaction(emojis)
    else:
        await message.add_reaction(emojis)

client.run(TOKEN)
