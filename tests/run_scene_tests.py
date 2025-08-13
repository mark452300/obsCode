#!/usr/bin/env python3
"""
运行场景管理器测试脚本

这个脚本用于运行 scenes.py 的测试用例。
运行前请确保：
1. OBS Studio 正在运行
2. WebSocket 服务器已启用（工具 -> WebSocket 服务器设置）
3. 配置正确的连接参数

使用方法：
    python run_scene_tests.py
    
可选参数：
    --verbose, -v: 详细输出
    --test-method, -t: 运行特定的测试方法
    --config-check, -c: 仅检查连接配置
"""

import sys
import argparse
import logging
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent  # 上一级目录是项目根目录
sys.path.insert(0, str(project_root))

from obs_sdk import OBSManager, OBSConfig
from obs_sdk.exceptions import OBSConnectionError


def check_obs_connection(config: OBSConfig) -> bool:
    """
    检查 OBS 连接
    
    Args:
        config: OBS 配置
        
    Returns:
        bool: 连接是否成功
    """
    print("正在检查 OBS 连接...")
    print(f"连接地址: {config.get_websocket_url()}")
    
    try:
        obs = OBSManager(config, auto_connect=False)
        if obs.connect():
            print("✓ 成功连接到 OBS Studio")
            
            # 获取版本信息
            version_info = obs.get_version()
            if version_info:
                print(f"✓ OBS 版本: {version_info.get('obsVersion', 'Unknown')}")
                print(f"✓ WebSocket 版本: {version_info.get('obsWebSocketVersion', 'Unknown')}")
            
            # 获取基本信息
            scenes = obs.scenes.get_names()
            print(f"✓ 发现 {len(scenes)} 个场景: {scenes}")
            
            current_scene = obs.scenes.get_current_program()
            if current_scene:
                print(f"✓ 当前场景: {current_scene}")
            
            obs.disconnect()
            return True
            
        else:
            print("✗ 无法连接到 OBS Studio")
            return False
            
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


def run_tests(verbose: bool = False, test_method: str = None):
    """
    运行测试
    
    Args:
        verbose: 是否详细输出
        test_method: 特定的测试方法名
    """
    import unittest
    
    # 配置日志级别
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 导入测试模块
    from tests.test_scenes import TestSceneManager
    
    # 创建测试套件
    if test_method:
        # 运行特定测试方法
        suite = unittest.TestSuite()
        suite.addTest(TestSceneManager(test_method))
    else:
        # 运行所有测试
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestSceneManager)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    # 输出结果摘要
    print("\n" + "="*50)
    print("测试结果摘要:")
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n测试结果: {'✓ 成功' if success else '✗ 失败'}")
    
    return success


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="运行 OBS 场景管理器测试",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python run_scene_tests.py                          # 运行所有测试
    python run_scene_tests.py -v                       # 详细输出
    python run_scene_tests.py -c                       # 仅检查连接
    python run_scene_tests.py -t test_create_scene     # 运行特定测试
        """
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细输出'
    )
    
    parser.add_argument(
        '--test-method', '-t',
        type=str,
        help='运行特定的测试方法'
    )
    
    parser.add_argument(
        '--config-check', '-c',
        action='store_true',
        help='仅检查连接配置'
    )
    
    args = parser.parse_args()
    
    # 创建配置
    config = OBSConfig()
    
    print("OBS 场景管理器测试工具")
    print("="*50)
    
    # 检查连接
    if not check_obs_connection(config):
        print("\n请检查以下事项:")
        print("1. OBS Studio 是否正在运行")
        print("2. WebSocket 服务器是否已启用（工具 -> WebSocket 服务器设置）")
        print("3. 连接参数是否正确（host, port, password）")
        print(f"4. 当前配置: {config.get_websocket_url()}")
        return False
    
    # 如果只是检查配置，则退出
    if args.config_check:
        print("\n配置检查完成！")
        return True
    
    print("\n开始运行测试...")
    print("="*50)
    
    # 运行测试
    success = run_tests(args.verbose, args.test_method)
    
    if success:
        print("\n🎉 所有测试通过！")
    else:
        print("\n❌ 部分测试失败，请检查输出信息")
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
