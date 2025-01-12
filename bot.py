import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from aiohttp import web
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
        await super().start(*args, **kwargs)  # Pass extra arguments to the superclass
        me = await self.get_me()
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", 8080).start()
        print(f"{me.first_name} Now Working 😘")

    async def stop(self, *args, **kwargs):
        await super().stop(*args, **kwargs)
        print("Bot stopped.")

# Main entry point
if __name__ == "__main__":
    app = Bot()

    async def main():
        try:
            await app.start()
            await asyncio.Event().wait()  # Keep the bot running indefinitely
        except KeyboardInterrupt:
            pass
        finally:
            await app.stop()

    asyncio.run(main())
