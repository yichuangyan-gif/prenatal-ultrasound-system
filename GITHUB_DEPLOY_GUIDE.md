# GitHub 部署完全指南

## 第一部分：推送代码到 GitHub

### 1. 在 GitHub 创建仓库

访问: https://github.com/new

填写信息:
- Repository name: `prenatal-ultrasound-system`
- Description: 孕期彩超检查报告系统 - Prenatal Ultrasound Report System
- 选择 Public（公开）或 Private（私有）
- **不要**勾选 "Initialize this repository with a README"（因为本地已有）
- 点击 **Create repository**

### 2. 配置本地仓库连接 GitHub

打开 PowerShell 或 CMD，执行以下命令：

```bash
# 进入项目目录
cd C:\Users\Administrator\WorkBuddy\prenatal_ultrasound_system

# 查看当前远程仓库（应该是空的或错误的）
git remote -v

# 删除旧的远程仓库配置（如果有）
git remote remove origin

# 添加新的远程仓库（替换 YOUR_USERNAME 为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/prenatal-ultrasound-system.git

# 验证配置
git remote -v
```

### 3. 推送代码到 GitHub

```bash
# 确保所有更改已提交
git add -A
git commit -m "准备部署到GitHub"

# 推送到GitHub（使用main分支）
git branch -M main
git push -u origin main

# 如果提示输入用户名密码，输入你的GitHub用户名和Personal Access Token
```

### 4. 验证推送成功

访问: `https://github.com/YOUR_USERNAME/prenatal-ultrasound-system`

应该能看到所有代码文件。

---

## 第二部分：删除 GitHub 仓库中的文件/代码

### 方法 A：删除单个文件

#### 通过网页删除（最简单）

1. 访问 GitHub 仓库页面
2. 点击进入要删除的文件
3. 点击右上角的 **...**（三个点）
4. 选择 **Delete file**
5. 填写删除说明（Commit message）
6. 点击 **Commit changes**

#### 通过命令行删除

```bash
# 删除文件
git rm 文件名.txt

# 删除文件夹（递归）
git rm -r 文件夹名/

# 提交更改
git commit -m "删除不必要的文件"

# 推送到GitHub
git push origin main
```

### 方法 B：删除整个文件夹

```bash
# 例如删除 venv 文件夹（不应该上传到GitHub）
git rm -r venv/
git commit -m "删除venv文件夹"
git push origin main
```

### 方法 C：清空整个仓库（保留仓库，删除所有文件）

```bash
# 1. 删除所有文件（保留.git）
git rm -rf .

# 2. 提交更改
git commit -m "清空仓库"

# 3. 推送
git push origin main

# 4. 重新添加需要的文件...
```

### 方法 D：完全删除仓库（整个删除）

#### 通过网页删除（推荐）

1. 访问 GitHub 仓库页面
2. 点击 **Settings**（设置）
3. 滚动到最底部 **Danger Zone**（危险区域）
4. 点击 **Delete this repository**
5. 输入仓库名称确认
6. 点击 **I understand the consequences, delete this repository**

#### 通过命令行删除本地关联

```bash
# 只删除本地git关联，不影响GitHub仓库
cd C:\Users\Administrator\WorkBuddy\prenatal_ultrasound_system
rm -rf .git

# 重新初始化（如果需要）
git init
```

---

## 第三部分：忽略不需要的文件

### 创建 .gitignore 文件

```bash
# 创建 .gitignore
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "*.db" >> .gitignore
echo ".env" >> .gitignore
echo "uploads/*" >> .gitignore
```

### 从GitHub删除已上传的敏感文件

```bash
# 1. 停止追踪文件但保留本地副本
git rm --cached venv/ -r
git rm --cached .env
git rm --cached *.db

# 2. 提交更改
git commit -m "移除敏感文件和依赖目录"

# 3. 推送
git push origin main

# 4. 添加到 .gitignore（防止再次上传）
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "更新.gitignore"
git push origin main
```

---

## 第四部分：常见问题

### Q1: 推送时提示 "Permission denied"

**解决**: 需要配置 GitHub Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 选择有效期和权限（至少勾选 `repo`）
4. 生成后复制 Token
5. 推送时输入 Token 作为密码

### Q2: 如何修改已上传的文件？

```bash
# 修改文件后
git add 文件名
git commit -m "修改说明"
git push origin main
```

### Q3: 如何回滚到之前的版本？

```bash
# 查看历史
git log --oneline

# 回滚到某个版本（替换abc123为实际的commit id）
git revert abc123

# 或者强制回滚（危险！会丢失之后的更改）
git reset --hard abc123
git push -f origin main
```

### Q4: 推送时提示 "rejected"

```bash
# 先拉取远程更改
git pull origin main

# 解决冲突后再次推送
git push origin main
```

---

## 第五部分：部署到 Render（通过 GitHub）

### 1. 推送代码到 GitHub（按第一部分操作）

### 2. 在 Render 部署

1. 访问 https://render.com/
2. 用 GitHub 账号登录
3. 点击 **New +** → **Web Service**
4. 选择你的 GitHub 仓库 `prenatal-ultrasound-system`
5. 配置：
   - **Name**: prenatal-ultrasound-system
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free
6. 点击 **Create Web Service**
7. 等待 2-3 分钟部署完成
8. 获得公网链接（如 `https://prenatal-ultrasound-system.onrender.com`）

### 3. 在不同电脑访问

部署完成后，你可以在任何电脑的浏览器访问：
```
https://你的服务名.onrender.com
```

---

## 快速命令参考

```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 推送代码
git push origin main

# 拉取代码
git pull origin main

# 删除远程文件
git rm 文件名
git commit -m "删除文件"
git push origin main

# 强制推送（危险）
git push -f origin main
```

---

**提示**: 首次配置完成后，日常只需要3个命令：
```bash
git add -A
git commit -m "更新说明"
git push origin main
```
