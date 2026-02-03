import aiosqlite

class DB:
    async def on_startup(self):
        self.con = await aiosqlite.connect("database/user.db")

        await self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                verified TEXT,
                user_id BIGINT PRIMARY KEY,
                lang TEXT
            )
            """
        )

        await self.con.execute(
            """
            CREATE TABLE IF NOT EXISTS refs (
                ref TEXT
            )
            """
        )

        # если таблица refs пустая — вставляем одну строку
        cursor = await self.con.execute("SELECT COUNT(*) FROM refs")
        count = (await cursor.fetchone())[0]
        if count == 0:
            await self.con.execute(
                "INSERT INTO refs (ref) VALUES (?)",
                ("https://1wbegp.live/?open-register&p=0tb6",)
            )

        await self.con.commit()

    # ---------- REF ----------

    async def get_ref(self) -> str:
        cursor = await self.con.execute("SELECT ref FROM refs LIMIT 1")
        row = await cursor.fetchone()
        return row[0]

    async def edit_ref(self, url: str) -> None:
        await self.con.execute(
            "UPDATE refs SET ref = ?",
            (url,)
        )
        await self.con.commit()

    # ---------- USERS ----------

    async def get_users_count(self) -> int:
        cursor = await self.con.execute("SELECT COUNT(*) FROM users")
        return (await cursor.fetchone())[0]

    async def get_verified_users_count(self) -> int:
        cursor = await self.con.execute(
            "SELECT COUNT(*) FROM users WHERE verified = 'verified'"
        )
        return (await cursor.fetchone())[0]

    async def register(self, user_id, language: str, verified="0"):
        try:
            await self.con.execute(
                "INSERT INTO users (verified, user_id, lang) VALUES (?, ?, ?)",
                (verified, user_id, language)
            )
            await self.con.commit()
        except aiosqlite.IntegrityError:
            pass

    async def update_verified(self, user_id, verified="verified"):
        await self.con.execute(
            "UPDATE users SET verified = ? WHERE user_id = ?",
            (verified, user_id)
        )
        await self.con.commit()

    async def get_user(self, user_id):
        cursor = await self.con.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()

    async def get_user_info(self, user_id):
        cursor = await self.con.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )
        return await cursor.fetchone()

    async def get_users(self):
        cursor = await self.con.execute("SELECT * FROM users")
        return await cursor.fetchall()

    async def update_lang(self, user_id, language: str):
        await self.con.execute(
            "UPDATE users SET lang = ? WHERE user_id = ?",
            (language, user_id)
        )
        await self.con.commit()

    async def get_lang(self, user_id):
        cursor = await self.con.execute(
            "SELECT lang FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()
        return row[0] if row else None

Database = DB()
