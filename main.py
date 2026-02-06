import asyncio
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from aiogram import Dispatcher, Bot

from config import BOT_TOKEN
from handlers.client import router as client_router
from handlers.admin import router as admin_router
from database.db import DataBase

# ---------------- HTTP SERVER (для Render) ----------------

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# запускаем HTTP сервер СРАЗУ
threading.Thread(target=run_http_server, daemon=True).start()

# ---------------- BOT ----------------

logging.basicConfig(
    level=logging.INFO,
    format="[BOT] %(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

async def on_startup(dispatcher: Dispatcher):
    await DataBase.on_startup()
    logger.info("Database initialized")

async def main():
    logger.info("Starting bot...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(client_router, admin_router)

    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
