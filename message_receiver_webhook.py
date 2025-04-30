import asyncio
import logging
import json
import socket
import pickle
import os
from aiohttp import web
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import threading

# 配置日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='telegram_webhook.log'
)

logger = logging.getLogger(__name__)

# Webhook配置
WEBHOOK_HOST = '0.0.0.0'  # 监听所有网络接口
WEBHOOK_PORT = 8443  # 建议使用443,8443或8080端口
WEBHOOK_URL_PATH = "/telegram_webhook"
WEBHOOK_URL = "https://your_public_domain" + WEBHOOK_URL_PATH  # 替换为你的公网域名

# 本地通信服务器配置
HOST = '127.0.0.1'  # 本地主机
PORT = 65432        # 使用非特权端口

# 存储接收到的更新
updates_buffer = []
updates_lock = threading.Lock()

async def start_command(update, context):
    """处理/start命令"""
    user = update.effective_user
    logger.info(f"用户 {user.id} ({user.first_name}) 发送了 /start 命令")
    await update.message.reply_text(f"您好 {user.first_name}！")
    
    with updates_lock:
        updates_buffer.append(update)

async def help_command(update, context):
    """处理/help命令"""
    logger.info(f"用户 {update.effective_user.id} 发送了 /help 命令")
    await update.message.reply_text(
        "使用指南:\n"
        "1. 发送任何消息给我\n"
        "2. 您可以发送文本、图片或文件\n"
        "3. 您可以在客户端界面回复消息\n\n"
        "命令列表:\n"
        "/start - 开始使用机器人\n"
        "/help - 显示此帮助信息"
    )
    
    with updates_lock:
        updates_buffer.append(update)

async def handle_message(update, context):
    """处理所有类型的消息"""
    with updates_lock:
        updates_buffer.append(update)
    
    logger.info(f"收到消息: {update.message}")
    await update.message.reply_text("收到您的消息！")

async def error_handler(update, context):
    """处理错误"""
    logger.error(f"更新导致错误: {context.error}")

def start_server():
    """启动本地通信服务器"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"本地通信服务器启动在 {HOST}:{PORT}")
        
        while True:
            try:
                conn, addr = s.accept()
                logger.info(f"客户端连接: {addr}")
                
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        
                        command = data.decode('utf-8')
                        
                        if command == "GET_UPDATES":
                            with updates_lock:
                                if updates_buffer:
                                    updates_data = pickle.dumps(updates_buffer)
                                    conn.sendall(updates_data)
                                    updates_buffer.clear()
                                else:
                                    conn.sendall(pickle.dumps([]))
                        else:
                            logger.warning(f"未知命令: {command}")
            except Exception as e:
                logger.error(f"服务器错误: {e}")

class WebhookReceiver:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """设置消息处理器"""
        self.app.add_handler(CommandHandler("start", start_command))
        self.app.add_handler(CommandHandler("help", help_command))
        self.app.add_handler(MessageHandler(filters.ALL, handle_message))
        self.app.add_error_handler(error_handler)
    
    async def webhook_handler(self, request):
        """处理webhook请求"""
        try:
            update = Update.de_json(await request.json(), self.app.bot)
            await self.app.process_update(update)
            return web.Response(text="OK")
        except Exception as e:
            logger.error(f"处理webhook请求时出错: {e}")
            return web.Response(text="Error", status=500)
    
    async def setup_webhook(self, url):
        """设置webhook"""
        await self.app.bot.delete_webhook()
        webhook_info = await self.app.bot.set_webhook(url=url)
        logger.info(f"Webhook设置状态: {webhook_info}")
        return webhook_info
    
    async def run(self, webhook_url=None, host='0.0.0.0', port=8443):
        """运行webhook接收器"""
        if webhook_url:
            await self.setup_webhook(webhook_url)
        
        # 启动本地通信服务器
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # 创建web应用
        app = web.Application()
        app.router.add_post(f"/webhook/{self.token}", self.webhook_handler)
        
        # 启动web服务器
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info(f"Webhook接收器运行在 {host}:{port}")
        
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            logger.info("正在关闭webhook接收器...")
            await runner.cleanup()
            await self.app.bot.delete_webhook()