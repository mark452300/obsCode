#!/usr/bin/env python3
"""
输入管理器综合测试

测试 InputManager 的所有功能，包括：
- 获取输入源列表
- 获取输入类型列表
- 静音控制
- 设置管理
- 错误处理
"""


import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def test_input_lists():
    """测试输入列表相关功能"""
    print("=" * 60)
    print("测试输入列表功能")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            print("✅ 成功连接到 OBS")

            # 1. 测试获取所有输入源
            print("\n📋 测试 get_all():")
            all_inputs = obs.inputs.get_all()
            print(f"找到 {len(all_inputs)} 个输入源")
            for i, inp in enumerate(all_inputs, 1):
                name = inp.get('inputName', 'Unknown')
                kind = inp.get('inputKind', 'Unknown')
                print(f"  {i:2d}. {name} ({kind})")

            # 2. 测试获取输入源名称
            print("\n📝 测试 get_names():")
            input_names = obs.inputs.get_names()
            print(f"输入源名称: {input_names}")

            # 3. 测试获取音频输入源
            print("\n🎵 测试 get_audio_inputs():")
            audio_inputs = obs.inputs.get_audio_inputs()
            print(f"音频输入源: {audio_inputs}")

            # 4. 测试获取输入类型列表
            print("\n🔧 测试 get_input_kinds():")
            input_kinds = obs.inputs.get_input_kinds()
            print(f"支持 {len(input_kinds)} 种输入类型")

            # 5. 测试获取特殊输入源
            print("\n🎯 测试 get_special_inputs():")
            special_inputs = obs.inputs.get_special_inputs()
            print(f"特殊输入源: {special_inputs}")
            if special_inputs:
                for key, value in special_inputs.items():
                    status = "✅ 已配置" if value else "⚠️ 未配置"
                    print(f"  {key}: {value} ({status})")

            # 6. 测试输入源存在性检查
            print("\n✅ 测试 exists():")
            if input_names:
                test_input = input_names[0]
                exists = obs.inputs.exists(test_input)
                print(f"输入源 '{test_input}' 存在: {exists}")

                # 测试不存在的输入源
                fake_input = "不存在的输入源"
                exists_fake = obs.inputs.exists(fake_input)
                print(f"输入源 '{fake_input}' 存在: {exists_fake}")

            return True

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_mute_controls():
    """测试静音控制功能"""
    print("\n" + "=" * 60)
    print("测试静音控制功能")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            # 获取音频输入源进行测试
            audio_inputs = obs.inputs.get_audio_inputs()

            if not audio_inputs:
                print("⚠️ 没有找到音频输入源，跳过静音测试")
                return True

            test_input = audio_inputs[0]
            print(f"使用输入源 '{test_input}' 进行静音测试")

            # 1. 获取初始静音状态
            print(f"\n🔍 测试 is_muted():")
            initial_muted = obs.inputs.is_muted(test_input)
            print(f"初始静音状态: {initial_muted}")

            # 2. 测试静音
            print(f"\n🔇 测试 mute():")
            mute_result = obs.inputs.mute(test_input)
            print(f"静音操作结果: {mute_result}")
            time.sleep(0.5)  # 等待状态更新

            muted_state = obs.inputs.is_muted(test_input)
            print(f"静音后状态: {muted_state}")

            # 3. 测试取消静音
            print(f"\n🔊 测试 unmute():")
            unmute_result = obs.inputs.unmute(test_input)
            print(f"取消静音操作结果: {unmute_result}")
            time.sleep(0.5)  # 等待状态更新

            unmuted_state = obs.inputs.is_muted(test_input)
            print(f"取消静音后状态: {unmuted_state}")

            # 4. 测试切换静音
            print(f"\n🔄 测试 toggle_mute():")
            current_state = obs.inputs.is_muted(test_input)
            print(f"切换前状态: {current_state}")

            toggled_state = obs.inputs.toggle_mute(test_input)
            print(f"切换后状态: {toggled_state}")
            time.sleep(0.5)

            # 恢复初始状态
            print(f"\n🔄 恢复初始状态:")
            if initial_muted != obs.inputs.is_muted(test_input):
                if initial_muted:
                    obs.inputs.mute(test_input)
                else:
                    obs.inputs.unmute(test_input)
                print(f"已恢复到初始状态: {initial_muted}")

            return True

    except Exception as e:
        print(f"❌ 静音测试失败: {e}")
        return False


def test_settings_management():
    """测试设置管理功能"""
    print("\n" + "=" * 60)
    print("测试设置管理功能")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            input_names = obs.inputs.get_names()

            if not input_names:
                print("⚠️ 没有找到输入源，跳过设置测试")
                return True

            test_input = input_names[0]
            print(f"使用输入源 '{test_input}' 进行设置测试")

            # 1. 测试获取设置
            print(f"\n⚙️ 测试 get_settings():")
            settings = obs.inputs.get_settings(test_input)
            print(f"设置数量: {len(settings)} 项")

            # 显示部分设置（避免输出过长）
            if settings:
                print("部分设置:")
                for i, (key, value) in enumerate(list(settings.items())[:5]):
                    print(f"  {key}: {value}")
                if len(settings) > 5:
                    print(f"  ... 还有 {len(settings) - 5} 项设置")

            # 2. 测试设置更新（谨慎操作，只测试安全的设置）
            print(f"\n🔧 测试 set_settings():")
            print("(跳过设置更新测试以避免影响 OBS 配置)")

            return True

    except Exception as e:
        print(f"❌ 设置测试失败: {e}")
        return False


def test_info_summary():
    """测试信息摘要功能"""
    print("\n" + "=" * 60)
    print("测试信息摘要功能")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            print("📊 测试 get_info():")
            info = obs.inputs.get_info()

            print("输入源信息摘要:")
            for key, value in info.items():
                if isinstance(value, dict):
                    print(f"  {key}: {len(value)} 项")
                elif isinstance(value, list):
                    print(f"  {key}: {len(value)} 个")
                else:
                    print(f"  {key}: {value}")

            return True

    except Exception as e:
        print(f"❌ 信息摘要测试失败: {e}")
        return False


def test_special_inputs():
    """测试特殊输入源功能"""
    print("\n" + "=" * 60)
    print("测试特殊输入源功能")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            print("🎯 测试 get_special_inputs():")

            # 1. 基本功能测试
            special_inputs = obs.inputs.get_special_inputs()
            print(f"获取到特殊输入源: {type(special_inputs)}")

            # 2. 验证返回类型
            if not isinstance(special_inputs, dict):
                print(f"❌ 返回类型错误，期望 dict，实际 {type(special_inputs)}")
                return False

            print("✅ 返回类型正确 (dict)")

            # 3. 验证预期的键
            expected_keys = ['desktop1', 'desktop2', 'mic1', 'mic2', 'mic3', 'mic4']
            print(f"\n📋 验证预期键:")

            for key in expected_keys:
                if key in special_inputs:
                    value = special_inputs[key]
                    status = "✅ 已配置" if value else "⚠️ 未配置"
                    print(f"  {key}: '{value}' ({status})")
                else:
                    print(f"  {key}: ❌ 缺失")

            # 4. 检查是否有额外的键
            extra_keys = set(special_inputs.keys()) - set(expected_keys)
            if extra_keys:
                print(f"\n⚠️ 发现额外的键: {extra_keys}")
            else:
                print(f"\n✅ 没有额外的键")

            # 5. 统计配置情况
            configured_count = sum(1 for v in special_inputs.values() if v)
            total_count = len(expected_keys)
            print(f"\n📊 配置统计: {configured_count}/{total_count} 个特殊输入源已配置")

            # 6. 验证值的类型
            print(f"\n🔍 验证值类型:")
            all_strings = True
            for key, value in special_inputs.items():
                if not isinstance(value, str):
                    print(f"  ❌ {key}: 期望 str，实际 {type(value)}")
                    all_strings = False
                else:
                    print(f"  ✅ {key}: str")

            if all_strings:
                print("✅ 所有值都是字符串类型")

            return True

    except Exception as e:
        print(f"❌ 特殊输入源测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 60)
    print("测试错误处理")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            fake_input = "不存在的输入源"

            print(f"🚫 测试不存在输入源的错误处理:")

            # 测试静音状态检查
            try:
                is_muted = obs.inputs.is_muted(fake_input)
                print(f"❌ 应该抛出异常，但返回了: {is_muted}")
            except Exception as e:
                print(f"✅ 正确抛出异常: {type(e).__name__}")

            # 测试静音操作
            try:
                mute_result = obs.inputs.mute(fake_input)
                print(f"❌ 应该抛出异常，但返回了: {mute_result}")
            except Exception as e:
                print(f"✅ 正确抛出异常: {type(e).__name__}")

            # 测试获取设置
            try:
                settings = obs.inputs.get_settings(fake_input)
                print(f"❌ 应该抛出异常，但返回了: {settings}")
            except Exception as e:
                print(f"✅ 正确抛出异常: {type(e).__name__}")

            return True

    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始输入管理器综合测试...")

    tests = [
        ("输入列表功能", test_input_lists),
        ("特殊输入源功能", test_special_inputs),
        ("静音控制功能", test_mute_controls),
        ("设置管理功能", test_settings_management),
        ("信息摘要功能", test_info_summary),
        ("删除输入源功能", test_remove_input),
        ("重命名输入源功能", test_rename_input),
        ("错误处理", test_error_handling),
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


def test_source():
    print("测试所有可用的系统输入源")

    try:
        with OBSManager() as obs:
            print("✅ 成功连接到 OBS")

            all_inputs = obs.inputs.get_input_kinds()
            print(f"获取到所有输入源: {all_inputs}")
            return True

    except Exception as e:
        print(f"❌ 获取失败: {e}")
        return False


def test_remove_input():
    """测试删除输入源功能"""
    print("\n" + "=" * 60)
    print("测试删除输入源功能")
    print("=" * 60)

    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False

            test_scene = scenes[0]
            test_input_name = f"测试删除_{int(time.time())}"

            print(f"🎯 创建测试输入源: {test_input_name}")

            # 创建测试输入源
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "即将被删除的文本"}
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

            # 测试使用名称删除
            print(f"\n🗑️ 删除输入源: {test_input_name}")
            success = obs.inputs.remove_input(input_name=test_input_name)

            if success:
                print("✅ 删除操作成功")
            else:
                print("❌ 删除操作失败")
                return False

            # 验证输入源已被删除
            if not obs.inputs.exists(test_input_name):
                print("✅ 验证输入源已被删除")
            else:
                print("❌ 输入源仍然存在")
                return False

            # 测试删除不存在的输入源
            print(f"\n🚫 测试删除不存在的输入源")
            try:
                obs.inputs.remove_input(input_name="不存在的输入源")
                print("❌ 应该抛出异常")
                return False
            except Exception as e:
                print(f"✅ 正确抛出异常: {type(e).__name__}")

            return True

    except Exception as e:
        print(f"❌ 删除输入源测试失败: {e}")
        return False


def test_rename_input():
    """测试重命名输入源功能"""
    print("\n" + "=" * 60)
    print("测试重命名输入源功能")
    print("=" * 60)

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

            print(f"🎯 创建测试输入源: {original_name}")

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
            print(f"\n✏️ 重命名: {original_name} -> {new_name}")
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
                return False

    except Exception as e:
        print(f"❌ 重命名输入源测试失败: {e}")
        return False


def test_create_red_centered_text():
    """创建红色居中文本的测试"""
    try:
        with OBSManager() as obs:
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False

            test_scene = scenes[0]
            test_input_name = f"红色居中文本_{int(time.time())}"

            # 设置红色居中文本的参数    这里的颜色不清楚为什么不会生效
            text_settings = {
                "text": "这是红色居中文本",      # 文本内容
                "font": {                      # 字体设置
                    "face": "微软雅黑",         # 字体名称
                    "size": 48,                # 字体大小
                    "style": ""                # 字体样式
                },
                "color": obs.inputs.rgb_to_bgr(0xff557f),  # 粉红色 (RGB转BGR)
                "align": "center",             # 水平居中
                "valign": "center",            # 垂直居中
                "outline": False,              # 是否显示轮廓
                "drop_shadow": False,          # 是否显示阴影
                "word_wrap": True              # 是否自动换行
            }

            # 创建文本输入源
            result = obs.inputs.create_input(
                input_name=test_input_name,
                input_kind="text_gdiplus_v3",  # 或 "text_ft2_source_v2"
                scene_name=test_scene,
                input_settings=text_settings
            )

            if result.get('success'):
                print(f"✅ 成功创建红色居中文本: {result['input_uuid']}")
                return True
            else:
                print("❌ 创建失败")
                return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


if __name__ == "__main__":
    # success = main()
    success = test_create_red_centered_text()
    sys.exit(0 if success else 1)
