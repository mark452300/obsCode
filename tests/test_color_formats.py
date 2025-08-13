#!/usr/bin/env python3
"""
颜色格式测试

测试不同的颜色格式在 OBS 中的显示效果
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def test_color_formats():
    """测试不同的颜色格式"""
    print("🎨 测试不同的颜色格式")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            
            # 定义要测试的红色格式
            red_formats = [
                ("RGB_HEX", 0xFF0000),           # 标准 RGB 十六进制
                ("RGB_DEC", 16711680),           # 标准 RGB 十进制
                ("BGR_HEX", 0x0000FF),           # BGR 格式
                ("BGR_DEC", 255),                # BGR 十进制
                ("ARGB_HEX", 0xFFFF0000),        # ARGB 格式
                ("RGBA_HEX", 0xFF0000FF),        # RGBA 格式
                ("ABGR_HEX", 0xFF0000FF),        # ABGR 格式
            ]
            
            print("创建不同颜色格式的文本输入源:")
            created_inputs = []
            
            for format_name, color_value in red_formats:
                test_name = f"红色测试_{format_name}_{int(time.time())}"
                
                print(f"\n测试 {format_name}: {color_value} (0x{color_value:08X})")
                
                try:
                    result = obs.inputs.create_input(
                        input_name=test_name,
                        input_kind="text_gdiplus_v3",
                        scene_name=test_scene,
                        input_settings={
                            "text": f"红色 {format_name}",
                            "color": color_value,
                            "align": "center",
                            "valign": "center",
                            "font": {
                                "face": "微软雅黑",
                                "size": 48
                            }
                        }
                    )
                    
                    if result.get('success'):
                        print(f"✅ 创建成功: {test_name}")
                        created_inputs.append(test_name)
                    else:
                        print(f"❌ 创建失败")
                        
                except Exception as e:
                    print(f"❌ 创建异常: {e}")
            
            print(f"\n🎯 请在 OBS 中查看这些文本的颜色:")
            for name in created_inputs:
                print(f"  - {name}")
            
            print(f"\n⚠️ 注意: 测试输入源未被自动删除，请手动清理或运行清理脚本")
            
            return len(created_inputs) > 0
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_specific_colors():
    """测试特定颜色值"""
    print("\n🌈 测试特定颜色值")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            
            # 测试您想要的粉红色 #ff557f
            pink_formats = [
                ("粉色_RGB", 0xff557f),          # 您想要的颜色
                ("粉色_BGR", 0x7f55ff),          # BGR 格式
                ("粉色_DEC", 16733567),          # 十进制
                ("粉色_ARGB", 0xFFff557f),       # ARGB 格式
            ]
            
            print("创建粉红色测试:")
            created_inputs = []
            
            for format_name, color_value in pink_formats:
                test_name = f"粉色测试_{format_name}_{int(time.time())}"
                
                print(f"\n测试 {format_name}: {color_value} (0x{color_value:08X})")
                
                try:
                    result = obs.inputs.create_input(
                        input_name=test_name,
                        input_kind="text_gdiplus_v3",
                        scene_name=test_scene,
                        input_settings={
                            "text": f"粉色 {format_name}",
                            "color": color_value,
                            "align": "center",
                            "valign": "center",
                            "font": {
                                "face": "微软雅黑",
                                "size": 36
                            }
                        }
                    )
                    
                    if result.get('success'):
                        print(f"✅ 创建成功: {test_name}")
                        created_inputs.append(test_name)
                    else:
                        print(f"❌ 创建失败")
                        
                except Exception as e:
                    print(f"❌ 创建异常: {e}")
            
            return len(created_inputs) > 0
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def get_default_color():
    """获取默认颜色值"""
    print("\n🔍 获取默认颜色值")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 获取文本输入源的默认设置
            defaults = obs.inputs.get_input_default_settings("text_gdiplus_v3")
            
            if 'color' in defaults:
                default_color = defaults['color']
                print(f"默认颜色值: {default_color}")
                print(f"十六进制: 0x{default_color:08X}")
                print(f"二进制: {bin(default_color)}")
                
                # 分解颜色分量 (假设是 RGB)
                r = (default_color >> 16) & 0xFF
                g = (default_color >> 8) & 0xFF
                b = default_color & 0xFF
                print(f"RGB 分量: R={r}, G={g}, B={b}")
                
                # 分解颜色分量 (假设是 BGR)
                b_bgr = (default_color >> 16) & 0xFF
                g_bgr = (default_color >> 8) & 0xFF
                r_bgr = default_color & 0xFF
                print(f"BGR 分量: B={b_bgr}, G={g_bgr}, R={r_bgr}")
                
                return True
            else:
                print("❌ 默认设置中没有颜色信息")
                return False
                
    except Exception as e:
        print(f"❌ 获取默认颜色失败: {e}")
        return False


def cleanup_test_inputs():
    """清理测试输入源"""
    print("\n🧹 清理测试输入源")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            all_inputs = obs.inputs.get_names()
            
            # 查找测试输入源
            test_inputs = [name for name in all_inputs if '测试_' in name or 'Test_' in name]
            
            if not test_inputs:
                print("没有找到测试输入源")
                return True
            
            print(f"找到 {len(test_inputs)} 个测试输入源:")
            
            cleaned = 0
            for name in test_inputs:
                try:
                    if obs.inputs.remove_input(input_name=name):
                        print(f"✅ 删除: {name}")
                        cleaned += 1
                    else:
                        print(f"❌ 删除失败: {name}")
                except Exception as e:
                    print(f"❌ 删除异常 {name}: {e}")
            
            print(f"清理完成: {cleaned}/{len(test_inputs)}")
            return cleaned > 0
            
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始颜色格式测试...")
    print("=" * 60)
    
    tests = [
        ("获取默认颜色值", get_default_color),
        ("测试不同颜色格式", test_color_formats),
        ("测试特定颜色值", test_specific_colors),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} 测试通过")
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    print(f"\n{'='*60}")
    print(f"测试结果: {passed}/{total} 通过")
    print(f"{'='*60}")
    
    # 询问是否清理
    print(f"\n是否要清理测试输入源? (输入 'y' 确认)")
    try:
        response = input().strip().lower()
        if response == 'y':
            cleanup_test_inputs()
    except:
        pass
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
