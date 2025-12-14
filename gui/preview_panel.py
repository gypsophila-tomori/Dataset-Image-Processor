#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import os


class PreviewPanel(QWidget):
    """预览面板"""

    keep_changed = pyqtSignal(bool)
    rotation_changed = pyqtSignal(int)
    navigate = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_image = None
        self.current_rotation = 0
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)

        # 图片信息
        info_group = QGroupBox("图片信息")
        info_layout = QHBoxLayout()
        self.label_info = QLabel("未加载图片")
        self.label_info.setWordWrap(True)
        info_layout.addWidget(self.label_info)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 图片显示区域
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; border: 1px solid #ccc; }")
        self.image_label.setMinimumSize(600, 400)
        self.image_label.setScaledContents(False)
        layout.addWidget(self.image_label, stretch=1)

        # 控制按钮
        control_layout = QHBoxLayout()

        self.btn_prev = QPushButton("← 上一张")
        self.btn_prev.clicked.connect(lambda: self.navigate.emit('prev'))
        control_layout.addWidget(self.btn_prev)

        self.checkbox_keep = QCheckBox("保留此图片")
        self.checkbox_keep.setChecked(True)
        self.checkbox_keep.stateChanged.connect(self.on_keep_changed)
        self.checkbox_keep.setStyleSheet("QCheckBox { font-size: 14px; font-weight: bold; }")
        control_layout.addWidget(self.checkbox_keep)

        control_layout.addStretch()

        self.btn_rotate_left = QPushButton("↶ 旋转-90°")
        self.btn_rotate_left.clicked.connect(lambda: self.rotate_image(-90))
        control_layout.addWidget(self.btn_rotate_left)

        self.btn_rotate_right = QPushButton("↺ 旋转+90°")
        self.btn_rotate_right.clicked.connect(lambda: self.rotate_image(90))
        control_layout.addWidget(self.btn_rotate_right)

        control_layout.addStretch()

        self.btn_next = QPushButton("下一张 →")
        self.btn_next.clicked.connect(lambda: self.navigate.emit('next'))
        control_layout.addWidget(self.btn_next)

        layout.addLayout(control_layout)

    def set_image(self, image, path, keep, rotation, index, total):
        """设置图片"""
        self.current_image = image
        self.current_rotation = rotation

        # 更新信息
        filename = os.path.basename(path)
        width, height = image.size
        file_size = os.path.getsize(path) / (1024 * 1024)  # MB

        info_text = (f"<b>文件: </b> {filename} | "
                     f"<b>分辨率:</b> {width}x{height} | "
                     f"<b>大小:</b> {file_size:.2f} MB | "
                     f"<b>旋转:</b> {rotation}° | "
                     f"<b>进度:</b> {index + 1}/{total}")
        self.label_info.setText(info_text)

        # 更新复选框
        self.checkbox_keep.blockSignals(True)
        self.checkbox_keep.setChecked(keep)
        self.checkbox_keep.blockSignals(False)

        # 显示图片
        self.display_image()

    def display_image(self):
        """显示图片"""
        if self.current_image is None:
            return

        # 应用旋转
        image = self.current_image.rotate(-self.current_rotation, expand=True)

        # 转换为QPixmap
        img_data = image.tobytes("raw", "RGB")
        qimage = QImage(img_data, image.width, image.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # 缩放以适应显示区域
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.image_label.setPixmap(scaled_pixmap)

    def rotate_image(self, angle):
        """旋转图片"""
        self.current_rotation = (self.current_rotation + angle) % 360
        self.display_image()
        self.rotation_changed.emit(self.current_rotation)

    def on_keep_changed(self, state):
        """保留状态改变"""
        self.keep_changed.emit(state == Qt.Checked)

    def resizeEvent(self, event):
        """窗口大小改变"""
        super().resizeEvent(event)
        if self.current_image:
            self.display_image()