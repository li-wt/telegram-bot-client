import sys
import logging
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from config import LOG_LEVEL, LOG_FILE

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    try:
        # 创建Qt应用
        app = QApplication(sys.argv)
        
        # 创建并显示主窗口
        main_window = MainWindow()
        main_window.show()
        
        # 运行应用
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f'应用程序启动失败: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
