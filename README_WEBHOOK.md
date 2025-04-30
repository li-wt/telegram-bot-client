# Webhook实现说明

本文档详细说明了项目中Webhook的实现方式和使用方法。

## 问题背景

在使用传统的轮询方式获取Telegram更新时，可能会遇到以下错误：
```
telegram.error.Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

这个错误发生的原因是多个实例同时尝试轮询同一个机器人的更新。为了解决这个问题，我们实现了两种替代方案：

1. Webhook方案
2. 非轮询客户端方案

## Webhook方案

### 工作原理

1. 设置Webhook URL，让Telegram服务器主动推送更新
2. 本地运行Web服务器接收更新
3. 使用ngrok等工具将本地服务器暴露到公网

### 实现细节

主要实现在 `message_receiver_webhook.py` 中：

1. Web服务器：
   - 使用aiohttp实现异步Web服务器
   - 监听指定端口接收Webhook请求
   - 处理Telegram发送的更新

2. 本地通信：
   - 使用Socket实现本地进程间通信
   - 缓存接收到的更新
   - 提供接口供UI获取更新

### 配置说明

在 `.env` 文件中配置：
```
WEBHOOK_URL=https://your_domain.com/webhook
WEBHOOK_PORT=8443
USE_WEBHOOK=true
```

## 非轮询客户端方案

### 工作原理

1. 主进程负责接收更新
2. 客户端通过本地Socket获取更新
3. 避免多个实例同时轮询

### 实现细节

主要实现在 `telegram_client_no_polling.py` 中：

1. 本地服务器：
   - 使用Socket监听本地端口
   - 接收客户端的更新请求
   - 返回缓存的更新

2. 客户端：
   - 定期连接本地服务器
   - 获取并处理更新
   - 支持多个客户端实例

### 配置说明

在 `.env` 文件中配置：
```
USE_POLLING=false
SOCKET_HOST=127.0.0.1
SOCKET_PORT=65432
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

3. 复制ngrok提供的公网URL，设置为WEBHOOK_URL

4. 运行应用：
   ```bash
   python main_no_polling.py --use-webhook
   ```

## 生产环境

1. 配置域名和SSL证书

2. 设置环境变量：
   ```
   WEBHOOK_URL=https://your_domain.com/webhook
   USE_WEBHOOK=true
   ```

3. 运行应用：
   ```bash
   python main_no_polling.py --use-webhook
   ```

## 故障排除

1. Webhook设置失败：
   - 检查域名和SSL证书
   - 确保端口(8443, 443, 80, 88, 8080)可访问
   - 查看webhook_setup.log日志

2. 更新接收失败：
   - 检查网络连接
   - 确认Webhook URL配置正确
   - 查看telegram_webhook.log日志

3. 本地通信问题：
   - 确保端口65432未被占用
   - 检查防火墙设置
   - 查看应用日志