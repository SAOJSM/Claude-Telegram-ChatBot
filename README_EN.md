# Claude Telegram Bot

[中文版 README](README.md)

This is a chatbot project that integrates Claude AI with Telegram, allowing users to have conversations with Claude AI through Telegram.

## Features

- Converse with Claude AI through Telegram
- Display the number of tokens used
- Reset conversations
- Support for Traditional Chinese and English interfaces
- Budget control and token usage limits

## Installation

### Windows Environment

1. Clone this project:
   ```
   git clone https://github.com/SAOJSM/Claude-Telegram-ChatBot.git
   cd Claude-Telegram-ChatBot
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure the `config.ini` file:
   - Enter your Claude API key
   - Enter your Telegram Bot Token
   - Set authorized users' Telegram IDs
   - Adjust other settings (model, token limit, budget, etc.)

### Linux VPS Environment (Ubuntu/Debian)

1. Update the system and install necessary packages:
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git screen
   ```

2. Clone this project:
   ```bash
   git clone https://github.com/SAOJSM/Claude-Telegram-ChatBot.git
   cd Claude-Telegram-ChatBot
   ```

3. Install required Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

4. Configure the `config.ini` file:
   ```bash
   nano config.ini
   ```
   - Enter your Claude API key
   - Enter your Telegram Bot Token
   - Set authorized users' Telegram IDs
   - Adjust other settings (model, token limit, budget, etc.)

5. Create a log directory:
   ```bash
   mkdir -p logs
   ```

## Usage

### Windows Environment

1. Start the bot:
   ```
   python main.py --log-file logs/bot.log
   ```

2. Begin chatting with your bot in Telegram

### Linux VPS Environment

1. Run the bot in the background using Screen (recommended):
   ```bash
   screen -S claude-bot
   python3 main.py --log-file logs/bot.log
   ```

   Press `Ctrl+A` then `D` to detach the screen session, and the bot will continue running in the background.

2. Reconnect to the screen session:
   ```bash
   screen -r claude-bot
   ```

3. View logs:
   ```bash
   tail -f logs/bot.log
   ```

4. Begin chatting with your bot in Telegram

### Available Commands

- `/start` - Start a conversation
- `/help` - Display help message
- `/reset` - Reset the conversation
- `/stats` - Display the number of tokens used and cost

## Configuration Details

In the `config.ini` file, you can set the following parameters:

- `claude_api_key`: Claude API key
- `model`: Claude model to use (e.g., claude-3-opus-20240229, claude-3.5-sonnet-20240620), default is claude-3-5-sonnet-20240620
- `max_requests_per_second`: Maximum requests per second
- `temperature`: Randomness of generated responses (0.0-1.0)
- `telegram_token`: Telegram Bot API Token
- `authorized_users`: Telegram IDs of authorized users (separate multiple IDs with commas)
- `max_tokens`: Token limit per conversation
- `budget_limit`: Budget limit (in USD)
- `language`: Bot language (en or zh-tw)

## Notes

### General Notes
- Keep your Claude API key and Telegram Bot Token confidential
- It's recommended to set authorized users to prevent unauthorized use
- Monitor token usage to control costs

### Linux VPS Notes
- Ensure your VPS has sufficient memory and storage
- It's recommended to use Screen or tmux to run the bot in the background so it continues running after you log out of the VPS
- Regularly check log files to monitor the bot's status
- If your VPS restarts, you'll need to manually restart the bot
- Consider setting up a firewall to allow only necessary connections

### Troubleshooting
- If the bot fails to start, check if the settings in the config.ini file are correct
- If the bot cannot connect to the Telegram API, ensure your VPS can access api.telegram.org
- If the bot cannot connect to the Claude API, ensure your API key is valid and hasn't exceeded usage limits
- Check the log file for more detailed error messages
- If you encounter issues with the bot, please report the error messages from the log as an issue
