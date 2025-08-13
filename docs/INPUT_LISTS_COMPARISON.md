# 输入列表 vs 输入类型列表 详细对比

本文档详细说明 OBS SDK 中"获取输入列表"和"获取输入类型列表"两个功能的区别和用途。

## 📋 功能对比表

| 功能 | 获取输入列表 | 获取输入类型列表 |
|------|-------------|-----------------|
| **方法名** | `get_names()` / `get_all()` | `get_input_kinds()` |
| **OBS 请求** | `GetInputList` | `GetInputKindList` |
| **返回内容** | 已创建的输入源实例名称 | 系统支持的输入源类型 |
| **数据性质** | 动态（用户创建的） | 静态（系统支持的） |
| **用途** | 操作现有输入源 | 创建新输入源 |
| **示例返回** | `["麦克风", "桌面音频"]` | `["wasapi_input_capture", "dshow_input"]` |

## 🔍 详细说明

### 1. 获取输入列表 (`get_names()`)

**功能描述：**
- 获取当前 OBS 中**已经创建**的输入源实例
- 返回用户自定义的输入源名称
- 这些是可以直接操作的输入源

**代码示例：**
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 获取所有输入源名称
    input_names = obs.get_inputs()
    print("当前输入源:", input_names)
    # 输出: ['桌面音频', '麦克风/Aux', '我的摄像头', '游戏声音']
    
    # 操作这些输入源
    obs.mute_input("麦克风/Aux")
    obs.unmute_input("桌面音频")
```

**使用场景：**
- 静音/取消静音操作
- 检查输入源是否存在
- 获取输入源设置
- 显示当前可用的输入源列表

### 2. 获取输入类型列表 (`get_input_kinds()`)

**功能描述：**
- 获取 OBS 系统**支持**的所有输入源类型
- 返回技术性的类型标识符
- 这些是可以用来创建新输入源的类型

**代码示例：**
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 获取所有支持的输入类型
    input_kinds = obs.get_input_kinds()
    print("支持的输入类型:", input_kinds)
    # 输出: ['wasapi_input_capture', 'dshow_input', 'image_source', ...]
    
    # 获取无版本的类型（用于创建源）
    unversioned_kinds = obs.get_input_kinds(unversioned=True)
    print("无版本类型:", unversioned_kinds)
    # 输出: ['wasapi_input_capture', 'dshow_input', 'image_source', ...]
```

**使用场景：**
- 创建新的输入源
- 检查系统支持哪些输入类型
- 开发输入源创建界面
- 系统兼容性检查

## 🎯 实际应用示例

### 场景1：检查和操作现有输入源

```python
with OBSManager() as obs:
    # 获取现有输入源
    inputs = obs.get_inputs()
    
    # 检查特定输入源是否存在
    if "麦克风" in inputs:
        # 操作现有输入源
        obs.mute_input("麦克风")
        print("麦克风已静音")
    else:
        print("未找到麦克风输入源")
```

### 场景2：检查系统能力并创建输入源

```python
with OBSManager() as obs:
    # 获取系统支持的输入类型
    supported_kinds = obs.get_input_kinds()
    
    # 检查是否支持摄像头输入
    if "dshow_input" in supported_kinds:
        # 可以创建摄像头输入源
        obs.sources.create_source(
            source_name="我的摄像头",
            source_type="dshow_input",
            settings={"video_device_id": "摄像头设备ID"}
        )
        print("摄像头输入源创建成功")
    else:
        print("系统不支持摄像头输入")
```

## 📊 常见输入类型说明

### 音频输入类型
- `wasapi_input_capture` - Windows 音频输入捕获（麦克风等）
- `wasapi_output_capture` - Windows 音频输出捕获（桌面音频等）
- `wasapi_process_output_capture` - 特定进程音频捕获

### 视频输入类型
- `dshow_input` - DirectShow 输入（摄像头、采集卡等）
- `monitor_capture` - 显示器捕获
- `window_capture` - 窗口捕获
- `game_capture` - 游戏捕获

### 媒体源类型
- `image_source` - 图像源
- `ffmpeg_source` - 媒体源（视频/音频文件）
- `text_gdiplus_v3` - 文本源
- `browser_source` - 浏览器源
- `color_source_v3` - 颜色源

## ⚠️ 注意事项

### 版本化类型
- **带版本**: `text_gdiplus_v3`, `color_source_v3`
- **无版本**: `text_gdiplus`, `color_source`
- 创建源时通常使用无版本类型
- 使用 `unversioned=True` 参数获取无版本类型

### 平台差异
- 不同操作系统支持的输入类型可能不同
- Windows: `wasapi_*`, `dshow_input`
- macOS: `coreaudio_*`, `av_capture_input`
- Linux: `pulse_*`, `v4l2_input`

### 最佳实践
1. **操作现有源**: 使用 `get_names()` 获取输入列表
2. **创建新源**: 使用 `get_input_kinds()` 检查支持的类型
3. **错误处理**: 始终检查输入源是否存在再进行操作
4. **跨平台**: 检查特定输入类型的可用性

## 🔗 相关方法

```python
# InputManager 相关方法
inputs.get_all()                    # 获取完整输入源信息
inputs.get_names()                  # 获取输入源名称列表
inputs.get_audio_inputs()           # 获取音频输入源
inputs.get_input_kinds()            # 获取输入类型列表
inputs.exists("输入源名")           # 检查输入源是否存在
inputs.get_info()                   # 获取输入源信息摘要

# OBSManager 便捷方法
obs.get_inputs()                    # 获取输入源名称列表
obs.get_audio_inputs()              # 获取音频输入源
obs.get_input_kinds()               # 获取输入类型列表
```
