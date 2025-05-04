import configparser
import os
import sys

class ConfigManager:
    """
    配置管理器類，用於讀取和驗證配置檔案
    """

    def __init__(self, config_file='config.ini'):
        """
        初始化配置管理器

        Args:
            config_file (str): 配置檔案路徑
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()

        # 檢查配置檔案是否存在
        if not os.path.exists(config_file):
            print(f"錯誤：找不到配置檔案 '{config_file}'")
            sys.exit(1)

        # 讀取配置檔案
        self.config.read(config_file, encoding='utf-8')

        # 驗證必要的配置項
        self._validate_config()

    def _validate_config(self):
        """
        驗證配置檔案中的必要項目
        """
        required_sections = {
            'API': ['claude_api_key', 'model', 'max_requests_per_second', 'temperature'],
            'TELEGRAM': ['telegram_token', 'authorized_users'],
            'LIMITS': ['max_tokens', 'budget_limit'],
            'BOT': ['language']
        }

        for section, keys in required_sections.items():
            if not self.config.has_section(section):
                print(f"錯誤：配置檔案缺少 '{section}' 部分")
                sys.exit(1)

            for key in keys:
                if not self.config.has_option(section, key):
                    print(f"錯誤：配置檔案缺少 '{section}.{key}' 設定")
                    sys.exit(1)

                # 檢查值是否為空
                if not self.config.get(section, key).strip():
                    print(f"錯誤：'{section}.{key}' 設定值不能為空")
                    sys.exit(1)

        # 檢查 API 金鑰是否為預設值
        if self.get_claude_api_key() == 'your_claude_api_key_here':
            print("錯誤：請在配置檔案中設定您的 Claude API 金鑰")
            sys.exit(1)

        # 檢查 Telegram Token 是否為預設值
        if self.get_telegram_token() == 'your_telegram_token_here':
            print("錯誤：請在配置檔案中設定您的 Telegram Bot Token")
            sys.exit(1)

        # 驗證數值型配置
        try:
            float(self.config.get('API', 'temperature'))
            float(self.config.get('LIMITS', 'budget_limit'))
            float(self.config.get('API', 'max_requests_per_second'))
            int(self.config.get('LIMITS', 'max_tokens'))
        except ValueError:
            print("錯誤：數值型配置項必須為有效數字")
            sys.exit(1)

        # 驗證 temperature 範圍
        temp = float(self.config.get('API', 'temperature'))
        if temp < 0.0 or temp > 1.0:
            print("錯誤：temperature 必須在 0.0 到 1.0 之間")
            sys.exit(1)

    def get_claude_api_key(self):
        """
        獲取 Claude API 金鑰

        Returns:
            str: Claude API 金鑰
        """
        return self.config.get('API', 'claude_api_key')

    def get_model(self):
        """
        獲取使用的 Claude 模型

        Returns:
            str: Claude 模型名稱
        """
        return self.config.get('API', 'model')

    def get_max_requests_per_second(self):
        """
        獲取每秒最大請求數

        Returns:
            float: 每秒最大請求數
        """
        return self.config.getfloat('API', 'max_requests_per_second')

    def get_temperature(self):
        """
        獲取 temperature 設定

        Returns:
            float: Temperature 值
        """
        return self.config.getfloat('API', 'temperature')

    def get_telegram_token(self):
        """
        獲取 Telegram Bot Token

        Returns:
            str: Telegram Bot Token
        """
        return self.config.get('TELEGRAM', 'telegram_token')

    def get_authorized_users(self):
        """
        獲取授權使用者的 Telegram ID 列表

        Returns:
            list: 授權使用者 ID 列表
        """
        users = self.config.get('TELEGRAM', 'authorized_users')
        return [int(user.strip()) for user in users.split(',') if user.strip()]

    def get_max_tokens(self):
        """
        獲取 Token 上限

        Returns:
            int: Token 上限
        """
        return self.config.getint('LIMITS', 'max_tokens')

    def get_budget_limit(self):
        """
        獲取預算上限

        Returns:
            float: 預算上限（美元）
        """
        return self.config.getfloat('LIMITS', 'budget_limit')

    def get_language(self):
        """
        獲取機器人語言設定

        Returns:
            str: 語言設定 (en 或 zh-tw)
        """
        return self.config.get('BOT', 'language')
