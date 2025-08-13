# 场景创建功能 - 新增特性说明

## 概述

为 OBS SDK 的 `SceneManager` 类添加了场景创建和删除功能，现在可以通过代码动态创建和管理 OBS 场景。

## 新增功能

### SceneManager 新方法

#### 1. `create(scene_name: str) -> bool`
创建新场景

**参数:**
- `scene_name`: 场景名称

**返回值:**
- `bool`: 操作是否成功

**特性:**
- 自动检查场景是否已存在，避免重复创建
- 创建成功后记录日志
- 异常处理和错误日志

**示例:**
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    success = obs.scenes.create("我的新场景")
    if success:
        print("场景创建成功!")
```

#### 2. `delete(scene_name: str) -> bool`
删除场景

**参数:**
- `scene_name`: 场景名称

**返回值:**
- `bool`: 操作是否成功

**异常:**
- `OBSResourceNotFoundError`: 场景不存在时抛出

**特性:**
- 删除前检查场景是否存在
- 提供详细的错误信息和可用场景列表
- 完整的异常处理

**示例:**
```python
from obs_sdk import OBSManager
from obs_sdk.exceptions import OBSResourceNotFoundError

with OBSManager() as obs:
    try:
        success = obs.scenes.delete("旧场景")
        if success:
            print("场景删除成功!")
    except OBSResourceNotFoundError as e:
        print(f"场景不存在: {e}")
        print(f"可用场景: {e.available_resources}")
```

### OBSManager 新的便捷方法

#### 1. `create_scene(scene_name: str) -> bool`
创建新场景的便捷方法

#### 2. `delete_scene(scene_name: str) -> bool`
删除场景的便捷方法

**示例:**
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 创建场景
    obs.create_scene("录制场景")
    obs.create_scene("直播场景")
    
    # 切换场景
    obs.switch_scene("录制场景")
    
    # 删除不需要的场景
    obs.delete_scene("旧场景")
```

## 使用场景

### 1. 动态场景管理
```python
def setup_recording_environment():
    with OBSManager() as obs:
        # 创建录制所需的场景
        scenes_to_create = [
            "开场画面",
            "主要内容", 
            "结束画面"
        ]
        
        for scene in scenes_to_create:
            if not obs.scenes.exists(scene):
                obs.create_scene(scene)
                print(f"创建场景: {scene}")
```

### 2. 批量场景操作
```python
def batch_scene_management():
    with OBSManager() as obs:
        # 获取当前场景
        current_scenes = obs.get_scenes()
        print(f"当前场景: {current_scenes}")
        
        # 创建新场景
        new_scenes = ["场景1", "场景2", "场景3"]
        for scene in new_scenes:
            success = obs.create_scene(scene)
            print(f"创建 {scene}: {'成功' if success else '失败'}")
        
        # 显示更新后的场景列表
        updated_scenes = obs.get_scenes()
        print(f"更新后场景: {updated_scenes}")
```

### 3. 临时场景管理
```python
def temporary_scene_workflow():
    with OBSManager() as obs:
        temp_scene = "临时场景"
        
        try:
            # 创建临时场景
            obs.create_scene(temp_scene)
            obs.switch_scene(temp_scene)
            
            # 执行一些操作...
            print("在临时场景中执行操作")
            
        finally:
            # 清理临时场景
            if obs.scenes.exists(temp_scene):
                obs.delete_scene(temp_scene)
                print("临时场景已清理")
```

## 技术实现

### OBS WebSocket 协议支持
- 使用 `CreateScene` 请求创建场景
- 使用 `RemoveScene` 请求删除场景
- 通过 obs-websocket-py 的动态类生成机制实现

### 错误处理
- 创建场景前检查是否已存在
- 删除场景前检查是否存在
- 完整的异常处理和日志记录
- 使用自定义异常 `OBSResourceNotFoundError`

### 日志记录
- 成功操作记录 INFO 级别日志
- 失败操作记录 ERROR 级别日志
- 重复创建记录 WARNING 级别日志

## 文档更新

已更新以下文档文件:
- `docs/README.md` - 添加场景创建示例
- `docs/MODULAR_DESIGN.md` - 更新 SceneManager 功能说明
- `modular_example.py` - 添加场景创建演示

## 测试文件

创建了以下测试和示例文件:
- `test_scene_creation.py` - 完整的功能测试脚本
- `scene_creation_example.py` - 简单的使用示例

## 兼容性

- 与现有 OBS SDK 功能完全兼容
- 不影响现有代码的使用
- 遵循现有的代码风格和设计模式
- 支持 obs-websocket v5 协议

## 注意事项

1. **场景名称唯一性**: OBS 中场景名称必须唯一
2. **权限要求**: 需要 OBS WebSocket 的场景管理权限
3. **错误处理**: 建议使用 try-catch 处理可能的异常
4. **资源清理**: 及时删除不需要的场景以保持 OBS 整洁

## 示例代码

完整的使用示例请参考:
- `scene_creation_example.py` - 基础使用示例
- `test_scene_creation.py` - 功能测试示例
- `modular_example.py` - 集成演示
