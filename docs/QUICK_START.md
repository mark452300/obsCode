# OBS SDK 快速开始指南

## 安装和运行

### 方法1：直接运行（推荐）

1. **确保依赖已安装**：
   ```bash
   pip install obs-websocket-py
   ```

2. **使用运行脚本**：
   ```bash
   python run_tests.py
   ```

3. **或者直接运行测试文件**：
   ```bash
   # 从项目根目录运行
   python tests/test_scene_creation.py
   python tests/scene_creation_example.py
   ```

### 方法2：安装为包

1. **安装 obs_sdk 包**：
   ```bash
   pip install -e .
   ```

2. **运行测试**：
   ```bash
   python tests/test_scene_creation.py
   ```

### 方法3：手动设置路径

如果上述方法都不行，可以在 Python 脚本开头添加：

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

## 配置 OBS

在运行测试之前，请确保：

1. **OBS Studio 正在运行**
2. **启用 WebSocket 服务器**：
   - 打开 OBS Studio
   - 进入 **工具** → **obs-websocket 设置**
   - 勾选 **启用 WebSocket 服务器**
   - 设置端口 (默认: 4455)
   - 设置密码（可选）
   - 点击 **应用**

3. **配置连接**：
   - 如果设置了密码，修改测试文件中的配置
   - 如果没有密码，使用 `OBSConfig()` 即可

## 运行测试

### 基础功能测试
```bash
python tests/scene_creation_example.py
```

### 完整功能测试
```bash
python tests/test_scene_creation.py
```

### 使用运行脚本（推荐）
```bash
python run_tests.py
```

## 常见问题

### 1. ModuleNotFoundError: No module named 'obs_sdk'

**解决方案**：
- 确保在项目根目录运行脚本
- 使用 `python run_tests.py` 运行
- 或者运行 `pip install -e .` 安装包

### 2. 连接失败

**检查项**：
- OBS Studio 是否正在运行
- WebSocket 服务器是否已启用
- 端口和密码配置是否正确
- 防火墙是否阻止连接

### 3. 权限错误

**解决方案**：
- 确保 OBS WebSocket 允许场景管理操作
- 检查 OBS 版本是否支持相关功能

## 示例代码

### 基本使用
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 创建场景
    obs.create_scene("我的新场景")
    
    # 切换场景
    obs.switch_scene("我的新场景")
    
    # 获取场景列表
    scenes = obs.get_scenes()
    print(f"当前场景: {scenes}")
```

### 批量操作
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 批量创建场景
    scenes_to_create = ["开场", "内容", "结尾"]
    
    for scene in scenes_to_create:
        success = obs.create_scene(scene)
        print(f"创建 {scene}: {'成功' if success else '失败'}")
```

## 下一步

1. 查看 `docs/README.md` 了解完整功能
2. 查看 `docs/MODULAR_DESIGN.md` 了解架构设计
3. 查看 `SCENE_CREATION_FEATURE.md` 了解新功能详情
4. 运行 `modular_example.py` 查看完整示例
