# Claude Telegram Bot

[English README](README_EN.md)

這是一個整合 Claude AI 與 Telegram 的聊天機器人專案，允許使用者透過 Telegram 與 Claude AI 進行對話。

## 功能

- 透過 Telegram 與 Claude AI 進行對話
- 顯示已使用的 Token 數量
- 重置對話
- 支援繁體中文和英文介面
- 預算控制和 Token 使用限制

## 安裝

### Windows 環境

1. 克隆此專案：
   ```
   git clone https://github.com/SAOJSM/Claude-Telegram-ChatBot.git
   cd Claude-Telegram-ChatBot
   ```

2. 安裝所需套件：
   ```
   pip install -r requirements.txt
   ```

3. 設定 `config.ini` 檔案：
   - 填入您的 Claude API 金鑰
   - 填入您的 Telegram Bot Token
   - 設定授權使用者的 Telegram ID
   - 調整其他設定（模型、Token 上限、預算等）

### Linux VPS 環境 (Ubuntu/Debian)

1. 更新系統並安裝必要的套件：
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git screen
   ```

2. 克隆此專案：
   ```bash
   git clone https://github.com/SAOJSM/Claude-Telegram-ChatBot.git
   cd Claude-Telegram-ChatBot
   ```

3. 安裝所需的 Python 套件：
   ```bash
   pip3 install -r requirements.txt
   ```

4. 設定 `config.ini` 檔案：
   ```bash
   nano config.ini
   ```
   - 填入您的 Claude API 金鑰
   - 填入您的 Telegram Bot Token
   - 設定授權使用者的 Telegram ID
   - 調整其他設定（模型、Token 上限、預算等）

5. 創建日誌目錄：
   ```bash
   mkdir -p logs
   ```

## 使用方法

### Windows 環境

1. 啟動機器人：
   ```
   python main.py --log-file logs/bot.log
   ```

2. 在 Telegram 中與您的機器人開始對話

### Linux VPS 環境

1. 使用 Screen 在背景運行機器人（推薦）：
   ```bash
   screen -S claude-bot
   python3 main.py --log-file logs/bot.log
   ```

   按下 `Ctrl+A` 然後按 `D` 來分離 screen 會話，機器人將繼續在背景運行。

2. 重新連接到 screen 會話：
   ```bash
   screen -r claude-bot
   ```

3. 查看日誌：
   ```bash
   tail -f logs/bot.log
   ```

4. 在 Telegram 中與您的機器人開始對話

### 可用指令

- `/start` - 開始對話
- `/help` - 顯示幫助訊息
- `/reset` - 重置對話
- `/stats` - 顯示已使用的 Token 數量和成本

## 配置說明

在 `config.ini` 檔案中，您可以設定以下參數：

- `claude_api_key`: Claude API 金鑰
- `model`: 使用的 Claude 模型（例如：claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307, claude-3-5-sonnet-20240620, claude-opus-4-20250514, claude-sonnet-4-20250514），預設是 claude-3-5-sonnet-20240620
- `max_requests_per_second`: 每秒最大請求數
- `temperature`: 生成回應的隨機性（0.0-1.0）
- `telegram_token`: Telegram Bot API Token
- `authorized_users`: 授權使用者的 Telegram ID（多個 ID 請用逗號分隔）
- `max_tokens`: 每次對話的 Token 上限
- `budget_limit`: 預算上限（美元）
- `language`: 機器人語言（en 或 zh-tw）

## 注意事項

### 一般注意事項
- 請確保您的 Claude API 金鑰和 Telegram Bot Token 保密
- 建議設定授權使用者，以防止未授權使用
- 監控 Token 使用情況，以控制成本

### Linux VPS 注意事項
- 確保您的 VPS 有足夠的記憶體和儲存空間
- 建議使用 Screen 或 tmux 在背景運行機器人，以便在您登出 VPS 後機器人仍能繼續運行
- 定期檢查日誌檔案，以監控機器人的運行狀態
- 如果您的 VPS 重新啟動，您需要手動重新啟動機器人
- 考慮設定防火牆，只允許必要的連接

### 故障排除
- 如果機器人無法啟動，請檢查 config.ini 檔案中的設定是否正確
- 如果機器人無法連接到 Telegram API，請確保您的 VPS 可以訪問 api.telegram.org
- 如果機器人無法連接到 Claude API，請確保您的 API 金鑰有效且未超出使用限制
- 查看日誌檔案以獲取更詳細的錯誤訊息
- 如果機器人執行上有問題，請直接將log中的錯誤訊息以issue回報
