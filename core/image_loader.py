#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from PyQt5.QtGui import QPixmap, QImage
import os


class ImageLoader:
    """图片加载器"""

    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '. bmp', '.tiff', '.webp')
    THUMBNAIL_SIZE = (160, 160)

    def __init__(self):
        self.thumbnail_cache = {}

    def scan_folder(self, folder):
        """扫描文件夹，返回所有图片路径"""
        image_files = []

        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(self.SUPPORTED_FORMATS):
                    image_files.append(os.path.join(root, file))

        return sorted(image_files)

    def load_image(self, path):
        """加载图片"""
        try:
            image = Image.open(path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def get_thumbnail(self, path):
        """获取缩略图"""
        if path in self.thumbnail_cache:
            return self.thumbnail_cache[path]

        try:
            image = Image.open(path)
            image.thumbnail(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)

            # 转换为QPixmap
            if image.mode != 'RGB':
                image = image.convert('RGB')

            img_data = image.tobytes("raw", "RGB")
            qimage = QImage(img_data, image.width, image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)

            self.thumbnail_cache[path] = pixmap
            return pixmap

        except Exception as e:
            print(f"Error creating thumbnail for {path}: {e}")
            # 返回默认缩略图
            return QPixmap(160, 160)

    def clear_cache(self):
        """清空缓存"""
        self.thumbnail_cache.clear()