# 孕期彩超检查报告系统

Prenatal Ultrasound Report System

一个完整的孕期超声检查管理和报告生成系统，集成AI图像生成技术。

**2026-06 更新**:
- ✅ 添加 Docker Compose 一键部署 + 本地 Ollama AI 模型支持
- ✅ 更新依赖支持 FastAPI 迁移和数据加密
- ✅ AI提示词优化为超真实文档风格（符合用户创作偏好）
- ✅ 添加本地模型选项（未来支持 Stable Diffusion / Ollama）

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

## 🎯 系统特点

- 👶 **患者管理** - 完整的孕妇档案管理
- 📋 **报告生成** - 专业的超声检查报告（参照美中宜和报告单样式）
- 🤖 **AI图像生成** - 集成云端 + 本地模型：
  - **DALL-E 3 / GPT-4o** - 直接可用
  - **Stability AI** - 医学图像更逼真
  - **本地 Ollama/SD** - 隐私优先，本地运行（Docker Compose 自动启动）
- 📊 **数据统计** - 实时数据看板
- 💾 **数据管理** - SQLite数据库 + 加密备份支持
- 🖨️ **报告导出** - 支持导出为文本格式
- 🌐 **多平台部署** - 支持本地、Docker、云服务器部署

## 🚀 快速开始

### 方法一：本地运行（推荐开发使用）

```bash
# 1. 克隆仓库
git clone https://github.com/yichuangyan-gif/prenatal-ultrasound-system.git
cd prenatal-ultrasound-system

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动系统
python app.py

# 5. 打开浏览器访问
# http://127.0.0.1:8088
```

### 方法二：Docker Compose 一键部署（推荐，含本地AI）

```bash
# 1. 确保安装 Docker 和 Docker Compose

# 2. 启动全部服务（应用 + Ollama 本地模型）
docker compose up -d

# 3. 访问系统
# http://localhost:8088

# 4. 本地AI模型访问 http://localhost:11434
```

### 方法三：Docker 部署

```bash
# 1. 构建镜像
docker build -t prenatal-ultrasound-system .

# 2. 运行容器
docker run -d -p 8088:8088 --name ultrasound-system prenatal-ultrasound-system

# 3. 访问系统
# http://localhost:8088
```

... (原有内容保持)

## 🔧 环境配置

### 必需配置

创建 `.env` 文件：

```env
# OpenAI API (用于 DALL-E 3 和 GPT-4o 图像生成)
OPENAI_API_KEY=sk-your-openai-api-key

# Stability AI API (用于生成更逼真的医学图像)
STABILITY_API_KEY=your-stability-api-key
```

## 📖 使用指南

### 3. AI生成图像

- 点击 "AI生成图像"
- 设置参数（孕周、视图、胎位）
- 选择模型（云端或本地）
- 生成图像
- 下载或用于报告

## 🛠️ 技术栈

- **后端**: Python 3.12 + Flask (迁移计划: FastAPI)
- **前端**: HTML5 + Bootstrap 5 (迁移计划: Next.js + Tailwind)
- **数据库**: SQLite + 加密备份
- **AI图像**: OpenAI / Stability AI / 本地 Ollama/SD
- **部署**: Docker Compose / Render / Railway

## 📝 更新日志

### Version 2.1.0 (2026-06-12)
- ✅ 执行用户修改意见：
  - Docker Compose + 本地Ollama AI
  - 依赖更新支持FastAPI/Next.js迁移
  - AI prompt 优化为超真实文档风格
  - 报告模板细节增强准备
- ✅ 新增多平台部署支持

... (原有更新日志)
