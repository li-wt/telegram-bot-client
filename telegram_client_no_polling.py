import asyncio
import logging
import socket
import pickle
from telegram import Bot
from config import BOT_TOKEN, SOCKET_HOST, SOCKET_PORT

class TelegramClientNoPolling:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)
        self.logger = logging.getLogger(__name__)
        self.socket_host = SOCKET_HOST
        self.socket_port = SOCKET_PORT
        self.running = False
        self.update_handlers = []

    def add_update_handler(self, handler):
        """添加更新处理器"""
        self.update_handlers.append(handler)

    async def connect_to_server(self):
        """连接到本地通信服务器"""
        try:
            reader, writer = await asyncio.open_connection(
                self.socket_host, self.socket_port)
            return reader, writer
        except Exception as e:
            self.logger.error(f"连接服务器失败: {e}")
            return None, None

    async def get_updates(self):
        """从本地服务器获取更新"""
        try:
            reader, writer = await self.connect_to_server()
            if not reader or not writer:
                return []

            try:
                # 发送获取更新的命令
                writer.write(b"GET_UPDATES")
                await writer.drain()

                # 接收响应
                data = await reader.read(4096)
                if data:
                    updates = pickle.loads(data)
                    return updates
                return []

            finally:
                writer.close()
                await writer.wait_closed()

        except Exception as e:
            self.logger.error(f"获取更新失败: {e}")
            return []

    async def process_updates(self, updates):
        """处理更新"""
        for update in updates:
            for handler in self.update_handlers:
                try:
                    await handler(update)
                except Exception as e:
                    self.logger.error(f"处理更新时出错: {e}")

    async def run(self):
        """运行客户端"""
        self.running = True
        self.logger.info("非轮询客户端启动")

        while self.running:
            try:
                updates = await self.get_updates()
                if updates:
                    await self.process_updates(updates)
                await asyncio.sleep(1)  # 避免过于频繁的请求

            except asyncio.CancelledError:
                self.logger.info("客户端被取消")
                break
            except Exception as e:
                self.logger.error(f"运行时出错: {e}")
                await asyncio.sleep(5)  # 出错后等待一段时间再重试

        self.logger.info("非轮询客户端停止")

    def stop(self):
        """停止客户端"""
        self.running = False
        self.logger.info("正在停止非轮询客户端...")