# openai_wrapper/config/logger.py

import logging
import logging.handlers
import os
from typing import Optional


class LoggerConfig:
    """日志配置类"""

    _instance = None
    _initialized = False

    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化日志配置"""
        if LoggerConfig._initialized:
            return

        LoggerConfig._initialized = True
        self.logger = None
        self._setup_logger()

    def _setup_logger(self):
        """设置日志记录器"""
        # 创建logger
        self.logger = logging.getLogger('openai_wrapper')
        self.logger.setLevel(logging.INFO)

        # 避免重复添加handler
        if self.logger.handlers:
            return

        # 创建日志目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 配置文件处理器 - 按天轮转
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, 'openai_wrapper.log'),
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)

        # 配置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 设置日志格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """获取日志记录器"""
        if cls._instance is None:
            cls()
        return cls._instance.logger

    @classmethod
    def set_level(cls, level: int):
        """设置日志级别"""
        logger = cls.get_logger()
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)