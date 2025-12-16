from mutagen import File
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.oggvorbis import OggVorbis
from mutagen.m4a import M4A
import math


def get_audio_duration(file_path):
    """获取音频时长（秒）"""
    try:
        audio = File(file_path)
        if audio:
            return audio.info.length
        return 0
    except Exception as e:
        print(f"获取音频时长失败: {e}")
        return 0


def format_duration(seconds):
    """格式化时长为 MM:SS 格式"""
    minutes = math.floor(seconds / 60)
    secs = math.floor(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def get_audio_metadata(file_path):
    """获取音频元数据（标题、艺术家、专辑）"""
    metadata = {
        'title': '',
        'artist': '',
        'album': '',
        'duration': 0,
        'duration_str': '00:00'
    }

    try:
        audio = File(file_path, easy=True)
        if audio:
            # 获取元数据
            if 'title' in audio:
                metadata['title'] = audio['title'][0] if audio['title'] else Path(file_path).stem
            if 'artist' in audio:
                metadata['artist'] = audio['artist'][0] if audio['artist'] else '未知艺术家'
            if 'album' in audio:
                metadata['album'] = audio['album'][0] if audio['album'] else '未知专辑'

            # 获取时长
            metadata['duration'] = audio.info.length
            metadata['duration_str'] = format_duration(audio.info.length)
        else:
            # 如果没有元数据，使用文件名
            metadata['title'] = Path(file_path).stem
    except Exception as e:
        print(f"获取音频元数据失败: {e}")

    return metadata