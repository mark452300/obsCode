# OBS SDK - 模块化的 OBS 控制库

一个用于通过 obs-websocket v5 协议控制 OBS Studio 的 Python 库，采用模块化设计。

## 🚀 快速开始

### 安装依赖
```bash
pip install obs-websocket-py
```

### 配置 OBS
1. 打开 OBS Studio
2. 进入 **工具** → **obs-websocket 设置**
3. 勾选 **启用 WebSocket 服务器**
4. 设置端口 (默认: 4455)
5. 设置密码
6. 点击 **应用**

### 基本使用

```python
from obs_sdk import OBSManager, OBSConfig

# 使用默认配置（从环境变量读取）
with OBSManager() as obs:
    obs.start_recording()
    obs.switch_scene("游戏场景")
    obs.mute_input("麦克风")

# 自定义配置
config = OBSConfig(password="your_password")
with OBSManager(config) as obs:
    # 快速录制 10 秒
    output_file = obs.quick_record(10)
    print(f"录制完成: {output_file}")
```

## 📁 项目结构

```
obs_sdk/                           # 主 SDK 包
├── __init__.py                    # 包初始化
├── client.py                      # WebSocket 客户端
├── config.py                      # 配置管理
├── exceptions.py                  # 异常定义
├── manager.py                     # 统一管理器（推荐）
├── recording.py                   # 录制管理器
├── streaming.py                   # 推流管理器
├── scenes.py                      # 场景管理器
├── inputs.py                      # 输入管理器
├── virtual_camera.py              # 虚拟摄像头管理器
└── scene_items.py                 # 场景项管理器
```

## 🎯 使用方式

### 方式1: 统一管理器（推荐）
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 录制控制
    obs.start_recording()
    obs.stop_recording()
    obs.quick_record(30)  # 录制30秒
    
    # 场景控制
    obs.switch_scene("场景名")
    obs.get_scenes()
    
    # 输入控制
    obs.mute_input("麦克风")
    obs.unmute_input("麦克风")
    
    # 推流控制
    obs.start_streaming()
    obs.stop_streaming()
    
    # 虚拟摄像头
    obs.start_virtual_camera()
    obs.stop_virtual_camera()
```

### 方式2: 独立模块使用
```python
from obs_sdk import OBSClient
from obs_sdk.recording import RecordingManager
from obs_sdk.scenes import SceneManager

client = OBSClient()
client.connect()

# 只使用需要的功能
recording = RecordingManager(client)
scenes = SceneManager(client)

recording.start()
scenes.switch_to("场景1")
recording.stop()

client.disconnect()
```

### 方式3: 混合使用
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 使用便捷方法
    obs.start_recording()
    
    # 访问特定模块的高级功能
    recording_info = obs.recording.get_info()
    scene_items = obs.scene_items.get_list("当前场景")
```

## 🔧 功能模块

### RecordingManager - 录制管理
```python
recording = obs.recording

recording.start()                    # 开始录制
recording.stop()                     # 停止录制
recording.pause()                    # 暂停录制
recording.resume()                   # 恢复录制
recording.toggle()                   # 切换录制状态
recording.quick_record(10)           # 快速录制10秒
recording.is_recording()             # 检查录制状态
recording.get_info()                 # 获取录制信息
```

### SceneManager - 场景管理
```python
scenes = obs.scenes

scenes.get_names()                   # 获取场景列表
scenes.create("新场景")              # 创建场景
scenes.delete("旧场景")              # 删除场景
scenes.switch_to("场景名")           # 切换场景
scenes.get_current_program()         # 获取当前场景
scenes.enable_studio_mode(True)      # 启用Studio Mode
scenes.trigger_transition()          # 触发转场
```

### InputManager - 输入管理
```python
inputs = obs.inputs

inputs.get_names()                   # 获取输入列表
inputs.get_audio_inputs()            # 获取音频输入
inputs.get_input_kinds()             # 获取输入类型列表
inputs.mute("麦克风")                # 静音
inputs.unmute("麦克风")              # 取消静音
inputs.toggle_mute("麦克风")         # 切换静音
inputs.is_muted("麦克风")            # 检查静音状态
```

### StreamingManager - 推流管理
```python
streaming = obs.streaming

streaming.start()                    # 开始推流
streaming.stop()                     # 停止推流
streaming.is_streaming()             # 检查推流状态
streaming.get_info()                 # 获取推流信息
```

### VirtualCameraManager - 虚拟摄像头
```python
virtual_cam = obs.virtual_camera

virtual_cam.start()                  # 启动虚拟摄像头
virtual_cam.stop()                   # 停止虚拟摄像头
virtual_cam.is_active()              # 检查状态
```

### SceneItemManager - 场景项管理
```python
scene_items = obs.scene_items

scene_items.show_by_source_name("场景名", "源名")    # 显示场景项
scene_items.hide_by_source_name("场景名", "源名")    # 隐藏场景项
scene_items.get_list("场景名")                      # 获取场景项列表
```

## 📋 配置选项

### 环境变量配置
```bash
export OBS_HOST=127.0.0.1
export OBS_PORT=4455
export OBS_PASSWORD=your_password
export OBS_TIMEOUT=10.0
```

### 代码配置
```python
from obs_sdk import OBSConfig

config = OBSConfig(
    host="127.0.0.1",
    port=4455,
    password="your_password",
    timeout=10.0,
    max_retries=3,
    auto_connect=True
)
```

## 🎯 实用示例

### 自动录制工作流
```python
from obs_sdk import OBSManager
import time

def auto_record_workflow():
    with OBSManager() as obs:
        # 准备环境
        obs.switch_scene("录制场景")
        obs.unmute_input("麦克风")
        
        # 开始录制
        obs.start_recording()
        print("录制开始...")
        
        # 等待完成
        time.sleep(60)  # 录制1分钟
        
        # 停止录制
        output_path = obs.stop_recording()
        print(f"录制完成: {output_path}")

auto_record_workflow()
```

### 直播自动化
```python
def start_live_stream():
    with OBSManager() as obs:
        obs.switch_scene("直播场景")
        obs.start_streaming()
        print("直播已开始")

def stop_live_stream():
    with OBSManager() as obs:
        obs.stop_streaming()
        obs.switch_scene("待机场景")
        print("直播已结束")
```

## 🔧 故障排除

### 连接失败
1. 确认 OBS 正在运行
2. 确认 obs-websocket 已启用
3. 检查主机地址和端口
4. 验证密码是否正确

### 常见错误
```python
from obs_sdk.exceptions import OBSResourceNotFoundError

try:
    obs.switch_scene("不存在的场景")
except OBSResourceNotFoundError as e:
    print(f"场景不存在: {e}")
    print(f"可用场景: {e.available_resources}")
```

## 📚 更多文档

- [模块化设计说明](MODULAR_DESIGN.md)
- [项目总结](PROJECT_SUMMARY.md)
- [快速开始指南](QUICK_START.md)

## 🎉 开始使用

1. 复制 `obs_sdk/` 目录到你的项目
2. 安装依赖: `pip install obs-websocket-py`
3. 配置 OBS WebSocket 设置
4. 开始编码:

```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 你的 OBS 控制逻辑
    pass
```

## 许可证

MIT License
