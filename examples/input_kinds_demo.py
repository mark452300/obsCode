#!/usr/bin/env python3
"""
输入类型列表功能示例

演示如何使用 get_input_kinds() 方法获取 OBS 支持的所有输入类型
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def main():
    """主函数"""
    
    print("🎬 OBS 输入类型列表示例")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            print("✅ 已连接到 OBS")
            
            # 1. 获取输入类型列表（带版本）
            print("\n📋 可用的输入类型（带版本）:")
            input_kinds_versioned = obs.get_input_kinds(unversioned=False)
            
            # 按类别分组显示
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
            
            print(f"\n🎵 音频类型 ({len(audio_types)} 种):")
            for audio_type in audio_types:
                print(f"   • {audio_type}")
            
            print(f"\n🎥 视频/媒体类型 ({len(video_types)} 种):")
            for video_type in video_types:
                print(f"   • {video_type}")
            
            print(f"\n📹 捕获类型 ({len(capture_types)} 种):")
            for capture_type in capture_types:
                print(f"   • {capture_type}")
            
            if other_types:
                print(f"\n🔧 其他类型 ({len(other_types)} 种):")
                for other_type in other_types:
                    print(f"   • {other_type}")
            
            # 2. 对比当前使用的输入源
            print(f"\n📝 当前 OBS 中的输入源:")
            current_inputs = obs.get_inputs()
            
            if current_inputs:
                for i, input_name in enumerate(current_inputs, 1):
                    print(f"   {i}. {input_name}")
            else:
                print("   (没有找到输入源)")
            
            # 3. 显示统计信息
            print(f"\n📊 统计信息:")
            print(f"   • 系统支持的输入类型: {len(input_kinds_versioned)} 种")
            print(f"   • 当前创建的输入源: {len(current_inputs)} 个")
            
            # 4. 获取无版本的输入类型（用于创建源时使用）
            print(f"\n🔧 无版本输入类型（用于创建源）:")
            input_kinds_unversioned = obs.get_input_kinds(unversioned=True)
            
            # 显示版本差异示例
            print(f"\n💡 版本对比示例:")
            for versioned, unversioned in zip(input_kinds_versioned[:3], input_kinds_unversioned[:3]):
                if versioned != unversioned:
                    print(f"   带版本: {versioned}")
                    print(f"   无版本: {unversioned}")
                    print()
            
            print("✅ 示例完成!")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请确保:")
        print("  1. OBS Studio 正在运行")
        print("  2. obs-websocket 插件已启用")
        print("  3. 连接配置正确")


if __name__ == "__main__":
    main()
