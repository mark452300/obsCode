#!/usr/bin/env python3
"""
重命名输入源测试

专门测试 InputManager.rename_input() 方法的功能
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def test_rename_input_basic():
    """测试基本重命名功能"""
    print("✏️ 测试基本重命名功能")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            original_name = f"原始名称_{int(time.time())}"
            new_name = f"新名称_{int(time.time())}"
            
            print(f"创建测试输入源: {original_name}")
            
            # 创建测试输入源
            result = obs.inputs.create_input(
                input_name=original_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "重命名测试"}
            )
            
            if not result.get('success'):
                print("❌ 创建测试输入源失败")
                return False
            
            print(f"✅ 创建成功，UUID: {result['input_uuid']}")
            
            # 验证原始输入源存在
            if not obs.inputs.exists(original_name):
                print("❌ 原始输入源不存在")
                return False
            
            print("✅ 验证原始输入源存在")
            
            # 重命名输入源
            print(f"重命名: {original_name} -> {new_name}")
            success = obs.inputs.rename_input(
                new_input_name=new_name,
                input_name=original_name
            )
            
            if success:
                print("✅ 重命名操作成功")
            else:
                print("❌ 重命名操作失败")
                return False
            
            # 等待重命名生效
            time.sleep(0.5)
            
            # 验证重命名结果
            if obs.inputs.exists(new_name) and not obs.inputs.exists(original_name):
                print("✅ 验证重命名成功")
                
                # 清理测试输入源
                obs.inputs.remove_input(input_name=new_name)
                print("🧹 清理完成")
                return True
            else:
                print("❌ 重命名验证失败")
                print(f"新名称存在: {obs.inputs.exists(new_name)}")
                print(f"原名称存在: {obs.inputs.exists(original_name)}")
                return False
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rename_input_by_uuid():
    """测试使用 UUID 重命名"""
    print("\n🆔 测试使用 UUID 重命名")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            original_name = f"UUID测试_{int(time.time())}"
            new_name = f"UUID新名称_{int(time.time())}"
            
            # 创建测试输入源
            result = obs.inputs.create_input(
                input_name=original_name,
                input_kind="color_source_v3",
                scene_name=test_scene,
                input_settings={"color": 0x00FF00}
            )
            
            if not result.get('success'):
                print("❌ 创建测试输入源失败")
                return False
            
            input_uuid = result['input_uuid']
            print(f"✅ 创建成功，UUID: {input_uuid}")
            
            # 使用 UUID 重命名
            print(f"使用 UUID 重命名: {original_name} -> {new_name}")
            success = obs.inputs.rename_input(
                new_input_name=new_name,
                input_uuid=input_uuid
            )
            
            if success:
                print("✅ 使用 UUID 重命名成功")
                
                # 验证结果
                time.sleep(0.5)
                if obs.inputs.exists(new_name):
                    print("✅ 验证重命名成功")
                    # 清理
                    obs.inputs.remove_input(input_name=new_name)
                    return True
                else:
                    print("❌ 重命名验证失败")
                    return False
            else:
                print("❌ 使用 UUID 重命名失败")
                return False
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_rename_input_error_handling():
    """测试错误处理"""
    print("\n🚫 测试错误处理")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 测试1: 空的新名称
            print("测试空的新名称...")
            try:
                obs.inputs.rename_input(
                    new_input_name="",
                    input_name="测试"
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确抛出 ValueError: {e}")
            
            # 测试2: 既不提供名称也不提供 UUID
            print("测试缺少参数...")
            try:
                obs.inputs.rename_input(new_input_name="新名称")
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确抛出 ValueError: {e}")
            
            # 测试3: 同时提供名称和 UUID
            print("测试同时提供名称和 UUID...")
            try:
                obs.inputs.rename_input(
                    new_input_name="新名称",
                    input_name="旧名称",
                    input_uuid="fake-uuid"
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确抛出 ValueError: {e}")
            
            # 测试4: 新名称已存在
            print("测试新名称已存在...")
            scenes = obs.scenes.get_names()
            if scenes:
                # 创建两个测试输入源
                name1 = f"存在测试1_{int(time.time())}"
                name2 = f"存在测试2_{int(time.time())}"
                
                obs.inputs.create_input(
                    input_name=name1,
                    input_kind="text_gdiplus_v3",
                    scene_name=scenes[0],
                    input_settings={"text": "测试1"}
                )
                
                obs.inputs.create_input(
                    input_name=name2,
                    input_kind="text_gdiplus_v3",
                    scene_name=scenes[0],
                    input_settings={"text": "测试2"}
                )
                
                try:
                    # 尝试将 name1 重命名为 name2（已存在）
                    obs.inputs.rename_input(
                        new_input_name=name2,
                        input_name=name1
                    )
                    print("❌ 应该抛出 ValueError")
                    return False
                except ValueError as e:
                    print(f"✅ 正确抛出 ValueError: {e}")
                
                # 清理
                obs.inputs.remove_input(input_name=name1)
                obs.inputs.remove_input(input_name=name2)
            
            return True
            
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False


def test_rename_input_integration():
    """测试与其他方法的集成"""
    print("\n🔗 测试与其他方法的集成")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            
            # 创建、重命名、再重命名的完整流程
            original_name = f"集成测试_{int(time.time())}"
            middle_name = f"中间名称_{int(time.time())}"
            final_name = f"最终名称_{int(time.time())}"
            
            print(f"完整流程测试: {original_name} -> {middle_name} -> {final_name}")
            
            # 1. 创建
            result = obs.inputs.create_input(
                input_name=original_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "集成测试"}
            )
            
            if not result.get('success'):
                print("❌ 创建失败")
                return False
            
            print(f"✅ 创建: {original_name}")
            
            # 2. 第一次重命名
            obs.inputs.rename_input(
                new_input_name=middle_name,
                input_name=original_name
            )
            time.sleep(0.3)
            
            if obs.inputs.exists(middle_name):
                print(f"✅ 第一次重命名: {original_name} -> {middle_name}")
            else:
                print("❌ 第一次重命名失败")
                return False
            
            # 3. 第二次重命名
            obs.inputs.rename_input(
                new_input_name=final_name,
                input_name=middle_name
            )
            time.sleep(0.3)
            
            if obs.inputs.exists(final_name):
                print(f"✅ 第二次重命名: {middle_name} -> {final_name}")
            else:
                print("❌ 第二次重命名失败")
                return False
            
            # 4. 验证最终状态
            all_names = obs.inputs.get_names()
            if (final_name in all_names and 
                original_name not in all_names and 
                middle_name not in all_names):
                print("✅ 最终状态验证成功")
            else:
                print("❌ 最终状态验证失败")
                return False
            
            # 5. 清理
            obs.inputs.remove_input(input_name=final_name)
            print("🧹 清理完成")
            
            return True
            
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始重命名输入源测试...")
    print("=" * 60)
    
    tests = [
        ("基本重命名功能", test_rename_input_basic),
        ("使用 UUID 重命名", test_rename_input_by_uuid),
        ("错误处理", test_rename_input_error_handling),
        ("与其他方法的集成", test_rename_input_integration),
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
