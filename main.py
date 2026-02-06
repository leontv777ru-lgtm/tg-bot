import asyncio
import logging

from aiogram import Dispatcher, Bot

from config import BOT_TOKEN
from handlers.client import router as client_router
from handlers.admin import router as admin_router
from database.db import DataBase

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[BOT] %(filename)s:%(lineno)d %(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info("Starting bot...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(client_router, admin_router)

    # ✅ ВАЖНО: оборачиваем в lambda
    dp.startup.register(lambda: DataBase.on_startup())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# запускаем HTTP сервер в отдельном потоке
threading.Thread(target=run_http_server, daemon=True).start()

