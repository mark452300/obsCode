"""
OBS SDK - 模块化的 OBS 控制库

这是一个模块化设计的 OBS 控制 SDK，将不同功能分离到不同的模块中，
便于维护和扩展。

使用示例:
    from obs_sdk import OBSClient
    from obs_sdk.recording import RecordingManager
    from obs_sdk.scenes import SceneManager
    
    client = OBSClient()
    recording = RecordingManager(client)
    scenes = SceneManager(client)
    
    scenes.switch_to("游戏场景")
    recording.start()
"""

# 导入核心组件
from .core import OBSClient, OBSConfig, OBSManager
from .core.exceptions import *

# 导入各个功能模块
from .managers import (
    RecordingManager,
    StreamingManager,
    SceneManager,
    InputManager,
    VirtualCameraManager,
    SceneItemManager,
    SourceManager,
)

__version__ = "1.0.0"
__author__ = "OBS SDK Team"

__all__ = [
    # 核心组件
    "OBSClient",
    "OBSConfig", 
    "OBSManager",
    
    # 功能管理器
    "RecordingManager",
    "StreamingManager",
    "SceneManager",
    "InputManager",
    "VirtualCameraManager",
    "SceneItemManager",
    "SourceManager",
    
    # 异常类
    "OBSError",
    "OBSConnectionError",
    "OBSAuthenticationError",
    "OBSRequestError",
    "OBSResourceNotFoundError",
    "OBSNotReadyError",
]
