#!/usr/bin/env python3
"""
将输入类型数据保存为 JSON 格式

JSON 格式适合：
- 数据交换
- 配置文件
- Web API
- 跨语言使用
"""

import sys
import os
import json
from datetime import datetime

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def save_input_kinds_to_json():
    """将输入类型数据保存为 JSON 格式"""
    
    print("📋 获取输入类型数据并保存为 JSON...")
    
    try:
        with OBSManager() as obs:
            # 获取输入类型数据
            input_kinds_versioned = obs.get_input_kinds(unversioned=False)
            input_kinds_unversioned = obs.get_input_kinds(unversioned=True)
            current_inputs = obs.get_inputs()
            
            # 按类别分组
            audio_types = []
            video_types = []
            capture_types = []
            other_types = []
            
            for kind in input_kinds_versioned:
                if 'audio' in kind.lower() or 'wasapi' in kind.lower():
                    audio_types.append(kind)
                elif 'capture' in kind.lower():
                    capture_types.append(kind)
                elif any(x in kind.lower() for x in ['image', 'video', 'ffmpeg', 'text', 'browser', 'color']):
                    video_types.append(kind)
                else:
                    other_types.append(kind)
            
            # 构建数据结构
            data = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "obs_version": obs.get_version().get('obsVersion', 'Unknown'),
                    "websocket_version": obs.get_version().get('obsWebSocketVersion', 'Unknown'),
                    "total_kinds": len(input_kinds_versioned),
                    "current_inputs_count": len(current_inputs)
                },
                "input_kinds": {
                    "versioned": input_kinds_versioned,
                    "unversioned": input_kinds_unversioned,
                    "by_category": {
                        "audio": audio_types,
                        "video_media": video_types,
                        "capture": capture_types,
                        "other": other_types
                    }
                },
                "current_inputs": current_inputs,
                "statistics": {
                    "audio_types_count": len(audio_types),
                    "video_types_count": len(video_types),
                    "capture_types_count": len(capture_types),
                    "other_types_count": len(other_types)
                }
            }
            
            # 保存到文件
            output_file = "data/input_kinds.json"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 数据已保存到: {output_file}")
            print(f"📊 统计信息:")
            print(f"   • 总输入类型: {len(input_kinds_versioned)} 种")
            print(f"   • 音频类型: {len(audio_types)} 种")
            print(f"   • 视频/媒体类型: {len(video_types)} 种")
            print(f"   • 捕获类型: {len(capture_types)} 种")
            print(f"   • 其他类型: {len(other_types)} 种")
            print(f"   • 当前输入源: {len(current_inputs)} 个")
            
            return output_file
            
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return None


def load_and_display_json():
    """加载并显示 JSON 数据"""
    
    json_file = "data/input_kinds.json"
    
    if not os.path.exists(json_file):
        print(f"❌ 文件不存在: {json_file}")
        return
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n📖 从 {json_file} 加载的数据:")
        print(f"   生成时间: {data['metadata']['timestamp']}")
        print(f"   OBS 版本: {data['metadata']['obs_version']}")
        
        print(f"\n🎵 音频类型 ({len(data['input_kinds']['by_category']['audio'])} 种):")
        for audio_type in data['input_kinds']['by_category']['audio']:
            print(f"   • {audio_type}")
        
        print(f"\n🎥 视频/媒体类型 ({len(data['input_kinds']['by_category']['video_media'])} 种):")
        for video_type in data['input_kinds']['by_category']['video_media']:
            print(f"   • {video_type}")
        
        print(f"\n📹 捕获类型 ({len(data['input_kinds']['by_category']['capture'])} 种):")
        for capture_type in data['input_kinds']['by_category']['capture']:
            print(f"   • {capture_type}")
        
        print(f"\n🔧 其他类型 ({len(data['input_kinds']['by_category']['other'])} 种):")
        for other_type in data['input_kinds']['by_category']['other']:
            print(f"   • {other_type}")
        
    except Exception as e:
        print(f"❌ 加载失败: {e}")


if __name__ == "__main__":
    print("💾 输入类型数据 JSON 保存示例")
    print("=" * 50)
    
    # 保存数据
    saved_file = save_input_kinds_to_json()
    
    if saved_file:
        # 加载并显示数据
        load_and_display_json()
    
    print("\n✅ 示例完成!")
