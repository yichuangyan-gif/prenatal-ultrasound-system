# 使用 Personal Access Token 推送到 GitHub
# 用户: yichuangyan-gi

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  推送到 GitHub - 使用 Token" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 进入项目目录
$projectPath = "C:\Users\Administrator\WorkBuddy\prenatal_ultrasound_system"
Set-Location $projectPath

Write-Host "[1/5] 检查Git配置..." -ForegroundColor Yellow

# 配置Git用户信息（如果还没配置）
git config --global user.name "yichuangyan-gi" 2>$null
git config --global user.email "your-email@example.com" 2>$null

Write-Host "[2/5] 准备提交文件..." -ForegroundColor Yellow
git add -A
git status

Write-Host ""
Write-Host "[3/5] 提交更改..." -ForegroundColor Yellow
git commit -m "v2.0 完整版 - 孕期超声检查报告系统" 2>$null

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  请输入您的 GitHub Personal Access Token" -ForegroundColor Green
Write-Host "  获取地址: https://github.com/settings/tokens" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

$token = Read-Host -Prompt "请输入Token" -AsSecureString
$plainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))

Write-Host ""
Write-Host "[4/5] 配置远程仓库..." -ForegroundColor Yellow

# 配置远程仓库使用Token
git remote remove origin 2>$null
git remote add origin "https://yichuangyan-gi:$plainToken@github.com/yichuangyan-gi/prenatal-ultrasound-system.git"

Write-Host "[5/5] 推送到GitHub..." -ForegroundColor Yellow
git branch -M main

# 尝试推送
try {
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "  ✅ 推送成功！" -ForegroundColor Green
        Write-Host "  访问地址: https://github.com/yichuangyan-gi/prenatal-ultrasound-system" -ForegroundColor Green
        Write-Host "==========================================" -ForegroundColor Green
    } else {
        throw "推送失败"
    }
} catch {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Red
    Write-Host "  ❌ 推送失败" -ForegroundColor Red
    Write-Host "  请检查:" -ForegroundColor Red
    Write-Host "  1. Token是否正确" -ForegroundColor Red
    Write-Host "  2. 仓库是否已创建" -ForegroundColor Red
    Write-Host "  3. 仓库名是否正确: prenatal-ultrasound-system" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Red
}

Write-Host ""
Read-Host -Prompt "按 Enter 键退出"
