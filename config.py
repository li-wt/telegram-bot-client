import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Bot配置
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Webhook配置
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '0.0.0.0')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# 本地Socket配置
SOCKET_HOST = os.getenv('SOCKET_HOST', '127.0.0.1')
SOCKET_PORT = int(os.getenv('SOCKET_PORT', '65432'))

# UI配置
UI_UPDATE_INTERVAL = int(os.getenv('UI_UPDATE_INTERVAL', '1000'))  # 毫秒

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'telegram_receiver.log')

# 运行模式配置
USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
USE_POLLING = os.getenv('USE_POLLING', 'true').lower() == 'true'
