import aiosqlite
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "user.db")


class DB:
    async def on_startup(self):
        self.con = await aiosqlite.connect(DB_PATH)

        await self.con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            verifed TEXT,
            lang TEXT
        )
        """)

        await self.con.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        await self.con.execute(
            "INSERT OR IGNORE INTO settings (key, value) VALUES ('ref', ?)",
            ("https://1wyuds.com/?open=register&p=0tb6",)
        )

        await self.con.commit()

    async def get_ref(self):
        cur = await self.con.execute(
            "SELECT value FROM settings WHERE key='ref'"
        )
        row = await cur.fetchone()
        return row[0]

    async def edit_ref(self, url: str):
        await self.con.execute(
            "UPDATE settings SET value=? WHERE key='ref'",
            (url,)
        )
        await self.con.commit()

    async def register(self, user_id: int, lang: str):
        await self.con.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
            (user_id, "0", lang)
        )
        await self.con.commit()

    async def update_verifed(self, user_id: int):
        await self.con.execute(
            "UPDATE users SET verifed='verifed' WHERE user_id=?",
            (user_id,)
        )
        await self.con.commit()

    async def get_user_info(self, user_id: int):
        cur = await self.con.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )
        return await cur.fetchone()

    async def get_lang(self, user_id: int):
        cur = await self.con.execute(
            "SELECT lang FROM users WHERE user_id=?",
            (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else "ru"


DataBase = DB()
