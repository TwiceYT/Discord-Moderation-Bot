import nextcord 
import nextcord.interactions
from nextcord.ext import commands, application_checks
from nextcord.ext.commands.cooldowns import BucketType
import api
import time

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",intents=intents, case_insensitive=False, help_command=None)

#Prefix Test (!Hello)
@bot.command()
async def hello(ctx):
   await ctx.send("Hello, I hope you have an amazing day :D")

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Hello
#

@bot.slash_command(
    name="hello",
    description="Send hello in chat<3",
    guild_ids=[api.GuildID]
)
async def hello(ctx):
    await ctx.send("Hello, I hope you have an amazing day <3")

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Ping
#

@bot.slash_command(
   name="ping", 
   description="API Latency",
   guild_ids=[api.GuildID]
)
async def ping(i: nextcord.Interaction):
    return await i.response.send_message(f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True)

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Embed
#

@application_checks.has_permissions(manage_messages=True)
@bot.slash_command(
   name="embed",
   description="send embeded",
   guild_ids=[api.GuildID]
)
async def embed(i: nextcord.Interaction, title: str = "Default Title" ,field1:str=None, embed_color: int = 0x3498db):
    async with i.channel.typing():
        color=nextcord.Color(embed_color)
        embed = nextcord.Embed(
            title=title,
            description="",
            color=color
        )

        #embed.set_author(name="Author: "+i.user.name, icon_url=i.user.avatar.url)  
        embed.add_field(name="", value=field1, inline=False)
        embed.set_footer(text="Posted by: "+i.user.name, icon_url=i.user.avatar.url)
        await i.channel.send(embed=embed)
        await i.response.send_message("Message sent", ephemeral=True) 

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Ban
#

@application_checks.has_permissions(ban_members=True)
@bot.slash_command(
   name="ban",
   description="Ban user",
   guild_ids=[api.GuildID]
)
# author name last time
@application_checks.has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason=None):
    guild = ctx.guild
    member = guild.get_member(member.id)
    print("A member got banned")
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned', ephemeral=True)

            # Sending the reason to the log
    channel = ctx.guild.get_channel(api.CidLogM)  # Channel "Private"
    if channel:
            embed = nextcord.Embed(
                title="User banned",
                description=f"User {member} has been banned!",
                color=0xFF6FFF  # pink color
                )
            embed.add_field(name="Ban Reason", value=reason, inline=False)
            embed.set_footer(text=f"User banned by: {ctx.user.name}")
            await channel.send(embed=embed)
#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Unban
#

@application_checks.has_permissions(ban_members=True)
@bot.slash_command(
   name="unban",
   description="Unban a user",
   guild_ids=[api.GuildID]
)
async def unban(ctx: nextcord.Interaction, user: nextcord.User):
    try:
        # Check if the user has permissions to unban users (you can customize this check)
        if ctx.user.guild_permissions:
            # Fetch the ban entry for the user
            ban_entry = await ctx.guild.fetch_ban(user)
            
            if ban_entry:
                # Unban the user
                await ctx.guild.unban(user)
                
                # Inform that the user has been unbanned
                await ctx.send(f'User {user} has been unbanned!', ephemeral=True)
                
                # Sending the action to the log channel
                channel = ctx.guild.get_channel(api.CidLogM)
                if channel:
                    embed = nextcord.Embed(
                        title="User Unbanned",
                        description=f"User {user} has been unbanned!",
                        color=0xFF6FFF  # pink color
                    )
                    embed.set_footer(text=f"Unbanned by {ctx.user.name}")
                    await channel.send(embed=embed)
            else:
                await ctx.send("User is not banned.", ephemeral=True)
        else:
            await ctx.send("You don't have permission to use this command.", ephemeral=True)
    except Exception as e:
        # Log the error and inform the user
        print(f"An error occurred: {str(e)}")
        await ctx.send("An error occurred while processing your request.", ephemeral=True)


#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Kick
#

 #kick command
@application_checks.has_permissions(kick_members=True)
@bot.slash_command(
    name="kick",
   description="Kick a user",
   guild_ids=[api.GuildID]
)
async def kick(ctx, member: nextcord.Member, *, reason=None):
    print("A member got kicked")
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has got kicked!', ephemeral=True)

    #Sending the reason to log channel!
    channel = ctx.guild.get_channel(api.CidLogM) #Channel "Private"
    if channel: 
        embed = nextcord.Embed(
            title="User Kicked",
            description=f"User {member} has been kicked for the following reason:",
            color=0xFF6FFF  #pink color
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=embed)

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Unkick
#

# @bot.slash_command(
#    name="unkick",
#    description="Unkick a user",
#    guild_ids=[api.GuildID]
# )
# async def unkick(ctx: nextcord.Interaction, user: nextcord.User):
#     # Check if the user has permissions to unkick users (you can customize this check)
#     if ctx.user.guild_permissions:
#         try:
#             # Generate an invite link for the server
#             #invite= await ctx.guild.text_channels[api.CidInv].create_invite()
#             invite_channel = None
#             for channel in ctx.guild.text_channels:
#                 if channel.permissions_for(ctx.guild.me).create_instant_invite:
#                     invite_channel = channel
#                     break

#             if invite_channel:
#                 # Generate an invite link for the selected channel
#                 invite = await invite_channel.create_invite()

#             # Send the invite link to the user
#             await user.send(f"You have been 'unkicked' from {ctx.guild.name}! Here's an invite link to rejoin: {invite}")
            
#             # Inform the user that they have been "unkicked"
#             await ctx.send(f'User {user} has been "unkicked" and sent an invitation to rejoin the server!', ephemeral=True)
            
#             # Sending the action to the log channel
#             channel = ctx.guild.get_channel(api.CidLogM)
#             if channel:
#                 embed = nextcord.Embed(
#                     title="User Unkicked",
#                     description=f"User {user} has been 'unkicked' and sent an invitation to rejoin the server.",
#                     color=0xFF6FFF  # pink color
#                 )
#                 await channel.send(embed=embed)
#         except Exception as e:
#             await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)
#     else:
#         await ctx.send("You don't have permission to use this command.", ephemeral=True) 

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#DM Feature
#
@application_checks.has_permissions(administrator=True)
@bot.slash_command(
    name="dm",
    description="Send a message to a user",
    guild_ids=[api.GuildID]
)
async def dm(ctx: nextcord.Interaction, user: nextcord.Member, *, field1:str=None ,title: str = "Default Title", embed_color: int = 0x3498db):
    try:
        print("Messaged a user!")

        # Create an embed with the provided message
        embed = nextcord.Embed(
            title=title,
            description="",
            color=embed_color
        )
        embed.add_field(name="", value=field1, inline=False)
        # Send the embed to the user
        await user.send(embed=embed)

        # Send a confirmation message in the current channel
        await ctx.send("Message is sent to the user!", ephemeral=True)
    except Exception as e:
        # Handle any errors and inform the user
        await ctx.send(f"An error occurred: {str(e)}", ephemeral=True)
#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#DM LOGS Features, DM Listener
#

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself

    if isinstance(message.channel, nextcord.DMChannel, ):
        # Message is from a DM, forward it to the modmail channel
        modmail_channel = bot.get_channel(api.CidDM)
        if modmail_channel:
         #  await modmail_channel.send(f'{message.author}: {message.content}')
                
                # Sending the action to the log channel
            embed = nextcord.Embed(
            title=f"{message.author} sent a DM",
            description=f"{message.content}",
            color=0xFF6FFF  #pink color
        )
        await modmail_channel.send(embed=embed)


        # Optionally, you can reply to the user to acknowledge receipt of their message
        await message.author.send("Your message has been taken!")

    await bot.process_commands(message)

#
#
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Support Command
#

@bot.slash_command(
   name="support",
   description="Send a support Message!",
   guild_ids=[api.GuildID]
)
async def embed(ctx, title: str = "Default Title" ,field1:str=None, embed_color: int = 0x3498db):
        channel = ctx.guild.get_channel(api.CidSH) #Channel "Private" 
        color=nextcord.Color(embed_color)
        embed = nextcord.Embed(
            title=title,
            description="",
            color=0xff6fff
        )

        #embed.set_author(name="Author: "+i.user.name, icon_url=i.user.avatar.url)  
        embed.add_field(name="", value=field1, inline=False)
        embed.set_footer(text=f"Posted by: {ctx.user.display_name}")
                         
        await channel.send(embed=embed)
        await ctx.send("Message sent, you will soon get response through bot dms!", ephemeral=True) 


bot.run(api.Token)