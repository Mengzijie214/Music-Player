from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QFont


class DragArea(QWidget):
    """拖拽区域组件"""
    files_dropped = pyqtSignal(list)  # 文件拖拽信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 提示标签
        self.label = QLabel("拖拽音乐文件到此处导入")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #888888;")

        # 支持格式标签
        supported_formats = "支持格式: MP3, FLAC, WAV, OGG, M4A, AAC, WMA"
        self.format_label = QLabel(supported_formats)
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.format_label.setStyleSheet("font-size: 12px; color: #666666; margin-top: 8px;")

        layout.addWidget(self.label)
        layout.addWidget(self.format_label)

        self.setMinimumHeight(150)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("border-color: #FF3A3A; background-color: #252525;")

    def dragLeaveEvent(self, event):
        """拖拽离开事件"""
        self.setStyleSheet("")

    def dropEvent(self, event: QDropEvent):
        """拖拽释放事件"""
        self.setStyleSheet("")

        # 获取文件路径
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        if file_paths:
            self.files_dropped.emit(file_paths)
            event.acceptProposedAction()