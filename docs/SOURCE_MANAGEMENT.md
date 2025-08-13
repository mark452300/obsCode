# 源管理功能文档

OBS SDK 提供了完整的源管理功能，允许您创建、删除、配置各种类型的源，并将它们添加到场景中。

## 功能概述

源管理器 (`SourceManager`) 提供以下核心功能：

- ✅ **创建源** - 支持文本、图像、视频、颜色、浏览器等多种源类型
- ✅ **删除源** - 安全删除不需要的源
- ✅ **源属性管理** - 获取和设置源的各种属性
- ✅ **源到场景添加** - 将源添加到指定场景并设置位置、缩放等
- ✅ **源信息查询** - 获取源列表、检查源存在性等

## 快速开始

### 基本使用

```python
from obs_sdk import OBSManager, OBSConfig

# 创建 OBS 管理器
config = OBSConfig()
with OBSManager(config) as obs:
    # 创建文本源
    obs.create_text_source("我的文本", "Hello World!", font_size=48, color=0xFF0000)
    
    # 创建颜色源
    obs.create_color_source("背景色", color=0x00FF00, width=1920, height=1080)
    
    # 将源添加到当前场景
    current_scene = obs.get_current_scene()
    obs.add_source_to_scene(current_scene, "我的文本", position=(100, 100))
    
    # 修改文本内容
    obs.set_text_content("我的文本", "新的文本内容")
    
    # 删除源
    obs.delete_source("我的文本")
```

## 支持的源类型

### 1. 文本源

```python
# 创建文本源
obs.create_text_source(
    source_name="标题文本",
    text="欢迎观看直播",
    font_size=48,
    color=0xFFFFFF  # 白色
)

# 更新文本内容
obs.set_text_content("标题文本", "新的标题")
```

### 2. 图像源

```python
# 创建图像源
obs.create_image_source("背景图", "/path/to/image.png")

# 更改图像路径
obs.set_image_path("背景图", "/path/to/new_image.jpg")
```

### 3. 视频源

```python
# 创建视频源
obs.create_video_source("宣传视频", "/path/to/video.mp4", loop=True)

# 更改视频路径
obs.set_video_path("宣传视频", "/path/to/new_video.mp4")
```

### 4. 颜色源

```python
# 创建颜色源（常用作背景）
obs.create_color_source(
    source_name="纯色背景",
    color=0x000000,  # 黑色
    width=1920,
    height=1080
)
```

### 5. 浏览器源

```python
# 创建浏览器源
obs.create_browser_source(
    source_name="网页内容",
    url="https://example.com",
    width=1280,
    height=720
)
```

## 源管理操作

### 查询源信息

```python
# 获取所有源名称
sources = obs.get_sources()
print(f"所有源: {sources}")

# 检查源是否存在
exists = obs.source_exists("我的源")
print(f"源存在: {exists}")

# 获取源管理信息摘要
info = obs.sources.get_info()
print(f"源信息: {info}")
```

### 源到场景管理

```python
# 将源添加到场景（基本）
obs.add_source_to_scene("游戏场景", "我的文本")

# 将源添加到场景（指定位置和缩放）
obs.add_source_to_scene(
    scene_name="游戏场景",
    source_name="我的文本",
    position=(100, 200),  # x=100, y=200
    scale=(1.5, 1.5)      # 放大1.5倍
)
```

### 高级源操作

```python
# 直接使用 SourceManager
source_manager = obs.sources

# 创建自定义源
source_manager.create_source(
    source_name="自定义源",
    source_type="text_gdiplus_v2",  # 使用原始源类型
    settings={
        'text': '自定义文本',
        'font': {'face': 'Arial', 'size': 32}
    }
)

# 获取和设置源设置
settings = source_manager.get_settings("我的源")
settings['text'] = '修改后的文本'
source_manager.set_settings("我的源", settings)

# 获取源详细信息
info = source_manager.get_source_info("我的源")
print(f"源详细信息: {info}")
```

## 源类型常量

SourceManager 提供了常用源类型的常量：

```python
from obs_sdk.sources import SourceManager

# 可用的源类型
print(SourceManager.SOURCE_TYPES)
# 输出:
# {
#     'text': 'text_gdiplus_v2',
#     'image': 'image_source',
#     'video': 'ffmpeg_source',
#     'audio': 'ffmpeg_source',
#     'window': 'window_capture',
#     'display': 'monitor_capture',
#     'camera': 'dshow_input',
#     'browser': 'browser_source',
#     'color': 'color_source'
# }
```

## 错误处理

```python
from obs_sdk.exceptions import OBSResourceNotFoundError

try:
    # 尝试删除不存在的源
    obs.delete_source("不存在的源")
except OBSResourceNotFoundError as e:
    print(f"源不存在: {e}")
    print(f"可用源: {e.available_resources}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 完整示例

```python
#!/usr/bin/env python3
from obs_sdk import OBSManager, OBSConfig

def setup_streaming_scene():
    """设置一个完整的直播场景"""
    config = OBSConfig()
    
    with OBSManager(config) as obs:
        # 创建或切换到直播场景
        scene_name = "直播场景"
        if not obs.scenes.exists(scene_name):
            obs.create_scene(scene_name)
        obs.switch_scene(scene_name)
        
        # 创建背景
        obs.create_color_source("背景", color=0x1a1a1a, width=1920, height=1080)
        obs.add_source_to_scene(scene_name, "背景", position=(0, 0))
        
        # 创建标题
        obs.create_text_source("标题", "欢迎观看直播", font_size=48, color=0xFFFFFF)
        obs.add_source_to_scene(scene_name, "标题", position=(100, 50))
        
        # 创建信息栏
        obs.create_text_source("信息", "正在直播中...", font_size=24, color=0x00FF00)
        obs.add_source_to_scene(scene_name, "信息", position=(100, 120))
        
        # 创建网页源（如聊天窗口）
        obs.create_browser_source("聊天", "https://chat.example.com", 400, 600)
        obs.add_source_to_scene(scene_name, "聊天", position=(1500, 200))
        
        print("直播场景设置完成！")

if __name__ == "__main__":
    setup_streaming_scene()
```

## 注意事项

1. **源名称唯一性** - 每个源的名称必须唯一
2. **文件路径** - 图像和视频源需要提供有效的文件路径
3. **场景存在性** - 添加源到场景前确保场景存在
4. **资源清理** - 不需要的源应及时删除以释放资源
5. **权限问题** - 确保 OBS 有权限访问指定的文件和网络资源

## 测试

运行源管理功能测试：

```bash
python tests/test_source_management.py
```

这将测试所有源管理功能，包括创建、删除、属性设置和场景添加等操作。
