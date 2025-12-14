#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                             QGroupBox, QSlider)
from PyQt5.QtCore import Qt


class SettingsPanel(QWidget):
    """设置面板"""

    def __init__(self):
        super().__init__()
        self.input_folder = ""
        self.output_folder = ""
        self.init_ui()

    def init_ui(self):
        """初始化界面"""
        layout = QHBoxLayout(self)

        # 缩放设置
        scale_group = QGroupBox("缩放设置")
        scale_layout = QHBoxLayout()

        scale_layout.addWidget(QLabel("等比例缩放:"))
        self.spin_scale = QSpinBox()
        self.spin_scale.setRange(1, 100)
        self.spin_scale.setValue(50)
        self.spin_scale.setSuffix(" %")
        scale_layout.addWidget(self.spin_scale)

        scale_group.setLayout(scale_layout)
        layout.addWidget(scale_group)

        # 输出格式
        format_group = QGroupBox("输出格式")
        format_layout = QHBoxLayout()

        format_layout.addWidget(QLabel("格式:"))
        self.combo_format = QComboBox()
        self.combo_format.addItems(["PNG", "JPG", "JPEG"])
        self.combo_format.setCurrentText("PNG")
        format_layout.addWidget(self.combo_format)

        format_layout.addWidget(QLabel("质量:"))
        self.spin_quality = QSpinBox()
        self.spin_quality.setRange(1, 100)
        self.spin_quality.setValue(95)
        format_layout.addWidget(self.spin_quality)

        format_group.setLayout(format_layout)
        layout.addWidget(format_group)

        # 文件命名
        naming_group = QGroupBox("文件命名")
        naming_layout = QHBoxLayout()

        naming_layout.addWidget(QLabel("前缀:"))
        self.edit_prefix = QLineEdit("train_")
        self.edit_prefix.setMaximumWidth(100)
        naming_layout.addWidget(self.edit_prefix)

        naming_layout.addWidget(QLabel("起始序号:"))
        self.spin_start = QSpinBox()
        self.spin_start.setRange(0, 99999)
        self.spin_start.setValue(1)
        naming_layout.addWidget(self.spin_start)

        naming_layout.addWidget(QLabel("补零位数:"))
        self.spin_padding = QSpinBox()
        self.spin_padding.setRange(1, 10)
        self.spin_padding.setValue(5)
        naming_layout.addWidget(self.spin_padding)

        naming_group.setLayout(naming_layout)
        layout.addWidget(naming_group)

        # 统计信息
        stats_group = QGroupBox("统计")
        stats_layout = QVBoxLayout()

        self.label_stats = QLabel("已标记保留:  0 / 0")
        self.label_stats.setStyleSheet("font-size: 14px; font-weight: bold;")
        stats_layout.addWidget(self.label_stats)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        layout.addStretch()

    def get_settings(self):
        """获取设置"""
        return {
            'input_folder': self.input_folder,
            'output_folder': self.output_folder,
            'scale_percent': self.spin_scale.value(),
            'output_format': self.combo_format.currentText().lower(),
            'quality': self.spin_quality.value(),
            'prefix': self.edit_prefix.text(),
            'start_number': self.spin_start.value(),
            'padding': self.spin_padding.value()
        }

    def update_stats(self, keep_count, total):
        """更新统计"""
        self.label_stats.setText(f"已标记保留: {keep_count} / {total}")