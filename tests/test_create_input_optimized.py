#!/usr/bin/env python3
"""
优化后的创建输入源测试

测试优化后的 InputManager.create_input() 方法的功能
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def test_create_input_basic():
    """测试基本创建功能"""
    print("🎯 测试基本创建功能")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 获取可用场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            print(f"使用场景: {test_scene}")
            
            # 生成唯一的输入名称
            test_input_name = f"Test_Basic_{int(time.time())}"
            
            # 创建输入
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "Hello World!"}
            )
            
            print(f"创建结果: {result}")
            
            # 验证结果
            if result.get('success'):
                print("✅ 基本创建功能测试通过")
                return True
            else:
                print("❌ 创建失败")
                return False
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_parameter_validation():
    """测试参数验证"""
    print("\n🔍 测试参数验证")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            
            # 测试1: 空输入名称
            print("测试空输入名称...")
            try:
                obs.inputs.create_input(
                    input_name="",
                    input_kind="text_gdiplus_v3",
                    scene_name=test_scene
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获错误: {e}")
            
            # 测试2: 空输入类型
            print("测试空输入类型...")
            try:
                obs.inputs.create_input(
                    input_name="Test Input",
                    input_kind="",
                    scene_name=test_scene
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获错误: {e}")
            
            # 测试3: 既不提供场景名称也不提供UUID
            print("测试缺少场景参数...")
            try:
                obs.inputs.create_input(
                    input_name="Test Input",
                    input_kind="text_gdiplus_v3"
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获错误: {e}")
            
            # 测试4: 同时提供场景名称和UUID
            print("测试同时提供场景名称和UUID...")
            try:
                obs.inputs.create_input(
                    input_name="Test Input",
                    input_kind="text_gdiplus_v3",
                    scene_name=test_scene,
                    scene_uuid="fake-uuid"
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获错误: {e}")
            
            print("✅ 参数验证测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 参数验证测试失败: {e}")
        return False


def test_duplicate_check():
    """测试重复名称检查"""
    print("\n🔄 测试重复名称检查")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            test_input_name = f"Test_Duplicate_{int(time.time())}"
            
            # 第一次创建
            print(f"第一次创建输入: {test_input_name}")
            result1 = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene
            )
            
            if not result1.get('success'):
                print("❌ 第一次创建失败")
                return False
            
            print("✅ 第一次创建成功")
            
            # 第二次创建相同名称（应该失败）
            print(f"第二次创建相同名称的输入...")
            try:
                obs.inputs.create_input(
                    input_name=test_input_name,
                    input_kind="text_gdiplus_v3",
                    scene_name=test_scene
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确捕获重复名称错误: {e}")
            
            # 测试禁用重复检查
            print("测试禁用重复检查...")
            try:
                result2 = obs.inputs.create_input(
                    input_name=test_input_name,
                    input_kind="text_gdiplus_v3",
                    scene_name=test_scene,
                    check_duplicates=False
                )
                print(f"禁用重复检查的结果: {result2}")
                # 这可能成功也可能失败，取决于 OBS 的行为
            except Exception as e:
                print(f"禁用重复检查时的错误: {e}")
            
            print("✅ 重复名称检查测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 重复名称检查测试失败: {e}")
        return False


def test_return_value_structure():
    """测试返回值结构"""
    print("\n📊 测试返回值结构")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            test_input_name = f"Test_Return_{int(time.time())}"
            
            # 创建输入
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "Return Value Test"}
            )
            
            print(f"返回值: {result}")
            
            # 验证返回值结构
            expected_keys = ['input_uuid', 'scene_item_id', 'input_name', 'input_kind', 'success']
            
            for key in expected_keys:
                if key not in result:
                    print(f"❌ 缺少键: {key}")
                    return False
                print(f"✅ 包含键: {key} = {result[key]}")
            
            # 验证数据类型
            if not isinstance(result['input_uuid'], str):
                print(f"❌ input_uuid 应该是字符串，实际是 {type(result['input_uuid'])}")
                return False
            
            if not isinstance(result['scene_item_id'], int):
                print(f"❌ scene_item_id 应该是整数，实际是 {type(result['scene_item_id'])}")
                return False
            
            if not isinstance(result['success'], bool):
                print(f"❌ success 应该是布尔值，实际是 {type(result['success'])}")
                return False
            
            print("✅ 返回值结构测试通过")
            return True
            
    except Exception as e:
        print(f"❌ 返回值结构测试失败: {e}")
        return False


def test_input_kind_validation():
    """测试输入类型验证"""
    print("\n🔧 测试输入类型验证")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            
            # 测试不支持的输入类型
            print("测试不支持的输入类型...")
            test_input_name = f"Test_InvalidKind_{int(time.time())}"
            
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="invalid_input_type",
                scene_name=test_scene
            )
            
            print(f"使用无效类型的结果: {result}")
            # 这应该会记录警告但仍然尝试创建
            
            print("✅ 输入类型验证测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 输入类型验证测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始优化后的创建输入源测试...")
    print("=" * 60)
    
    tests = [
        ("基本创建功能", test_create_input_basic),
        ("参数验证", test_parameter_validation),
        ("重复名称检查", test_duplicate_check),
        ("返回值结构", test_return_value_structure),
        ("输入类型验证", test_input_kind_validation),
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
    
    if passed < total:
        print("\n⚠️ 注意：测试创建的输入源未被自动删除，请手动清理")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
