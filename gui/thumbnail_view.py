#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QGridLayout,
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QImage


class ThumbnailWidget(QFrame):
    """单个缩略图部件"""

    clicked = pyqtSignal(int)

    def __init__(self, index, pixmap, filename, keep=True):
        super().__init__()
        self.index = index
        self.keep = keep
        self.is_selected = False

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        self.setFixedSize(180, 180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # 缩略图
        self.img_label = QLabel()
        self.img_label.setFixedSize(160, 140)
        self.img_label.setScaledContents(True)
        self.img_label.setPixmap(pixmap)
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        # 文件名和状态
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.update_display(filename, keep)

    def update_display(self, filename, keep):
        """更新显示"""
        self.keep = keep
        status = "✓ 保留" if keep else "✗ 跳过"
        color = "green" if keep else "red"
        self.status_label.setText(
            f'<span style="color:{color}; font-weight:bold;">{status}</span><br>{filename[: 15]}...')

    def set_selected(self, selected):
        """设置选中状态"""
        self.is_selected = selected
        if selected:
            self.setStyleSheet("ThumbnailWidget { border: 3px solid #2196F3; background-color: #E3F2FD; }")
        else:
            self.setStyleSheet("ThumbnailWidget { border: 1px solid #ccc; }")

    def mousePressEvent(self, event):
        """鼠标点击"""
        self.clicked.emit(self.index)


class ThumbnailView(QWidget):
    """缩略图视图"""

    image_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.thumbnails = []
        self.current_index = -1

        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 标题
        title = QLabel("图片列表")
        title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        layout.addWidget(title)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 网格容器
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(10)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def set_images(self, pixmaps, images_data):
        """设置图片列表"""
        # 清空现有
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.thumbnails.clear()

        # 添加新缩略图
        cols = 2  # 每行2个
        for i, (pixmap, data) in enumerate(zip(pixmaps, images_data)):
            filename = data['path'].split('/')[-1]
            thumb = ThumbnailWidget(i, pixmap, filename, data['keep'])
            thumb.clicked.connect(self.on_thumbnail_clicked)

            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(thumb, row, col)
            self.thumbnails.append(thumb)

    def on_thumbnail_clicked(self, index):
        """缩略图被点击"""
        self.image_selected.emit(index)

    def set_current_index(self, index):
        """设置当前选中的索引"""
        if self.current_index >= 0 and self.current_index < len(self.thumbnails):
            self.thumbnails[self.current_index].set_selected(False)

        self.current_index = index

        if 0 <= index < len(self.thumbnails):
            self.thumbnails[index].set_selected(True)
            # 滚动到可见
            # self.thumbnails[index].ensureVisible() # 如果需要

    def update_keep_status(self, index, keep):
        """更新保留状态"""
        if 0 <= index < len(self.thumbnails):
            filename = "img"  # 这里可以传入实际文件名
            self.thumbnails[index].update_display(filename, keep)