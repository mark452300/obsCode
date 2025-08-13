# 模块化 OBS SDK 设计

## 🎯 设计理念

模块化的架构，具有以下优势：

### ✅ 模块化优势

1. **职责分离** - 每个模块只负责特定功能
2. **易于维护** - 修改某个功能不影响其他模块
3. **可扩展性** - 新增功能只需添加新模块
4. **代码复用** - 模块可以独立使用
5. **测试友好** - 每个模块可以独立测试
6. **团队协作** - 不同开发者可以负责不同模块

## 📁 项目结构

```
obs_sdk/                           # 主 SDK 包
├── __init__.py                    # 包初始化，导出主要接口
├── client.py                      # WebSocket 客户端（底层通信）
├── config.py                      # 配置管理
├── exceptions.py                  # 异常定义
├── manager.py                     # 统一管理器（推荐使用）
├── recording.py                   # 录制管理器
├── streaming.py                   # 推流管理器
├── scenes.py                      # 场景管理器
├── inputs.py                      # 输入管理器
├── virtual_camera.py              # 虚拟摄像头管理器
└── scene_items.py                 # 场景项管理器

your_project/                      # 你的项目
├── obs_sdk/                       # 复制整个 obs_sdk 目录
├── main.py                        # 你的主程序
├── requirements.txt               # 依赖：obs-websocket-py
└── README.md                      # 使用说明
```

## 🏗️ 架构层次

```
┌─────────────────────────────────────┐
│           你的应用代码                │
├─────────────────────────────────────┤
│         OBSManager (统一接口)        │
├─────────────────────────────────────┤
│  功能管理器层                        │
│  ┌─────────┬─────────┬─────────┐    │
│  │Recording│Streaming│ Scenes  │    │
│  ├─────────┼─────────┼─────────┤    │
│  │ Inputs  │VirtCam  │SceneItem│    │
│  └─────────┴─────────┴─────────┘    │
├─────────────────────────────────────┤
│         OBSClient (通信层)           │
├─────────────────────────────────────┤
│       obs-websocket-py              │
├─────────────────────────────────────┤
│         OBS Studio                  │
└─────────────────────────────────────┘
```

## 💡 使用方式

### 方式1: 统一管理器（推荐）

```python
from obs_sdk import OBSManager, OBSConfig

# 最简单的使用
with OBSManager() as obs:
    obs.start_recording()
    obs.switch_scene("游戏场景")
    obs.mute_input("麦克风")

# 自定义配置
config = OBSConfig(password="your_password")
with OBSManager(config) as obs:
    # 使用便捷方法
    obs.quick_record(10)  # 录制10秒
  
    # 获取完整状态
    status = obs.get_status()
    print(status)
```

### 方式2: 独立模块使用

```python
from obs_sdk import OBSClient, OBSConfig
from obs_sdk.recording import RecordingManager
from obs_sdk.scenes import SceneManager

config = OBSConfig(password="your_password")
client = OBSClient(config)
client.connect()

# 只使用录制功能
recording = RecordingManager(client)
recording.start()
recording.stop()

# 只使用场景功能
scenes = SceneManager(client)
scenes.switch_to("场景1")

client.disconnect()
```

### 方式3: 混合使用

```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 使用统一接口的便捷方法
    obs.start_recording()
  
    # 直接访问特定模块的高级功能
    recording_info = obs.recording.get_info()
    scene_items = obs.scene_items.get_list("当前场景")
  
    # 使用底层客户端
    version = obs.client.get_version()
```

## 🔧 各模块功能

### RecordingManager (录制管理器)

```python
recording = obs.recording

# 基本操作
recording.start()                    # 开始录制
recording.stop()                     # 停止录制
recording.toggle()                   # 切换录制状态
recording.pause()                    # 暂停录制
recording.resume()                   # 恢复录制

# 状态查询
recording.is_recording()             # 是否正在录制
recording.is_paused()                # 是否暂停
recording.get_duration()             # 录制时长
recording.get_timecode()             # 时间码

# 便捷功能
recording.quick_record(10)           # 快速录制10秒
recording.get_info()                 # 获取录制信息摘要
```

### SceneManager (场景管理器)

```python
scenes = obs.scenes

# 场景操作
scenes.get_names()                   # 获取场景名称列表
scenes.get_current_program()         # 获取当前节目场景
scenes.create("新场景")              # 创建场景
scenes.delete("旧场景")              # 删除场景
scenes.switch_to("场景名")           # 切换场景
scenes.exists("场景名")              # 检查场景是否存在

# Studio Mode
scenes.is_studio_mode_enabled()      # 检查Studio Mode状态
scenes.enable_studio_mode(True)      # 启用Studio Mode
scenes.set_preview("预览场景")       # 设置预览场景
scenes.trigger_transition()          # 触发转场

# 信息查询
scenes.get_info()                    # 获取场景信息摘要
```

### InputManager (输入管理器)

```python
inputs = obs.inputs

# 输入查询
inputs.get_names()                   # 获取所有输入名称
inputs.get_audio_inputs()            # 获取音频输入名称
inputs.get_input_kinds()             # 获取输入类型列表
inputs.exists("输入名")              # 检查输入是否存在

# 静音控制
inputs.is_muted("麦克风")            # 检查静音状态
inputs.mute("麦克风")                # 静音
inputs.unmute("麦克风")              # 取消静音
inputs.toggle_mute("麦克风")         # 切换静音状态

# 设置管理
inputs.get_settings("输入名")        # 获取输入设置
inputs.set_settings("输入名", {})    # 设置输入设置
inputs.get_info()                    # 获取输入信息摘要
```

### StreamingManager (推流管理器)

```python
streaming = obs.streaming

# 基本操作
streaming.start()                    # 开始推流
streaming.stop()                     # 停止推流
streaming.toggle()                   # 切换推流状态

# 状态查询
streaming.is_streaming()             # 是否正在推流
streaming.is_reconnecting()          # 是否正在重连
streaming.get_duration()             # 推流时长
streaming.get_bytes_sent()           # 已发送字节数
streaming.get_dropped_frames()       # 丢帧数
streaming.get_congestion()           # 网络拥塞度

# 信息查询
streaming.get_info()                 # 获取推流信息摘要
```

### VirtualCameraManager (虚拟摄像头管理器)

```python
virtual_cam = obs.virtual_camera

# 基本操作
virtual_cam.start()                  # 启动虚拟摄像头
virtual_cam.stop()                   # 停止虚拟摄像头
virtual_cam.toggle()                 # 切换虚拟摄像头状态

# 状态查询
virtual_cam.is_active()              # 是否激活
virtual_cam.get_info()               # 获取信息摘要
```

### SceneItemManager (场景项管理器)

```python
scene_items = obs.scene_items

# 场景项操作
scene_items.get_list("场景名")                    # 获取场景项列表
scene_items.get_id("场景名", "源名")              # 获取场景项ID
scene_items.is_enabled("场景名", item_id)        # 检查是否启用

# 显示控制
scene_items.show("场景名", item_id)               # 显示场景项
scene_items.hide("场景名", item_id)               # 隐藏场景项
scene_items.toggle("场景名", item_id)             # 切换显示状态

# 便捷方法（通过源名称）
scene_items.show_by_source_name("场景名", "源名")
scene_items.hide_by_source_name("场景名", "源名")
scene_items.toggle_by_source_name("场景名", "源名")

# 变换控制
scene_items.get_transform("场景名", item_id)      # 获取变换信息
scene_items.set_transform("场景名", item_id, {})  # 设置变换信息
scene_items.get_info("场景名")                    # 获取场景项信息摘要
```

## 🎯 实际使用示例

### 自动化录制工作流

```python
from obs_sdk import OBSManager

def automated_recording(duration=60):
    with OBSManager() as obs:
        # 1. 准备环境
        obs.switch_scene("录制场景")
        obs.unmute_input("麦克风")
      
        # 2. 开始录制
        obs.start_recording()
        print(f"开始录制 {duration} 秒...")
      
        # 3. 等待完成
        time.sleep(duration)
      
        # 4. 停止录制
        output_path = obs.stop_recording()
        print(f"录制完成: {output_path}")
      
        return output_path

# 使用
video_file = automated_recording(30)
```

### 直播自动化

```python
from obs_sdk import OBSManager

def start_live_stream():
    with OBSManager() as obs:
        # 切换到直播场景
        obs.switch_scene("直播场景")
      
        # 确保音频正常
        for input_name in obs.get_audio_inputs():
            obs.unmute_input(input_name)
      
        # 开始推流
        if obs.start_streaming():
            print("直播已开始")
            return True
        return False

def stop_live_stream():
    with OBSManager() as obs:
        obs.stop_streaming()
        obs.switch_scene("待机场景")
        print("直播已结束")

# 使用
start_live_stream()
# ... 直播进行中 ...
stop_live_stream()
```

### 场景自动化

```python
from obs_sdk import OBSManager

def scene_automation():
    with OBSManager() as obs:
        scenes = ["开场", "内容", "结尾"]
      
        for scene_name in scenes:
            print(f"切换到: {scene_name}")
            obs.switch_scene(scene_name)
          
            # 控制场景项
            if scene_name == "内容":
                obs.show_scene_item(scene_name, "Logo")
                obs.hide_scene_item(scene_name, "水印")
          
            time.sleep(10)  # 停留10秒

# 使用
scene_automation()
```

## 🚀 开始使用

1. **复制 obs_sdk 目录** 到你的项目
2. **安装依赖** `pip install obs-websocket-py`
3. **配置 OBS** WebSocket 设置
4. **开始编码**：

```python
from obs_sdk import OBSManager

# 最简单的使用
with OBSManager() as obs:
    # 你的 OBS 控制逻辑
    pass
```

这种模块化设计让你可以：

- ✅ **按需使用** - 只导入需要的模块
- ✅ **职责清晰** - 每个模块功能明确
- ✅ **易于扩展** - 新增功能不影响现有代码
- ✅ **便于测试** - 每个模块可独立测试
- ✅ **团队协作** - 多人开发不冲突

比单一 controller 的设计要好很多！🎉
