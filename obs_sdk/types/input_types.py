#!/usr/bin/env python3
"""
OBS 输入类型映射配置

提供英文输入类型和中文名称的双向映射关系

真实软件里面还包含其他两个 :
一个是 场景  一个是 群组

"text_ft2_source_v2": "文本(FreeType 2)",  在真实软件中已经被启用
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum


class InputCategory(Enum):
    """输入类型分类"""
    MEDIA = "媒体"
    AUDIO = "音频"
    VIDEO = "视频"
    TEXT = "文本"
    CAPTURE = "采集"
    EFFECT = "效果"


# 输入类型映射表
INPUT_TYPE_MAPPING = {
    # 媒体类
    "image_source": "图像",
    "slideshow_v2": "图像幻灯片放映",
    "ffmpeg_source": "媒体源",
    "browser_source": "浏览器",
    
    # 文本类
    "text_gdiplus_v3": "文本(GDI+)",
    "text_ft2_source_v2": "文本(FreeType 2)",
    
    # 采集类
    "monitor_capture": "显示器采集",
    "window_capture": "窗口采集", 
    "game_capture": "游戏采集",
    "dshow_input": "视频采集设备",
    
    # 音频类
    "wasapi_input_capture": "音频输入采集",
    "wasapi_output_capture": "音频输出采集",
    "wasapi_process_output_capture": "应用程序音频采集(测试)",
    
    # 效果类
    "color_source_v3": "色源",
}

# 输入类型分类映射
INPUT_TYPE_CATEGORIES = {
    # 媒体类
    "image_source": InputCategory.MEDIA,
    "slideshow_v2": InputCategory.MEDIA,
    "ffmpeg_source": InputCategory.MEDIA,
    "browser_source": InputCategory.MEDIA,
    
    # 文本类
    "text_gdiplus_v3": InputCategory.TEXT,
    "text_ft2_source_v2": InputCategory.TEXT,
    
    # 采集类
    "monitor_capture": InputCategory.CAPTURE,
    "window_capture": InputCategory.CAPTURE,
    "game_capture": InputCategory.CAPTURE,
    "dshow_input": InputCategory.VIDEO,
    
    # 音频类
    "wasapi_input_capture": InputCategory.AUDIO,
    "wasapi_output_capture": InputCategory.AUDIO,
    "wasapi_process_output_capture": InputCategory.AUDIO,
    
    # 效果类
    "color_source_v3": InputCategory.EFFECT,
}

# 反向映射（中文到英文）
CHINESE_TO_ENGLISH_MAPPING = {v: k for k, v in INPUT_TYPE_MAPPING.items()}


class InputTypeHelper:
    """输入类型辅助工具类"""
    
    @staticmethod
    def get_chinese_name(english_type: str) -> str:
        """
        获取英文输入类型对应的中文名称
        
        Args:
            english_type: 英文输入类型
            
        Returns:
            str: 中文名称，如果未找到返回原英文类型
        """
        return INPUT_TYPE_MAPPING.get(english_type, english_type)
    
    @staticmethod
    def get_english_type(chinese_name: str) -> str:
        """
        获取中文名称对应的英文输入类型
        
        Args:
            chinese_name: 中文名称
            
        Returns:
            str: 英文输入类型，如果未找到返回原中文名称
        """
        return CHINESE_TO_ENGLISH_MAPPING.get(chinese_name, chinese_name)
    
    @staticmethod
    def get_category(english_type: str) -> Optional[InputCategory]:
        """
        获取输入类型的分类
        
        Args:
            english_type: 英文输入类型
            
        Returns:
            InputCategory: 输入类型分类，如果未找到返回 None
        """
        return INPUT_TYPE_CATEGORIES.get(english_type)
    
    @staticmethod
    def get_types_by_category(category: InputCategory) -> List[str]:
        """
        根据分类获取输入类型列表
        
        Args:
            category: 输入类型分类
            
        Returns:
            List[str]: 该分类下的英文输入类型列表
        """
        return [k for k, v in INPUT_TYPE_CATEGORIES.items() if v == category]
    
    @staticmethod
    def get_all_mappings() -> Dict[str, str]:
        """
        获取所有映射关系
        
        Returns:
            Dict[str, str]: 英文到中文的映射字典
        """
        return INPUT_TYPE_MAPPING.copy()
    
    @staticmethod
    def get_mapping_with_category() -> Dict[str, Tuple[str, str]]:
        """
        获取带分类的映射关系
        
        Returns:
            Dict[str, Tuple[str, str]]: 英文类型 -> (中文名称, 分类名称)
        """
        result = {}
        for english_type, chinese_name in INPUT_TYPE_MAPPING.items():
            category = INPUT_TYPE_CATEGORIES.get(english_type)
            category_name = category.value if category else "未分类"
            result[english_type] = (chinese_name, category_name)
        return result
    
    @staticmethod
    def search_by_keyword(keyword: str, search_chinese: bool = True) -> List[Tuple[str, str]]:
        """
        根据关键词搜索输入类型
        
        Args:
            keyword: 搜索关键词
            search_chinese: 是否搜索中文名称，False 则搜索英文类型
            
        Returns:
            List[Tuple[str, str]]: 匹配的 (英文类型, 中文名称) 列表
        """
        keyword = keyword.lower()
        results = []
        
        for english_type, chinese_name in INPUT_TYPE_MAPPING.items():
            if search_chinese:
                if keyword in chinese_name.lower():
                    results.append((english_type, chinese_name))
            else:
                if keyword in english_type.lower():
                    results.append((english_type, chinese_name))
        
        return results
    
    @staticmethod
    def is_valid_type(english_type: str) -> bool:
        """
        检查是否为有效的输入类型
        
        Args:
            english_type: 英文输入类型
            
        Returns:
            bool: 是否为有效类型
        """
        return english_type in INPUT_TYPE_MAPPING
    
    @staticmethod
    def get_formatted_list() -> str:
        """
        获取格式化的类型列表（用于显示）
        
        Returns:
            str: 格式化的字符串
        """
        lines = ["输入类型对照表:"]
        lines.append("=" * 50)
        
        # 按分类组织
        for category in InputCategory:
            types_in_category = InputTypeHelper.get_types_by_category(category)
            if types_in_category:
                lines.append(f"\n【{category.value}】")
                for english_type in types_in_category:
                    chinese_name = INPUT_TYPE_MAPPING[english_type]
                    lines.append(f"  {english_type:<30} -> {chinese_name}")
        
        return "\n".join(lines)


# 便捷函数
def to_chinese(english_type: str) -> str:
    """将英文输入类型转换为中文名称"""
    return InputTypeHelper.get_chinese_name(english_type)


def to_english(chinese_name: str) -> str:
    """将中文名称转换为英文输入类型"""
    return InputTypeHelper.get_english_type(chinese_name)


def get_category_name(english_type: str) -> str:
    """获取输入类型的分类名称"""
    category = InputTypeHelper.get_category(english_type)
    return category.value if category else "未分类"


# 导出常用的映射表
__all__ = [
    'INPUT_TYPE_MAPPING',
    'CHINESE_TO_ENGLISH_MAPPING', 
    'INPUT_TYPE_CATEGORIES',
    'InputCategory',
    'InputTypeHelper',
    'to_chinese',
    'to_english',
    'get_category_name'
]
