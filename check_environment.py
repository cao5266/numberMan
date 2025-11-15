#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DH_live 环境检查脚本
用于检查项目运行所需的环境和文件是否完整
"""

import os
import sys
import importlib
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("=== Python 版本检查 ===")
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and 8 <= version.minor <= 11:
        print("✅ Python版本兼容")
        return True
    else:
        print("❌ Python版本不兼容，推荐使用Python 3.8-3.11")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n=== 依赖包检查 ===")
    
    required_packages = [
        'torch',
        'cv2',
        'numpy',
        'mediapipe',
        'gradio',
        'tqdm',
        'sklearn',
        'glfw',
        'OpenGL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                importlib.import_module('cv2')
            elif package == 'sklearn':
                importlib.import_module('sklearn')
            elif package == 'OpenGL':
                importlib.import_module('OpenGL.GL')
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺失的包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有依赖包已安装")
        return True

def check_model_files():
    """检查模型文件"""
    print("\n=== 模型文件检查 ===")
    
    model_files = [
        'checkpoint/lstm/lstm_model_epoch_325.pkl',
        'checkpoint/DINet_mini/epoch_40.pth'
    ]
    
    missing_files = []
    
    for file_path in model_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"✅ {file_path} ({file_size:.1f} MB)")
        else:
            print(f"❌ {file_path} - 文件不存在")
            missing_files.append(file_path)
    
    if missing_files:
        print("\n缺失的模型文件:")
        for file in missing_files:
            print(f"  - {file}")
        print("\n请下载模型文件并放置到对应目录")
        print("下载方法请参考 Anaconda运行指南.md")
        return False
    else:
        print("\n✅ 所有模型文件已就位")
        return True

def check_project_structure():
    """检查项目结构"""
    print("\n=== 项目结构检查 ===")
    
    required_dirs = [
        'talkingface',
        'mini_live',
        'web_demo',
        'data'
    ]
    
    required_files = [
        'app.py',
        'demo_mini.py',
        'data_preparation_mini.py',
        'requirements.txt'
    ]
    
    missing_items = []
    
    # 检查目录
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ - 目录不存在")
            missing_items.append(dir_name)
    
    # 检查文件
    for file_name in required_files:
        if os.path.isfile(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - 文件不存在")
            missing_items.append(file_name)
    
    if missing_items:
        print(f"\n缺失的项目文件/目录: {', '.join(missing_items)}")
        return False
    else:
        print("\n✅ 项目结构完整")
        return True

def main():
    """主函数"""
    print("DH_live 环境检查工具")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_project_structure(),
        check_dependencies(),
        check_model_files()
    ]
    
    print("\n" + "=" * 50)
    print("检查结果汇总:")
    
    if all(checks):
        print("🎉 所有检查通过！可以运行项目了")
        print("\n运行命令:")
        print("  python app.py")
        return True
    else:
        print("❌ 存在问题，请根据上述提示解决")
        print("\n常见解决方案:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 下载模型: 参考 Anaconda运行指南.md")
        print("  3. 检查Python版本: 推荐使用Python 3.8-3.11")
        return False

if __name__ == "__main__":
    main()