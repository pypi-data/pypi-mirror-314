import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json


class ChatDB:
    def __init__(self, db_path: str = "chats.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    timestamp TEXT,
                    model TEXT,
                    system_prompt TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp TEXT,
                    FOREIGN KEY (chat_id) REFERENCES chats (id)
                )
            """)

    def create_chat(self, chat_id: str, name: str, model: str, system_prompt: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO chats (id, name, timestamp, model, system_prompt) VALUES (?, ?, ?, ?, ?)",
                (chat_id, name, datetime.now().isoformat(), model, system_prompt)
            )

    def add_message(self, chat_id: str, role: str, content: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO messages (chat_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (chat_id, role, content, datetime.now().isoformat())
            )

    def get_chat(self, chat_id: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            chat = conn.execute("SELECT * FROM chats WHERE id = ?", (chat_id,)).fetchone()
            if not chat:
                return None

            messages = conn.execute(
                "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY timestamp",
                (chat_id,)
            ).fetchall()

            return {
                "id": chat["id"],
                "name": chat["name"],
                "timestamp": chat["timestamp"],
                "model": chat["model"],
                "system_prompt": chat["system_prompt"],
                "messages": [dict(m) for m in messages]
            }

    def get_all_chats(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            chats = conn.execute("SELECT * FROM chats ORDER BY timestamp DESC").fetchall()
            return [dict(c) for c in chats]

    def delete_chat(self, chat_id: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
            conn.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
