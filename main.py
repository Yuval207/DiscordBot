import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import asyncio

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Store opted-in users
opt_in_users = set()

# Cooldown dictionary
cooldowns = {}

# Helper function to create embeds
def create_embed(title, description, color=discord.Color.blue()):
    return discord.Embed(title=title, description=description, color=color, timestamp=datetime.utcnow())

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Type !help for commands"))

@bot.command(name='help')
async def help(ctx):
    """Shows this help message"""
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    embed = discord.Embed(
        title="📚 Bot Commands Help",
        description="Here are all available commands:",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )

    # General Commands
    embed.add_field(
        name="🌟 General Commands",
        value="""
        `!help` - Shows this help message
        `!ping` - Check bot's response time
        `!userinfo [@user]` - Get information about a user
        """,
        inline=False
    )

    # Notification Commands
    embed.add_field(
        name="📨 Notification Commands",
        value="""
        `!optin` - Opt in to receive notifications
        `!optout` - Opt out of notifications
        """,
        inline=False
    )

    # Admin Commands
    embed.add_field(
        name="👑 Admin Commands",
        value="""
        `!notify @user message` - Send a DM to specific user
        `!notifyall message` - Send a DM to all opted-in users
        """,
        inline=False
    )

    # Usage Examples
    embed.add_field(
        name="📝 Examples",
        value="""
        • `!userinfo @JohnDoe`
        • `!notify @JohnDoe Hello there!`
        • `!notifyall Server maintenance in 5 minutes`
        """,
        inline=False
    )

    embed.set_footer(text="💡 Tip: Admin commands require administrator permissions")

    await ctx.reply(embed=embed)
    
    cooldowns[ctx.author.id] = datetime.utcnow().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)



# Helper function to create embeds
def create_embed(title, description, color=discord.Color.blue()):
    return discord.Embed(title=title, description=description, color=color, timestamp=datetime.now())

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Type !help for commands"))

@bot.event
async def on_guild_join(guild):
    # Find first available text channel
    channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
    
    if channel:
        # Welcome embed
        welcome_embed = discord.Embed(
            title="👋 Hello, I'm Your New Bot!",
            description="Thanks for adding me to your server! Here's what I can do for you:",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        welcome_embed.add_field(
            name="📬 Notification System",
            value="I can send DM notifications to specific users or broadcast to all opted-in users."
        )
        welcome_embed.add_field(
            name="👥 User Information",
            value="Get detailed information about server members."
        )
        welcome_embed.add_field(
            name="⚡ Quick Commands",
            value="Type `!help` to see all available commands!"
        )
        welcome_embed.set_footer(text="Made with ❤️ | Use !help for more information")

        # Stats embed
        stats_embed = discord.Embed(
            title="📊 Server Statistics",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        stats_embed.add_field(name="Server Name", value=guild.name, inline=True)
        stats_embed.add_field(name="Total Members", value=str(guild.member_count), inline=True)
        stats_embed.add_field(name="Text Channels", value=str(len(guild.text_channels)), inline=True)
        stats_embed.add_field(name="Voice Channels", value=str(len(guild.voice_channels)), inline=True)

        try:
            await channel.send(embeds=[welcome_embed, stats_embed])
        except Exception as e:
            print(f"Could not send welcome message to {guild.name}: {e}")

# Command cooldown check
def check_cooldown(user_id):
    if user_id in cooldowns:
        time_left = cooldowns[user_id] - datetime.now().timestamp()
        if time_left > 0:
            return time_left
    return 0

@bot.command(name='optin')
async def optin(ctx):
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    opt_in_users.add(ctx.author.id)
    embed = create_embed("", "✅ You have opted in to receive notifications!", discord.Color.green())
    await ctx.reply(embed=embed)
    
    # Set cooldown
    cooldowns[ctx.author.id] = datetime.now().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)

@bot.command(name='optout')
async def optout(ctx):
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    opt_in_users.discard(ctx.author.id)
    embed = create_embed("", "❌ You have opted out of notifications.", discord.Color.red())
    await ctx.reply(embed=embed)
    
    cooldowns[ctx.author.id] = datetime.now().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)

@bot.command(name='notify')
@commands.has_permissions(administrator=True)
async def notify(ctx, user: discord.Member, *, message: str):
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    try:
        embed = discord.Embed(
            title="New Notification",
            description=message,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Sent by {ctx.author}")
        
        await user.send(embed=embed)
        await ctx.reply(f"Message sent to {user.name} successfully!")
    except Exception as e:
        await ctx.reply(f"Failed to send message to {user.name}. They might have DMs disabled.")
        print(e)

    cooldowns[ctx.author.id] = datetime.now().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)

@bot.command(name='notifyall')
@commands.has_permissions(administrator=True)
async def notifyall(ctx, *, message: str):
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    success_count = 0
    fail_count = 0

    embed = discord.Embed(
        title="Broadcast Notification",
        description=message,
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Sent by {ctx.author}")

    for user_id in opt_in_users:
        try:
            user = await bot.fetch_user(user_id)
            await user.send(embed=embed)
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Failed to send to {user_id}: {e}")

    await ctx.reply(f"Broadcast complete!\nSuccessful: {success_count}\nFailed: {fail_count}")
    
    cooldowns[ctx.author.id] = datetime.now().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)

@bot.command(name='ping')
async def ping(ctx):
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    sent = await ctx.reply("Pinging...")
    latency = (sent.created_at - ctx.message.created_at).total_seconds() * 1000
    await sent.edit(content=f"Pong! Roundtrip latency: {latency:.2f}ms")
    
    cooldowns[ctx.author.id] = datetime.now().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    cooldown = check_cooldown(ctx.author.id)
    if cooldown > 0:
        await ctx.reply(f"Please wait {int(cooldown)} seconds before using commands again.")
        return

    member = member or ctx.author
    roles = [role.name for role in member.roles[1:]]  # Skip @everyone role

    embed = discord.Embed(
        title="User Information",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles", inline=False)

    await ctx.reply(embed=embed)
    
    cooldowns[ctx.author.id] = datetime.now().timestamp() + 3
    await asyncio.sleep(3)
    cooldowns.pop(ctx.author.id, None)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing required argument! Please check the command usage.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply("User not found! Please mention a valid user.")
    else:
        print(f"Error: {error}")

# Run the bot
bot.run(os.getenv('BOT_TOKEN'))