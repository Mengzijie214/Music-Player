from PyQt6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QPushButton, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
import os


class MusicList(QWidget):
    """音乐列表组件"""
    music_selected = pyqtSignal(dict)  # 音乐选中信号
    delete_requested = pyqtSignal(int)  # 删除请求信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.music_list = []

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 音乐表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['标题', '艺术家', '专辑', '时长', '操作'])

        # 表头样式
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 80)

        # 表格设置
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setShowGrid(False)

        # 点击事件
        self.table.cellClicked.connect(self.on_cell_clicked)

        layout.addWidget(self.table)

    def update_music_list(self, music_list):
        """更新音乐列表"""
        self.music_list = music_list
        self.table.setRowCount(0)

        for music in music_list:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # 设置表格内容
            self.table.setItem(row, 0, QTableWidgetItem(music['title']))
            self.table.setItem(row, 1, QTableWidgetItem(music['artist']))
            self.table.setItem(row, 2, QTableWidgetItem(music['album']))
            self.table.setItem(row, 3, QTableWidgetItem(music['duration_str']))

            # 删除按钮
            delete_btn = QPushButton("删除")
            delete_btn.setStyleSheet("color: #FF3A3A; background-color: transparent; border: none;")
            delete_btn.clicked.connect(lambda _, m=music: self.on_delete_clicked(m['id']))
            self.table.setCellWidget(row, 4, delete_btn)

            # 设置行数据
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, music)

    def on_cell_clicked(self, row, column):
        """单元格点击事件"""
        if column < 4:  # 点击除删除按钮外的单元格
            music_item = self.table.item(row, 0)
            if music_item:
                music = music_item.data(Qt.ItemDataRole.UserRole)
                self.music_selected.emit(music)

    def on_delete_clicked(self, music_id):
        """删除按钮点击事件"""
        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这首音乐吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.delete_requested.emit(music_id)

    def get_selected_music(self):
        """获取选中的音乐"""
        selected_items = self.table.selectedItems()
        if selected_items:
            return selected_items[0].data(Qt.ItemDataRole.UserRole)
        return None