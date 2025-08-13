#!/usr/bin/env python3
"""
输入类型映射演示

展示如何使用输入类型映射功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk.input_types import (
    InputTypeHelper, 
    to_chinese, 
    to_english, 
    get_category_name,
    InputCategory
)
from obs_sdk import OBSManager


def demo_basic_mapping():
    """演示基本映射功能"""
    print("🔄 基本映射功能演示")
    print("=" * 50)
    
    # 英文转中文
    english_types = ["text_gdiplus_v3", "image_source", "wasapi_input_capture"]
    
    print("英文 -> 中文:")
    for eng_type in english_types:
        chinese = to_chinese(eng_type)
        print(f"  {eng_type:<25} -> {chinese}")
    
    print("\n中文 -> 英文:")
    chinese_names = ["文本(GDI+)", "图像", "音频输入采集"]
    for chinese in chinese_names:
        english = to_english(chinese)
        print(f"  {chinese:<15} -> {english}")


def demo_category_features():
    """演示分类功能"""
    print("\n🏷️ 分类功能演示")
    print("=" * 50)
    
    # 显示各分类的输入类型
    for category in InputCategory:
        types = InputTypeHelper.get_types_by_category(category)
        print(f"\n【{category.value}】({len(types)} 个):")
        for eng_type in types:
            chinese = to_chinese(eng_type)
            print(f"  {eng_type:<30} -> {chinese}")


def demo_search_functionality():
    """演示搜索功能"""
    print("\n🔍 搜索功能演示")
    print("=" * 50)
    
    # 搜索包含"音频"的类型
    print("搜索包含'音频'的类型:")
    results = InputTypeHelper.search_by_keyword("音频", search_chinese=True)
    for eng_type, chinese in results:
        print(f"  {eng_type:<30} -> {chinese}")
    
    # 搜索包含"capture"的类型
    print("\n搜索包含'capture'的类型:")
    results = InputTypeHelper.search_by_keyword("capture", search_chinese=False)
    for eng_type, chinese in results:
        print(f"  {eng_type:<30} -> {chinese}")


def demo_validation():
    """演示验证功能"""
    print("\n✅ 验证功能演示")
    print("=" * 50)
    
    test_types = [
        "text_gdiplus_v3",      # 有效
        "invalid_type",         # 无效
        "image_source",         # 有效
        "old_text_source"       # 无效
    ]
    
    for test_type in test_types:
        is_valid = InputTypeHelper.is_valid_type(test_type)
        status = "✅ 有效" if is_valid else "❌ 无效"
        chinese = to_chinese(test_type) if is_valid else "未知类型"
        print(f"  {test_type:<20} -> {status} ({chinese})")


def demo_with_real_obs():
    """与真实 OBS 数据对比演示"""
    print("\n🎯 与真实 OBS 数据对比")
    print("=" * 50)
    
    try:
        with OBSManager() as obs:
            # 获取 OBS 实际支持的类型
            actual_types = obs.inputs.get_input_kinds()
            print(f"OBS 实际支持 {len(actual_types)} 种输入类型")
            
            # 检查映射覆盖率
            mapped_count = 0
            unmapped_types = []
            
            print("\n类型映射状态:")
            for actual_type in actual_types:
                if InputTypeHelper.is_valid_type(actual_type):
                    chinese = to_chinese(actual_type)
                    category = get_category_name(actual_type)
                    print(f"  ✅ {actual_type:<30} -> {chinese} ({category})")
                    mapped_count += 1
                else:
                    print(f"  ❌ {actual_type:<30} -> 未映射")
                    unmapped_types.append(actual_type)
            
            print(f"\n📊 映射统计:")
            print(f"  已映射: {mapped_count}/{len(actual_types)} ({mapped_count/len(actual_types)*100:.1f}%)")
            
            if unmapped_types:
                print(f"  未映射的类型: {unmapped_types}")
                
    except Exception as e:
        print(f"❌ 无法连接到 OBS: {e}")


def demo_practical_usage():
    """演示实际使用场景"""
    print("\n💡 实际使用场景演示")
    print("=" * 50)
    
    # 场景1: 用户界面显示
    print("场景1: 用户界面下拉菜单")
    mappings = InputTypeHelper.get_mapping_with_category()
    
    # 按分类组织显示
    for category in InputCategory:
        category_items = []
        for eng_type, (chinese, cat_name) in mappings.items():
            if cat_name == category.value:
                category_items.append((eng_type, chinese))
        
        if category_items:
            print(f"\n  {category.value}:")
            for eng_type, chinese in category_items:
                print(f"    {chinese} ({eng_type})")
    
    # 场景2: 配置文件处理
    print(f"\n场景2: 配置文件处理")
    config_data = {
        "inputs": [
            {"type": "text_gdiplus_v3", "name": "标题文本"},
            {"type": "image_source", "name": "背景图片"},
            {"type": "wasapi_input_capture", "name": "麦克风"}
        ]
    }
    
    print("配置文件中的输入源:")
    for input_config in config_data["inputs"]:
        eng_type = input_config["type"]
        chinese = to_chinese(eng_type)
        category = get_category_name(eng_type)
        print(f"  {input_config['name']}: {chinese} ({category})")


def demo_formatted_display():
    """演示格式化显示"""
    print("\n📋 完整类型对照表")
    print("=" * 50)
    print(InputTypeHelper.get_formatted_list())


def main():
    """主演示函数"""
    print("🚀 输入类型映射系统演示")
    print("=" * 60)
    
    demos = [
        demo_basic_mapping,
        demo_category_features,
        demo_search_functionality,
        demo_validation,
        demo_with_real_obs,
        demo_practical_usage,
        demo_formatted_display
    ]
    
    for demo_func in demos:
        try:
            demo_func()
            print()  # 空行分隔
        except Exception as e:
            print(f"❌ 演示 {demo_func.__name__} 失败: {e}")
    
    print("✅ 演示完成")


if __name__ == "__main__":
    main()
