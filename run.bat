@echo off
chcp 65001 >nul
title AI 合同审查工具

echo ========================================
echo    AI 合同审查工具 - 启动脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [提示] 首次运行，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo [完成] 依赖安装成功
    echo.
)

REM 检查 .env 文件
if not exist .env (
    echo [提示] 未检测到 .env 文件，正在从 .env.example 复制...
    copy .env.example .env >nul
    echo.
    echo ========================================
    echo  重要：请编辑 .env 文件，填入你的 DeepSeek API Key
    echo  获取地址: https://platform.deepseek.com/
    echo ========================================
    echo.
    echo 按任意键打开 .env 文件进行编辑...
    pause >nul
    notepad .env
    echo.
)

echo [启动] 正在启动 AI 合同审查工具...
echo [提示] 启动后请在浏览器访问 http://localhost:8000
echo [提示] 按 Ctrl+C 停止服务
echo.

python app.py

pause
