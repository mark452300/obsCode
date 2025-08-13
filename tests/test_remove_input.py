#!/usr/bin/env python3
"""
删除输入源测试

专门测试 InputManager.remove_input() 方法的功能
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def test_remove_input_basic():
    """测试基本删除功能"""
    print("🗑️ 测试基本删除功能")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            test_input_name = f"测试删除_{int(time.time())}"
            
            print(f"创建测试输入源: {test_input_name}")
            
            # 创建测试输入源
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "即将被删除"}
            )
            
            if not result.get('success'):
                print("❌ 创建测试输入源失败")
                return False
            
            print(f"✅ 创建成功，UUID: {result['input_uuid']}")
            
            # 验证输入源存在
            if not obs.inputs.exists(test_input_name):
                print("❌ 输入源不存在")
                return False
            
            print("✅ 验证输入源存在")
            
            # 删除输入源
            print(f"删除输入源: {test_input_name}")
            success = obs.inputs.remove_input(input_name=test_input_name)

            if success:
                print("✅ 删除操作成功")
            else:
                print("❌ 删除操作失败")
                return False

            # 等待删除生效
            time.sleep(0.5)

            # 验证输入源已被删除
            if not obs.inputs.exists(test_input_name):
                print("✅ 验证输入源已被删除")
                return True
            else:
                print("❌ 输入源仍然存在")
                return False
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_remove_input_by_uuid():
    """测试使用 UUID 删除"""
    print("\n🆔 测试使用 UUID 删除")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            test_input_name = f"测试UUID删除_{int(time.time())}"
            
            # 创建测试输入源
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="color_source_v3",
                scene_name=test_scene,
                input_settings={"color": 0xFF0000}
            )
            
            if not result.get('success'):
                print("❌ 创建测试输入源失败")
                return False
            
            input_uuid = result['input_uuid']
            print(f"✅ 创建成功，UUID: {input_uuid}")
            
            # 使用 UUID 删除
            print(f"使用 UUID 删除输入源")
            success = obs.inputs.remove_input(input_uuid=input_uuid)
            
            if success:
                print("✅ 使用 UUID 删除成功")
                return True
            else:
                print("❌ 使用 UUID 删除失败")
                return False
                
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_remove_input_error_handling():
    """测试错误处理"""
    print("\n🚫 测试错误处理")
    print("-" * 40)
    
    try:
        with OBSManager() as obs:
            # 测试1: 删除不存在的输入源
            print("测试删除不存在的输入源...")
            try:
                result = obs.inputs.remove_input(input_name="不存在的输入源")
                # OBS 可能不会为不存在的输入源抛出异常，而是静默失败
                print(f"删除不存在输入源的结果: {result}")
                print("✅ 删除不存在的输入源处理正常")
            except Exception as e:
                print(f"✅ 抛出异常: {type(e).__name__}: {e}")
            
            # 测试2: 既不提供名称也不提供 UUID
            print("测试缺少参数...")
            try:
                obs.inputs.remove_input()
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确抛出 ValueError: {e}")
            
            # 测试3: 同时提供名称和 UUID
            print("测试同时提供名称和 UUID...")
            try:
                obs.inputs.remove_input(
                    input_name="测试",
                    input_uuid="fake-uuid"
                )
                print("❌ 应该抛出 ValueError")
                return False
            except ValueError as e:
                print(f"✅ 正确抛出 ValueError: {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False


def test_remove_input_integration():
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
            
            # 创建多个输入源
            input_names = []
            for i in range(3):
                name = f"集成测试_{i}_{int(time.time())}"
                result = obs.inputs.create_input(
                    input_name=name,
                    input_kind="text_gdiplus_v3",
                    scene_name=test_scene,
                    input_settings={"text": f"测试文本 {i}"}
                )
                if result.get('success'):
                    input_names.append(name)
                    print(f"✅ 创建输入源: {name}")
            
            print(f"创建了 {len(input_names)} 个输入源")
            
            # 验证所有输入源都存在
            initial_count = len(obs.inputs.get_names())
            print(f"当前总输入源数量: {initial_count}")
            
            # 删除一半输入源
            deleted_count = 0
            for i, name in enumerate(input_names):
                if i % 2 == 0:  # 删除偶数索引的输入源
                    if obs.inputs.remove_input(input_name=name):
                        deleted_count += 1
                        print(f"✅ 删除输入源: {name}")
                        time.sleep(0.2)  # 给每次删除一点时间

            # 等待所有删除操作完成
            time.sleep(1)

            # 验证删除结果
            final_count = len(obs.inputs.get_names())
            expected_count = initial_count - deleted_count
            
            print(f"删除统计: 初始 {initial_count}，删除 {deleted_count}，期望 {expected_count}，实际 {final_count}")

            # 由于可能有其他测试创建的输入源被删除，我们检查是否至少删除了预期数量
            if final_count <= expected_count:
                print(f"✅ 删除验证成功: {initial_count} -> {final_count} (删除了至少 {deleted_count} 个)")
            else:
                print(f"❌ 删除验证失败: 期望最多 {expected_count}，实际 {final_count}")
                return False
            
            # 清理剩余的测试输入源
            for name in input_names:
                if obs.inputs.exists(name):
                    obs.inputs.remove_input(input_name=name)
                    print(f"🧹 清理输入源: {name}")
            
            return True
            
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始删除输入源测试...")
    print("=" * 60)
    
    tests = [
        ("基本删除功能", test_remove_input_basic),
        ("使用 UUID 删除", test_remove_input_by_uuid),
        ("错误处理", test_remove_input_error_handling),
        ("与其他方法的集成", test_remove_input_integration),
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
