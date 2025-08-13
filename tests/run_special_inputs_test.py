#!/usr/bin/env python3
"""
特殊输入源测试运行器

用于运行 get_special_inputs 方法的各种测试
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def test_get_special_inputs():
    """测试 get_special_inputs 方法"""
    print("🚀 开始测试 get_special_inputs 方法...")
    print("=" * 60)
    
    try:
        with OBSManager() as obs:
            print("✅ 成功连接到 OBS")
            
            # 1. 基本功能测试
            print("\n🎯 测试基本功能:")
            special_inputs = obs.inputs.get_special_inputs()
            
            # 验证返回类型
            print(f"返回类型: {type(special_inputs)}")
            if not isinstance(special_inputs, dict):
                print("❌ 返回类型错误，应该是 dict")
                return False
            
            print("✅ 返回类型正确")
            
            # 2. 验证键的完整性
            print(f"\n📋 验证键的完整性:")
            expected_keys = ['desktop1', 'desktop2', 'mic1', 'mic2', 'mic3', 'mic4']
            
            print(f"期望的键: {expected_keys}")
            print(f"实际的键: {list(special_inputs.keys())}")
            
            missing_keys = set(expected_keys) - set(special_inputs.keys())
            extra_keys = set(special_inputs.keys()) - set(expected_keys)
            
            if missing_keys:
                print(f"❌ 缺失的键: {missing_keys}")
                return False
            
            if extra_keys:
                print(f"⚠️ 额外的键: {extra_keys}")
            
            print("✅ 键的完整性验证通过")
            
            # 3. 验证值的类型
            print(f"\n🔍 验证值的类型:")
            for key, value in special_inputs.items():
                print(f"  {key}: {type(value)} = '{value}'")
                if not isinstance(value, str):
                    print(f"❌ {key} 的值类型错误，应该是 str")
                    return False
            
            print("✅ 所有值的类型都正确")
            
            # 4. 显示配置状态
            print(f"\n📊 配置状态:")
            configured_count = 0
            for key, value in special_inputs.items():
                if value:
                    print(f"  ✅ {key}: '{value}' (已配置)")
                    configured_count += 1
                else:
                    print(f"  ⚠️ {key}: (未配置)")
            
            total_count = len(expected_keys)
            print(f"\n📈 配置统计: {configured_count}/{total_count} 个特殊输入源已配置")
            
            # 5. 测试多次调用的一致性
            print(f"\n🔄 测试多次调用的一致性:")
            special_inputs_2 = obs.inputs.get_special_inputs()
            
            if special_inputs == special_inputs_2:
                print("✅ 多次调用结果一致")
            else:
                print("⚠️ 多次调用结果不一致")
                print(f"第一次: {special_inputs}")
                print(f"第二次: {special_inputs_2}")
            
            print(f"\n✅ get_special_inputs 测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration_with_other_methods():
    """测试与其他方法的集成"""
    print("\n" + "=" * 60)
    print("测试与其他方法的集成")
    print("=" * 60)
    
    try:
        with OBSManager() as obs:
            # 获取特殊输入源
            special_inputs = obs.inputs.get_special_inputs()
            
            # 获取所有输入源
            all_inputs = obs.inputs.get_all()
            all_input_names = [inp.get('inputName', '') for inp in all_inputs]
            
            print(f"特殊输入源数量: {len([v for v in special_inputs.values() if v])}")
            print(f"总输入源数量: {len(all_input_names)}")
            
            # 检查特殊输入源是否在总输入源列表中
            print(f"\n🔍 检查特殊输入源是否存在于总输入源中:")
            for key, value in special_inputs.items():
                if value:
                    if value in all_input_names:
                        print(f"  ✅ {key} ('{value}') 存在于输入源列表中")
                    else:
                        print(f"  ⚠️ {key} ('{value}') 不在输入源列表中")
                else:
                    print(f"  ⚪ {key} 未配置")
            
            return True
            
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始特殊输入源综合测试...")
    
    tests = [
        ("get_special_inputs 基本功能", test_get_special_inputs),
        ("与其他方法的集成", test_integration_with_other_methods),
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
