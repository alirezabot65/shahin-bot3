import sqlite3
from pathlib import Path

DB = Path("data/database.db")
DB.parent.mkdir(exist_ok=True)

def conn():
    return sqlite3.connect(DB)

def init_db():
    c = conn()
    c.execute("""CREATE TABLE IF NOT EXISTS bots (
        token TEXT PRIMARY KEY,
        bot_id TEXT,
        name TEXT,
        bio TEXT,
        start_message TEXT DEFAULT ''
    )""")
    c.commit()
    c.close()

def save_bot(token, data):
    c = conn()
    c.execute("""INSERT INTO bots(token,bot_id,name,bio)
                 VALUES(?,?,?,?)
                 ON CONFLICT(token) DO UPDATE SET
                 bot_id=excluded.bot_id,name=excluded.name,bio=excluded.bio""",
              (token, data.get("bot_id") or data.get("user_id"),
               data.get("name",""), data.get("bio","")))
    c.commit()
    c.close()

def get_bot(token):
    c = conn()
    row = c.execute("SELECT bot_id,name,bio,start_message FROM bots WHERE token=?",(token,)).fetchone()
    c.close()
    if not row:
        return {}
    return {"bot_id":row[0],"name":row[1],"bio":row[2],"start_message":row[3]}
