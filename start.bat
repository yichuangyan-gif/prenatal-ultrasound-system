@echo off
REM 孕期彩超检查报告系统启动脚本
REM Prenatal Ultrasound Report System Startup Script

echo ========================================
echo 孕期彩超检查报告系统
echo Prenatal Ultrasound Report System
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python安装
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate

REM 安装依赖
echo 安装依赖包...
pip install -r requirements.txt

REM 检查环境变量
if not exist ".env" (
    echo.
    echo 警告: 未找到 .env 配置文件
    echo 请创建 .env 文件并添加API密钥
    echo.
    echo 示例 .env 内容：
    echo OPENAI_API_KEY=sk-your-openai-key
    echo GOOGLE_API_KEY=your-google-key
    echo GOOGLE_CSE_ID=your-cse-id
    echo.
    pause
)

echo.
echo ========================================
echo 系统启动中...
echo 启动完成后，请打开浏览器访问: http://127.0.0.1:8088
echo ========================================
echo.

REM 启动应用
python app.py

pause
