import logging
import sys
import os
import argparse
from logging.handlers import RotatingFileHandler
from config_manager import ConfigManager
from claude_api import ClaudeAPI
from telegram_bot import TelegramBot

# 解析命令行參數
parser = argparse.ArgumentParser(description='Claude Telegram Bot')
parser.add_argument('--log-file', dest='log_file', default='bot.log',
                    help='日誌檔案路徑 (預設: bot.log)')
parser.add_argument('--log-level', dest='log_level', default='INFO',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help='日誌級別 (預設: INFO)')
parser.add_argument('--config', dest='config_file', default='config.ini',
                    help='配置檔案路徑 (預設: config.ini)')
args = parser.parse_args()

# 確保日誌目錄存在
log_dir = os.path.dirname(os.path.abspath(args.log_file))
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 設定日誌
log_level = getattr(logging, args.log_level)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 控制台處理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

# 檔案處理器 (使用 RotatingFileHandler 以避免日誌檔案過大)
file_handler = RotatingFileHandler(
    args.log_file, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
)
file_handler.setFormatter(log_formatter)

# 設定根日誌記錄器
root_logger = logging.getLogger()
root_logger.setLevel(log_level)
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

def main():
    """
    主函數，初始化並啟動機器人
    """
    try:
        # 初始化配置管理器
        logger.info("初始化配置管理器...")
        config_manager = ConfigManager(args.config_file)

        # 初始化 Claude API
        logger.info("初始化 Claude API...")
        claude_api = ClaudeAPI(config_manager)

        # 初始化 Telegram 機器人
        logger.info("初始化 Telegram 機器人...")
        telegram_bot = TelegramBot(config_manager, claude_api)

        # 啟動機器人
        logger.info("啟動機器人...")
        telegram_bot.start()

    except KeyboardInterrupt:
        logger.info("接收到中斷信號，正在關閉...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"發生錯誤: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
