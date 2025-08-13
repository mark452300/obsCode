# OBS SDK 目录结构说明

## 📁 重新组织后的目录结构

```
obs_sdk/
├── __init__.py                 # 主入口文件，导出所有公共接口
├── core/                       # 核心组件
│   ├── __init__.py            # 核心模块导出
│   ├── client.py              # OBS 客户端连接
│   ├── config.py              # 配置管理
│   ├── exceptions.py          # 异常定义
│   └── manager.py             # 统一管理器接口
├── managers/                   # 功能管理器
│   ├── __init__.py            # 管理器模块导出
│   ├── inputs.py              # 输入源管理
│   ├── scenes.py              # 场景管理
│   ├── recording.py           # 录制管理
│   ├── streaming.py           # 推流管理
│   ├── virtual_camera.py      # 虚拟摄像头管理
│   ├── scene_items.py         # 场景项管理
│   └── sources.py             # 源管理
├── types/                      # 类型定义
│   ├── __init__.py            # 类型模块导出
│   └── input_types.py         # 输入类型定义和辅助函数
└── utils/                      # 工具类
    ├── __init__.py            # 工具模块导出
    └── color_utils.py         # 颜色转换工具
```

## 🎯 模块分类说明

### 1. **core** - 核心组件
- **client.py**: OBS WebSocket 客户端连接和通信
- **config.py**: 配置管理，包括连接参数等
- **exceptions.py**: 自定义异常类定义
- **manager.py**: 统一的 OBSManager 接口，整合所有功能

### 2. **managers** - 功能管理器
- **inputs.py**: 输入源相关功能（音量、静音、创建等）
- **scenes.py**: 场景管理（切换、创建、删除等）
- **recording.py**: 录制功能（开始、停止、暂停等）
- **streaming.py**: 推流功能（开始、停止推流等）
- **virtual_camera.py**: 虚拟摄像头控制
- **scene_items.py**: 场景项管理（位置、大小、可见性等）
- **sources.py**: 源管理功能

### 3. **types** - 类型定义
- **input_types.py**: 输入类型映射和转换辅助函数

### 4. **utils** - 工具类
- **color_utils.py**: 颜色格式转换工具（RGB ↔ BGR）

## 📦 导入方式

### 原有导入方式保持不变
```python
# 主要接口
from obs_sdk import OBSManager, OBSConfig

# 单独使用某个管理器
from obs_sdk import InputManager, SceneManager

# 使用工具类
from obs_sdk.utils import ColorUtils
```

### 新的模块化导入方式
```python
# 从核心模块导入
from obs_sdk.core import OBSClient, OBSConfig, OBSManager

# 从管理器模块导入
from obs_sdk.managers import InputManager, SceneManager

# 从类型模块导入
from obs_sdk.types import InputTypeHelper

# 从工具模块导入
from obs_sdk.utils import ColorUtils
```

## 🔄 重构的优势

1. **清晰的模块分离**: 每个目录有明确的职责
2. **更好的可维护性**: 相关功能集中在一起
3. **便于扩展**: 新功能可以轻松添加到对应目录
4. **向后兼容**: 原有的导入方式仍然有效
5. **代码组织**: 工具类和业务逻辑分离

## 🚀 使用建议

1. **新项目**: 推荐使用模块化导入方式
2. **现有项目**: 可以继续使用原有导入方式，无需修改
3. **工具类**: 建议使用 `from obs_sdk.utils import ColorUtils`
4. **核心功能**: 建议使用 `from obs_sdk import OBSManager`

## 📝 注意事项

- 所有原有的公共接口都保持不变
- 内部导入路径已更新，但不影响外部使用
- 新的目录结构更符合 Python 包的最佳实践
- 便于后续添加更多工具类和类型定义
