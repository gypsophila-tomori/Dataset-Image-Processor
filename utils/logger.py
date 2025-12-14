#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime


class Logger:
    """日志记录器"""

    @staticmethod
    def setup(log_folder="logs"):
        """设置日志"""
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file = os.path.join(log_folder, f"app_{datetime.now().strftime('%Y%m%d')}.log")

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def info(message):
        """信息日志"""
        logging.info(message)

    @staticmethod
    def error(message):
        """错误日志"""
        logging.error(message)