import sqlite3


class DataBase():

    async def create(self):

        self.con = sqlite3.connect('./database/users.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user_groups(user_id INTEGER PRIMARY KEY, group_id TEXT)''')
        self.con.commit()

    async def save_user_group(self, user_id, group_id):
        try:
            self.cur.execute('''INSERT OR REPLACE INTO user_groups (user_id, group_id) VALUES (?, ?)''', (user_id, group_id))
            self.con.commit()
        except BaseException:
            pass

    async def get_user_group(self, user_id):
        self.cur.execute("SELECT group_id FROM user_groups WHERE user_id = ?", (user_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return None


DB = DataBase()
