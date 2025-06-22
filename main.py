import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def shorten_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        r = requests.get(f'https://tinyurl.com/api-create.php?url={url}')
        return r.text.strip() if r.status_code == 200 else None
    except:
        return None

@client.event
async def on_ready():
    print(f'{client.user} is online!')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!hidelink"):
        parts = message.content.split(maxsplit=1)
        if len(parts) < 2:
            await message.channel.send("❌ Usage: `!hidelink <url>`")
            return

        shortened = shorten_url(parts[1])
        if shortened:
            await message.channel.send(f"🔗 Shortened URL: {shortened}")
        else:
            await message.channel.send("❌ Failed to shorten URL.")

token = os.getenv("TOKEN")
if token:
    client.run(token)
else:
    print("⚠️ TOKEN not found in environment variables.")
