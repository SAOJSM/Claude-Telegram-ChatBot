import telebot
import logging
import time
from telebot import types

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class TelegramBot:
    """
    Telegram 機器人類，處理與 Telegram 的通信
    """

    def __init__(self, config_manager, claude_api):
        """
        初始化 Telegram 機器人

        Args:
            config_manager: 配置管理器實例
            claude_api: Claude API 處理器實例
        """
        self.config = config_manager
        self.claude_api = claude_api
        self.bot = telebot.TeleBot(config_manager.get_telegram_token())
        self.authorized_users = config_manager.get_authorized_users()
        self.language = config_manager.get_language()

        # 設定多語言文本
        self.texts = self._setup_texts()

        # 設定命令處理器
        self._setup_handlers()

    def _setup_texts(self):
        """
        設定多語言文本

        Returns:
            dict: 包含不同語言文本的字典
        """
        texts = {
            'zh-tw': {
                'welcome': '歡迎使用 Claude AI 聊天機器人！\n\n您可以直接發送消息與 Claude AI 對話。\n\n可用命令：\n/start - 開始對話\n/help - 顯示幫助訊息\n/reset - 重置對話\n/stats - 顯示已使用的 Token 數量和成本',
                'help': '您可以直接發送消息與 Claude AI 對話。\n\n可用命令：\n/start - 開始對話\n/help - 顯示幫助訊息\n/reset - 重置對話\n/stats - 顯示已使用的 Token 數量和成本',
                'reset': '對話已重置。',
                'unauthorized': '抱歉，您未被授權使用此機器人。',
                'thinking': '思考中...',
                'token_usage': '已使用的 Token：\n輸入：{input_tokens}\n輸出：{output_tokens}\n總計：{total_tokens}\n估計成本：${total_cost:.4f}'
            },
            'en': {
                'welcome': 'Welcome to Claude AI Chat Bot!\n\nYou can send messages directly to chat with Claude AI.\n\nAvailable commands:\n/start - Start conversation\n/help - Show help message\n/reset - Reset conversation\n/stats - Show token usage and cost',
                'help': 'You can send messages directly to chat with Claude AI.\n\nAvailable commands:\n/start - Start conversation\n/help - Show help message\n/reset - Reset conversation\n/stats - Show token usage and cost',
                'reset': 'Conversation has been reset.',
                'unauthorized': 'Sorry, you are not authorized to use this bot.',
                'thinking': 'Thinking...',
                'token_usage': 'Token usage:\nInput: {input_tokens}\nOutput: {output_tokens}\nTotal: {total_tokens}\nEstimated cost: ${total_cost:.4f}'
            }
        }

        # 如果語言設定不存在，使用英文
        if self.language not in texts:
            logger.warning(f"未知語言 '{self.language}'，使用英文")
            return texts['en']

        return texts[self.language]

    def _setup_handlers(self):
        """
        設定 Telegram 命令處理器
        """
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            """處理 /start 命令"""
            if not self._is_authorized(message.from_user.id):
                self.bot.reply_to(message, self.texts['unauthorized'])
                return

            self.bot.reply_to(message, self.texts['welcome'])

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            """處理 /help 命令"""
            if not self._is_authorized(message.from_user.id):
                self.bot.reply_to(message, self.texts['unauthorized'])
                return

            self.bot.reply_to(message, self.texts['help'])

        @self.bot.message_handler(commands=['reset'])
        def handle_reset(message):
            """處理 /reset 命令"""
            if not self._is_authorized(message.from_user.id):
                self.bot.reply_to(message, self.texts['unauthorized'])
                return

            self.claude_api.reset_conversation()
            self.bot.reply_to(message, self.texts['reset'])

        @self.bot.message_handler(commands=['stats'])
        def handle_stats(message):
            """處理 /stats 命令"""
            if not self._is_authorized(message.from_user.id):
                self.bot.reply_to(message, self.texts['unauthorized'])
                return

            # 獲取本地記錄的 token 使用情況
            usage = self.claude_api.get_token_usage()
            token_message = self.texts['token_usage'].format(
                input_tokens=usage['input_tokens'],
                output_tokens=usage['output_tokens'],
                total_tokens=usage['total_tokens'],
                total_cost=usage['total_cost']
            )
            self.bot.reply_to(message, token_message)

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            """處理一般消息"""
            if not self._is_authorized(message.from_user.id):
                self.bot.reply_to(message, self.texts['unauthorized'])
                return

            # 顯示「思考中」狀態
            thinking_message = self.bot.reply_to(message, self.texts['thinking'])

            # 發送消息到 Claude API
            response_text, token_usage = self.claude_api.send_message(message.text)

            # 刪除「思考中」消息
            self.bot.delete_message(message.chat.id, thinking_message.message_id)

            # 發送回應
            self.bot.reply_to(message, response_text)

            # 如果獲取到 Token 使用情況，顯示在日誌中
            if token_usage:
                logger.info(f"Token usage: Input={token_usage['input_tokens']}, Output={token_usage['output_tokens']}, Cost=${token_usage['cost']:.4f}")

    def _is_authorized(self, user_id):
        """
        檢查用戶是否被授權使用機器人

        Args:
            user_id (int): Telegram 用戶 ID

        Returns:
            bool: 如果用戶被授權則返回 True，否則返回 False
        """
        # 如果沒有設定授權用戶，則允許所有用戶
        if not self.authorized_users:
            return True

        return user_id in self.authorized_users

    def start(self):
        """
        啟動 Telegram 機器人
        """
        logger.info("啟動 Telegram 機器人...")
        self.bot.infinity_polling()
