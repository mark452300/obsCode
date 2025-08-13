# get_input_default_settings 方法文档

## 📋 **概述**

`get_input_default_settings` 方法用于获取指定输入类型的默认设置，基于 OBS WebSocket API 的 `GetInputDefaultSettings` 请求实现。

## 🔧 **方法签名**

```python
def get_input_default_settings(self, input_kind: str) -> Dict[str, Any]:
```

## 📝 **参数说明**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `input_kind` | `str` | 是 | 要获取默认设置的输入类型名称 |

## 🎯 **返回值**

- **类型**：`Dict[str, Any]`
- **说明**：包含输入类型默认设置的字典对象
- **空字典**：当输入类型无效或无设置时返回 `{}`

## 🚨 **异常情况**

| 异常类型 | 触发条件 | 说明 |
|----------|----------|------|
| `ValueError` | 输入类型为空或 None | 参数验证失败 |
| `OBSResourceNotFoundError` | 输入类型不存在 | 某些情况下可能抛出 |
| `Exception` | OBS 连接或其他错误 | 网络问题或 OBS 内部错误 |

## 💡 **使用示例**

### 基本使用

```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 获取文本输入源的默认设置
    text_settings = obs.inputs.get_input_default_settings("text_gdiplus_v3")
    print(f"文本输入源有 {len(text_settings)} 个默认设置")
    
    # 获取颜色源的默认设置
    color_settings = obs.inputs.get_input_default_settings("color_source_v3")
    print(f"颜色源默认颜色: {color_settings.get('color', 'N/A')}")
```

### 使用默认设置创建输入源

```python
with OBSManager() as obs:
    # 1. 获取默认设置
    default_settings = obs.inputs.get_input_default_settings("text_gdiplus_v3")
    
    # 2. 修改部分设置
    custom_settings = default_settings.copy()
    custom_settings["text"] = "我的自定义文本"
    custom_settings["color"] = 0xFF0000  # 红色
    
    # 3. 创建输入源
    result = obs.inputs.create_input(
        input_name="自定义文本",
        input_kind="text_gdiplus_v3",
        scene_name="主场景",
        input_settings=custom_settings
    )
```

### 批量获取所有输入类型的默认设置

```python
with OBSManager() as obs:
    # 获取所有可用的输入类型
    available_types = obs.inputs.get_input_kinds()
    
    # 获取每种类型的默认设置
    all_defaults = {}
    for input_type in available_types:
        try:
            settings = obs.inputs.get_input_default_settings(input_type)
            all_defaults[input_type] = settings
            print(f"{input_type}: {len(settings)} 个设置项")
        except Exception as e:
            print(f"{input_type}: 获取失败 - {e}")
```

### 错误处理

```python
try:
    settings = obs.inputs.get_input_default_settings("text_gdiplus_v3")
    print(f"获取到 {len(settings)} 个默认设置")
    
except ValueError as e:
    print(f"参数错误: {e}")
    
except OBSResourceNotFoundError as e:
    print(f"输入类型不存在: {e}")
    
except Exception as e:
    print(f"获取失败: {e}")
```

## 📊 **常见输入类型的默认设置**

基于测试结果，以下是各种输入类型的默认设置数量：

| 输入类型 | 中文名称 | 设置项数量 | 主要设置 |
|----------|----------|------------|----------|
| `text_gdiplus_v3` | 文本(GDI+) | 19 | font, color, align, valign |
| `browser_source` | 浏览器 | 10 | css, fps, height, width |
| `game_capture` | 游戏采集 | 11 | capture_mode, window |
| `dshow_input` | 视频采集设备 | 9 | video_device_id, resolution |
| `ffmpeg_source` | 媒体源 | 9 | local_file, looping |
| `text_ft2_source_v2` | 文本(FreeType 2) | 8 | font, color, text |
| `slideshow_v2` | 图像幻灯片放映 | 7 | files, slide_time |
| `monitor_capture` | 显示器采集 | 5 | monitor, capture_cursor |
| `window_capture` | 窗口采集 | 5 | window, capture_cursor |
| `color_source_v3` | 色源 | 3 | color, width, height |
| `image_source` | 图像 | 2 | linear_alpha, unload |
| `wasapi_input_capture` | 音频输入采集 | 2 | device_id |
| `wasapi_output_capture` | 音频输出采集 | 2 | device_id |

## 🎨 **文本输入源详细设置**

`text_gdiplus_v3` 的默认设置示例：

```python
{
    "align": "left",              # 水平对齐
    "valign": "top",              # 垂直对齐
    "color": 16777215,            # 文本颜色 (白色)
    "font": {                     # 字体设置
        "face": "Arial",          # 字体名称
        "size": 256               # 字体大小
    },
    "antialiasing": True,         # 抗锯齿
    "opacity": 100,               # 不透明度
    "outline_size": 2,            # 轮廓大小
    "outline_color": 16777215,    # 轮廓颜色
    "bk_color": 0,                # 背景颜色
    "bk_opacity": 0,              # 背景不透明度
    "extents_cx": 100,            # 宽度范围
    "extents_cy": 100,            # 高度范围
    "extents_wrap": True,         # 自动换行
    # ... 更多设置
}
```

## 🎯 **实际应用场景**

### 1. **智能输入源创建**
```python
def create_smart_text_input(obs, text_content, color=None):
    """智能创建文本输入源"""
    # 获取默认设置
    defaults = obs.inputs.get_input_default_settings("text_gdiplus_v3")
    
    # 应用自定义设置
    defaults["text"] = text_content
    if color:
        defaults["color"] = color
    
    # 创建输入源
    return obs.inputs.create_input(
        input_name=f"文本_{int(time.time())}",
        input_kind="text_gdiplus_v3",
        scene_name="主场景",
        input_settings=defaults
    )
```

### 2. **设置模板系统**
```python
def create_input_template(obs, input_type):
    """创建输入源设置模板"""
    defaults = obs.inputs.get_input_default_settings(input_type)
    
    # 保存为模板文件
    template = {
        "type": input_type,
        "defaults": defaults,
        "timestamp": time.time()
    }
    
    return template
```

### 3. **配置验证**
```python
def validate_input_settings(obs, input_type, user_settings):
    """验证用户设置是否有效"""
    defaults = obs.inputs.get_input_default_settings(input_type)
    
    # 检查用户设置的键是否有效
    invalid_keys = set(user_settings.keys()) - set(defaults.keys())
    if invalid_keys:
        print(f"无效的设置键: {invalid_keys}")
    
    # 合并设置
    final_settings = defaults.copy()
    final_settings.update(user_settings)
    
    return final_settings
```

## 🧪 **测试覆盖**

我们为 `get_input_default_settings` 方法创建了全面的测试：

### 测试用例

1. **基本功能测试**
   - 获取常见输入类型的默认设置
   - 验证返回值类型和结构

2. **全类型测试**
   - 测试所有可用输入类型
   - 统计成功率和失败情况

3. **详细内容测试**
   - 验证具体设置项的存在
   - 检查设置值的类型和格式

4. **错误处理测试**
   - 空输入类型
   - 无效输入类型
   - None 值处理

5. **实际应用测试**
   - 使用默认设置创建输入源
   - 设置比较和分析

### 运行测试

```bash
# 运行专门的默认设置测试
py -3.11 tests/test_input_default_settings.py
```

## 📈 **性能和最佳实践**

1. **缓存默认设置**：对于频繁使用的输入类型，可以缓存默认设置
2. **设置验证**：使用默认设置来验证用户提供的设置
3. **模板创建**：基于默认设置创建输入源模板
4. **错误恢复**：当用户设置无效时，回退到默认设置

## 🔄 **与其他方法的配合**

### 完整的输入源管理流程

```python
with OBSManager() as obs:
    # 1. 获取默认设置
    defaults = obs.inputs.get_input_default_settings("text_gdiplus_v3")
    
    # 2. 自定义设置
    defaults["text"] = "Hello World"
    defaults["color"] = 0xFF0000
    
    # 3. 创建输入源
    result = obs.inputs.create_input(
        input_name="我的文本",
        input_kind="text_gdiplus_v3",
        scene_name="主场景",
        input_settings=defaults
    )
    
    # 4. 重命名（如果需要）
    if result['success']:
        obs.inputs.rename_input(
            new_input_name="重命名的文本",
            input_name="我的文本"
        )
    
    # 5. 删除（清理）
    obs.inputs.remove_input(input_name="重命名的文本")
```

这个方法为输入源的创建和管理提供了重要的基础信息，使得开发者能够更好地理解和使用各种输入类型的设置选项。
