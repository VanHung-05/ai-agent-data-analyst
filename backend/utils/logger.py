"""
📋 logger.py — Cấu hình Logging chung cho Backend
====================================================
Sử dụng: from utils.logger import logger
"""

import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import app_config


def setup_logger(name: str = "ai-agent") -> logging.Logger:
    """Tạo logger với format chuẩn"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, app_config.log_level.upper(), logging.INFO))

    # Tránh duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Format
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Logger mặc định — import trực tiếp
logger = setup_logger()
