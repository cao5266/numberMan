#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动化视频处理脚本
从指定目录的原始视频生成Web演示所需的所有数据文件

使用方法:
    python process_video.py <视频文件路径> [角色名称]
    
示例:
    python process_video.py D:/videos/person.mp4 my_character
    python process_video.py ./raw_videos/person.mp4
"""

import sys
import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime


def check_requirements():
    """检查必要的文件和依赖"""
    print("🔍 检查环境要求...")
    
    # 检查FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            print("  ✅ FFmpeg 已安装")
        else:
            print("  ❌ FFmpeg 未正确安装")
            return False
    except Exception as e:
        print(f"  ❌ FFmpeg 检查失败: {e}")
        print("  请确保 FFmpeg 已安装并添加到系统 PATH")
        return False
    
    # 检查必要的脚本文件
    required_scripts = [
        'data_preparation_mini.py',
        'data_preparation_web.py'
    ]
    
    for script in required_scripts:
        if not os.path.exists(script):
            print(f"  ❌ 缺少必要文件: {script}")
            return False
        else:
            print(f"  ✅ 找到脚本: {script}")
    
    # 检查模型文件
    model_path = 'checkpoint/DINet_mini/epoch_40.pth'
    if not os.path.exists(model_path):
        print(f"  ⚠️  模型文件不存在: {model_path}")
        print("  继续执行，但可能会在后续步骤中失败")
    else:
        print(f"  ✅ 找到模型文件")
    
    return True


def get_character_name(video_path, custom_name=None):
    """生成角色名称"""
    if custom_name:
        return custom_name
    
    # 使用视频文件名（不含扩展名）+ 时间戳
    video_name = Path(video_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{video_name}_{timestamp}"


def process_video(video_path, character_name=None, auto_update_html=False):
    """
    自动化处理视频文件
    
    参数:
        video_path: 输入视频文件路径
        character_name: 角色名称（可选，默认使用视频文件名）
        auto_update_html: 是否自动更新HTML文件（默认False）
    
    返回:
        成功返回True，失败返回False
    """
    
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"📹 开始处理视频: {video_path}")
    print(f"{'='*60}\n")
    
    # 生成角色名称
    character_name = get_character_name(video_path, character_name)
    print(f"📝 角色名称: {character_name}\n")
    
    # 定义路径
    video_data_dir = f"video_data/{character_name}"
    web_static_dir = f"web_demo/static/{character_name}"
    
    try:
        # ============================================================
        # 步骤1: 预处理视频
        # ============================================================
        print(f"{'='*60}")
        print("🔄 步骤1: 预处理视频 (生成 processed.mp4 和 processed.pkl)")
        print(f"{'='*60}")
        
        from data_preparation_mini import data_preparation_mini
        
        print(f"输入视频: {video_path}")
        print(f"输出目录: {video_data_dir}")
        print("开始处理...\n")
        
        data_preparation_mini(video_path, video_data_dir)
        
        # 验证输出文件
        processed_mp4 = os.path.join(video_data_dir, "data", "processed.mp4")
        processed_pkl = os.path.join(video_data_dir, "data", "processed.pkl")
        
        if not os.path.exists(processed_mp4) or not os.path.exists(processed_pkl):
            print("❌ 步骤1失败: 未生成必要的文件")
            return False
        
        print("\n✅ 步骤1完成!")
        print(f"  - {processed_mp4}")
        print(f"  - {processed_pkl}\n")
        
        # ============================================================
        # 步骤2: 生成Web资源
        # ============================================================
        print(f"{'='*60}")
        print("🔄 步骤2: 生成Web资源 (生成 01.mp4 和 combined_data.json.gz)")
        print(f"{'='*60}")
        
        from data_preparation_web import data_preparation_web
        
        print(f"处理目录: {video_data_dir}")
        print("开始生成Web资源...\n")
        
        data_preparation_web(video_data_dir)
        
        # 验证输出文件
        assets_mp4 = os.path.join(video_data_dir, "assets", "01.mp4")
        assets_json = os.path.join(video_data_dir, "assets", "combined_data.json.gz")
        
        if not os.path.exists(assets_mp4) or not os.path.exists(assets_json):
            print("❌ 步骤2失败: 未生成必要的Web资源文件")
            return False
        
        print("\n✅ 步骤2完成!")
        print(f"  - {assets_mp4}")
        print(f"  - {assets_json}\n")
        
        # ============================================================
        # 步骤3: 复制到Web目录
        # ============================================================
        print(f"{'='*60}")
        print("🔄 步骤3: 复制文件到Web目录")
        print(f"{'='*60}")
        
        # 创建Web目录
        os.makedirs(web_static_dir, exist_ok=True)
        print(f"创建目录: {web_static_dir}")
        
        # 复制文件
        web_mp4 = os.path.join(web_static_dir, "01.mp4")
        web_json = os.path.join(web_static_dir, "combined_data.json.gz")
        
        shutil.copy2(assets_mp4, web_mp4)
        shutil.copy2(assets_json, web_json)
        
        print(f"复制文件:")
        print(f"  - {web_mp4}")
        print(f"  - {web_json}")
        
        print("\n✅ 步骤3完成!\n")
        
        # ============================================================
        # 步骤4: 更新HTML文件（可选）
        # ============================================================
        print(f"{'='*60}")
        print("🔄 步骤4: 更新HTML文件")
        print(f"{'='*60}")
        
        html_file = "web_demo/static/MiniLive_new.html"
        
        if auto_update_html and os.path.exists(html_file):
            try:
                # 读取HTML文件
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # 检查是否已存在该选项
                if f'value="{character_name}"' in html_content:
                    print(f"⚠️  HTML中已存在角色选项: {character_name}")
                else:
                    # 查找 select 标签的结束位置
                    select_end = html_content.find('</select>')
                    if select_end != -1:
                        # 在结束标签前插入新选项
                        new_option = f'    <option value="{character_name}">{character_name}</option>\n'
                        new_content = html_content[:select_end] + new_option + html_content[select_end:]
                        
                        # 写回文件
                        with open(html_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ 已自动添加角色选项到HTML文件")
                    else:
                        print("⚠️  未找到 <select> 标签，请手动添加")
            except Exception as e:
                print(f"⚠️  自动更新HTML失败: {e}")
                print("请手动更新HTML文件")
        else:
            print("📝 需要手动更新HTML文件:")
            print(f"\n在 {html_file} 的 <select id=\"characterDropdown\"> 中添加:")
            print(f'<option value="{character_name}">{character_name}</option>')
        
        print("\n✅ 步骤4完成!\n")
        
        # ============================================================
        # 完成总结
        # ============================================================
        print(f"{'='*60}")
        print("🎉 处理完成!")
        print(f"{'='*60}")
        print(f"\n角色名称: {character_name}")
        print(f"Web资源目录: {web_static_dir}")
        print(f"\n生成的文件:")
        print(f"  - {web_mp4}")
        print(f"  - {web_json}")
        
        if not auto_update_html:
            print(f"\n⚠️  请记得在HTML文件中添加角色选项:")
            print(f'<option value="{character_name}">{character_name}</option>')
        
        print(f"\n{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def batch_process(video_dir, auto_update_html=False):
    """
    批量处理目录下的所有视频文件
    
    参数:
        video_dir: 视频文件目录
        auto_update_html: 是否自动更新HTML
    """
    print(f"\n📁 批量处理目录: {video_dir}\n")
    
    # 支持的视频格式
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    
    # 查找所有视频文件
    video_files = []
    for ext in video_extensions:
        video_files.extend(Path(video_dir).glob(f'*{ext}'))
    
    if not video_files:
        print(f"❌ 目录中没有找到视频文件: {video_dir}")
        return
    
    print(f"找到 {len(video_files)} 个视频文件:\n")
    for i, video_file in enumerate(video_files, 1):
        print(f"{i}. {video_file.name}")
    print()
    
    # 处理每个视频
    success_count = 0
    failed_count = 0
    
    for i, video_file in enumerate(video_files, 1):
        print(f"\n{'#'*60}")
        print(f"处理第 {i}/{len(video_files)} 个视频")
        print(f"{'#'*60}\n")
        
        result = process_video(str(video_file), auto_update_html=auto_update_html)
        
        if result:
            success_count += 1
        else:
            failed_count += 1
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("批量处理完成!")
    print(f"{'='*60}")
    print(f"总计: {len(video_files)} 个视频")
    print(f"成功: {success_count} 个")
    print(f"失败: {failed_count} 个")
    print(f"{'='*60}\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='自动化视频处理脚本 - 从原始视频生成Web演示数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 处理单个视频（自动生成角色名）
  python process_video.py D:/videos/person.mp4
  
  # 处理单个视频（指定角色名）
  python process_video.py D:/videos/person.mp4 --name my_character
  
  # 处理单个视频并自动更新HTML
  python process_video.py D:/videos/person.mp4 --name my_character --auto-html
  
  # 批量处理目录下的所有视频
  python process_video.py --batch D:/videos/
  
  # 批量处理并自动更新HTML
  python process_video.py --batch D:/videos/ --auto-html
        """
    )
    
    parser.add_argument('video_path', nargs='?', help='视频文件路径')
    parser.add_argument('--name', '-n', help='角色名称（可选，默认使用视频文件名）')
    parser.add_argument('--auto-html', '-a', action='store_true', 
                       help='自动更新HTML文件')
    parser.add_argument('--batch', '-b', metavar='DIR', 
                       help='批量处理模式，指定视频文件目录')
    parser.add_argument('--no-check', action='store_true',
                       help='跳过环境检查')
    
    args = parser.parse_args()
    
    # 显示欢迎信息
    print("\n" + "="*60)
    print("  视频自动化处理脚本 v1.0")
    print("  从原始视频生成Web演示所需的所有数据")
    print("="*60 + "\n")
    
    # 检查环境
    if not args.no_check:
        if not check_requirements():
            print("\n❌ 环境检查失败，请先解决上述问题")
            sys.exit(1)
        print()
    
    # 批量处理模式
    if args.batch:
        batch_process(args.batch, args.auto_html)
        return
    
    # 单文件处理模式
    if not args.video_path:
        parser.print_help()
        print("\n❌ 错误: 请提供视频文件路径或使用 --batch 指定目录")
        sys.exit(1)
    
    # 处理视频
    result = process_video(
        args.video_path, 
        args.name,
        args.auto_html
    )
    
    if result:
        print("✅ 所有步骤执行成功!")
        sys.exit(0)
    else:
        print("❌ 处理过程中出现错误")
        sys.exit(1)


if __name__ == "__main__":
    main()
