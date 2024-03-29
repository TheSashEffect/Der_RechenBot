#bot.py

#import stuff
import os
import random
import praw
import datetime
import string
import re
import aiohttp
import subprocess
import asyncio

import discord
from  dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands

import seventv
from seventv.seventv import seventvException

#oeffnet yogi tea quotes datei bei start von bot
with open('yogi_tea_quotes.txt', encoding='utf-8') as f:
    yogi_tea_quotes = f.read().split("|") 



#oeffnet guildliste datei bei start von bot
with open('./guildliste.txt', encoding='utf-8') as f:
    guildliste = f.read().split('|')





#laedt .env datei wegen sicherheit und so
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



#Zugangsdaten fur Reddit damit der Bot posts holen kann        
reddit = praw.Reddit(client_id=os.getenv("client_id"),
                     client_secret=os.getenv("client_secret"),
                     password=os.getenv("password"),
                     user_agent=os.getenv("user_agent"),
                     username=os.getenv("username"))





#das intents alle intents sind, die discord zu bieten hat
intents = discord.Intents().all()





#erstens fur allgemein bot und das der grosz-kleinschreibung ignoriert, command braucht ! davor und intents=intents
bot = commands.Bot(case_insensitive=True, command_prefix='!', intents=intents, activity=discord.Streaming(name="for the people who are watching", url='https://www.twitch.tv/the_sash_effect'), help_command = None)


        


#wenn bot startet dann sagt der das er connected ist und zu welchen Servern        
@bot.event
async def on_ready():       
    print(f'{bot.user.name} has connected to Discord in following Guild(s): ')
    print(guildliste)


@bot.event
async def on_command_error(ctx, error):
    # Check if the error is a command-related error
    if isinstance(error, commands.CommandError):
        # Get the error message
        error_message = f"An error occurred: {type(error).__name__} - {str(error)}"

        # Get the error channel
        error_channel1 = bot.get_channel(1172493971298201642)
        error_channel2 = bot.get_channel(1172582080878747668)

        # Send the error message to the specified channel
        await error_channel1.send(error_message)
        await error_channel2.send(error_message)


#wenn jemand joined, dann dm mit herzlich willkommen
"""@bot.event
async def on_member_join(member):
    await member.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )"""





#wenn nachricht geschickt wird checkst nach:
@bot.event
async def on_message(message):
    
    if message.author.id != (1118464907470450709):
        channel = bot.get_channel(1130843895887048785)
        embed = discord.Embed(
        title = f"""{message.author.display_name}'s message in {message.guild} 
        Channel: {message.channel.name}; Send at: {message.created_at}""",
        description = message.content)
        
        await channel.send(embed = embed)
    
    
    
    #wenn sender dieser bot ist nicht nochmal senden
    if message.author == bot.user:
        return
        
    
    
    #wenn sender ein anderer bot ist, nicht nochmal senden
    if message.author.id in (1063806186048192532,1122866223185662124,):
        return
    
    
    
    """if message.author.id in (769525682039947314,):
        channel = bot.get_channel(1130587241417277503)
        await channel.send("<:jaessin:1130580133942661352>")
        
    if 'jässin' in message.content.lower():
        channel = bot.get_channel(1130587241417277503)
        await channel.send(message.content.lower().count('jässin') * "<:jaessin:1130580133942661352>")
        
    if 'jaessin' in message.content.lower():
        channel = bot.get_channel(1130587241417277503)
        await channel.send(message.content.lower().count('jaessin') * "<:jaessin:1130580133942661352>")
    
    if 'jassin' in message.content.lower():
        channel = bot.get_channel(1130587241417277503)
        await channel.send(message.content.lower().count('jassin') * "<:jaessin:1130580133942661352>")
    """
    
    
    
    #wenn balls in nachricht, so oft emote machen wie balls in Nachricht und grosz klein egal
    if 'balls' in message.content.lower():
        await message.channel.send(message.content.lower().count('balls') * "<:balls:1122153712840871996>")
    


    #wenn fehler, dann nicht fehler ausgeben oder so kein plan hilfe
    elif message.content == 'raise-exception':
        raise discord.DiscordException()
    
    
    
    #wenn Nachricht kein on message argument hat trotzdem weiter schauen weil evtl. command 
    await bot.process_commands(message)





#wenn !happy_birthday, dann ...
@bot.command()
async def happy_birthday(ctx):
    response = 'Happy Birthday! 🎈🎉'
    await ctx.send(response)





#wenn !hello, dann ...
@bot.command()
async def hello(ctx):
    await ctx.send('Hello {0.display_name}.'.format(ctx.author))





#wenn spruch, random spruch aus liste
@bot.command()
async def spruch(ctx):
    response = random.choice(yogi_tea_quotes)
    await ctx.send(response)
    




#wenn !f groszes F aus emotes
@bot.command()
async def f(ctx):
    response = '<:balls:1122153712840871996>'
    await ctx.send(4 * response + '\n' + response + '\n' + 2 * response + '\n' + response + '\n' + response)
    




#wenn !post post von reddit schicken
@bot.command()
async def post(ctx, message=''):
    #wenn keine kategorie, random aus memes
    if message == '':
        memes = reddit.subreddit('memes')
        submission = random.choice([meme for meme in memes.hot(limit=200)])
        await ctx.send('No Subreddit added to the message, but here is an other Meme: \n' + submission.title + '\n' + submission.url)
        
        
        
    else:
        #schaut of subreddit existiert
        try:
            #wenn ja dann random aus dem Subreddit
            memes =  reddit.subreddit(message)      
            if memes:
                submission = random.choice([meme for meme in memes.hot(limit=50)])
                await ctx.send(submission.title + '\n' + submission.url)
                
                
                
        #wenn nicht, random aus memes
        except:
            memes = reddit.subreddit('memes')
            submission = random.choice([meme for meme in memes.hot(limit=200)])
            await ctx.send('Subreddit: ' + message + ' not found, but here is an other Meme: \n' + submission.title + '\n' +  submission.url)
            
            
            
    #warten, das reddit sich schlieszt (kein Plan wieso)        
    await reddit.close()





#wenn !info dann infos zu User ausgeben
@bot.command(name='info')
async def info(ctx,user:discord.Member=None):
    #wenn kein user erwaehnt, dann man sender
    if user==None:
        user=ctx.author
    
        
        
    #liste fuer rolen eines Users auszer @everyone    
    rlist = []
    for role in user.roles:
        if role.name != '@everyone':
            rlist.append(role.mention)
    b = ','.join(rlist)
    
    
    
    #erstellen eines Textfeld zum ordentlichen sortieren der infos mit farbe user und wann erstellt
    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)
    
    
    
    #einfuegen Infos von wenn, Avatar und von wem    
    embed.set_author(name=f'User Info for: {user}' ),
    embed.set_thumbnail(url=user.avatar),
    embed.set_footer(text=f'Requested by: {user}',icon_url=ctx.author.avatar)
    
    
    
    #einfuegen von name und Id des requesteten, inline = Zeilensprung damit besser sichtbar   
    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value = user.display_name,inline=False)



    #einfuegen, wann account erstellt und seit wann aufm server
    embed.add_field(name='Created at:',value = user.created_at,inline=False)
    embed.add_field(name='Joined at:',value = user.joined_at,inline=False)
    
    
    
    #einfuegen, ob user ein bot ist
    embed.add_field(name='Bot?',value=user.bot,inline=False)
    
    
    
    #einfuegen, was fuer rolen user hat und was top role ist
    embed.add_field(name=f'Roles: ({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)
    
    
    
    #textfeld senden
    await ctx.send(embed=embed)
        
        
        
        

#error message senden, aber dann sehe ich keine errors mehr deshalb nein
"""@bot.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        em = discord.Embed(title="<:balls:1122153712840871996>", description=f"Command not found.", color=ctx.author.color) 
        await ctx.send(embed=em)"""





#wenn auf eine nachricht reagiert wird, rolen zuweisen
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    
    
    
    if message_id:
        member = (await bot.get_guild(payload.guild_id).fetch_member(payload.user_id))
        print({member})
        guild_id = payload.guild_id
        guild = bot.get_guild(guild_id)        



        role_name = None
        if payload.emoji.name == "🔴":
            role_name = "weekdays_morning"
        elif payload.emoji.name == "🟠":
            role_name = "weekdays_midday"
        elif payload.emoji.name == "🟡":
            role_name = "weekdays_evening"
        elif payload.emoji.name == "🟢":
            role_name = "weekdays_night"
        elif payload.emoji.name == "🔵":
            role_name = "weekend_morning"
        elif payload.emoji.name == "🟣":
            role_name = "weekend_midday"
        elif payload.emoji.name == "🟤":
            role_name = "weekend_evening"
        elif payload.emoji.name == "⚪":
            role_name = "weekend_night"
        elif payload.emoji.name == "⚫":
            role_name = "dogfight_only"
        elif payload.emoji.name == "1️⃣":
            role_name = "+1"
        elif payload.emoji.name == "2️⃣":
            role_name = "+2"



        role = get(payload.member.guild.roles, name = role_name)



        if role_name is not None:
            member = get(guild.members, id=payload.user_id)
            
            
            
            if member is not None:
                await payload.member.add_roles(role)
                print(f"Added role to {member}")
            
            
            
            else:
                print("User not found . . .")
        
        
        
        else:
            print("Role not found . . .")




        
@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    message_id = payload.message_id
    
    
    
    if message_id: 
        member = (await bot.get_guild(payload.guild_id).fetch_member(payload.user_id))
        print({member})
        guild_id = payload.guild_id
        guild = bot.get_guild(guild_id)



        role_name = None
        if payload.emoji.name == "🔴":
            role_name = "weekdays_morning"
        elif payload.emoji.name == "🟠":
            role_name = "weekdays_midday"
        elif payload.emoji.name == "🟡":
            role_name = "weekdays_evening"
        elif payload.emoji.name == "🟢":
            role_name = "weekdays_night"
        elif payload.emoji.name == "🔵":
            role_name = "weekend_morning"
        elif payload.emoji.name == "🟣":
            role_name = "weekend_midday"
        elif payload.emoji.name == "🟤":
            role_name = "weekend_evening"
        elif payload.emoji.name == "⚪":
            role_name = "weekend_night"
        elif payload.emoji.name == "⚫":
            role_name = "dogfight_only"
        elif payload.emoji.name == "1️⃣":
            role_name = "+1"
        elif payload.emoji.name == "2️⃣":
            role_name = "+2"



        role = discord.utils.get(bot.get_guild(payload.guild_id).roles,name = role_name)



        if role_name is not None:
            member = (await bot.get_guild(payload.guild_id).fetch_member(payload.user_id))
            
            
            
            if member and role:
                await member.remove_roles(role)
                print(f"Removed role from {member}")
                
                
                
            else:
                print("User not found . . .")
        
        
        
        else:
            print("Role not found . . .")    



@bot.command()
async def boosting(ctx, *, message=''):
    if ctx.guild.id != 1120611898937847881: 
        await ctx.send("You're not on the right server")
    else:
        channel = bot.get_channel(1120778128005005312)
        boosttype = message.split(", ")[0]
        boostdate = message.split(", ")[1]
        timezone = float(message.split(", ")[2])
        
        if timezone < 0:
            timezone = abs(timezone) + 2 -1           
            
        elif timezone > 0:
            timezone = 0 - (timezone * 2 - (timezone + 2)) -1
            
        else:
            timezone = timezone + 2 -1
            
        
        UTC = int(datetime.datetime.strptime(boostdate, '%d.%m.%Y %H:%M').timestamp())
        print(UTC)
        
        await channel.send('@everyone, ' + boosttype + ' <t:' + str(int(UTC + timezone * 3600)) + ':R>, <t:' + str(int(UTC + timezone * 3600)) + ':F>')
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        
 
@bot.command()
async def ping(ctx):
    await ctx.send('Pong! ' + str(bot.latency) + 'ms')
        


@bot.command()
async def emote(ctx: commands.Context, *, query: str = ""):
    httpSession = aiohttp.ClientSession()
    mySevenTvSession = seventv.seventv()
    limit = 100 if not query else 20
    if not query: query = random.choice(string.ascii_letters)
    try:
        data = await mySevenTvSession.emote_search(query, limit, query="url")        
    except seventvException	as error:
        await ctx.send("https://cdn.7tv.app/emote/6250b5ea2667140c8cedd1e9/2x.gif")
        return await ctx.send(embed = discord.Embed(description=re.sub(r'\d+', '', str(error)), color=ctx.author.color))
    if not data:
        await ctx.send("https://cdn.7tv.app/emote/60abf171870d317bef23d399/2x.gif")
        return await ctx.send(embed = discord.Embed(description="I didn't find any emotes", color=ctx.author.color))
    url = f'https:{random.choice(data).host_url}'
    await ctx.send(f'{url}/2x.gif')
        
    await mySevenTvSession.close() 

        
        
@bot.command()
async def temp(ctx):
    if ctx.author.id in (726079395974086680,769525682039947314,):
        await ctx.send(subprocess.run(["vcgencmd", "measure_temp"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip())
    else:
        await ctx.send(f"You don't have access to this command @{ctx.author.name}")


async def download_file(file_url, filename, save_directory, file_format):
    try:
            
        # Download the file from the provided URL
        command = ["wget", "-O", f'{save_directory}/{filename}.{file_format}', file_url]
        
        subprocess.run(["sudo", *command], capture_output=True, text=True)

        # Send a message indicating success
        #await ctx.send(f'The file has been successfully downloaded and saved in `{save_directory} as {filename}.{file_format}`')
        return
    except Exception as e:
        # Send a message indicating failure
        #await ctx.send(f'An error occurred while downloading the file: {e}')
        return
    




@bot.command()
async def download(ctx, *, message=""):
    if ctx.author.id == 726079395974086680:
        file_url = message.split(", ")[0]
        filename = message.split(", ")[1]
        folder = message.split(", ")[2]
        save_directory = f'/mnt/drive/{folder}'
        file_format = file_url.split(".")[-1].split("?")[0]
        await ctx.send(f"""Downloading file from {file_url}
                       ... This may take a while.""")
    
        # Run the download_file function in the background
        await asyncio.gather(download_file(file_url, filename, save_directory, file_format))

        # Continue with other commands or respond to the user in the meantime
        await ctx.send(f'The file has been successfully downloaded and saved in `{save_directory} as {filename}.{file_format}`')
        
    else:
        # Send a message if the command is used in a direct message (DM)
        await ctx.send(f'This command can not be used by @{ctx.author.name}.')    

        
@bot.command()
async def help(ctx: commands.Context):
    bot = ctx.guild.get_member(1118464907470450709)
    embed = discord.Embed(
        title = f'{bot.display_name} - commands',
        description = f'For detailed explanations use\n !help_{{command}}'
    )
    embed.set_thumbnail(url=bot.display_avatar)
    embed.add_field(
        name = "Commands:", 
        value = f'''
        boosting
        download
        emote
        f
        happy_birthday
        hello
        info
        ping
        post
        spruch
        temp
        '''
    )
    await ctx.send(embed = embed)
    

    
@bot.command()
async def help_f(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="f", 
            description="Press F to pay respect."
        ))
    
@bot.command()
async def help_emote(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="emote \{emotename (optional)\}", 
            description="""Sends you the 7tv emote for the emote you search. 
            If you don't add an emote, you'll get a random one."""
        ))

@bot.command()
async def help_happy_birthday(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="happy_birthday", 
            description="If anyone has birthday, why don't you congratulate him."
        ))
    
@bot.command()
async def help_hello(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="hello", 
            description="If you feel lonely, there is still one person who will respond to you immediately."
        ))
    
@bot.command()
async def help_info(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="info \{person (optional\}", 
            description="""If you wan't to get someones Discord informations, just use this command.
            But when you don't add a user, your informations will be published."""
        ))
 
@bot.command()
async def help_ping(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="ping", 
            description="When you want to play ping-pong... and to figure out the response time from the server."
        ))
    
@bot.command()
async def help_post(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="post \{subreddit (optional)\}", 
            description="""Gives you a random Reddit post from the Subreddit you added. 
            If you haven't added a Subreddit, you'll get a random meme."""
        ))
    
@bot.command()
async def help_spruch(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="spruch", 
            description="Get an motivating quote. But it's in german."
        ))
    
@bot.command()
async def help_temp(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
            title="temp", 
            description="""Gives you the current server temperature.
            But why do you try it? Because you probably don't have access to the command"""
        ))
    
    
@bot.command()
async def help_download(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
        title="download {URL-Link}, {name of the saved file}, [name of the folder]",
        description="""Downloads a file with a provided URL to a folder on the Raspberry Pi.
        The file gets saved as the name you give it but you can't access this command.
        
        For instance: !download https://example.com, example name, example folder"""
    ))
    
    
@bot.command()
async def help_boosting(ctx: commands.Context):
    await ctx.send(embed = discord.Embed(
        title="boosting {type of boosting}, {boosting date and time}, {your current time zone}",
        description="""Creates a boosting session.
        Boosting date and time format: dd.mm.yyyy HH:MM
        e.g.: 17.07.2023 16:00
        The current timezone in +-n depending on the timezone you're in.
        
        For instance: !boosting dogfight kills, 17.07.2023 16:00, +2"""
    ))    





bot.run(TOKEN)