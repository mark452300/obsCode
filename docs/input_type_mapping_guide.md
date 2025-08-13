# OBS 输入类型映射系统使用指南

## 📋 **概述**

为了解决英文输入类型和中文名称对应的问题，我们创建了一个完整的映射系统，支持双向转换、分类管理和智能搜索。

## 🎯 **为什么使用 `text_gdiplus_v3`**

在测试中使用 `text_gdiplus_v3` 的原因：

1. **版本兼容性**：您的 OBS 版本支持 v3 而不是 v2
2. **功能完整性**：v3 版本提供了更好的文本渲染功能
3. **向前兼容**：使用最新支持的版本确保功能稳定

## 📊 **完整的输入类型对照表**

| 英文类型 | 中文名称 | 分类 | 说明 |
|---------|---------|------|------|
| `image_source` | 图像 | 媒体 | 静态图片显示 |
| `color_source_v3` | 色源 | 效果 | 纯色背景 |
| `slideshow_v2` | 图像幻灯片放映 | 媒体 | 多图片轮播 |
| `browser_source` | 浏览器 | 媒体 | 网页内容显示 |
| `ffmpeg_source` | 媒体源 | 媒体 | 视频/音频文件 |
| `text_gdiplus_v3` | 文本(GDI+) | 文本 | Windows 文本渲染 |
| `text_ft2_source_v2` | 文本(FreeType 2) | 文本 | 跨平台文本渲染 |
| `monitor_capture` | 显示器采集 | 采集 | 整个显示器内容 |
| `window_capture` | 窗口采集 | 采集 | 特定窗口内容 |
| `game_capture` | 游戏采集 | 采集 | 游戏画面采集 |
| `dshow_input` | 视频采集设备 | 视频 | 摄像头等设备 |
| `wasapi_input_capture` | 音频输入采集 | 音频 | 麦克风等输入 |
| `wasapi_output_capture` | 音频输出采集 | 音频 | 系统音频输出 |
| `wasapi_process_output_capture` | 应用程序音频采集(测试) | 音频 | 特定应用音频 |

## 🛠️ **推荐的存储和使用方式**

### 1. **模块化设计**
```python
# obs_sdk/input_types.py - 专门的映射模块
INPUT_TYPE_MAPPING = {
    "text_gdiplus_v3": "文本(GDI+)",
    "image_source": "图像",
    # ...
}
```

### 2. **分类管理**
```python
class InputCategory(Enum):
    MEDIA = "媒体"
    AUDIO = "音频" 
    TEXT = "文本"
    CAPTURE = "采集"
    # ...
```

### 3. **辅助工具类**
```python
class InputTypeHelper:
    @staticmethod
    def get_chinese_name(english_type: str) -> str:
        """英文转中文"""
        
    @staticmethod
    def get_english_type(chinese_name: str) -> str:
        """中文转英文"""
        
    @staticmethod
    def search_by_keyword(keyword: str) -> List[Tuple[str, str]]:
        """关键词搜索"""
```

## 💡 **实际使用场景**

### 1. **用户界面开发**
```python
# 按分类显示输入类型选择器
for category in InputCategory:
    types = InputTypeHelper.get_types_by_category(category)
    print(f"【{category.value}】")
    for eng_type in types:
        chinese_name = to_chinese(eng_type)
        print(f"  {chinese_name}")
```

### 2. **配置文件处理**
```python
# 用户友好的中文配置
user_config = {
    "输入源": [
        {"类型": "文本(GDI+)", "名称": "标题"},
        {"类型": "图像", "名称": "背景"}
    ]
}

# 转换为 API 调用
for item in user_config["输入源"]:
    english_type = to_english(item["类型"])
    obs.inputs.create_input(
        input_name=item["名称"],
        input_kind=english_type,
        scene_name="主场景"
    )
```

### 3. **智能搜索和建议**
```python
# 搜索音频相关类型
audio_types = InputTypeHelper.search_by_keyword("音频", search_chinese=True)
for eng_type, chinese_name in audio_types:
    print(f"{chinese_name} ({eng_type})")
```

### 4. **类型验证**
```python
def validate_input_type(user_input: str) -> bool:
    # 尝试作为中文名称
    english_type = to_english(user_input)
    if InputTypeHelper.is_valid_type(english_type):
        return True
    
    # 尝试作为英文类型
    return InputTypeHelper.is_valid_type(user_input)
```

## 🔧 **集成到现有代码**

### 在 InputManager 中添加便捷方法：
```python
class InputManager:
    def get_chinese_name(self, input_kind: str) -> str:
        """获取输入类型的中文名称"""
        return to_chinese(input_kind)
    
    def get_english_type(self, chinese_name: str) -> str:
        """根据中文名称获取英文输入类型"""
        return to_english(chinese_name)
    
    def get_input_types_with_chinese(self) -> Dict[str, str]:
        """获取输入类型及其中文名称映射"""
        return InputTypeHelper.get_all_mappings()
```

## 📈 **优势**

1. **双向映射**：支持英文↔中文双向转换
2. **分类管理**：按功能分类，便于组织和查找
3. **智能搜索**：支持关键词搜索和模糊匹配
4. **类型验证**：验证输入类型的有效性
5. **扩展性强**：易于添加新的输入类型
6. **用户友好**：提供中文界面支持

## 🚀 **使用示例**

### 基本使用
```python
from obs_sdk.input_types import to_chinese, to_english

# 英文转中文
chinese = to_chinese("text_gdiplus_v3")  # "文本(GDI+)"

# 中文转英文  
english = to_english("文本(GDI+)")       # "text_gdiplus_v3"
```

### 高级功能
```python
from obs_sdk.input_types import InputTypeHelper, InputCategory

# 搜索功能
results = InputTypeHelper.search_by_keyword("音频")

# 分类获取
text_types = InputTypeHelper.get_types_by_category(InputCategory.TEXT)

# 验证功能
is_valid = InputTypeHelper.is_valid_type("text_gdiplus_v3")
```

## 📝 **最佳实践**

1. **统一使用映射系统**：避免硬编码中英文对应关系
2. **分类组织界面**：按分类显示输入类型，提升用户体验
3. **提供搜索功能**：支持用户快速找到需要的类型
4. **验证用户输入**：确保输入的类型名称有效
5. **保持映射更新**：随 OBS 版本更新及时维护映射表

## 🔄 **维护和扩展**

当 OBS 新增输入类型时，只需要：

1. 在 `INPUT_TYPE_MAPPING` 中添加新的映射
2. 在 `INPUT_TYPE_CATEGORIES` 中指定分类
3. 系统自动支持新类型的所有功能

这种设计确保了系统的可维护性和扩展性。
