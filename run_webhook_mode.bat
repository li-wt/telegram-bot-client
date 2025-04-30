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
set USE_WEBHOOK=true
set USE_POLLING=false
set WEBHOOK_PORT=8443

:: 检查ngrok是否已经运行
tasklist /FI "IMAGENAME eq ngrok.exe" 2>NUL | find /I /N "ngrok.exe">NUL
if errorlevel 1 (
    :: 启动ngrok
    echo 启动ngrok...
    start /B ngrok http 8443
    :: 等待ngrok启动
    timeout /t 5
)

:: 获取ngrok的公网URL
for /f "tokens=*" %%a in ('curl -s http://127.0.0.1:4040/api/tunnels ^| python -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"') do set WEBHOOK_URL=%%a

echo Webhook URL: %WEBHOOK_URL%

:: 启动应用
echo 启动Telegram客户端...
python main_no_polling.py --use-webhook

:: 停止ngrok
taskkill /F /IM ngrok.exe

endlocal