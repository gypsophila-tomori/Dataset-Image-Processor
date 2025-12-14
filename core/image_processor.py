#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os


class ImageProcessor:
    """图片处理器"""

    @staticmethod
    def resize_image(image, scale_percent):
        """等比例缩放图片"""
        width, height = image.size
        new_width = int(width * scale_percent / 100)
        new_height = int(height * scale_percent / 100)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    @staticmethod
    def rotate_image(image, angle):
        """旋转图片"""
        if angle == 0:
            return image
        return image.rotate(-angle, expand=True)

    @staticmethod
    def save_image(image, output_path, format='png', quality=95):
        """保存图片"""
        try:
            if format.lower() in ['jpg', 'jpeg']:
                image.save(output_path, 'JPEG', quality=quality)
            else:
                image.save(output_path, format.upper())
            return True
        except Exception as e:
            print(f"Error saving image {output_path}: {e}")
            return False