@echo off
setlocal enabledelayedexpansion

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Python未安装，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

:: 检查虚拟环境是否存在
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境
call venv\Scripts\activate

:: 安装依赖
echo 安装依赖...
pip install -r requirements.txt

:: 设置环境变量
set USE_WEBHOOK=false
set USE_POLLING=false

:: 启动应用
echo 启动Telegram客户端...
python main_no_polling.py --no-polling

endlocal