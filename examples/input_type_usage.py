#!/usr/bin/env python3
"""
输入类型映射实际使用示例

展示如何在实际项目中使用输入类型映射功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager
from obs_sdk.input_types import InputTypeHelper, InputCategory


def example_user_interface():
    """示例：用户界面中的输入类型选择"""
    print("🖥️ 用户界面示例：输入类型选择器")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 获取可用的输入类型
            available_types = obs.inputs.get_input_kinds()
            
            # 按分类组织显示
            print("请选择要创建的输入类型：\n")
            
            option_num = 1
            type_options = {}
            
            for category in InputCategory:
                category_types = []
                for eng_type in available_types:
                    if InputTypeHelper.get_category(eng_type) == category:
                        category_types.append(eng_type)
                
                if category_types:
                    print(f"【{category.value}】")
                    for eng_type in category_types:
                        chinese_name = obs.inputs.get_chinese_name(eng_type)
                        print(f"  {option_num}. {chinese_name}")
                        type_options[option_num] = eng_type
                        option_num += 1
                    print()
            
            # 模拟用户选择
            print("用户选择了选项 6 (文本(GDI+))")
            selected_type = type_options.get(6, "text_gdiplus_v3")
            chinese_name = obs.inputs.get_chinese_name(selected_type)
            print(f"选择的类型: {chinese_name} ({selected_type})")
            
    except Exception as e:
        print(f"❌ 示例失败: {e}")


def example_config_processing():
    """示例：配置文件处理"""
    print("\n📄 配置文件处理示例")
    print("=" * 50)
    
    # 模拟配置文件（用户友好的中文配置）
    user_config = {
        "场景配置": {
            "主场景": [
                {"名称": "背景图片", "类型": "图像", "文件": "background.jpg"},
                {"名称": "标题文字", "类型": "文本(GDI+)", "内容": "欢迎观看"},
                {"名称": "麦克风", "类型": "音频输入采集", "设备": "默认"}
            ]
        }
    }
    
    print("用户配置文件 (中文):")
    for scene_name, inputs in user_config["场景配置"].items():
        print(f"\n场景: {scene_name}")
        for input_config in inputs:
            print(f"  - {input_config['名称']}: {input_config['类型']}")
    
    # 转换为 OBS API 需要的英文类型
    print(f"\n转换为 OBS API 格式:")
    try:
        with OBSManager() as obs:
            for scene_name, inputs in user_config["场景配置"].items():
                print(f"\n场景: {scene_name}")
                for input_config in inputs:
                    chinese_type = input_config["类型"]
                    english_type = obs.inputs.get_english_type(chinese_type)
                    print(f"  - {input_config['名称']}: {chinese_type} -> {english_type}")
                    
                    # 验证类型是否有效
                    if InputTypeHelper.is_valid_type(english_type):
                        print(f"    ✅ 类型有效")
                    else:
                        print(f"    ❌ 类型无效")
    
    except Exception as e:
        print(f"❌ 配置处理失败: {e}")


def example_input_creation_with_chinese():
    """示例：使用中文名称创建输入源"""
    print("\n🎯 使用中文名称创建输入源")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return
            
            target_scene = scenes[0]
            
            # 用户想要创建的输入源（使用中文名称）
            desired_inputs = [
                {"中文类型": "文本(GDI+)", "名称": "测试文本", "设置": {"text": "Hello World"}},
                {"中文类型": "色源", "名称": "红色背景", "设置": {"color": 0xFF0000}},
            ]
            
            print(f"在场景 '{target_scene}' 中创建输入源:")
            
            for input_info in desired_inputs:
                chinese_type = input_info["中文类型"]
                english_type = obs.inputs.get_english_type(chinese_type)
                
                print(f"\n创建: {input_info['名称']} ({chinese_type})")
                print(f"  中文类型: {chinese_type}")
                print(f"  英文类型: {english_type}")
                
                if InputTypeHelper.is_valid_type(english_type):
                    # 创建输入源
                    import time
                    unique_name = f"{input_info['名称']}_{int(time.time())}"
                    
                    result = obs.inputs.create_input(
                        input_name=unique_name,
                        input_kind=english_type,
                        scene_name=target_scene,
                        input_settings=input_info.get("设置", {})
                    )
                    
                    if result.get('success'):
                        print(f"  ✅ 创建成功: UUID={result['input_uuid']}")
                    else:
                        print(f"  ❌ 创建失败")
                else:
                    print(f"  ❌ 无效的输入类型")
    
    except Exception as e:
        print(f"❌ 创建输入源失败: {e}")


def example_search_and_filter():
    """示例：搜索和过滤输入类型"""
    print("\n🔍 搜索和过滤示例")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 搜索包含"音频"的类型
            print("搜索包含'音频'的输入类型:")
            audio_types = InputTypeHelper.search_by_keyword("音频", search_chinese=True)
            for eng_type, chinese_name in audio_types:
                # 检查是否在当前 OBS 中可用
                available_types = obs.inputs.get_input_kinds()
                status = "✅ 可用" if eng_type in available_types else "❌ 不可用"
                category = InputTypeHelper.get_category(eng_type)
                category_name = category.value if category else "未分类"
                print(f"  {chinese_name} ({eng_type}) - {status} [{category_name}]")
            
            # 按分类过滤
            print(f"\n获取所有文本类型:")
            text_types = InputTypeHelper.get_types_by_category(InputCategory.TEXT)
            available_types = obs.inputs.get_input_kinds()
            
            for eng_type in text_types:
                chinese_name = obs.inputs.get_chinese_name(eng_type)
                status = "✅ 可用" if eng_type in available_types else "❌ 不可用"
                print(f"  {chinese_name} ({eng_type}) - {status}")
    
    except Exception as e:
        print(f"❌ 搜索示例失败: {e}")


def example_validation_and_suggestions():
    """示例：类型验证和建议"""
    print("\n✅ 类型验证和建议示例")
    print("=" * 50)
    
    # 用户输入的类型（可能有错误）
    user_inputs = [
        "文本(GDI+)",           # 正确
        "文本源",               # 不准确
        "text_gdiplus_v3",     # 英文正确
        "old_text_source",     # 过时的类型
        "图像",                # 正确
        "图片",                # 不准确
    ]
    
    try:
        with OBSManager() as obs:
            available_types = obs.inputs.get_input_kinds()
            
            print("用户输入验证:")
            for user_input in user_inputs:
                print(f"\n输入: '{user_input}'")
                
                # 尝试作为中文名称
                english_type = obs.inputs.get_english_type(user_input)
                if InputTypeHelper.is_valid_type(english_type):
                    status = "✅ 可用" if english_type in available_types else "⚠️ 已映射但不可用"
                    print(f"  识别为: {user_input} -> {english_type} ({status})")
                    continue
                
                # 尝试作为英文类型
                if InputTypeHelper.is_valid_type(user_input):
                    chinese_name = obs.inputs.get_chinese_name(user_input)
                    status = "✅ 可用" if user_input in available_types else "⚠️ 已映射但不可用"
                    print(f"  识别为: {user_input} -> {chinese_name} ({status})")
                    continue
                
                # 提供建议
                print(f"  ❌ 未识别，搜索相似类型:")
                suggestions = InputTypeHelper.search_by_keyword(user_input[:2], search_chinese=True)
                if suggestions:
                    for eng_type, chinese_name in suggestions[:3]:  # 最多显示3个建议
                        print(f"    建议: {chinese_name} ({eng_type})")
                else:
                    print(f"    没有找到相似类型")
    
    except Exception as e:
        print(f"❌ 验证示例失败: {e}")


def main():
    """主函数"""
    print("🚀 输入类型映射实际使用示例")
    print("=" * 60)
    
    examples = [
        example_user_interface,
        example_config_processing,
        example_input_creation_with_chinese,
        example_search_and_filter,
        example_validation_and_suggestions
    ]
    
    for example_func in examples:
        try:
            example_func()
            print()  # 空行分隔
        except Exception as e:
            print(f"❌ 示例 {example_func.__name__} 失败: {e}")
    
    print("✅ 所有示例完成")


if __name__ == "__main__":
    main()
