#!/usr/bin/env python3
"""
构建静态网站版本，用于GitHub Pages部署
"""
import os
import shutil
from pathlib import Path

def build_static_site():
    """构建静态网站"""
    # 创建输出目录
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # 复制静态文件
    static_dir = Path('static')
    if static_dir.exists():
        shutil.copytree(static_dir, dist_dir / 'static')
    
    # 复制模板文件为HTML
    templates_dir = Path('templates')
    for template_file in templates_dir.glob('*.html'):
        # 读取模板内容
        content = template_file.read_text(encoding='utf-8')
        
        # 处理Jinja2模板语法（简化处理）
        # 移除extends和block标签
        content = content.replace('{% extends "base.html" %}', '')
        content = content.replace('{% block title %}', '<!-- title -->')
        content = content.replace('{% endblock %}', '<!-- end -->')
        content = content.replace('{% block content %}', '')
        content = content.replace('{% block extra_css %}', '<style>')
        content = content.replace('{% block extra_js %}', '<script>')
        
        # 移除其他Jinja2标签
        import re
        content = re.sub(r'{%\s*[^}]+\s*%}', '', content)
        content = re.sub(r'{{\s*[^}]+\s*}}', '', content)
        
        # 写入输出文件
        output_file = dist_dir / template_file.name
        output_file.write_text(content, encoding='utf-8')
    
    # 创建index.html（复制首页）
    index_source = dist_dir / 'index.html'
    if index_source.exists():
        print(f"✅ 构建完成！输出目录: {dist_dir.absolute()}")
        print(f"📁 文件列表:")
        for f in dist_dir.rglob('*'):
            if f.is_file():
                print(f"   - {f.relative_to(dist_dir)}")
    else:
        # 创建一个简单的index.html
        index_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>孕期彩超检查报告系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .welcome-card {
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
        }
        .welcome-icon {
            font-size: 80px;
            color: #667eea;
            margin-bottom: 20px;
        }
        .btn-custom {
            padding: 15px 40px;
            font-size: 18px;
            border-radius: 30px;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="welcome-card">
        <div class="welcome-icon">
            <i class="fas fa-baby"></i>
        </div>
        <h1 class="mb-3">孕期彩超检查报告系统</h1>
        <p class="text-muted mb-4">Prenatal Ultrasound Report System</p>
        <p class="mb-4">专业的产前超声诊断与管理平台</p>
        
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i>
            <strong>部署提示</strong><br>
            本系统需要Python后端支持，GitHub Pages仅支持静态页面。<br>
            请使用以下方式运行完整功能：
        </div>
        
        <div class="text-start bg-light p-3 rounded mb-4">
            <h6><i class="fas fa-terminal"></i> 本地运行：</h6>
            <code>
                git clone https://github.com/username/prenatal-ultrasound-system.git<br>
                cd prenatal-ultrasound-system<br>
                pip install -r requirements.txt<br>
                python app.py
            </code>
        </div>
        
        <a href="https://github.com/username/prenatal-ultrasound-system" class="btn btn-primary btn-custom" target="_blank">
            <i class="fab fa-github"></i> 查看源码
        </a>
    </div>
</body>
</html>"""
        (dist_dir / 'index.html').write_text(index_content, encoding='utf-8')
        print(f"✅ 已创建默认首页")

if __name__ == '__main__':
    build_static_site()
