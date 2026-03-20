# GitHub 网页上传详细步骤

## 步骤 1：打开 GitHub 仓库页面

在浏览器地址栏输入：
```
https://github.com/yichuangyan-gi/prenatal-ultrasound-system
```

然后按回车键访问

---

## 步骤 2：找到 "Add file" 按钮

进入仓库页面后，看页面**右上角**区域：

```
┌─────────────────────────────────────────────────────────┐
│  yichuangyan-gi / prenatal-ultrasound-system      ⭐ ▾  │
│                                                         │
│  [Code] [Issues] [Pull requests] [Actions] [...]        │
│                                                         │
│  main ▾  📁 2 branches  📋 0 tags  🔄 0 commits         │
│                                                         │
│  ┌──────────────────────────────────────────┐          │
│  │ 📄 README.md                    [Add file▼] │  ← 在这里！
│  └──────────────────────────────────────────┘          │
│                                                         │
│  This repository is empty.                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**"Add file"** 按钮位置：
- 在页面中间偏右
- 在 "main" 分支选择器的右边
- 是一个白色按钮，带下拉箭头 ▼

---

## 步骤 3：点击 "Add file" 展开菜单

点击 **"Add file"** 按钮后，会显示下拉菜单：

```
[Add file ▼]
    │
    ├─ 📝 Create new file      ← 创建新文件
    └─ 📤 Upload files         ← 上传文件（选这个！）
```

点击 **"Upload files"**

---

## 步骤 4：上传文件

点击后会进入上传页面：

```
┌─────────────────────────────────────────────────────────┐
│  Upload files                                           │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │    拖拽文件到这里                               │   │
│  │                                                 │   │
│  │    或者                                         │   │
│  │                                                 │   │
│  │    [ choose your files ]                        │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Commit changes                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Add files via upload                              │   │
│  │                                                   │   │
│  │ Add an optional extended description...           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ● Commit directly to the main branch                   │
│  ○ Create a new branch for this commit and start a...   │
│                                                         │
│  [ Commit changes ]                                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 步骤 5：选择文件上传

### 方法 A：拖拽上传（推荐）

1. 打开文件资源管理器
2. 进入文件夹：`C:\Users\Administrator\WorkBuddy\prenatal_ultrasound_system`
3. 选择以下文件（按住 Ctrl 键多选）：
   - ✅ app.py
   - ✅ requirements.txt
   - ✅ README.md
   - ✅ Dockerfile
   - ✅ render.yaml
   - ✅ railway.json
   - ✅ build_static.py
   - ✅ .github 文件夹
   - ✅ templates 文件夹
   - ✅ static 文件夹
   - ✅ reports 文件夹

4. 将这些文件**拖拽**到 GitHub 网页的虚线框内

### 方法 B：点击选择文件

1. 点击 **"choose your files"** 按钮
2. 在弹出的文件选择器中
3. 进入项目文件夹
4. 选择要上传的文件
5. 点击 **打开**

---

## 步骤 6：提交更改

文件上传后，填写提交信息：

```
Commit changes
┌────────────────────────────────────────┐
│ Add files via upload                    │  ← 第一行（标题）
│                                         │
│ v2.0 完整版 - 孕期超声检查报告系统      │  ← 第二行（描述）
│ 包含报告详情页、AI图像生成、数据统计    │
└────────────────────────────────────────┘
```

然后点击绿色的 **"Commit changes"** 按钮

---

## 步骤 7：验证上传成功

上传完成后，页面会自动跳转到仓库主页，显示所有上传的文件：

```
┌─────────────────────────────────────────────────────────┐
│  yichuangyan-gi / prenatal-ultrasound-system            │
│                                                         │
│  📄 README.md              📄 app.py                    │
│  📄 requirements.txt       📁 templates/                │
│  📁 static/                📁 reports/                  │
│  ...                                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚠️ 注意事项

### 不要上传这些文件：
- ❌ `venv/` 文件夹（太大，可以重新生成）
- ❌ `__pycache__/` 文件夹（缓存文件）
- ❌ `ultrasound_system.db`（数据库文件）
- ❌ `.env`（包含敏感信息）

### 必须上传的文件：
- ✅ `app.py`（主程序）
- ✅ `requirements.txt`（依赖列表）
- ✅ `templates/`（HTML模板文件夹）
- ✅ `static/`（静态文件文件夹）
- ✅ `README.md`（说明文档）
- ✅ `Dockerfile`（Docker配置）
- ✅ `.github/workflows/`（GitHub Actions配置）

---

## 如果找不到 "Add file" 按钮

可能原因：
1. 仓库页面还没完全加载 → 刷新页面
2. 没有写入权限 → 检查是否登录了正确的账号
3. 浏览器问题 → 尝试换 Chrome 或 Edge

---

## 快速链接

直接访问上传页面：
```
https://github.com/yichuangyan-gi/prenatal-ultrasound-system/upload/main
```

---

## 上传完成后

访问仓库确认：
```
https://github.com/yichuangyan-gi/prenatal-ultrasound-system
```

然后就可以部署到 Render 了！
