import asyncio
import logging
import argparse
from message_receiver_webhook import WebhookReceiver
from telegram_client_no_polling import TelegramClientNoPolling
from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PORT

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='telegram_receiver.log'
)

logger = logging.getLogger(__name__)

async def run_webhook_mode():
    """运行Webhook模式"""
    try:
        receiver = WebhookReceiver(BOT_TOKEN)
        await receiver.run(
            webhook_url=WEBHOOK_URL,
            host='0.0.0.0',
            port=WEBHOOK_PORT
        )
    except Exception as e:
        logger.error(f"Webhook模式运行失败: {e}")
        raise

async def run_no_polling_mode():
    """运行非轮询模式"""
    try:
        client = TelegramClientNoPolling()
        
        # 添加消息处理器
        async def message_handler(update):
            if update.message:
                logger.info(f"收到消息: {update.message.text}")
        
        client.add_update_handler(message_handler)
        await client.run()
        
    except Exception as e:
        logger.error(f"非轮询模式运行失败: {e}")
        raise

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Telegram客户端')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--use-webhook', action='store_true', help='使用Webhook模式')
    group.add_argument('--no-polling', action='store_true', help='使用非轮询模式')
    
    args = parser.parse_args()
    
    try:
        if args.use_webhook:
            logger.info("启动Webhook模式...")
            asyncio.run(run_webhook_mode())
        elif args.no_polling:
            logger.info("启动非轮询模式...")
            asyncio.run(run_no_polling_mode())
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        raise

if __name__ == '__main__':
    main()