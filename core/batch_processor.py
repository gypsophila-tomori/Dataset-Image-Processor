#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.image_processor import ImageProcessor
from PIL import Image
import os


class BatchProcessor:
    """批量处理器"""

    def __init__(self):
        self.processor = ImageProcessor()
        self.processed_log = []
        self.skipped_log = []

    def process_image(self, input_path, output_folder, prefix, number, padding,
                      scale_percent, rotation, output_format, quality):
        """处理单张图片"""
        try:
            # 加载图片
            image = Image.open(input_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # 旋转
            if rotation != 0:
                image = self.processor.rotate_image(image, rotation)

            # 缩放
            if scale_percent != 100:
                image = self.processor.resize_image(image, scale_percent)

            # 生成输出文件名
            output_filename = f"{prefix}{str(number).zfill(padding)}.{output_format}"
            output_path = os.path.join(output_folder, output_filename)

            # 保存
            success = self.processor.save_image(image, output_path, output_format, quality)

            if success:
                log_entry = (f"{input_path} → {output_filename} → "
                             f"scaled {scale_percent}%, rotated {rotation}°")
                self.processed_log.append(log_entry)
                return True
            else:
                self.skipped_log.append(input_path)
                return False

        except Exception as e:
            print(f"Error processing {input_path}: {e}")
            self.skipped_log.append(f"{input_path} → Error:  {str(e)}")
            return False

    def save_logs(self, output_folder):
        """保存日志文件"""
        # 保存处理日志
        log_path = os.path.join(output_folder, "processed_log.txt")
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("处理日志\n")
            f.write("=" * 80 + "\n\n")
            for entry in self.processed_log:
                f.write(entry + "\n")

        # 保存跳过日志
        if self.skipped_log:
            skip_path = os.path.join(output_folder, "skipped_files.txt")
            with open(skip_path, 'w', encoding='utf-8') as f:
                f.write("跳过的文件\n")
                f.write("=" * 80 + "\n\n")
                for entry in self.skipped_log:
                    f.write(entry + "\n")

        # 清空日志
        self.processed_log.clear()
        self.skipped_log.clear()