@echo off
chcp 65001
echo ==========================================
echo  从 GitHub 删除文件/文件夹
echo ==========================================
echo.
echo 请选择操作:
echo [1] 删除 venv 文件夹（推荐，不应该上传）
echo [2] 删除数据库文件（ultrasound_system.db）
echo [3] 删除 __pycache__ 文件夹
echo [4] 删除其他文件/文件夹
echo [5] 完全清空仓库（危险！）
echo.
set /p choice=请输入选项 (1-5): 

if "%choice%"=="1" goto delete_venv
if "%choice%"=="2" goto delete_db
if "%choice%"=="3" goto delete_pycache
if "%choice%"=="4" goto delete_other
if "%choice%"=="5" goto delete_all
goto end

:delete_venv
echo [1/3] 停止追踪 venv 文件夹...
git rm -r --cached venv/
echo [2/3] 提交更改...
git commit -m "删除venv文件夹（不应该上传到GitHub）"
echo [3/3] 推送到GitHub...
git push origin main
echo 完成！venv文件夹已从GitHub删除
goto end

:delete_db
echo [1/3] 停止追踪数据库文件...
git rm --cached ultrasound_system.db
echo [2/3] 提交更改...
git commit -m "删除数据库文件（包含敏感数据）"
echo [3/3] 推送到GitHub...
git push origin main
echo 完成！数据库文件已从GitHub删除
goto end

:delete_pycache
echo [1/3] 停止追踪 __pycache__ 文件夹...
git rm -r --cached __pycache__/
echo [2/3] 提交更改...
git commit -m "删除__pycache__缓存文件夹"
echo [3/3] 推送到GitHub...
git push origin main
echo 完成！缓存文件夹已从GitHub删除
goto end

:delete_other
set /p filename=请输入要删除的文件/文件夹名: 
echo [1/3] 删除 %filename%...
git rm -r --cached %filename%
echo [2/3] 提交更改...
git commit -m "删除 %filename%"
echo [3/3] 推送到GitHub...
git push origin main
echo 完成！%filename% 已从GitHub删除
goto end

:delete_all
echo ⚠️ 警告：这将删除仓库中的所有文件！
set /p confirm=确定要清空仓库吗？(yes/no): 
if /i "%confirm%"=="yes" (
    echo [1/3] 删除所有文件...
    git rm -rf .
    echo [2/3] 提交更改...
    git commit -m "清空仓库"
    echo [3/3] 推送到GitHub...
    git push origin main
    echo 完成！仓库已清空
) else (
    echo 操作已取消
)
goto end

:end
echo.
pause
