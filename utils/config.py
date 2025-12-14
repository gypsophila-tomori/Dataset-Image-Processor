#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os


class Config:
    """配置管理"""

    CONFIG_FILE = "config.json"

    @staticmethod
    def load():
        """加载配置"""
        if os.path.exists(Config.CONFIG_FILE):
            try:
                with open(Config.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}

    @staticmethod
    def save(config):
        """保存配置"""
        try:
            with open(Config.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")