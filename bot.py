import discord
import time
import asyncio

messages = joined = 0


def read_token(): # hides token
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


@client.event
async def on_member_updates(before, after): # nickname interactions (tutorial 4)
    n = after.nick
    if n:
        if n.lower().count("ming") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="CANT DO THAT")


@client.event
async def on_member_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "general":
            await client.send_message(f"""Welcome to the server {member.mention}""")

@client.event
async def on_message(message):
    global messages
    messages += 1

    id = client.get_guild(667916321769521188)
    channels = ["commands"]
    valid_users = ["Ming#7825"] # add
    bad_words = ["fuck", "shit", "cunt", "bitch", "faggot", "fucker", "motherfucker", "mother fucker", "fucking", "ass",
                 "asshole", "dick", "cock", "dicksucker"]

    for word in bad_words:
        if message.content.count(word) > 0:
            print("A bad word was said")
            await message.channel.purge(limit=1)

    if message.content == "/help": # help center for bot
        embed = discord.Embed(title="Help for Super Helper :p", description="Some useful commands")
        embed.add_field(name="/hello", value="Greets the user")
        embed.add_field(name="/user", value="Print the number of users")
        await message.channel.send(content=None, embed=embed)

    if str(message.channel) in channels and str(message.author) in valid_users:
        if message.content.find("/hello") != -1:
            await message.channel.send("Hiya!") # if users prompts /hello, bot will say "Hiya"
        elif message.content == "/users":
            await message.channel.send(f"""Number of Members: {id.member_count}""") # tells number of users
    else:
        print(f"""User: {message.author} tried to do command {message.content}, in channel # {message.channel}""")


client.loop.create_task(update_stats()) # allows function to run in the background
client.run(token)


