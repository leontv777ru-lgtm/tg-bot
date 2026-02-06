import aiosqlite

class DataBase:
    def __init__(self):
        self.con: aiosqlite.Connection | None = None

    async def on_startup(self):
        self.con = await aiosqlite.connect("database/user.db")

        await self.con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                verified TEXT,
                user_id INTEGER PRIMARY KEY,
                lang TEXT
            )
        """)

        await self.con.execute("""
            CREATE TABLE IF NOT EXISTS refs (
                ref TEXT
            )
        """)

        # если refs пустая — кладём одну строку
        cur = await self.con.execute("SELECT COUNT(*) FROM refs")
        count = (await cur.fetchone())[0]
        if count == 0:
            await self.con.execute(
                "INSERT INTO refs (ref) VALUES (?)",
                ("https://1wbegp.live/?open=register&p=0tb6",)
            )

        await self.con.commit()

    async def get_ref(self) -> str:
        cur = await self.con.execute("SELECT ref FROM refs LIMIT 1")
        row = await cur.fetchone()
        return row[0]

    async def edit_ref(self, url: str):
        await self.con.execute("UPDATE refs SET ref = ?", (url,))
        await self.con.commit()

    async def register(self, user_id: int, lang: str):
        try:
            await self.con.execute(
                "INSERT INTO users (verified, user_id, lang) VALUES (?, ?, ?)",
                ("0", user_id, lang)
            )
            await self.con.commit()
        except aiosqlite.IntegrityError:
            pass

    async def update_verified(self, user_id: int):
        await self.con.execute(
            "UPDATE users SET verified = 'verified' WHERE user_id = ?",
            (user_id,)
        )
        await self.con.commit()

    async def get_user(self, user_id: int):
        cur = await self.con.execute(
            "SELECT * FROM users WHERE user_id = ? AND verified = 'verified'",
            (user_id,)
        )
        return await cur.fetchone()

    async def get_user_info(self, user_id: int):
        cur = await self.con.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cur.fetchone()

    async def get_lang(self, user_id: int):
        cur = await self.con.execute(
            "SELECT lang FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else "en"

# ❗ ЕДИНСТВЕННЫЙ экспортируемый объект
DataBase = DataBase()
