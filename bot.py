import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from aiohttp import web
from chatgpt import web_server  # Ensure this is correctly implemented

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

    async def start(self):
        print("Starting bot...")
        await super().start()
        me = await self.get_me()
        print(f"Bot {me.first_name} (@{me.username}) is now running!")

        # Start the web server
        try:
            app = web.AppRunner(await web_server())
            await app.setup()
            site = web.TCPSite(app, "0.0.0.0", 8080)
            await site.start()
            print("Web server running on http://0.0.0.0:8080")
        except Exception as e:
            print(f"Error starting web server: {e}")

    async def stop(self):
        print("Stopping bot...")
        await super().stop()
        print("Bot stopped.")

# Main entry point
async def main():
    app = Bot()
    try:
        await app.start()
        await asyncio.Event().wait()  # Keep running indefinitely
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Shutting down.")
    finally:
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Unhandled exception: {e}")
