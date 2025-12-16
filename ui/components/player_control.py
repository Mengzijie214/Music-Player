from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                             QSlider, QLabel, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize  # 新增QSize导入
from PyQt6.QtGui import QIcon
import os


class PlayerControl(QWidget):
    """播放控制组件"""
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    prev_clicked = pyqtSignal()
    next_clicked = pyqtSignal()
    seek_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.is_playing = False
        self.current_music = None
        self.total_duration = 0

    def init_ui(self):
        """初始化UI"""
        self.setObjectName("ControlBar")

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)

        # 歌曲信息
        info_layout = QHBoxLayout()

        self.title_label = QLabel("未选择音乐")
        self.title_label.setObjectName("TitleLabel")
        self.title_label.setMaximumWidth(400)

        self.artist_label = QLabel("")
        self.artist_label.setStyleSheet("color: #888888;")
        self.artist_label.setMaximumWidth(300)

        info_layout.addWidget(self.title_label)
        info_layout.addWidget(self.artist_label)
        info_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # 时间标签
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("StatusLabel")
        self.time_label.setMinimumWidth(100)
        info_layout.addWidget(self.time_label)

        main_layout.addLayout(info_layout)

        # 控制按钮和进度条布局
        control_layout = QHBoxLayout()
        control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 上一曲按钮
        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(QIcon(self.get_icon_path("prev.png")))
        self.prev_btn.setIconSize(QSize(32, 32))  # 修正为QSize
        self.prev_btn.setFixedSize(40, 40)
        self.prev_btn.clicked.connect(self.prev_clicked.emit)
        control_layout.addWidget(self.prev_btn)

        control_layout.addSpacing(20)

        # 播放/暂停按钮
        self.play_btn = QPushButton()
        self.play_btn.setObjectName("PlayButton")
        self.play_btn.setIcon(QIcon(self.get_icon_path("play.png")))
        self.play_btn.setIconSize(QSize(24, 24))  # 同步修正
        self.play_btn.clicked.connect(self.on_play_pause_clicked)
        control_layout.addWidget(self.play_btn)

        control_layout.addSpacing(20)

        # 下一曲按钮
        self.next_btn = QPushButton()
        self.next_btn.setIcon(QIcon(self.get_icon_path("next.png")))
        self.next_btn.setIconSize(QSize(32, 32))  # 同步修正
        self.next_btn.setFixedSize(40, 40)
        self.next_btn.clicked.connect(self.next_clicked.emit)
        control_layout.addWidget(self.next_btn)

        control_layout.addSpacing(40)

        # 进度条
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimumWidth(400)
        self.progress_slider.setRange(0, 100)
        self.progress_slider.sliderReleased.connect(self.on_seek)
        control_layout.addWidget(self.progress_slider)

        main_layout.addLayout(control_layout)

    def get_icon_path(self, icon_name):
        """获取图标路径"""
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "resources", "icons", icon_name
        )

    def update_play_status(self, is_playing):
        """更新播放状态"""
        self.is_playing = is_playing
        if is_playing:
            self.play_btn.setIcon(QIcon(self.get_icon_path("pause.png")))
            self.play_btn.setObjectName("PauseButton")
        else:
            self.play_btn.setIcon(QIcon(self.get_icon_path("play.png")))
            self.play_btn.setObjectName("PlayButton")
        self.play_btn.setStyleSheet("")  # 刷新样式

    def update_music_info(self, music):
        """更新音乐信息"""
        self.current_music = music
        if music:
            self.title_label.setText(music['title'])
            self.artist_label.setText(f"- {music['artist']}")
            self.total_duration = int(music['duration'])
            self.progress_slider.setRange(0, self.total_duration)
            self.time_label.setText(f"00:00 / {music['duration_str']}")
        else:
            self.title_label.setText("未选择音乐")
            self.artist_label.setText("")
            self.time_label.setText("00:00 / 00:00")
            self.progress_slider.setRange(0, 100)
            self.progress_slider.setValue(0)

    def update_progress(self, position):
        """更新播放进度"""
        if self.total_duration > 0:
            self.progress_slider.setValue(position)
            current_time = f"{position // 60:02d}:{position % 60:02d}"
            self.time_label.setText(f"{current_time} / {self.current_music['duration_str']}")

    def on_play_pause_clicked(self):
        """播放/暂停按钮点击"""
        if self.is_playing:
            self.pause_clicked.emit()
        else:
            self.play_clicked.emit()

    def on_seek(self):
        """进度条拖拽跳转"""
        position = self.progress_slider.value()
        self.seek_requested.emit(position)