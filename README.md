# 孕期彩超检查报告系统

Prenatal Ultrasound Report System

一个完整的孕期超声检查管理和报告生成系统，集成AI图像生成技术。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

## 🎯 系统特点

- 👶 **患者管理** - 完整的孕妇档案管理
- 📋 **报告生成** - 专业的超声检查报告（参照美中宜和报告单样式）
- 🤖 **AI图像生成** - 集成三种先进AI模型：
  - **DALL-E 3** - 直接可用，高质量生成
  - **Stability AI** - 医学图像更逼真
  - **GPT-4o** - 最新技术，质量最好
- 📊 **数据统计** - 实时数据看板
- 💾 **数据管理** - SQLite数据库，支持数据导出
- 🖨️ **报告导出** - 支持导出为文本格式
- 🌐 **多平台部署** - 支持本地、Docker、云服务器部署

## 🚀 快速开始

### 方法一：本地运行（推荐开发使用）

```bash
# 1. 克隆仓库
git clone https://github.com/username/prenatal-ultrasound-system.git
cd prenatal-ultrasound-system

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 启动系统
python app.py

# 6. 打开浏览器访问
# http://127.0.0.1:8088
```

### 方法二：Docker 部署

```bash
# 1. 构建镜像
docker build -t prenatal-ultrasound-system .

# 2. 运行容器
docker run -d -p 8088:8088 --name ultrasound-system prenatal-ultrasound-system

# 3. 访问系统
# http://localhost:8088
```

### 方法三：Render 部署（免费云服务器）

1. Fork 本仓库到你的 GitHub 账号
2. 登录 [Render](https://render.com/)
3. 点击 "New +" → "Web Service"
4. 选择你的 GitHub 仓库
5. 配置：
   - **Name**: prenatal-ultrasound-system
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. 点击 "Create Web Service"
7. 等待部署完成，获取访问链接

### 方法四：Railway 部署

1. Fork 本仓库
2. 登录 [Railway](https://railway.app/)
3. 点击 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. 自动部署完成，获取域名访问

### 方法五：GitHub Pages（静态展示）

⚠️ **注意**: GitHub Pages 仅支持静态页面，完整功能需要后端支持。

1. 进入仓库 Settings → Pages
2. Source 选择 "GitHub Actions"
3. 推送代码后自动部署

## 🔧 环境配置

### 必需配置

创建 `.env` 文件：

```env
# OpenAI API (用于 DALL-E 3 和 GPT-4o 图像生成)
# 获取地址: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key

# Stability AI API (用于生成更逼真的医学图像)
# 获取地址: https://platform.stability.ai/
STABILITY_API_KEY=your-stability-api-key
```

### 如何获取API密钥

#### OpenAI API Key

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账户
3. 进入 "API keys" 页面
4. 点击 "Create new secret key"
5. 复制密钥到 `.env` 文件

#### Stability AI API Key

1. 访问 [Stability AI Platform](https://platform.stability.ai/)
2. 注册/登录账户
3. 进入 "API Keys" 页面
4. 创建新密钥

## 📖 使用指南

### 1. 添加患者

- 点击 "添加患者"
- 填写基本信息（姓名、病历号为必填）
- 使用孕期计算器自动计算预产期
- 点击 "保存患者信息"

### 2. 创建报告

- 选择患者
- 填写检查信息（检查日期、类型、胎周等）
- 填写测量数据（BPD、HC、AC、FL等）
- 填写检查结果和印象
- 保存报告

### 3. AI生成图像

- 点击 "AI生成图像"
- 设置参数（孕周、视图、胎位）
- 生成图像
- 下载或用于报告

### 4. 查看报告

- 报告样式参照**北京万柳美中宜和妇儿医院**超声检查报告单
- 支持打印和导出

## 📁 项目结构

```
prenatal_ultrasound_system/
├── app.py                      # 主应用文件
├── requirements.txt            # 依赖包列表
├── Dockerfile                 # Docker配置
├── render.yaml                # Render部署配置
├── railway.json               # Railway部署配置
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions配置
├── ultrasound_system.db       # 数据库文件
├── templates/                 # HTML模板
│   ├── base.html             # 基础模板
│   ├── index.html            # 首页
│   ├── patients.html         # 患者列表
│   ├── add_patient.html      # 添加患者
│   ├── patient_detail.html   # 患者详情
│   ├── create_report.html    # 创建报告
│   ├── report_detail.html    # 报告详情（参照美中宜和样式）
│   ├── generate_image.html   # AI图像生成
│   ├── dashboard.html        # 数据统计看板
│   ├── 404.html              # 404错误页
│   └── 500.html              # 500错误页
├── static/                    # 静态文件
│   ├── css/
│   │   └── style.css         # 自定义样式
│   ├── js/
│   │   └── main.js           # JavaScript文件
│   └── uploads/              # 上传的图像
└── reports/                  # 导出的报告
```

## 🛠️ 技术栈

- **后端**: Python 3.12 + Flask
- **前端**: HTML5 + Bootstrap 5 + jQuery
- **数据库**: SQLite
- **AI图像**: OpenAI DALL-E 3 / GPT-4o / Stability AI
- **部署**: Docker / Render / Railway

## 🔒 安全说明

- API密钥保存在浏览器本地存储，不会上传到服务器
- 患者数据存储在本地SQLite数据库
- 建议定期备份数据库文件

## 📝 更新日志

### Version 2.0.0 (2024-03-20)
- ✅ 新增报告详情页（参照美中宜和报告单样式）
- ✅ 新增AI图像生成页面
- ✅ 新增数据统计看板
- ✅ 新增404/500错误页面
- ✅ 优化患者详情页
- ✅ 优化创建报告页面
- ✅ 新增多平台部署支持
- ✅ 新增Docker支持

### Version 1.0.0 (2024-01)
- ✅ 患者管理系统
- ✅ 检查报告系统
- ✅ AI图像生成功能
- ✅ 数据统计看板
- ✅ 报告导出功能

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目仅供学习和研究使用。使用AI生成的图像时，请遵守相关法律法规。

## 🆘 技术支持

如遇到问题：

1. 查看 [故障排除](#故障排除) 章节
2. 检查日志输出
3. 提交Issue到项目仓库

## 🔧 故障排除

### 问题1: 无法启动系统

**解决方案**:
```bash
# 确保在虚拟环境中
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 重新安装依赖
pip install -r requirements.txt
```

### 问题2: AI生成功能不可用

**解决方案**:
1. 检查 `.env` 文件是否存在
2. 确认 `OPENAI_API_KEY` 已正确设置
3. 重启系统

### 问题3: 端口被占用

**解决方案**:
修改 `app.py` 中的端口配置:
```python
app.run(host='127.0.0.1', port=8089)  # 改为其他端口
```

---

**祝使用愉快！** 👶🤖📊

如有问题，请联系技术支持或提交Issue。
