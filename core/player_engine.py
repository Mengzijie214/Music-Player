import pygame
import threading
import time
import os
from PyQt6.QtCore import QObject, pyqtSignal


class PlayerEngine(QObject):
    """音频播放引擎"""
    # 信号
    play_status_changed = pyqtSignal(bool)  # 播放状态改变（是否播放中）
    position_updated = pyqtSignal(int)  # 播放位置更新（秒）
    music_ended = pyqtSignal()  # 音乐播放结束

    def __init__(self):
        super().__init__()
        # 初始化pygame混音器
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.is_playing = False
        self.current_music = None
        self.play_position = 0
        self.total_duration = 0
        self.position_thread = None
        self.lock = threading.Lock()

    def load_music(self, music):
        """加载音乐"""
        try:
            self.stop()  # 停止当前播放

            with self.lock:
                self.current_music = music
                self.total_duration = int(music['duration'])
                self.play_position = 0

                # 加载音频文件
                if os.path.exists(music['file_path']):
                    pygame.mixer.music.load(music['file_path'])
                    return True
                return False
        except Exception as e:
            print(f"加载音乐失败: {e}")
            return False

    def play(self):
        """播放音乐"""
        try:
            if not self.current_music:
                return False

            with self.lock:
                if self.play_position > 0:
                    pygame.mixer.music.set_pos(self.play_position)

                pygame.mixer.music.play()
                self.is_playing = True
                self.play_status_changed.emit(True)

                # 启动位置更新线程
                self._start_position_thread()

            return True
        except Exception as e:
            print(f"播放音乐失败: {e}")
            return False

    def pause(self):
        """暂停播放"""
        with self.lock:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_status_changed.emit(False)

    def resume(self):
        """恢复播放"""
        with self.lock:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_status_changed.emit(True)
            self._start_position_thread()

    def stop(self):
        """停止播放"""
        with self.lock:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play_position = 0
            self.play_status_changed.emit(False)

            # 停止位置更新线程
            if self.position_thread and self.position_thread.is_alive():
                self.position_thread.join(timeout=0.5)

    def seek(self, position):
        """跳转到指定位置（秒）"""
        try:
            with self.lock:
                if 0 <= position <= self.total_duration:
                    self.play_position = position
                    pygame.mixer.music.set_pos(position)
                    self.position_updated.emit(position)
                return True
        except Exception as e:
            print(f"跳转失败: {e}")
            return False

    def _start_position_thread(self):
        """启动播放位置更新线程"""
        if self.position_thread and self.position_thread.is_alive():
            return

        def update_position():
            while self.is_playing:
                time.sleep(0.5)
                with self.lock:
                    if pygame.mixer.music.get_busy():
                        self.play_position = pygame.mixer.music.get_pos() / 1000
                        self.position_updated.emit(int(self.play_position))
                    else:
                        # 播放结束
                        self.is_playing = False
                        self.play_position = 0
                        self.play_status_changed.emit(False)
                        self.music_ended.emit()
                        break

        self.position_thread = threading.Thread(target=update_position, daemon=True)
        self.position_thread.start()

    def toggle_play_pause(self):
        """切换播放/暂停"""
        if self.is_playing:
            self.pause()
        else:
            if self.play_position == 0:
                self.play()
            else:
                self.resume()

    def cleanup(self):
        """清理资源"""
        self.stop()
        pygame.mixer.quit()