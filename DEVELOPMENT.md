# 开发指南

本文档提供了项目的开发指南，包括架构设计、代码规范和开发流程。

## 项目架构

### 核心组件

1. 消息接收器
   - `message_receiver.py`: 基础消息接收实现
   - `message_receiver_webhook.py`: Webhook实现
   - 负责接收和处理Telegram消息

2. 客户端
   - `telegram_client.py`: 基础客户端实现
   - `telegram_client_no_polling.py`: 非轮询实现
   - 负责与Telegram API交互

3. 用户界面
   - `ui/main_window.py`: 主窗口
   - `ui/chat_widget.py`: 聊天界面
   - 使用PyQt5实现

### 通信机制

1. Webhook模式
```
Telegram Server -> Webhook Server -> Local Socket -> UI
```

2. 非轮询模式
```
Main Process -> Local Socket -> Client -> UI
```

## 代码规范

### Python风格

- 遵循PEP 8规范
- 使用4空格缩进
- 最大行长度120字符

### 命名规范

1. 文件名：小写，下划线分隔
```python
message_receiver.py
telegram_client.py
```

2. 类名：驼峰命名
```python
class MessageReceiver:
class TelegramClient:
```

3. 函数和变量：小写，下划线分隔
```python
def handle_message():
webhook_url = "..."
```

### 注释规范

1. 文件头注释
```python
"""
文件名：xxx.py
功能：...
作者：...
日期：...
"""
```

2. 函数注释
```python
def function_name():
    """
    函数功能描述
    
    参数：
        param1 (type): 描述
    
    返回：
        type: 描述
    """
```

## 开发流程

### 1. 环境设置

1. 克隆仓库：
```bash
git clone https://github.com/your-username/telegram-bot-client.git
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装开发依赖：
```bash
pip install -r requirements.txt
```

### 2. 开发步骤

1. 创建新分支：
```bash
git checkout -b feature/xxx
```

2. 编写代码和测试

3. 运行测试：
```bash
python -m pytest tests/
```

4. 提交代码：
```bash
git add .
git commit -m "描述变更"
```

### 3. 测试

1. 单元测试
   - 使用pytest框架
   - 测试文件放在tests/目录
   - 运行：`python -m pytest`

2. 集成测试
   - 测试Webhook功能
   - 测试非轮询模式
   - 测试UI交互

### 4. 调试

1. 日志
   - 使用logging模块
   - 日志级别：DEBUG, INFO, WARNING, ERROR
   - 日志文件：telegram_receiver.log

2. 调试工具
   - PyCharm调试器
   - logging.debug()
   - print调试

## 发布流程

1. 版本号管理
   - 遵循语义化版本
   - 格式：主版本.次版本.修订号

2. 打包
```bash
python setup.py sdist bdist_wheel
```

3. 发布
```bash
twine upload dist/*
```

## 文档维护

1. 代码文档
   - 使用docstring
   - 生成API文档

2. 用户文档
   - README.md
   - USER_GUIDE.md
   - DEVELOPMENT.md

3. API文档
   - 使用Sphinx生成
   - 包含所有公共API