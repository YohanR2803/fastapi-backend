# discord_bot.py
import os, aiohttp
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
VERIFIED_ROLE_ID = os.getenv("VERIFIED_ROLE_ID")

async def assign_verified_role(discord_id: str):
    url = (
      f"https://discord.com/api/v10/guilds/"
      f"{GUILD_ID}/members/{discord_id}/roles/{VERIFIED_ROLE_ID}"
    )
    headers = {
      "Authorization": f"Bot {BOT_TOKEN}",
      "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
      async with session.put(url, headers=headers) as resp:
        if resp.status != 204:
          txt = await resp.text()
          print(f"Role assignment failed {resp.status}: {txt}")
        else:
          print(f"✅ Assigned role to {discord_id}")
