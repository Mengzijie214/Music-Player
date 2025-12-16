import sqlite3
import os
import time
from pathlib import Path
from utils.file_utils import init_data_dirs, copy_music_file, get_file_info
from utils.audio_utils import get_audio_metadata


class MusicManager:
    def __init__(self):
        # 初始化数据目录
        self.data_dirs = init_data_dirs()
        self.db_path = self.data_dirs['db_path']
        self.music_dir = self.data_dirs['music_dir']

        # 初始化数据库
        self.init_database()

    def init_database(self):
        """初始化音乐数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建音乐表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS music (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                album TEXT NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL UNIQUE,
                duration REAL NOT NULL,
                duration_str TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                import_time INTEGER NOT NULL,
                is_favorite INTEGER DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()

    def add_music(self, source_paths):
        """添加音乐到数据库"""
        added_music = []

        for source_path in source_paths:
            try:
                # 复制文件到应用存储目录
                target_path = copy_music_file(source_path, self.music_dir)
                if not target_path:
                    continue

                # 获取文件信息和音频元数据
                file_info = get_file_info(target_path)
                audio_metadata = get_audio_metadata(target_path)

                # 准备插入数据
                music_data = {
                    'title': audio_metadata['title'],
                    'artist': audio_metadata['artist'],
                    'album': audio_metadata['album'],
                    'filename': file_info['filename'],
                    'file_path': target_path,
                    'duration': audio_metadata['duration'],
                    'duration_str': audio_metadata['duration_str'],
                    'file_size': file_info['size'],
                    'import_time': int(time.time())
                }

                # 插入数据库
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()

                cursor.execute('''
                    INSERT OR IGNORE INTO music 
                    (title, artist, album, filename, file_path, duration, duration_str, file_size, import_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    music_data['title'],
                    music_data['artist'],
                    music_data['album'],
                    music_data['filename'],
                    music_data['file_path'],
                    music_data['duration'],
                    music_data['duration_str'],
                    music_data['file_size'],
                    music_data['import_time']
                ))

                if cursor.rowcount > 0:
                    music_id = cursor.lastrowid
                    music_data['id'] = music_id
                    added_music.append(music_data)
                    print(f"添加音乐成功: {music_data['title']}")

                conn.commit()
                conn.close()

            except Exception as e:
                print(f"添加音乐失败: {e}")

        return added_music

    def get_all_music(self):
        """获取所有音乐"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM music ORDER BY import_time DESC')
        columns = [desc[0] for desc in cursor.description]
        music_list = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return music_list

    def get_music_by_id(self, music_id):
        """通过ID获取音乐"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM music WHERE id = ?', (music_id,))
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()

        conn.close()
        return dict(zip(columns, result)) if result else None

    def delete_music(self, music_id):
        """删除音乐（数据库+文件）"""
        try:
            # 获取音乐信息
            music = self.get_music_by_id(music_id)
            if not music:
                return False

            # 删除数据库记录
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM music WHERE id = ?', (music_id,))
            conn.commit()
            conn.close()

            # 删除文件
            if os.path.exists(music['file_path']):
                os.remove(music['file_path'])

            print(f"删除音乐成功: {music['title']}")
            return True
        except Exception as e:
            print(f"删除音乐失败: {e}")
            return False