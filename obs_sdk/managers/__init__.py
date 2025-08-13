"""
OBS SDK 管理器模块

包含各种功能管理器，负责不同的 OBS 功能模块。
"""

from .inputs import InputManager
from .scenes import SceneManager
from .recording import RecordingManager
from .streaming import StreamingManager
from .virtual_camera import VirtualCameraManager
from .scene_items import SceneItemManager
from .sources import SourceManager

__all__ = [
    'InputManager',
    'SceneManager',
    'RecordingManager',
    'StreamingManager',
    'VirtualCameraManager',
    'SceneItemManager',
    'SourceManager',
]
