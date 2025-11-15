#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从视频生成完整人物数据的自动化脚本

用法:
    python generate_character.py <输入视频> <输出名称> [Web文件夹名称]

示例:
    python generate_character.py person.mp4 person_001
    python generate_character.py person.mp4 person_001 my_character
"""

import sys
import os
import shutil
from pathlib import Path

def generate_character(input_video, output_name, web_folder_name=None):
    """
    从视频生成完整的人物数据
    
    参数:
        input_video: 输入视频文件路径
        output_name: 输出目录名称（在video_data下）
        web_folder_name: Web资源文件夹名称（默认与output_name相同）
    """
    if web_folder_name is None:
        web_folder_name = output_name
    
    print("=" * 60)
    print("从视频生成人物数据")
    print("=" * 60)
    print(f"输入视频: {input_video}")
    print(f"输出目录: video_data/{output_name}")
    print(f"Web文件夹: web_demo/static/{web_folder_name}")
    print("=" * 60)
    
    # 检查输入视频是否存在
    if not os.path.exists(input_video):
        print(f"❌ 错误: 输入视频文件不存在: {input_video}")
        return False
    
    # 检查模型文件
    model_path = "checkpoint/DINet_mini/epoch_40.pth"
    if not os.path.exists(model_path):
        print(f"❌ 错误: 模型文件不存在: {model_path}")
        print("   请先下载模型文件！")
        return False
    
    try:
        # 步骤1：预处理视频
        print("\n" + "=" * 60)
        print("步骤1: 预处理视频...")
        print("=" * 60)
        from data_preparation_mini import data_preparation_mini
        
        video_dir_path = f"video_data/{output_name}"
        result = data_preparation_mini(input_video, video_dir_path)
        
        if result.get("status") != "success":
            print("❌ 步骤1失败！")
            return False
        
        print("✅ 步骤1完成！")
        print(f"   输出视频: {result['output_video']}")
        print(f"   输出数据: {result['output_pkl']}")
        
        # 步骤2：生成Web资源
        print("\n" + "=" * 60)
        print("步骤2: 生成Web资源...")
        print("=" * 60)
        from data_preparation_web import data_preparation_web
        
        data_preparation_web(video_dir_path)
        
        # 检查输出文件
        assets_dir = f"{video_dir_path}/assets"
        mp4_path = f"{assets_dir}/01.mp4"
        json_path = f"{assets_dir}/combined_data.json.gz"
        
        if not os.path.exists(mp4_path):
            print(f"❌ 错误: 视频文件未生成: {mp4_path}")
            return False
        
        if not os.path.exists(json_path):
            print(f"❌ 错误: JSON文件未生成: {json_path}")
            return False
        
        print("✅ 步骤2完成！")
        print(f"   视频文件: {mp4_path}")
        print(f"   数据文件: {json_path}")
        
        # 步骤3：复制到Web目录
        print("\n" + "=" * 60)
        print("步骤3: 复制到Web目录...")
        print("=" * 60)
        
        web_dir = f"web_demo/static/{web_folder_name}"
        os.makedirs(web_dir, exist_ok=True)
        
        # 复制文件
        shutil.copy(mp4_path, f"{web_dir}/01.mp4")
        shutil.copy(json_path, f"{web_dir}/combined_data.json.gz")
        
        print("✅ 步骤3完成！")
        print(f"   Web目录: {web_dir}")
        
        # 步骤4：提示修改HTML
        print("\n" + "=" * 60)
        print("步骤4: 需要手动修改HTML文件")
        print("=" * 60)
        print(f"请在 web_demo/static/MiniLive_new.html 中添加：")
        print(f'    <option value="{web_folder_name}">角色名称</option>')
        print("\n或者在 web_demo/static/MiniLive_RealTime.html 中添加：")
        print(f'    <option value="{web_folder_name}">角色名称</option>')
        print("=" * 60)
        
        # 完成
        print("\n" + "=" * 60)
        print("✅ 所有步骤完成！")
        print("=" * 60)
        print(f"Web资源已保存到: {web_dir}")
        print(f"下一步: 修改HTML文件并刷新浏览器")
        print("=" * 60)
        
        return True
        
    except ImportError as e:
        print(f"❌ 错误: 导入模块失败: {e}")
        print("   请确保已安装所有依赖包")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python generate_character.py <输入视频> <输出名称> [Web文件夹名称]")
        print("\n参数说明:")
        print("  输入视频: 要处理的视频文件路径")
        print("  输出名称: 输出目录名称（在video_data下）")
        print("  Web文件夹名称: Web资源文件夹名称（可选，默认与输出名称相同）")
        print("\n示例:")
        print("  python generate_character.py person.mp4 person_001")
        print("  python generate_character.py person.mp4 person_001 my_character")
        sys.exit(1)
    
    input_video = sys.argv[1]
    output_name = sys.argv[2]
    web_folder_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = generate_character(input_video, output_name, web_folder_name)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

