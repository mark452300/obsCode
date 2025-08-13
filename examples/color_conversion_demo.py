#!/usr/bin/env python3
"""
OBS 颜色转换演示

演示如何正确设置 OBS 输入源的颜色（BGR 格式）
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def demo_color_conversion():
    """演示颜色转换"""
    print("🎨 OBS 颜色转换演示")
    print("=" * 50)
    
    # 常用颜色的 RGB 和对应的 BGR 值
    colors = {
        "红色": {"rgb": 0xFF0000, "name": "Red"},
        "绿色": {"rgb": 0x00FF00, "name": "Green"},
        "蓝色": {"rgb": 0x0000FF, "name": "Blue"},
        "黄色": {"rgb": 0xFFFF00, "name": "Yellow"},
        "紫色": {"rgb": 0xFF00FF, "name": "Magenta"},
        "青色": {"rgb": 0x00FFFF, "name": "Cyan"},
        "白色": {"rgb": 0xFFFFFF, "name": "White"},
        "黑色": {"rgb": 0x000000, "name": "Black"},
        "粉红色": {"rgb": 0xFF557F, "name": "Pink"},
        "橙色": {"rgb": 0xFF8000, "name": "Orange"},
    }
    
    print("颜色转换对照表:")
    print("-" * 70)
    print(f"{'颜色':<8} {'RGB (网页)':<12} {'BGR (OBS)':<12} {'RGB分量':<15} {'BGR分量'}")
    print("-" * 70)
    
    for color_name, color_info in colors.items():
        rgb_color = color_info["rgb"]
        
        # 使用我们的转换函数
        from obs_sdk.utils import ColorUtils
        bgr_color = ColorUtils.rgb_to_bgr(rgb_color)
        
        # 分解 RGB 分量
        r = (rgb_color >> 16) & 0xFF
        g = (rgb_color >> 8) & 0xFF
        b = rgb_color & 0xFF
        
        # 分解 BGR 分量
        b_bgr = (bgr_color >> 16) & 0xFF
        g_bgr = (bgr_color >> 8) & 0xFF
        r_bgr = bgr_color & 0xFF
        
        print(f"{color_name:<8} 0x{rgb_color:06X}    0x{bgr_color:06X}    ({r:3},{g:3},{b:3})     ({r_bgr:3},{g_bgr:3},{b_bgr:3})")


def demo_create_colored_text():
    """演示创建彩色文本"""
    print("\n🌈 创建彩色文本演示")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            
            # 定义要创建的彩色文本
            colored_texts = [
                {"name": "红色文本", "rgb": 0xFF0000, "text": "这是红色文本"},
                {"name": "绿色文本", "rgb": 0x00FF00, "text": "这是绿色文本"},
                {"name": "蓝色文本", "rgb": 0x0000FF, "text": "这是蓝色文本"},
                {"name": "粉红色文本", "rgb": 0xFF557F, "text": "这是粉红色文本"},
            ]
            
            created_inputs = []
            
            for item in colored_texts:
                # 转换颜色格式
                from obs_sdk.utils import ColorUtils
                bgr_color = ColorUtils.rgb_to_bgr(item["rgb"])
                
                test_name = f"{item['name']}_{int(time.time())}"
                
                print(f"创建 {item['name']}:")
                print(f"  RGB: 0x{item['rgb']:06X}")
                print(f"  BGR: 0x{bgr_color:06X}")
                
                try:
                    result = obs.inputs.create_input(
                        input_name=test_name,
                        input_kind="text_gdiplus_v3",
                        scene_name=test_scene,
                        input_settings={
                            "text": item["text"],
                            "color": bgr_color,  # 使用 BGR 格式
                            "align": "center",
                            "valign": "center",
                            "font": {
                                "face": "微软雅黑",
                                "size": 36
                            }
                        }
                    )
                    
                    if result.get('success'):
                        print(f"  ✅ 创建成功: {test_name}")
                        created_inputs.append(test_name)
                    else:
                        print(f"  ❌ 创建失败")
                        
                except Exception as e:
                    print(f"  ❌ 创建异常: {e}")
            
            if created_inputs:
                print(f"\n🎯 成功创建了 {len(created_inputs)} 个彩色文本输入源")
                print("请在 OBS 中查看颜色效果!")
                
                # 询问是否清理
                print(f"\n是否要删除这些测试输入源? (输入 'y' 确认)")
                try:
                    response = input().strip().lower()
                    if response == 'y':
                        for name in created_inputs:
                            obs.inputs.remove_input(input_name=name)
                            print(f"🧹 删除: {name}")
                        print("清理完成!")
                except:
                    print("⚠️ 测试输入源未被删除，请手动清理")
            
            return len(created_inputs) > 0
            
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False


def demo_color_functions():
    """演示颜色转换函数"""
    print("\n🔧 颜色转换函数演示")
    print("=" * 50)
    
    from obs_sdk.utils import ColorUtils

    # 演示 RGB 到 BGR 转换
    print("1. RGB 到 BGR 转换:")
    rgb_colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFF557F]

    for rgb in rgb_colors:
        bgr = ColorUtils.rgb_to_bgr(rgb)
        print(f"   RGB 0x{rgb:06X} -> BGR 0x{bgr:06X}")

    # 演示 BGR 到 RGB 转换
    print("\n2. BGR 到 RGB 转换:")
    bgr_colors = [0x0000FF, 0x00FF00, 0xFF0000, 0x7F55FF]

    for bgr in bgr_colors:
        rgb = ColorUtils.bgr_to_rgb(bgr)
        print(f"   BGR 0x{bgr:06X} -> RGB 0x{rgb:06X}")

    # 演示 RGB 分量到 BGR 转换
    print("\n3. RGB 分量到 BGR 转换:")
    rgb_components = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 85, 127)]

    for r, g, b in rgb_components:
        bgr = ColorUtils.rgb_values_to_bgr(r, g, b)
        print(f"   RGB({r}, {g}, {b}) -> BGR 0x{bgr:06X}")


def main():
    """主演示函数"""
    print("🚀 OBS 颜色转换完整演示")
    print("=" * 60)
    
    demos = [
        demo_color_conversion,
        demo_color_functions,
        demo_create_colored_text,
    ]
    
    for demo_func in demos:
        try:
            demo_func()
            print()  # 空行分隔
        except Exception as e:
            print(f"❌ 演示 {demo_func.__name__} 失败: {e}")
    
    print("✅ 演示完成")
    print("\n💡 重要提示:")
    print("- OBS 使用 BGR 颜色格式，不是标准的 RGB")
    print("- 使用 ColorUtils.rgb_to_bgr() 转换网页颜色到 OBS 格式")
    print("- 例如: 网页红色 #FF0000 在 OBS 中应该使用 0x0000FF")


if __name__ == "__main__":
    main()
