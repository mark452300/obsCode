#!/usr/bin/env python3
"""
输入类型数据保存示例

演示如何将输入类型数据保存到 download 目录
"""

import sys
import os
import json

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def save_input_data_examples():
    """保存输入类型数据的各种示例"""
    
    print("💾 输入类型数据保存示例")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            print("✅ 已连接到 OBS")
            
            # 示例1: 默认保存（保存到 download/input_kinds.json）
            print("\n📁 示例1: 默认保存路径")
            default_file = obs.save_input_kinds()
            print(f"   保存到: {default_file}")
            
            # 示例2: 保存到 download 目录的子文件夹
            print("\n📁 示例2: download 子目录")
            config_file = obs.save_input_kinds("download/config/obs_input_types.json")
            print(f"   保存到: {config_file}")
            
            # 示例3: 按日期分类保存
            from datetime import datetime
            date_str = datetime.now().strftime("%Y%m%d")
            dated_file = obs.save_input_kinds(f"download/daily/{date_str}_input_kinds.json")
            print(f"   保存到: {dated_file}")
            
            # 示例4: 按 OBS 版本保存
            version = obs.get_version().get('obsVersion', 'unknown').replace('.', '_')
            version_file = obs.save_input_kinds(f"download/versions/obs_{version}_input_kinds.json")
            print(f"   保存到: {version_file}")
            
            # 示例5: 备份文件
            backup_file = obs.save_input_kinds("download/backup/input_kinds_backup.json")
            print(f"   保存到: {backup_file}")
            
            print(f"\n✅ 所有文件已保存完成！")
            return default_file
            
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return None


def load_and_display_data(filepath: str):
    """加载并显示保存的数据"""
    
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n📖 从 {filepath} 加载的数据:")
        print(f"   保存时间: {data['metadata']['timestamp']}")
        print(f"   总输入类型: {data['metadata']['total_kinds']} 种")
        print(f"   当前输入源: {data['metadata']['current_inputs_count']} 个")
        
        # 显示分类统计
        print(f"\n📊 分类统计:")
        stats = data['statistics']
        print(f"   • 音频类型: {stats['audio_types_count']} 种")
        print(f"   • 视频/媒体类型: {stats['video_types_count']} 种")
        print(f"   • 捕获类型: {stats['capture_types_count']} 种")
        print(f"   • 其他类型: {stats['other_types_count']} 种")
        
        # 显示音频类型
        print(f"\n🎵 音频类型:")
        for audio_type in data['input_kinds']['by_category']['audio']:
            print(f"   • {audio_type}")
        
        # 显示当前输入源
        print(f"\n📝 当前输入源:")
        for input_name in data['current_inputs']:
            print(f"   • {input_name}")
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")


def show_download_directory_structure():
    """显示 download 目录结构"""
    
    print(f"\n📁 download 目录结构:")
    
    download_dir = "download"
    if not os.path.exists(download_dir):
        print(f"   {download_dir}/ (目录不存在)")
        return
    
    def show_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(os.listdir(directory))
            for i, item in enumerate(items):
                if item.startswith('.'):
                    continue
                    
                item_path = os.path.join(directory, item)
                is_last = i == len(items) - 1
                
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item}")
                
                if os.path.isdir(item_path) and current_depth < max_depth - 1:
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    show_tree(item_path, next_prefix, max_depth, current_depth + 1)
        except PermissionError:
            pass
    
    print(f"   {download_dir}/")
    show_tree(download_dir, "   ")


def practical_usage_tips():
    """实用使用技巧"""
    
    print(f"\n💡 实用技巧:")
    print(f"   1. 默认保存: obs.save_input_kinds()")
    print(f"   2. 按日期保存: obs.save_input_kinds('download/daily/20250812_input_kinds.json')")
    print(f"   3. 按版本保存: obs.save_input_kinds('download/versions/obs_31_1_2.json')")
    print(f"   4. 配置备份: obs.save_input_kinds('download/backup/config_backup.json')")
    print(f"   5. 开发环境: obs.save_input_kinds('download/dev/dev_config.json')")
    
    print(f"\n📋 推荐目录结构:")
    print(f"   download/")
    print(f"   ├── input_kinds.json          # 默认文件")
    print(f"   ├── config/                   # 配置文件")
    print(f"   ├── daily/                    # 按日期保存")
    print(f"   ├── versions/                 # 按版本保存")
    print(f"   ├── backup/                   # 备份文件")
    print(f"   └── dev/                      # 开发环境")


if __name__ == "__main__":
    # 保存数据示例
    saved_file = save_input_data_examples()
    
    if saved_file:
        # 加载并显示数据
        load_and_display_data(saved_file)
        
        # 显示目录结构
        show_download_directory_structure()
        
        # 显示使用技巧
        practical_usage_tips()
    
    print("\n✅ 示例完成!")
    print(f"💾 所有文件都保存在 download 目录下")
