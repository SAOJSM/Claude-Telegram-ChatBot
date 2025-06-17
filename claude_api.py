import time
import anthropic
from anthropic.types import MessageParam
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class ClaudeAPI:
    """
    Claude API 處理類，負責與 Claude API 通信
    """

    def __init__(self, config_manager):
        """
        初始化 Claude API 處理器

        Args:
            config_manager: 配置管理器實例
        """
        self.config = config_manager
        self.api_key = config_manager.get_claude_api_key()
        self.model = config_manager.get_model()
        self.max_tokens = config_manager.get_max_tokens()
        self.temperature = config_manager.get_temperature()
        self.max_requests_per_second = config_manager.get_max_requests_per_second()
        self.budget_limit = config_manager.get_budget_limit()

        # 初始化 Anthropic 客戶端
        self.client = anthropic.Anthropic(api_key=self.api_key)

        # 追蹤 Token 使用情況
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0

        # 存儲對話歷史
        self.conversation_history = []

        # 設定語言
        self.language = config_manager.get_language()

        # 設定費率（根據不同模型）
        self.pricing = self._get_model_pricing()

        # 請求時間控制
        self.last_request_time = 0

    def _get_model_pricing(self):
        """
        獲取模型的費率

        Returns:
            dict: 包含輸入和輸出 Token 費率的字典
        """
        # 根據模型名稱設定費率（美元/1K tokens）
        pricing_table = {
            'claude-3-opus-20240229': {'input': 0.015, 'output': 0.075},
            'claude-3-sonnet-20240229': {'input': 0.003, 'output': 0.015},
            'claude-3-haiku-20240307': {'input': 0.00025, 'output': 0.00125},
            'claude-3-5-sonnet-20240620': {'input': 0.003, 'output': 0.015},
            'claude-opus-4-20250514': {'input': 0.015, 'output': 0.075},  # 新增 Opus 4 模型
            'claude-sonnet-4-20250514': {'input': 0.003, 'output': 0.015},  # 新增 Sonnet 4 模型
            # 可以根據需要添加更多模型
        }

        if self.model in pricing_table:
            return pricing_table[self.model]
        else:
            # 預設費率（使用 Sonnet 的費率）
            logger.warning(f"未知模型 '{self.model}'，使用預設費率")
            return {'input': 0.003, 'output': 0.015}

    def _calculate_cost(self, input_tokens, output_tokens):
        """
        計算 API 請求的成本

        Args:
            input_tokens (int): 輸入 Token 數量
            output_tokens (int): 輸出 Token 數量

        Returns:
            float: 請求成本（美元）
        """
        input_cost = (input_tokens / 1000) * self.pricing['input']
        output_cost = (output_tokens / 1000) * self.pricing['output']
        return input_cost + output_cost

    def _rate_limit(self):
        """
        實現請求頻率限制
        """
        if self.max_requests_per_second <= 0:
            return

        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        min_interval = 1.0 / self.max_requests_per_second

        if time_since_last_request < min_interval:
            sleep_time = min_interval - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def _check_budget(self, estimated_cost):
        """
        檢查是否超出預算限制

        Args:
            estimated_cost (float): 估計的請求成本

        Returns:
            bool: 如果未超出預算則返回 True，否則返回 False
        """
        if self.total_cost + estimated_cost > self.budget_limit:
            return False
        return True

    def reset_conversation(self):
        """
        重置對話歷史
        """
        self.conversation_history = []

    def get_token_usage(self):
        """
        獲取 Token 使用情況

        Returns:
            dict: 包含 Token 使用情況的字典
        """
        return {
            'input_tokens': self.total_input_tokens,
            'output_tokens': self.total_output_tokens,
            'total_tokens': self.total_input_tokens + self.total_output_tokens,
            'total_cost': self.total_cost
        }

    def send_message(self, user_message):
        """
        發送消息到 Claude API

        Args:
            user_message (str): 用戶消息

        Returns:
            tuple: (回應文本, Token 使用情況)
        """
        # 實現請求頻率限制
        self._rate_limit()

        # 準備消息
        messages = self._prepare_messages(user_message)

        try:
            # 發送請求到 Claude API（使用串流模式）
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=messages
            ) as stream:
                response_text = ""
                for text in stream.text_stream:
                    response_text += text

                # 獲取完整的回應
                response = stream.get_final_message()

            # 更新 Token 使用情況
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens

            # 計算成本
            cost = self._calculate_cost(input_tokens, output_tokens)
            self.total_cost += cost

            # 更新對話歷史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": response_text})

            # 返回回應和 Token 使用情況
            token_usage = {
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': input_tokens + output_tokens,
                'cost': cost
            }

            return response_text, token_usage

        except Exception as e:
            logger.error(f"Claude API 請求失敗: {str(e)}")

            # 根據語言返回錯誤消息
            if self.language == 'zh-tw':
                return f"抱歉，與 Claude API 通信時發生錯誤: {str(e)}", None
            else:
                return f"Sorry, an error occurred while communicating with the Claude API: {str(e)}", None

    def _prepare_messages(self, user_message):
        """
        準備發送到 Claude API 的消息

        Args:
            user_message (str): 用戶消息

        Returns:
            list: 消息列表
        """
        messages = []

        # 添加對話歷史
        for message in self.conversation_history:
            messages.append(MessageParam(role=message["role"], content=message["content"]))

        # 添加當前用戶消息
        messages.append(MessageParam(role="user", content=user_message))

        return messages
