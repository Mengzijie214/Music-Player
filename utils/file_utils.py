import os
import shutil
import uuid
from pathlib import Path

# 支持的音乐格式
SUPPORTED_FORMATS = ['.mp3', '.flac', '.wav', '.ogg', '.m4a', '.aac', '.wma']


def get_supported_files(file_paths):
    """筛选支持的音乐文件"""
    supported_files = []
    for path in file_paths:
        if Path(path).suffix.lower() in SUPPORTED_FORMATS:
            supported_files.append(path)
    return supported_files


def copy_music_file(source_path, target_dir):
    """复制音乐文件到应用存储目录"""
    try:
        # 创建目标目录
        os.makedirs(target_dir, exist_ok=True)

        # 生成唯一文件名避免冲突
        file_ext = Path(source_path).suffix
        unique_name = f"{uuid.uuid4().hex}{file_ext}"
        target_path = os.path.join(target_dir, unique_name)

        # 复制文件
        shutil.copy2(source_path, target_path)
        return target_path
    except Exception as e:
        print(f"复制文件失败: {e}")
        return None


def get_file_info(file_path):
    """获取文件信息"""
    path = Path(file_path)
    return {
        'filename': path.name,
        'basename': path.stem,
        'ext': path.suffix,
        'size': os.path.getsize(file_path),
        'path': file_path
    }


def init_data_dirs():
    """初始化数据目录"""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    music_dir = os.path.join(base_dir, 'music_files')

    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(music_dir, exist_ok=True)

    return {
        'base_dir': base_dir,
        'music_dir': music_dir,
        'db_path': os.path.join(base_dir, 'music_db.sqlite3')
    }