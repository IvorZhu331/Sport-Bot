import discord
from dotenv import load_dotenv
import os

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

client.run(TOKEN)
