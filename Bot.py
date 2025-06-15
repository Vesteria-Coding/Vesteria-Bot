import os
import discord
import random as r
from dotenv import load_dotenv
from discord import app_commands, Interaction, Embed

# Setup Credentials
load_dotenv()
BOT_TOKEN = os.getenv("discord_token")
GUILD_ID = 1251261187404857496
ALLOWED_USERS = [895402417112375296]
BLOCKED_USER_ID = [1015048641041412096]

# Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
fun_responses = ['ᓚᘏᗢ',
       'ฅ^•ﻌ•^ฅ',
       r"""(\\ (\
( -.-)
o_(")(")"""]

@client.event
async def on_ready():
    print(f"Bot is ready. Logged in as {client.user} (ID: {client.user.id})")
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("commands synced to guild")

@client.event
async def on_message(message):
    if message.author.id in BLOCKED_USER_ID:
        try:
            await message.delete()
        except discord.Forbidden:
            print("Missing permissions to delete the message.")
        except discord.HTTPException as e:
            print(f"Failed to delete message: {e}")
    else:
        await bot.process_commands(message)

@tree.command(name="ping", description="sends ping of bot", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    latency = client.latency * 1000  # Convert to ms
    await interaction.response.send_message(f'Pong! `{latency:.2f}ms`', ephemeral=True)

@tree.command(name="fun", description="List of fun commands", guild=discord.Object(id=GUILD_ID))
async def fun(interaction: discord.Interaction):
    r.seed(interaction.id)
    await interaction.response.send_message(r.choice(fun_responses), ephemeral=True)

@tree.command(name="speak", description="responds with what you type", guild=discord.Object(id=GUILD_ID))
async def speak(interaction: discord.Interaction, message: str):
    if interaction.user.id in ALLOWED_USERS:
        await interaction.response.send_message("Message sent!", ephemeral=True)
        await interaction.channel.send(message)
    else:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

@tree.command(name="rules", description="sends rules of the server", guild=discord.Object(id=GUILD_ID))
async def rules(interaction: discord.Interaction):
    embed = discord.Embed(title="Server Rules", description="Please read and follow these rules carefully:", color=discord.Color.dark_red())
    embed.add_field(name="1. No Offensive or Discriminatory Behavior", value="Hate speech, racism, sexism, or any form of discrimination is not tolerated.", inline=False)
    embed.add_field(name="2. No NSFW Content", value="Do not send explicit, suggestive, or inappropriate content.", inline=False)
    embed.add_field(name="3. Be Respectful", value="Treat everyone with kindness and respect. Harassment or bullying will not be tolerated.", inline=False)
    embed.add_field(name="4. Have Fun!", value="Enjoy the community and make it a welcoming space for everyone!", inline=False)
    embed.add_field(name="5. Report Issues Properly", value='If you have trouble with someone or want to report something, please DM the “ModMail” bot.', inline=False)
    embed.add_field(name="6. Swearing Policy", value="Swearing is allowed but do not go overboard or use it to insult others.", inline=False)
    embed.add_field(name="7. Use Common Sense", value="If you think something might be against the rules, it probably is. Think before you act.", inline=False)
    embed.add_field(name="8. No Advertising or Self-Promotion", value="Do not promote your own content or other servers without staff permission.", inline=False)
    embed.add_field(name="9. No Spamming or Flooding", value="Avoid sending repeated messages, emojis, or unnecessary mentions.", inline=False)
    embed.add_field(name="10. Stay on Topic", value="Please use the appropriate channels for your conversations.", inline=False)
    embed.add_field(name="11. No Impersonation", value="Do not impersonate mods, bots, or other members.", inline=False)
    embed.add_field(name="12. Respect Staff Decisions", value="Moderator decisions are final. If needed, appeal respectfully via ModMail.", inline=False)
    embed.add_field(name="13. English Only", value="Please use English in public channels to ensure everyone can understand.", inline=False)
    embed.add_field(name="14. Consequences", value="Breaking these rules may result in a kick or ban depending on severity.", inline=False)
    embed.add_field(name="15. 10-Minute Chat Delay", value="New members must wait 10 minutes before chatting. This helps prevent bot spam.", inline=False)
    embed.set_footer(text="Thanks for being part of Vesteria Club!")
    await interaction.response.send_message(embed=embed)


@tree.command(name="about", description="about the bot", guild=discord.Object(id=GUILD_ID))
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="About The Bot",
        color=discord.Color.dark_green()
    )
    embed.add_field(name="Who it is by?", value="Its a joint effort by Eclipse and Vesteria_", inline=False)
    embed.set_footer(text="Thanks for being part of Vesteria Club!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(guild=discord.Object(id=GUILD_ID), name="create_ticket", description="Create a new support ticket")
async def create_ticket(interaction: discord.Interaction):
    category = discord.utils.get(interaction.guild.categories, name="Tickets")
    if not category:
        category = await interaction.guild.create_category("Tickets")
    existing = discord.utils.get(category.channels, name=f"ticket—for—{interaction.user.name}")
    if existing:
        await interaction.response.send_message(f"You already have an open ticket: {existing.mention}", ephemeral=True)
        return
    channel = await interaction.guild.create_text_channel(name=f"ticket—for—{interaction.user.name}", category=category)
    await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)
    await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

@tree.command(guild=discord.Object(id=GUILD_ID), name="close_ticket", description="Close the current ticket")
async def close_ticket(interaction: discord.Interaction):
    if "ticket—for" in interaction.channel.name:
        await interaction.channel.delete()
        await interaction.response.send_message("Ticket closed", ephemeral=True)
    else:
        await interaction.response.send_message("This isn't a ticket channel!", ephemeral=True)

@tree.command(name="help", description="sends list of commands", guild=discord.Object(id=GUILD_ID))
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Server Commands", description="Here is a list of available bot commands:", color=discord.Color.dark_green())
    embed.add_field(name="/ping", value="Shows the current latency of the bot.", inline=False)
    embed.add_field(name="/fun", value="Sends a fun random cat-like emoticon.", inline=False)
    embed.add_field(name="/rules", value="Displays the server rules", inline=False)
    embed.add_field(name="/about", value="Gives information about this bot and its creators.", inline=False)
    embed.add_field(name="/create_ticket", value="Creates a private support ticket channel for you.", inline=False)
    embed.add_field(name="/close_ticket", value="Closes the ticket channel you are in.", inline=False)
    embed.add_field(name="/help", value="Displays this help message.", inline=False)
    embed.add_field(name="/socials", value="Displays Vesteria's social media.", inline=False)
    embed.set_footer(text="Thanks for being part of Vesteria Club!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="socials", description="send Vesteria_'s socials media", guild=discord.Object(id=GUILD_ID))
async def socials(interaction: discord.Interaction):
    embed = discord.Embed(title="Social Media")
    embed.add_field(name="Twitch", value="https://twitch.tv/Vester1a_", inline=False)
    embed.add_field(name="Youtube", value="https://www.youtube.com/@Vesteria_", inline=False)
    embed.set_footer(text="Thanks for being part of Vesteria Club!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(BOT_TOKEN)
