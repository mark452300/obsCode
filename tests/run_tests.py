#!/usr/bin/env python3
"""
OBS SDK 测试运行器

统一的测试运行脚本，支持运行所有测试模块。

使用方法：
    python tests/run_tests.py                    # 运行所有测试
    python tests/run_tests.py --scenes           # 只运行场景测试
    python tests/run_tests.py --inputs           # 只运行输入测试
    python tests/run_tests.py --examples         # 运行示例演示
    python tests/run_tests.py --check-connection # 检查 OBS 连接
"""

import sys
import os
import argparse
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager, OBSConfig


def check_obs_connection():
    """检查 OBS 连接"""
    print("🔍 检查 OBS 连接...")
    
    try:
        config = OBSConfig()
        with OBSManager(config) as obs:
            version_info = obs.get_version()
            print(f"✅ 成功连接到 OBS Studio")
            print(f"   OBS 版本: {version_info.get('obsVersion', 'Unknown')}")
            print(f"   WebSocket 版本: {version_info.get('obsWebSocketVersion', 'Unknown')}")
            return True
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("\n请检查:")
        print("  1. OBS Studio 是否正在运行")
        print("  2. obs-websocket 插件是否已启用")
        print("  3. WebSocket 端口配置是否正确")
        print("  4. 密码配置是否正确")
        return False


def run_scenes_tests():
    """运行场景管理测试"""
    print("\n" + "="*60)
    print("🎬 运行场景管理测试")
    print("="*60)
    
    try:
        # 导入并运行场景测试
        import unittest
        from test_scenes import TestSceneManager
        
        # 创建测试套件
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSceneManager)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        return result.wasSuccessful()
        
    except Exception as e:
        print(f"❌ 场景测试失败: {e}")
        return False


def run_inputs_tests():
    """运行输入管理测试"""
    print("\n" + "="*60)
    print("🎵 运行输入管理测试")
    print("="*60)
    
    try:
        # 导入并运行输入测试
        from test_inputs import main as run_comprehensive_test

        return run_comprehensive_test()
        
    except Exception as e:
        print(f"❌ 输入测试失败: {e}")
        return False


def run_examples():
    """运行示例演示"""
    print("\n" + "="*60)
    print("📚 运行示例演示")
    print("="*60)
    
    examples_passed = 0
    examples_total = 0
    
    # 运行输入类型示例
    try:
        print("\n📋 输入类型列表示例:")
        # 需要切换到项目根目录来导入示例
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from examples.input_kinds_demo import main as input_kinds_example
        input_kinds_example()
        examples_passed += 1
        print("✅ 输入类型示例完成")
    except Exception as e:
        print(f"❌ 输入类型示例失败: {e}")
    finally:
        examples_total += 1
    
    print(f"\n示例演示结果: {examples_passed}/{examples_total} 通过")
    return examples_passed == examples_total


def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行所有测试...")
    
    # 首先检查连接
    if not check_obs_connection():
        print("\n❌ OBS 连接失败，无法运行测试")
        return False
    
    results = []
    
    # 运行场景测试
    try:
        results.append(("场景管理", run_scenes_tests()))
    except Exception as e:
        print(f"❌ 场景测试异常: {e}")
        results.append(("场景管理", False))
    
    # 运行输入测试
    try:
        results.append(("输入管理", run_inputs_tests()))
    except Exception as e:
        print(f"❌ 输入测试异常: {e}")
        results.append(("输入管理", False))
    
    # 运行示例
    try:
        results.append(("示例演示", run_examples()))
    except Exception as e:
        print(f"❌ 示例演示异常: {e}")
        results.append(("示例演示", False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
        return True
    else:
        print("⚠️ 部分测试失败，请检查上面的错误信息")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="OBS SDK 测试运行器")
    parser.add_argument("--scenes", action="store_true", help="只运行场景测试")
    parser.add_argument("--inputs", action="store_true", help="只运行输入测试")
    parser.add_argument("--examples", action="store_true", help="运行示例演示")
    parser.add_argument("--check-connection", action="store_true", help="检查 OBS 连接")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 设置工作目录为 tests 目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = True
    
    if args.check_connection:
        success = check_obs_connection()
    elif args.scenes:
        success = check_obs_connection() and run_scenes_tests()
    elif args.inputs:
        success = check_obs_connection() and run_inputs_tests()
    elif args.examples:
        success = check_obs_connection() and run_examples()
    else:
        # 运行所有测试
        success = run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
