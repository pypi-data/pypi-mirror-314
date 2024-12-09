import configparser
import logging
import os
import sys

from ..utils.logger import Logging

Logging()


def load_config(configPath):
    config_path = os.path.join(configPath)

    # 确认文件存在
    if os.path.exists(config_path):
        # 读取配置文件
        config = configparser.ConfigParser()
        with open(config_path, 'r', encoding='utf-8') as f:  # 指定编码为 UTF-8
            config.read_file(f)
        return config
    else:
        logging.error(f"Config file does not exist at: {config_path}")
        sys.exit("1")
