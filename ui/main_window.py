from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QSplitter, QStatusBar)
from PyQt6.QtCore import Qt
from ui.components.drag_area import DragArea
from ui.components.music_list import MusicList
from ui.components.player_control import PlayerControl
from core.music_manager import MusicManager
from core.player_engine import PlayerEngine
from utils.file_utils import get_supported_files
import os


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.init_app()
        self.init_ui()
        self.init_signals()
        self.load_music_list()

    def init_app(self):
        """初始化应用"""
        self.setWindowTitle("音乐播放器")
        self.setMinimumSize(800, 600)

        # 初始化核心组件
        self.music_manager = MusicManager()
        self.player_engine = PlayerEngine()

        # 加载样式表
        self.load_stylesheet()

    def init_ui(self):
        """初始化UI"""
        # 中心窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部标题栏
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: #1E1E1E; padding: 10px;")
        title_layout = QHBoxLayout(title_bar)

        self.title_label = QLabel("音乐播放器")
        self.title_label.setObjectName("TitleLabel")
        title_layout.addWidget(self.title_label)

        title_layout.addStretch()

        self.status_label = QLabel("就绪")
        self.status_label.setObjectName("StatusLabel")
        title_layout.addWidget(self.status_label)

        main_layout.addWidget(title_bar)

        # 主体内容区域
        splitter = QSplitter(Qt.Orientation.Vertical)

        # 拖拽区域和音乐列表
        upper_widget = QWidget()
        upper_layout = QVBoxLayout(upper_widget)

        # 拖拽区域
        self.drag_area = DragArea()
        upper_layout.addWidget(self.drag_area)

        # 音乐列表
        self.music_list = MusicList()
        upper_layout.addWidget(self.music_list)

        splitter.addWidget(upper_widget)

        main_layout.addWidget(splitter, 1)  # 占满剩余空间

        # 底部控制栏
        self.player_control = PlayerControl()
        main_layout.addWidget(self.player_control)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪 - 拖拽音乐文件到窗口导入")

    def init_signals(self):
        """初始化信号连接"""
        # 拖拽区域信号
        self.drag_area.files_dropped.connect(self.on_files_dropped)

        # 音乐列表信号
        self.music_list.music_selected.connect(self.on_music_selected)
        self.music_list.delete_requested.connect(self.on_music_delete)

        # 播放控制信号
        self.player_control.play_clicked.connect(self.on_play_clicked)
        self.player_control.pause_clicked.connect(self.on_pause_clicked)
        self.player_control.seek_requested.connect(self.on_seek_requested)
        self.player_control.prev_clicked.connect(self.on_prev_clicked)
        self.player_control.next_clicked.connect(self.on_next_clicked)

        # 播放器引擎信号
        self.player_engine.play_status_changed.connect(self.player_control.update_play_status)
        self.player_engine.position_updated.connect(self.player_control.update_progress)
        self.player_engine.music_ended.connect(self.on_music_ended)

    def load_stylesheet(self):
        """加载样式表"""
        style_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources", "styles", "dark_theme.qss"
        )

        try:
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"加载样式表失败: {e}")

    def load_music_list(self):
        """加载音乐列表"""
        music_list = self.music_manager.get_all_music()
        self.music_list.update_music_list(music_list)
        self.status_bar.showMessage(f"已加载 {len(music_list)} 首音乐")

    def on_files_dropped(self, file_paths):
        """文件拖拽处理"""
        # 筛选支持的音乐文件
        supported_files = get_supported_files(file_paths)
        if not supported_files:
            self.status_bar.showMessage("未找到支持的音乐文件")
            return

        # 添加音乐
        self.status_bar.showMessage(f"正在导入 {len(supported_files)} 首音乐...")
        added_music = self.music_manager.add_music(supported_files)

        # 更新列表
        self.load_music_list()
        self.status_bar.showMessage(f"成功导入 {len(added_music)} 首音乐")

    def on_music_selected(self, music):
        """音乐选中处理"""
        if self.player_engine.load_music(music):
            self.player_control.update_music_info(music)
            self.status_bar.showMessage(f"已选择: {music['title']} - {music['artist']}")

    def on_play_clicked(self):
        """播放按钮点击"""
        selected_music = self.music_list.get_selected_music()
        if not selected_music:
            # 没有选中音乐，尝试播放第一首
            music_list = self.music_manager.get_all_music()
            if music_list:
                selected_music = music_list[0]
                self.music_list.music_selected.emit(selected_music)

        if selected_music:
            self.player_engine.play()
            self.status_bar.showMessage(f"正在播放: {selected_music['title']}")

    def on_pause_clicked(self):
        """暂停按钮点击"""
        self.player_engine.pause()
        selected_music = self.music_list.get_selected_music()
        if selected_music:
            self.status_bar.showMessage(f"已暂停: {selected_music['title']}")

    def on_seek_requested(self, position):
        """跳转请求处理"""
        self.player_engine.seek(position)

    def on_prev_clicked(self):
        """上一曲处理"""
        music_list = self.music_manager.get_all_music()
        if not music_list:
            return

        selected_music = self.music_list.get_selected_music()
        if not selected_music:
            return

        # 找到当前音乐索引
        current_index = next((i for i, m in enumerate(music_list) if m['id'] == selected_music['id']), -1)
        if current_index > 0:
            prev_music = music_list[current_index - 1]
            self.music_list.music_selected.emit(prev_music)
            self.player_engine.play()

    def on_next_clicked(self):
        """下一曲处理"""
        music_list = self.music_manager.get_all_music()
        if not music_list:
            return

        selected_music = self.music_list.get_selected_music()
        if not selected_music:
            return

        # 找到当前音乐索引
        current_index = next((i for i, m in enumerate(music_list) if m['id'] == selected_music['id']), -1)
        if current_index < len(music_list) - 1:
            next_music = music_list[current_index + 1]
            self.music_list.music_selected.emit(next_music)
            self.player_engine.play()

    def on_music_ended(self):
        """音乐播放结束"""
        self.on_next_clicked()

    def on_music_delete(self, music_id):
        """删除音乐处理"""
        if self.music_manager.delete_music(music_id):
            # 如果删除的是当前播放的音乐
            current_music = self.player_engine.current_music
            if current_music and current_music['id'] == music_id:
                self.player_engine.stop()
                self.player_control.update_music_info(None)

            self.load_music_list()
            self.status_bar.showMessage("音乐已删除")

    def closeEvent(self, event):
        """关闭窗口事件"""
        self.player_engine.cleanup()
        event.accept()