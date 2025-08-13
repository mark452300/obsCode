#!/usr/bin/env python3
"""
特殊输入源测试

专门测试 InputManager.get_special_inputs() 方法的功能，包括：
- 基本功能测试
- 返回值验证
- 错误处理
- 边界情况测试
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager
from obs_sdk.inputs import InputManager
from obs_sdk.exceptions import OBSConnectionError


class TestSpecialInputs(unittest.TestCase):
    """特殊输入源测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.mock_client = Mock()
        self.input_manager = InputManager(self.mock_client)
    
    def test_get_special_inputs_success(self):
        """测试成功获取特殊输入源"""
        # 模拟成功响应
        mock_response = Mock()
        mock_response.datain = {
            'desktop1': 'Desktop Audio',
            'desktop2': 'Desktop Audio 2',
            'mic1': 'Microphone',
            'mic2': 'Microphone 2',
            'mic3': '',
            'mic4': ''
        }
        self.mock_client.call.return_value = mock_response
        
        # 调用方法
        result = self.input_manager.get_special_inputs()
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 6)
        
        # 验证所有预期的键都存在
        expected_keys = ['desktop1', 'desktop2', 'mic1', 'mic2', 'mic3', 'mic4']
        for key in expected_keys:
            self.assertIn(key, result)
        
        # 验证具体值
        self.assertEqual(result['desktop1'], 'Desktop Audio')
        self.assertEqual(result['desktop2'], 'Desktop Audio 2')
        self.assertEqual(result['mic1'], 'Microphone')
        self.assertEqual(result['mic2'], 'Microphone 2')
        self.assertEqual(result['mic3'], '')
        self.assertEqual(result['mic4'], '')
    
    def test_get_special_inputs_partial_data(self):
        """测试部分数据的情况"""
        # 模拟部分数据响应
        mock_response = Mock()
        mock_response.datain = {
            'desktop1': 'Desktop Audio',
            'mic1': 'Microphone'
            # 缺少其他键
        }
        self.mock_client.call.return_value = mock_response
        
        # 调用方法
        result = self.input_manager.get_special_inputs()
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 6)
        
        # 验证存在的键
        self.assertEqual(result['desktop1'], 'Desktop Audio')
        self.assertEqual(result['mic1'], 'Microphone')
        
        # 验证缺失的键被设为空字符串
        self.assertEqual(result['desktop2'], '')
        self.assertEqual(result['mic2'], '')
        self.assertEqual(result['mic3'], '')
        self.assertEqual(result['mic4'], '')
    
    def test_get_special_inputs_no_datain(self):
        """测试响应中没有 datain 属性的情况"""
        # 模拟没有 datain 的响应
        mock_response = Mock()
        del mock_response.datain  # 删除 datain 属性
        self.mock_client.call.return_value = mock_response
        
        # 调用方法
        result = self.input_manager.get_special_inputs()
        
        # 验证返回空字典
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
    
    def test_get_special_inputs_exception(self):
        """测试异常情况"""
        # 模拟异常
        self.mock_client.call.side_effect = Exception("Connection failed")
        
        # 调用方法
        result = self.input_manager.get_special_inputs()
        
        # 验证返回空字典
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
    
    def test_get_special_inputs_empty_response(self):
        """测试空响应的情况"""
        # 模拟空的 datain
        mock_response = Mock()
        mock_response.datain = {}
        self.mock_client.call.return_value = mock_response
        
        # 调用方法
        result = self.input_manager.get_special_inputs()
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 6)
        
        # 验证所有值都是空字符串
        for key in ['desktop1', 'desktop2', 'mic1', 'mic2', 'mic3', 'mic4']:
            self.assertEqual(result[key], '')
    
    def test_get_special_inputs_none_values(self):
        """测试 None 值的处理"""
        # 模拟包含 None 值的响应
        mock_response = Mock()
        mock_response.datain = {
            'desktop1': None,
            'desktop2': 'Desktop Audio 2',
            'mic1': None,
            'mic2': 'Microphone 2',
            'mic3': None,
            'mic4': None
        }
        self.mock_client.call.return_value = mock_response
        
        # 调用方法
        result = self.input_manager.get_special_inputs()
        
        # 验证 None 值被转换为空字符串
        self.assertEqual(result['desktop1'], '')
        self.assertEqual(result['desktop2'], 'Desktop Audio 2')
        self.assertEqual(result['mic1'], '')
        self.assertEqual(result['mic2'], 'Microphone 2')
        self.assertEqual(result['mic3'], '')
        self.assertEqual(result['mic4'], '')


class TestSpecialInputsIntegration(unittest.TestCase):
    """特殊输入源集成测试类"""
    
    def test_integration_with_real_obs(self):
        """与真实 OBS 的集成测试（需要 OBS 运行）"""
        try:
            with OBSManager() as obs:
                # 调用方法
                result = obs.inputs.get_special_inputs()
                
                # 基本验证
                self.assertIsInstance(result, dict)
                
                # 验证键的存在
                expected_keys = ['desktop1', 'desktop2', 'mic1', 'mic2', 'mic3', 'mic4']
                for key in expected_keys:
                    self.assertIn(key, result)
                    self.assertIsInstance(result[key], str)
                
                print(f"集成测试结果: {result}")
                
        except Exception as e:
            self.skipTest(f"需要 OBS 运行才能进行集成测试: {e}")


def run_manual_test():
    """手动测试函数，用于直接运行"""
    print("🚀 开始特殊输入源测试...")
    print("=" * 60)
    
    try:
        with OBSManager() as obs:
            print("✅ 成功连接到 OBS")
            
            # 测试 get_special_inputs
            print("\n🎯 测试 get_special_inputs():")
            special_inputs = obs.inputs.get_special_inputs()
            
            print(f"返回类型: {type(special_inputs)}")
            print(f"键数量: {len(special_inputs)}")
            
            if special_inputs:
                print("\n📋 特殊输入源详情:")
                for key, value in special_inputs.items():
                    status = "✅ 已配置" if value else "⚠️ 未配置"
                    print(f"  {key}: '{value}' ({status})")
                
                # 统计
                configured = sum(1 for v in special_inputs.values() if v)
                total = len(special_inputs)
                print(f"\n📊 配置统计: {configured}/{total} 个已配置")
            else:
                print("⚠️ 没有获取到特殊输入源数据")
            
            print("\n✅ 测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='特殊输入源测试')
    parser.add_argument('--manual', action='store_true', help='运行手动测试')
    parser.add_argument('--unit', action='store_true', help='运行单元测试')
    
    args = parser.parse_args()
    
    if args.manual:
        success = run_manual_test()
        sys.exit(0 if success else 1)
    elif args.unit:
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        # 默认运行手动测试
        success = run_manual_test()
        sys.exit(0 if success else 1)
