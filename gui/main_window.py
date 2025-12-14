#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QFileDialog, QMessageBox, QSplitter,
                             QProgressDialog, QLabel)
from PyQt5.QtCore import Qt, QSettings
from gui.thumbnail_view import ThumbnailView
from gui.preview_panel import PreviewPanel
from gui.settings_panel import SettingsPanel
from core.image_loader import ImageLoader
from core.batch_processor import BatchProcessor
from utils.config import Config
import os


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.image_loader = ImageLoader()
        self.batch_processor = BatchProcessor()
        self.current_index = -1
        self.images_data = []  # [{path, keep, rotation}, ...]

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("Dataset Image Processor")
        self.setGeometry(100, 100, 1400, 900)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 顶部工具栏
        toolbar_layout = QHBoxLayout()

        self.btn_input = QPushButton("选择输入文件夹")
        self.btn_input.clicked.connect(self.select_input_folder)
        toolbar_layout.addWidget(self.btn_input)

        self.btn_output = QPushButton("选择输出文件夹")
        self.btn_output.clicked.connect(self.select_output_folder)
        toolbar_layout.addWidget(self.btn_output)

        toolbar_layout.addStretch()

        self.btn_process = QPushButton("开始批量处理")
        self.btn_process.clicked.connect(self.start_batch_process)
        self.btn_process.setEnabled(False)
        self.btn_process.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        toolbar_layout.addWidget(self.btn_process)

        main_layout.addLayout(toolbar_layout)

        # 路径显示
        path_layout = QHBoxLayout()
        self.label_input_path = QLabel("输入路径:  未选择")
        self.label_output_path = QLabel("输出路径: 未选择")
        path_layout.addWidget(self.label_input_path)
        path_layout.addWidget(self.label_output_path)
        main_layout.addLayout(path_layout)

        # 分割器：左边缩略图，右边预览
        splitter = QSplitter(Qt.Horizontal)

        # 左侧：缩略图视图
        self.thumbnail_view = ThumbnailView()
        self.thumbnail_view.image_selected.connect(self.on_image_selected)
        splitter.addWidget(self.thumbnail_view)

        # 右侧：预览面板
        self.preview_panel = PreviewPanel()
        self.preview_panel.keep_changed.connect(self.on_keep_changed)
        self.preview_panel.rotation_changed.connect(self.on_rotation_changed)
        self.preview_panel.navigate.connect(self.navigate_image)
        splitter.addWidget(self.preview_panel)

        splitter.setSizes([400, 1000])
        main_layout.addWidget(splitter)

        # 底部：设置面板
        self.settings_panel = SettingsPanel()
        main_layout.addWidget(self.settings_panel)

        # 状态栏
        self.statusBar().showMessage("就绪")

    def select_input_folder(self):
        """选择输入文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if folder:
            self.label_input_path.setText(f"输入路径: {folder}")
            self.load_images(folder)
            self.settings_panel.input_folder = folder
            self.check_ready_to_process()

    def select_output_folder(self):
        """选择输出文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder:
            self.label_output_path.setText(f"输出路径:  {folder}")
            self.settings_panel.output_folder = folder
            self.check_ready_to_process()

    def load_images(self, folder):
        """加载图片"""
        self.statusBar().showMessage("正在加载图片...")

        # 加载图片列表
        image_files = self.image_loader.scan_folder(folder)

        if not image_files:
            QMessageBox.warning(self, "警告", "未找到任何图片文件！")
            return

        # 初始化图片数据
        self.images_data = [
            {'path': img, 'keep': True, 'rotation': 0}
            for img in image_files
        ]

        # 生成缩略图
        progress = QProgressDialog("正在生成缩略图...", "取消", 0, len(image_files), self)
        progress.setWindowModality(Qt.WindowModal)

        thumbnails = []
        for i, img_path in enumerate(image_files):
            if progress.wasCanceled():
                break
            thumb = self.image_loader.get_thumbnail(img_path)
            thumbnails.append(thumb)
            progress.setValue(i + 1)

        progress.close()

        # 更新缩略图视图
        self.thumbnail_view.set_images(thumbnails, self.images_data)

        # 显示第一张
        if self.images_data:
            self.current_index = 0
            self.show_current_image()

        self.update_status()
        self.statusBar().showMessage(f"已加载 {len(image_files)} 张图片")

    def show_current_image(self):
        """显示当前图片"""
        if 0 <= self.current_index < len(self.images_data):
            data = self.images_data[self.current_index]
            image = self.image_loader.load_image(data['path'])

            self.preview_panel.set_image(
                image,
                data['path'],
                data['keep'],
                data['rotation'],
                self.current_index,
                len(self.images_data)
            )

            self.thumbnail_view.set_current_index(self.current_index)

    def on_image_selected(self, index):
        """缩略图被选中"""
        self.current_index = index
        self.show_current_image()

    def on_keep_changed(self, keep):
        """保留状态改变"""
        if 0 <= self.current_index < len(self.images_data):
            self.images_data[self.current_index]['keep'] = keep
            self.thumbnail_view.update_keep_status(self.current_index, keep)
            self.update_status()

    def on_rotation_changed(self, rotation):
        """旋转角度改变"""
        if 0 <= self.current_index < len(self.images_data):
            self.images_data[self.current_index]['rotation'] = rotation

    def navigate_image(self, direction):
        """导航图片"""
        if direction == 'prev' and self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()
        elif direction == 'next' and self.current_index < len(self.images_data) - 1:
            self.current_index += 1
            self.show_current_image()

    def update_status(self):
        """更新状态"""
        keep_count = sum(1 for img in self.images_data if img['keep'])
        self.settings_panel.update_stats(keep_count, len(self.images_data))

    def check_ready_to_process(self):
        """检查是否可以开始处理"""
        ready = (bool(self.settings_panel.input_folder) and
                 bool(self.settings_panel.output_folder) and
                 len(self.images_data) > 0)
        self.btn_process.setEnabled(ready)

    def start_batch_process(self):
        """开始批量处理"""
        # 获取设置
        settings = self.settings_panel.get_settings()

        # 过滤保留的图片
        images_to_process = [img for img in self.images_data if img['keep']]

        if not images_to_process:
            QMessageBox.warning(self, "警告", "没有标记为保留的图片！")
            return

        # 确认对话框
        reply = QMessageBox.question(
            self,
            "确认处理",
            f"将处理 {len(images_to_process)} 张图片，是否继续？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # 进度对话框
        progress = QProgressDialog("正在处理图片...", "取消", 0, len(images_to_process), self)
        progress.setWindowModality(Qt.WindowModal)

        # 批量处理
        success_count = 0
        for i, img_data in enumerate(images_to_process):
            if progress.wasCanceled():
                break

            success = self.batch_processor.process_image(
                img_data['path'],
                settings['output_folder'],
                settings['prefix'],
                settings['start_number'] + i,
                settings['padding'],
                settings['scale_percent'],
                img_data['rotation'],
                settings['output_format'],
                settings['quality']
            )

            if success:
                success_count += 1

            progress.setValue(i + 1)

        progress.close()

        # 生成日志
        self.batch_processor.save_logs(settings['output_folder'])

        # 完成提示
        QMessageBox.information(
            self,
            "处理完成",
            f"成功处理 {success_count}/{len(images_to_process)} 张图片！\n\n"
            f"输出路径: {settings['output_folder']}\n"
            f"日志文件: processed_log.txt, skipped_files.txt"
        )

        self.statusBar().showMessage(f"处理完成:  {success_count}/{len(images_to_process)} 张图片")

    def load_settings(self):
        """加载设置"""
        settings = QSettings("DatasetTools", "ImageProcessor")
        # 可以在这里恢复窗口大小、上次使用的路径等

    def save_settings(self):
        """保存设置"""
        settings = QSettings("DatasetTools", "ImageProcessor")
        # 保存设置

    def closeEvent(self, event):
        """关闭事件"""
        self.save_settings()
        event.accept()