import os
from pyrogram import Client
from aiohttp import web
from config import API_ID, API_HASH, BOT_TOKEN
from chatgpt import web_server

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="chatgpt",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "chatgpt"},
            sleep_threshold=15,
        )

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        me = await self.get_me()
        app = web.AppRunner(await web_server())
        await app.setup()
        port = int(os.getenv("PORT", 8080))  # Use dynamic port
        await web.TCPSite(app, "0.0.0.0", port).start()
        print(f"{me.first_name} Now Working 😘")

    async def stop(self, *args, **kwargs):
        await super().stop(*args, **kwargs)
        print("Bot stopped.")

# Run the bot
app = Bot()

from asyncio import run

async def main():
    await app.run()

run(main())
