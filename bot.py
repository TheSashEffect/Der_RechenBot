#bot.py

#import stuff
import  os
import random
import praw
import asyncpraw
import datetime
import time

import discord
from  dotenv import load_dotenv
from discord.utils import get
from discord.ext import commands



#oeffnet yogi tea quotes datei bei start von bot
with open('./yogi_tea_quotes.txt', encoding='utf-8') as f:
    yogi_tea_quotes = f.read().split("|") 



#oeffnet guildliste datei bei start von bot
with open('./guildliste.txt', encoding='utf-8') as f:
    guildliste = f.read().split('|')





#laedt .env datei wegen sicherheit und so
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



#Zugangsdaten fur Reddit damit der Bot posts holen kann        
reddit = praw.Reddit(client_id='aRrwturDzMingtn95Mmbvw',
                     client_secret='JlgeXUfvBEeYVkE5pZG4-ipc7dSb5Q',
                     password='ErTzUi123456',
                     user_agent='pc:Discord App:v1.0 (by /u/der_rechenbot)',
                     username='Der_RechenBot')





#das intents alle intents sind, die discord zu bieten hat
intents = discord.Intents().all()





#erstens fur allgemein bot und das der grosz-kleinschreibung ignoriert, command braucht ! davor und intents=intents
bot = commands.Bot(case_insensitive=True, command_prefix='!', intents=intents, activity=discord.Streaming(name="for the people who are watching", url='https://www.twitch.tv/the_sash_effect'))


        


#wenn bot startet dann sagt der das er connected ist und zu welchen Servern        
@bot.event
async def on_ready():       
    print(f'{bot.user.name} has connected to Discord in following Guild(s): ')
    print(guildliste)





#wenn jemand joined, dann dm mit herzlich willkommen
"""@bot.event
async def on_member_join(member):
    await member.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )"""





#wenn nachricht geschickt wird checkst nach:
@bot.event
async def on_message(message):
    
    #wenn sender dieser bot ist nicht nochmal senden
    if message.author == bot.user:
        return
    
    
    
    #wenn sender ein anderer bot ist, nicht nochmal senden
    if message.author.id in (1063806186048192532,1122866223185662124,):
        return
    
    
    
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
@bot.command(help = "test")
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
async def boosting(ctx, message=''):
    if ctx.guild.id != 1120611898937847881: 
        await ctx.send("You're not on the right server")
    else:
        channel = bot.get_channel(1128569303776636968)
        boosttype = message.split(",")[0]
        boostdate = message.split(",")[1]
        boosttime = message.split(",")[2]
        await channel.send('@everyone ' + str(boosttype) + ', ' + str(boostdate) + ', ' + str(boosttime)+ " o'clock")
    


bot.run(TOKEN)