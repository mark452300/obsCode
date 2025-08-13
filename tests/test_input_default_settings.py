#!/usr/bin/env python3
"""
获取输入默认设置测试

专门测试 InputManager.get_input_default_settings() 方法的功能
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager
from obs_sdk.types.input_types import InputTypeHelper


def test_get_default_settings_basic():
    """测试基本获取默认设置功能"""
    print("⚙️ 测试基本获取默认设置功能")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 测试常见的输入类型
            test_types = [
                "text_gdiplus_v3",
                "image_source", 
                "color_source_v3",
                "browser_source"
            ]
            
            for input_type in test_types:
                print(f"\n测试输入类型: {input_type}")
                
                try:
                    settings = obs.inputs.get_input_default_settings(input_type)
                    
                    print(f"✅ 成功获取默认设置")
                    print(f"设置类型: {type(settings)}")
                    print(f"设置数量: {len(settings) if isinstance(settings, dict) else 'N/A'}")
                    
                    if isinstance(settings, dict) and settings:
                        print("主要设置项:")
                        for key, value in list(settings.items()):  # 只显示前5个
                            print(f"  {key}: {type(value).__name__}")
                    
                except Exception as e:
                    print(f"❌ 获取失败: {e}")
                    continue
            
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_default_settings_all_types():
    """测试所有可用输入类型的默认设置"""
    print("\n📋 测试所有可用输入类型的默认设置")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 获取所有可用的输入类型
            available_types = obs.inputs.get_input_kinds()
            print(f"发现 {len(available_types)} 种输入类型")
            
            success_count = 0
            failed_types = []
            
            for input_type in available_types:
                try:
                    settings = obs.inputs.get_input_default_settings(input_type)
                    chinese_name = InputTypeHelper.get_chinese_name(input_type)
                    
                    if isinstance(settings, dict):
                        print(f"✅ {chinese_name} ({input_type}): {len(settings)} 个设置项")
                        success_count += 1
                    else:
                        print(f"⚠️ {chinese_name} ({input_type}): 非字典类型")
                        
                except Exception as e:
                    chinese_name = InputTypeHelper.get_chinese_name(input_type)
                    print(f"❌ {chinese_name} ({input_type}): {e}")
                    failed_types.append(input_type)
            
            print(f"\n📊 统计结果:")
            print(f"成功: {success_count}/{len(available_types)}")
            print(f"失败: {len(failed_types)}")
            
            if failed_types:
                print(f"失败的类型: {failed_types}")
            
            return success_count > 0
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_get_default_settings_detailed():
    """测试详细的默认设置内容"""
    print("\n🔍 测试详细的默认设置内容")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 测试文本输入源的详细设置
            print("测试文本输入源 (text_gdiplus_v3):")
            text_settings = obs.inputs.get_input_default_settings("text_gdiplus_v3")
            
            if isinstance(text_settings, dict):
                print(f"✅ 获取到 {len(text_settings)} 个设置项")
                
                # 检查常见的文本设置项
                expected_keys = ["text", "font", "color", "align", "valign"]
                found_keys = []
                
                for key in expected_keys:
                    if key in text_settings:
                        found_keys.append(key)
                        value = text_settings[key]
                        print(f"  {key}: {type(value).__name__} = {value}")
                
                print(f"找到预期设置项: {found_keys}")
                
                # 显示所有设置项
                print(f"\n所有设置项:")
                for key, value in text_settings.items():
                    if isinstance(value, dict):
                        print(f"  {key}: {type(value).__name__} (包含 {len(value)} 个子项)")
                    else:
                        print(f"  {key}: {type(value).__name__} = {value}")
            
            # 测试颜色源的设置
            print(f"\n测试颜色源 (color_source_v3):")
            color_settings = obs.inputs.get_input_default_settings("color_source_v3")
            
            if isinstance(color_settings, dict):
                print(f"✅ 获取到 {len(color_settings)} 个设置项")
                for key, value in color_settings.items():
                    print(f"  {key}: {type(value).__name__} = {value}")
            
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_get_default_settings_error_handling():
    """测试错误处理"""
    print("\n🚫 测试错误处理")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 测试1: 空输入类型
            print("测试空输入类型...")
            try:
                obs.inputs.get_input_default_settings("")
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确抛出 ValueError: {e}")
            
            # 测试2: 无效的输入类型
            print("测试无效的输入类型...")
            try:
                settings = obs.inputs.get_input_default_settings("invalid_input_type")
                print(f"获取无效类型的结果: {settings}")
                # 某些情况下可能返回空字典而不是抛出异常
                print("✅ 处理无效类型正常")
            except Exception as e:
                print(f"✅ 抛出异常: {type(e).__name__}: {e}")
            
            # 测试3: None 输入类型
            print("测试 None 输入类型...")
            try:
                obs.inputs.get_input_default_settings(None)
                print("❌ 应该抛出异常")
                return False
            except (ValueError, TypeError) as e:
                print(f"✅ 正确抛出异常: {type(e).__name__}: {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False


def test_get_default_settings_practical():
    """测试实际应用场景"""
    print("\n💡 测试实际应用场景")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 场景1: 获取默认设置并创建输入源
            print("场景1: 使用默认设置创建输入源")
            
            # 获取文本输入源的默认设置
            default_settings = obs.inputs.get_input_default_settings("text_gdiplus_v3")
            
            if isinstance(default_settings, dict):
                print(f"✅ 获取到默认设置: {len(default_settings)} 项")
                
                # 修改部分设置
                custom_settings = default_settings.copy()
                custom_settings["text"] = "使用默认设置创建的文本"
                
                # 获取场景
                scenes = obs.scenes.get_names()
                if scenes:
                    test_name = f"默认设置测试_{int(time.time())}"
                    
                    # 创建输入源
                    result = obs.inputs.create_input(
                        input_name=test_name,
                        input_kind="text_gdiplus_v3",
                        scene_name=scenes[0],
                        input_settings=custom_settings
                    )
                    
                    if result.get('success'):
                        print(f"✅ 使用默认设置成功创建输入源: {test_name}")
                        
                        # 清理
                        obs.inputs.remove_input(input_name=test_name)
                        print("🧹 清理完成")
                    else:
                        print("❌ 创建输入源失败")
            
            # 场景2: 比较不同输入类型的默认设置
            print(f"\n场景2: 比较不同输入类型的默认设置")
            
            types_to_compare = ["text_gdiplus_v3", "color_source_v3", "image_source"]
            settings_comparison = {}
            
            for input_type in types_to_compare:
                try:
                    settings = obs.inputs.get_input_default_settings(input_type)
                    settings_comparison[input_type] = len(settings) if isinstance(settings, dict) else 0
                    chinese_name = InputTypeHelper.get_chinese_name(input_type)
                    print(f"  {chinese_name}: {settings_comparison[input_type]} 个设置项")
                except Exception as e:
                    print(f"  {input_type}: 获取失败 - {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ 实际应用测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始获取输入默认设置测试...")
    print("=" * 60)
    
    tests = [
        ("基本获取默认设置功能", test_get_default_settings_basic),
        ("所有输入类型的默认设置", test_get_default_settings_all_types),
        ("详细的默认设置内容", test_get_default_settings_detailed),
        ("错误处理", test_get_default_settings_error_handling),
        ("实际应用场景", test_get_default_settings_practical),
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
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




