import sqlite3
from datetime import datetime
from typing import Optional

class TriageDatabase:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()
    
    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE triage_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id TEXT UNIQUE NOT NULL,
                channel TEXT NOT NULL,
                category TEXT,
                sentiment TEXT,
                priority INTEGER,
                subject TEXT,
                content TEXT,
                requester TEXT,
                recipient TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.execute("""
            CREATE INDEX idx_case_id ON triage_cases(case_id)
        """)
        self.conn.execute("""
            CREATE INDEX idx_priority ON triage_cases(priority)
        """)
    
    def store_triage(self, case_id: str, channel: str, category: str = None, 
                    sentiment: str = None, priority: int = None, subject: str = None, content: str = None,
                    requester: str = None, recipient: str = None) -> int:
        cursor = self.conn.execute("""
            INSERT OR REPLACE INTO triage_cases 
            (case_id, channel, category, sentiment, priority, subject, content, requester, recipient, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (case_id, channel, category, sentiment, priority, subject, content, requester, recipient, datetime.now()))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_case(self, case_id: str) -> Optional[dict]:
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.execute("""
            SELECT * FROM triage_cases WHERE case_id = ?
        """, (case_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_cases_by_priority(self, priority: int) -> list[dict]:
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.execute("""
            SELECT * FROM triage_cases WHERE priority = ? ORDER BY created_at
        """, (priority,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_cases(self, limit: int = 50, offset: int = 0) -> tuple[list[dict], int]:
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.execute("""
            SELECT * FROM triage_cases ORDER BY created_at DESC LIMIT ? OFFSET ?
        """, (limit, offset))
        cases = [dict(row) for row in cursor.fetchall()]
        total = self.conn.execute("SELECT COUNT(*) FROM triage_cases").fetchone()[0]
        return cases, total