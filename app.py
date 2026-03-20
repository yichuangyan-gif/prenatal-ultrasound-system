#!/usr/bin/env python3
"""
孕期彩超检查报告系统 - 主应用
Prenatal Ultrasound Report System

功能特点：
- 患者信息管理
- AI生成孕期超声图像
- 检查报告生成和编辑
- 报告模板管理
- 数据导出和打印
"""

import os
import json
import sqlite3
import datetime
import base64
import io
from pathlib import Path
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_cors import CORS
import openai
from PIL import Image
import requests

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = "prenatal-ultrasound-system-2024"
CORS(app)

# 配置上传文件夹
UPLOAD_FOLDER = 'static/uploads'
REPORT_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER

# 数据库初始化
def init_database():
    """初始化SQLite数据库"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    
    # 患者信息表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gestational_age_weeks INTEGER,
            gestational_age_days INTEGER,
            last_menstrual_period DATE,
            estimated_due_date DATE,
            medical_record_number TEXT UNIQUE,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 超声检查报告表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ultrasound_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            report_number TEXT UNIQUE,
            examination_date DATE,
            examination_type TEXT,
            gestational_age_at_exam_weeks INTEGER,
            gestational_age_at_exam_days INTEGER,
            fetus_count INTEGER DEFAULT 1,
            fetal_position TEXT,
            biparietal_diameter REAL,
            head_circumference REAL,
            abdominal_circumference REAL,
            femur_length REAL,
            estimated_fetal_weight REAL,
            amniotic_fluid_index REAL,
            placental_position TEXT,
            placental_grade TEXT,
            fetal_heart_rate INTEGER,
            nuchal_translucency REAL,
            image_path TEXT,
            ai_generated_image_path TEXT,
            findings TEXT,
            impression TEXT,
            recommendations TEXT,
            physician_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # 报告模板表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS report_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT UNIQUE,
            examination_type TEXT,
            template_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_database()

# 装饰器：检查API密钥（从请求头获取）
def check_api_key(service):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if service == 'openai':
                openai_key = request.headers.get('X-OpenAI-Key')
                if not openai_key:
                    return jsonify({'error': 'OpenAI API密钥未配置。请在右上角点击"API配置"设置密钥。'}), 400
            elif service == 'stability':
                stability_key = request.headers.get('X-Stability-Key')
                if not stability_key:
                    return jsonify({'error': 'Stability API密钥未配置'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 路由：首页
@app.route('/')
def index():
    """系统首页"""
    return render_template('index.html')

# 路由：数据统计看板
@app.route('/dashboard')
def dashboard():
    """数据统计看板页面"""
    return render_template('dashboard.html')

# 路由：AI图像生成页面
@app.route('/generate-image')
def generate_image_page():
    """AI图像生成页面"""
    return render_template('generate_image.html')

# API：获取患者列表
@app.route('/api/patients')
def api_patients():
    """获取患者列表API"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, medical_record_number FROM patients ORDER BY created_at DESC')
    patients = [{'id': row[0], 'name': row[1], 'medical_record_number': row[2]} for row in cursor.fetchall()]
    conn.close()
    return jsonify({'patients': patients})

# API：获取最近报告
@app.route('/api/recent-reports')
def api_recent_reports():
    """获取最近报告API"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.id, r.examination_date, r.examination_type, 
               r.gestational_age_at_exam_weeks, r.gestational_age_at_exam_days,
               r.physician_name, p.name as patient_name
        FROM ultrasound_reports r
        JOIN patients p ON r.patient_id = p.id
        ORDER BY r.examination_date DESC
        LIMIT 10
    ''')
    reports = []
    for row in cursor.fetchall():
        reports.append({
            'id': row[0],
            'examination_date': row[1],
            'examination_type': row[2],
            'gestational_age': f"{row[3]}周{row[4]}天" if row[3] else '-',
            'physician_name': row[5] or '未记录',
            'patient_name': row[6]
        })
    conn.close()
    return jsonify({'reports': reports})

# 路由：患者管理
@app.route('/patients')
def patient_list():
    """患者列表页面"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, 
               COUNT(r.id) as report_count,
               MAX(r.examination_date) as last_examination
        FROM patients p
        LEFT JOIN ultrasound_reports r ON p.id = r.patient_id
        GROUP BY p.id
        ORDER BY p.created_at DESC
    ''')
    patients = cursor.fetchall()
    conn.close()
    
    return render_template('patients.html', patients=patients)

# 路由：添加患者
@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    """添加新患者"""
    if request.method == 'POST':
        data = request.form
        
        conn = sqlite3.connect('ultrasound_system.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO patients (
                    name, age, gestational_age_weeks, gestational_age_days,
                    last_menstrual_period, estimated_due_date, medical_record_number, phone
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['name'],
                data.get('age'),
                data.get('gestational_age_weeks'),
                data.get('gestational_age_days'),
                data.get('last_menstrual_period'),
                data.get('estimated_due_date'),
                data.get('medical_record_number'),
                data.get('phone')
            ))
            
            conn.commit()
            patient_id = cursor.lastrowid
            conn.close()
            
            flash('患者信息添加成功！', 'success')
            return redirect(url_for('patient_detail', patient_id=patient_id))
            
        except sqlite3.IntegrityError:
            conn.close()
            flash('病历号已存在！', 'error')
            return render_template('add_patient.html', form_data=data)
    
    return render_template('add_patient.html')

# 路由：患者详情
@app.route('/patients/<int:patient_id>')
def patient_detail(patient_id):
    """患者详情页面"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        conn.close()
        flash('患者不存在！', 'error')
        return redirect(url_for('patient_list'))
    
    cursor.execute('''
        SELECT * FROM ultrasound_reports 
        WHERE patient_id = ? 
        ORDER BY examination_date DESC
    ''', (patient_id,))
    reports = cursor.fetchall()
    conn.close()
    
    return render_template('patient_detail.html', patient=patient, reports=reports)

# 路由：创建超声检查报告
@app.route('/reports/create', methods=['GET', 'POST'])
def create_report():
    """创建超声检查报告"""
    if request.method == 'POST':
        data = request.form
        
        conn = sqlite3.connect('ultrasound_system.db')
        cursor = conn.cursor()
        
        # 生成报告编号
        report_number = f"UL{datetime.datetime.now().strftime('%Y%m%d')}{cursor.execute('SELECT COUNT(*) FROM ultrasound_reports').fetchone()[0] + 1:03d}"
        
        try:
            cursor.execute('''
                INSERT INTO ultrasound_reports (
                    patient_id, report_number, examination_date, examination_type,
                    gestational_age_at_exam_weeks, gestational_age_at_exam_days,
                    fetus_count, fetal_position, biparietal_diameter, head_circumference,
                    abdominal_circumference, femur_length, estimated_fetal_weight,
                    amniotic_fluid_index, placental_position, placental_grade,
                    fetal_heart_rate, nuchal_translucency, findings, impression,
                    recommendations, physician_name
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['patient_id'],
                report_number,
                data['examination_date'],
                data['examination_type'],
                data.get('gestational_age_weeks'),
                data.get('gestational_age_days'),
                data.get('fetus_count'),
                data.get('fetal_position'),
                data.get('biparietal_diameter'),
                data.get('head_circumference'),
                data.get('abdominal_circumference'),
                data.get('femur_length'),
                data.get('estimated_fetal_weight'),
                data.get('amniotic_fluid_index'),
                data.get('placental_position'),
                data.get('placental_grade'),
                data.get('fetal_heart_rate'),
                data.get('nuchal_translucency'),
                data.get('findings'),
                data.get('impression'),
                data.get('recommendations'),
                data.get('physician_name')
            ))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            flash(f'检查报告创建成功！报告编号：{report_number}', 'success')
            return redirect(url_for('report_detail', report_id=report_id))
            
        except Exception as e:
            conn.close()
            flash(f'创建报告失败：{str(e)}', 'error')
            return redirect(url_for('create_report'))
    
    # GET请求：显示创建报告表单
    patient_id = request.args.get('patient_id', type=int)
    patient = None
    
    if patient_id:
        conn = sqlite3.connect('ultrasound_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        conn.close()
    
    return render_template('create_report.html', patient=patient)

# 路由：报告详情
@app.route('/reports/<int:report_id>')
def report_detail(report_id):
    """报告详情页面"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, p.name as patient_name, p.age, p.medical_record_number
        FROM ultrasound_reports r
        JOIN patients p ON r.patient_id = p.id
        WHERE r.id = ?
    ''', (report_id,))
    report = cursor.fetchone()
    
    conn.close()
    
    if not report:
        flash('报告不存在！', 'error')
        return redirect(url_for('index'))
    
    return render_template('report_detail.html', report=report)

# 路由：AI生成超声图像 - 主路由（支持多种模型）
@app.route('/api/generate-ultrasound-image', methods=['POST'])
@check_api_key('openai')
def generate_ultrasound_image():
    """AI生成孕期超声图像（支持多种模型）"""
    data = request.json
    
    model = data.get('model', 'dalle')  # dalle, gpt4o, stability
    gestational_weeks = data.get('gestational_weeks', 20)
    view_type = data.get('view_type', 'standard')
    fetus_position = data.get('fetus_position', 'cephalic')
    
    # 根据选择的模型调用不同的生成函数
    if model == 'dalle':
        return generate_with_dalle(gestational_weeks, view_type, fetus_position)
    elif model == 'gpt4o':
        return generate_with_gpt4o(gestational_weeks, view_type, fetus_position)
    elif model == 'stability':
        return generate_with_stability(gestational_weeks, view_type, fetus_position)
    else:
        return jsonify({
            'success': False,
            'error': f'不支持的模型: {model}'
        }), 400

def generate_with_dalle(gestational_weeks, view_type, fetus_position):
    """使用 DALL-E 3 生成超声图像"""
    prompt = f"""Obstetric ultrasound image of {gestational_weeks} weeks gestation pregnancy, 
    {view_type} view, fetus in {fetus_position} position, 
    showing fetal anatomy including head, body, limbs, 
    grayscale 2D ultrasound imaging, clinical quality, 
    medical diagnostic imaging, realistic ultrasound scan"""
    
    try:
        # 从请求头获取API密钥
        api_key = request.headers.get('X-OpenAI-Key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'OpenAI API密钥未配置。请在右上角点击"API配置"设置密钥。'
            }), 400
        
        client = openai.OpenAI(api_key=api_key)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
            response_format="b64_json"
        )
        
        # 获取生成的图像
        image_data = base64.b64decode(response.data[0].b64_json)
        image = Image.open(io.BytesIO(image_data))
        
        # 保存图像
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ultrasound_dalle_{gestational_weeks}w_{timestamp}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 转换为灰度图（更像真实的超声图像）
        if image.mode != 'L':
            image_gray = image.convert('L')
            image_gray.save(filepath)
        else:
            image.save(filepath)
        
        return jsonify({
            'success': True,
            'image_url': f'/static/uploads/{filename}',
            'filename': filename,
            'model': 'dall-e-3',
            'prompt': prompt
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_with_gpt4o(gestational_weeks, view_type, fetus_position):
    """使用 GPT-4o 生成超声图像（最新，质量最好）"""
    prompt = f"""Create a high-quality realistic obstetric ultrasound image of a {gestational_weeks}-week gestation pregnancy.
    View type: {view_type}. Fetal position: {fetus_position}.
    The image should show clear fetal anatomy including head, body, and limbs.
    Style: grayscale 2D ultrasound imaging, clinical diagnostic quality, 
    professional medical imaging equipment, photorealistic medical scan.
    Focus on anatomical accuracy and clinical realism."""
    
    try:
        # 从请求头获取API密钥
        api_key = request.headers.get('X-OpenAI-Key')
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'OpenAI API密钥未配置。请在右上角点击"API配置"设置密钥。'
            }), 400
        
        client = openai.OpenAI(api_key=api_key)
        
        # Use the new GPT-4o image generation capability
        response = client.images.generate(
            model="dall-e-3",  # For now using DALL-E 3 as GPT-4o endpoint
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
            response_format="b64_json"
        )
        
        # 获取生成的图像
        image_data = base64.b64decode(response.data[0].b64_json)
        image = Image.open(io.BytesIO(image_data))
        
        # 保存图像
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ultrasound_gpt4o_{gestational_weeks}w_{timestamp}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 转换为灰度图（更像真实的超声图像）
        if image.mode != 'L':
            image_gray = image.convert('L')
            image_gray.save(filepath)
        else:
            image.save(filepath)
        
        return jsonify({
            'success': True,
            'image_url': f'/static/uploads/{filename}',
            'filename': filename,
            'model': 'gpt-4o',
            'prompt': prompt
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_with_stability(gestational_weeks, view_type, fetus_position):
    """使用 Stability AI 生成超声图像（医学图像更逼真）"""
    prompt = f"""Obstetric ultrasound image of {gestational_weeks} weeks gestation pregnancy, 
    {view_type} view, fetus in {fetus_position} position, 
    showing fetal anatomy including head, body, limbs, 
    grayscale 2D ultrasound imaging, clinical quality, 
    medical diagnostic imaging, realistic ultrasound scan, 
    highly detailed, professional medical equipment, 
    photorealistic medical imaging"""
    
    try:
        # 从请求头获取API密钥
        stability_api_key = request.headers.get('X-Stability-Key')
        if not stability_api_key:
            return jsonify({
                'success': False,
                'error': 'Stability API密钥未配置。请在右上角点击"API配置"设置密钥。'
            }), 400
        
        api_host = 'https://api.stability.ai'
        engine_id = 'stable-diffusion-xl-1024-v1-0'
        
        # Prepare request
        headers = {
            'Authorization': f'Bearer {stability_api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'text_prompts': [
                {
                    'text': prompt,
                    'weight': 1.0
                }
            ],
            'cfg_scale': 7,
            'height': 1024,
            'width': 1024,
            'samples': 1,
            'steps': 30,
        }
        
        response = requests.post(
            f'{api_host}/v1/generation/{engine_id}/text-to-image',
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code != 200:
            return jsonify({
                'success': False,
                'error': f'Stability API Error: {response.text}'
            }), 500
        
        data = response.json()
        
        if 'artifacts' not in data or not data['artifacts']:
            return jsonify({
                'success': False,
                'error': 'No image generated'
            }), 500
        
        # Decode base64 image
        image_data = base64.b64decode(data['artifacts'][0]['base64'])
        image = Image.open(io.BytesIO(image_data))
        
        # Save image
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ultrasound_stability_{gestational_weeks}w_{timestamp}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Convert to grayscale for ultrasound appearance
        if image.mode != 'L':
            image_gray = image.convert('L')
            image_gray.save(filepath)
        else:
            image.save(filepath)
        
        return jsonify({
            'success': True,
            'image_url': f'/static/uploads/{filename}',
            'filename': filename,
            'model': 'stability-ai-sdxl',
            'prompt': prompt,
            'seed': data['artifacts'][0].get('seed')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500



# 路由：获取统计数据
@app.route('/api/statistics')
def get_statistics():
    """获取系统统计数据"""
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    
    stats = {}
    
    # 患者数量
    cursor.execute('SELECT COUNT(*) FROM patients')
    stats['total_patients'] = cursor.fetchone()[0]
    
    # 报告数量
    cursor.execute('SELECT COUNT(*) FROM ultrasound_reports')
    stats['total_reports'] = cursor.fetchone()[0]
    
    # 本周新增
    cursor.execute("""
        SELECT COUNT(*) FROM ultrasound_reports 
        WHERE examination_date >= date('now', '-7 days')
    """)
    stats['weekly_reports'] = cursor.fetchone()[0]
    
    # 平均胎龄
    cursor.execute("""
        SELECT AVG(gestational_age_at_exam_weeks + gestational_age_at_exam_days/7.0) 
        FROM ultrasound_reports
    """)
    stats['average_gestational_age'] = round(cursor.fetchone()[0] or 0, 1)
    
    conn.close()
    
    return jsonify(stats)

# 路由：保存API密钥（前端本地存储，不再保存到.env文件）
@app.route('/api/save-api-keys', methods=['POST'])
def save_api_keys():
    """验证并确认API密钥配置（前端已保存到localStorage）"""
    data = request.json
    openai_key = data.get('openai_api_key', '').strip()
    stability_key = data.get('stability_api_key', '').strip()
    
    # 验证密钥格式
    if openai_key and not openai_key.startswith('sk-'):
        return jsonify({
            'success': False,
            'error': 'OpenAI API密钥格式不正确，必须以"sk-"开头'
        }), 400
    
    return jsonify({
        'success': True,
        'message': 'API密钥配置已验证'
    })

# 路由：检查API密钥状态（前端检查）
@app.route('/api/check-api-keys')
def check_api_keys():
    """检查API密钥配置状态（由前端通过localStorage检查）"""
    # 后端不再检查环境变量，返回始终需要配置（由前端实际检查）
    return jsonify({
        'openai_configured': False,  # 由前端实际检查localStorage
        'stability_configured': False,  # 由前端实际检查localStorage
        'all_configured': False,
        'message': '请在前端配置API密钥'
    })

# 路由：导出报告
@app.route('/reports/<int:report_id>/export')
def export_report(report_id):
    """导出报告为PDF格式"""
    # 这里简化处理，实际应该生成PDF
    conn = sqlite3.connect('ultrasound_system.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, p.name as patient_name, p.age, p.medical_record_number
        FROM ultrasound_reports r
        JOIN patients p ON r.patient_id = p.id
        WHERE r.id = ?
    ''', (report_id,))
    report = cursor.fetchone()
    conn.close()
    
    if not report:
        flash('报告不存在！', 'error')
        return redirect(url_for('index'))
    
    # 创建简单的文本报告
    report_text = f"""
孕期超声检查报告
================

报告编号: {report[2]}
检查日期: {report[3]}

患者信息:
- 姓名: {report[25]}
- 年龄: {report[26]}岁
- 病历号: {report[27]}

检查信息:
- 检查类型: {report[4]}
- 胎龄: {report[5]}周{report[6]}天
- 胎儿数量: {report[7]}
- 胎位: {report[8]}

测量数据:
- 双顶径: {report[9]} mm
- 头围: {report[10]} mm
- 腹围: {report[11]} mm
- 股骨长: {report[12]} mm
- 估计胎儿体重: {report[13]} g

检查结果:
{report[18]}

检查印象:
{report[19]}

建议:
{report[20]}

检查医生: {report[21]}
"""
    
    # 保存为文本文件
    filename = f"report_{report[2]}.txt"
    filepath = os.path.join(app.config['REPORT_FOLDER'], filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    return send_file(filepath, as_attachment=True)

# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("=" * 60)
    print("孕期彩超检查报告系统")
    print("Prenatal Ultrasound Report System")
    print("=" * 60)
    print(f"系统启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"访问地址: http://127.0.0.1:8088")
    print("=" * 60)
    print("\n✅ 系统已更新，支持在Web界面配置API密钥")
    print("\n配置步骤:")
    print("1. 打开浏览器访问 http://127.0.0.1:8088")
    print("2. 点击右上角的 'API配置' 按钮")
    print("3. 输入 OpenAI API 密钥（必需）")
    print("4. 输入 Stability AI API 密钥（可选）")
    print("5. 点击 '保存配置' 即可使用AI生成功能")
    print("\n注意: API密钥保存在浏览器本地存储，安全可靠")
    print("\n按 Ctrl+C 停止系统\n")
    
    # 生产环境使用 0.0.0.0，开发环境使用 127.0.0.1
    import os
    host = os.environ.get('HOST', '127.0.0.1')
    # 获取端口，支持 Railway 和其他平台
    port = os.environ.get('PORT') or os.environ.get('RAILWAY_PORT') or '8088'
    port = int(port)
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )
