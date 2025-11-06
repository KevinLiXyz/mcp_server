import sqlite3
import pandas as pd
from datetime import datetime
import hashlib
from typing import Dict, Any
class SQLiteStorage:
    def __init__(self, db_path: str = './db_helper/scraped_data.db'):
        """Initialize the storage with a path to the SQLite database.

        The database schema is created (if it does not already exist) during
        initialization.
        """
        self.db_path = db_path
        # Ensure the schema is created using the instance's db_path
        self.create_database_schema()

    def create_database_schema(self) -> None:
        """Create the SQLite database and the required table schema.

        The method uses ``self.db_path`` so that the instance's configured
        database file is respected.
        """
        conn = sqlite3.connect(self.db_path)
        # ``cursor`` must be a callable to obtain a cursor object
        cursor = conn.cursor()
        
        #创建主表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraped_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                content_hash TEXT,
                url TEXT,
                publish_date TEXT,
                crawl_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                update_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,       
                tags TEXT,
                status TEXT DEFAULT 'active',
                UNIQUE(title, url)  -- 防止重复数据
            )   
        ''')
        # 创建索引以提高查询性能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON scraped_data(title)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON scraped_data(url)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_crawl_time ON scraped_data(crawl_timestamp)')
        conn.commit()
        conn.close()
        print("数据库架构创建成功!")

    def _generate_content_hash(self, content):
        """生成内容Hash值 用于去重"""
        if not content:
            return None
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def save_content(self, content: Dict[str, Any]) -> bool:
        """Insert or replace a single article record.

        Returns ``True`` on success and ``False`` on failure.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        content_hash = self._generate_content_hash(content.get('content'))
        try:
            cursor.execute(
                """
                INSERT OR REPLACE INTO scraped_data (
                    title,
                    content,
                    url,
                    publish_date,
                    crawl_timestamp,
                    tags,
                    content_hash,
                    update_timestamp,
                    status
                ) VALUES (
                    ?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, CURRENT_TIMESTAMP, 'active'
                )
                """,
                (
                    content.get('title'),
                    content.get('content'),
                    content.get('url'),
                    content.get('publish_date'),
                    content.get('tags'),
                    content_hash,
                ),
            )
            conn.commit()
            print('数据写入成功')
            return True
        except Exception as ex:
            print(ex)
            conn.rollback()
            return False
        finally:
            conn.close()
    def save_batch_content(self, ontent_list):
        """
        批量保存文章列表
        """
        success_count = 0
        for article in ontent_list:
            if self.save_content(article):
                success_count += 1
        print(f"批量保存完成: {success_count}/{len(ontent_list)} 篇文章保存成功")
        return success_count
    def get_recruitment_list(self):
        """Retrieve all recruitment entries ordered by publish date.

        The SQLite connection is configured with ``row_factory = sqlite3.Row`` so
        that each fetched row behaves like a mapping, allowing a direct
        conversion to ``dict``.
        """
        conn = sqlite3.connect(self.db_path)
        # Enable dict‑like access to columns
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT title, content, url, publish_date FROM scraped_data
            ORDER BY publish_date DESC
            """
        )
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
        
storage = SQLiteStorage('./db_helper/scraped_data.db')
