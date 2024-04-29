import discord
from dotenv import load_dotenv
import os
import f1_schedule

# Load environment variables
load_dotenv()

# Retrieve the token
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create an Intents object with specific intents enabled
intents = discord.Intents.default()  # This enables the default intents
intents.messages = True              # Enable the messages intent to receive messages
intents.guilds = True                # Enable the guilds intent for guild-related data
intents.message_content = True

# Create a client instance of the bot with specified intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    # Make sure the bot doesn't reply to itself
    print(f"Message from {message.author}: {message.content}")  # This line will print out any messages the bot can see
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello! How can I help you today?')

    if message.content.startswith('!f1schedule'):
        xml_data = await f1_schedule.fetch_f1_schedule()  # Your existing function to fetch the XML data
        schedule = f1_schedule.parse_f1_schedule(xml_data)  # Parse the XML data into a list of dictionaries
        schedule_message = f1_schedule.format_schedule_for_discord(schedule)  # Format it for Discord
        await message.channel.send(schedule_message)  # Send the formatted message

client.run(TOKEN)
