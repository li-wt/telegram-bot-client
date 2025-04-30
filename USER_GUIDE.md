# Telegram客户端使用指南

本指南将帮助您了解如何安装、配置和使用Telegram客户端。

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/your-username/telegram-bot-client.git
cd telegram-bot-client
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 复制环境变量模板：
```bash
cp env.example .env
```

2. 编辑 `.env` 文件，设置以下参数：
```
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your_domain.com/webhook
WEBHOOK_PORT=8443
LOG_LEVEL=INFO
```

## 运行模式

### 1. Webhook模式（推荐）

适用于有公网域名的环境：

```bash
python main_no_polling.py --use-webhook
```

或使用批处理脚本：
```bash
run_webhook_mode.bat
```

### 2. 非轮询模式

适用于本地开发环境：

```bash
python main_no_polling.py --no-polling
```

或使用批处理脚本：
```bash
run_nopolling_mode.bat
```

## 本地开发

1. 安装ngrok：
```bash
pip install ngrok
```

2. 启动ngrok：
```bash
ngrok http 8443
```

3. 复制ngrok提供的URL到 `.env` 文件：
```
WEBHOOK_URL=https://xxxx.ngrok.io/webhook
```

## 常见问题

### 1. 轮询冲突

如果遇到以下错误：
```
telegram.error.Conflict: terminated by other getUpdates request
```

解决方案：
- 使用Webhook模式
- 或使用非轮询模式

### 2. Webhook设置失败

检查：
- 域名是否配置正确
- SSL证书是否有效
- 端口是否开放（8443, 443, 80, 88, 8080）

### 3. 更新接收失败

检查：
- 网络连接
- Webhook URL配置
- 查看日志文件

## 日志文件

- `telegram_receiver.log`: 主程序日志
- `telegram_webhook.log`: Webhook相关日志

## 更多信息

- 查看 `README_WEBHOOK.md` 了解Webhook实现细节
- 查看 `DEVELOPMENT.md` 了解开发指南