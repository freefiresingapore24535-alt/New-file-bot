from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import pytz
from datetime import datetime
from config import *
from database.db_premium import *
from database.database import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

# Disable low-level APScheduler logs
logging.getLogger("apscheduler").setLevel(logging.WARNING)

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(remove_expired_users, "interval", seconds=10)

async def daily_reset_task():
    try:
        await db.reset_all_verify_counts()
    except:
        pass

scheduler.add_job(daily_reset_task, "cron", hour=0, minute=0)


def get_indian_time():
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="/data/newbot",         # IMPORTANT FIX
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        scheduler.start()

        usr_bot_me = await self.get_me()
        self.username = usr_bot_me.username
        self.uptime = get_indian_time()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel

            test = await self.send_message(db_channel.id, "Test Message")
            await test.delete()

        except Exception as e:
            LOGGER.warning(e)
            LOGGER.warning(
                f"Make sure bot is admin in DB Channel. Current CHANNEL_ID = {CHANNEL_ID}")
            LOGGER.info("Bot stopped. Join @Sk_Anime_1 for support.")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)

        LOGGER.info("Bot Running..! Created by @Minato_Sencie")

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        try:
            await self.send_message(
                OWNER_ID,
                "<b><blockquote>Bot Restarted by @Minato_Sencie</blockquote></b>"
            )
        except:
            pass

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Bot stopped.")

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        LOGGER.info("Bot is now running...")

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            LOGGER.info("Shutting down...")
        finally:
            loop.run_until_complete(self.stop())
