@echo off
chcp 65001
echo ==========================================
echo  推送代码到 GitHub
echo ==========================================
echo.

set /p username=请输入你的GitHub用户名: 

echo.
echo [1/5] 配置远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/%username%/prenatal-ultrasound-system.git

echo [2/5] 检查远程仓库...
git remote -v

echo [3/5] 添加所有文件...
git add -A

echo [4/5] 提交更改...
git commit -m "更新系统 v2.0 - 完整的超声报告系统"

echo [5/5] 推送到GitHub...
git branch -M main
git push -u origin main

echo.
echo ==========================================
echo  完成！
echo  访问: https://github.com/%username%/prenatal-ultrasound-system
echo ==========================================
echo.
pause
