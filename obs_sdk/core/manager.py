"""
OBS 统一管理器

提供一个统一的接口来管理所有 OBS 功能模块。
"""

import logging
from typing import Dict, Any, Optional

from .client import OBSClient
from .config import OBSConfig
from ..managers.recording import RecordingManager
from ..managers.streaming import StreamingManager
from ..managers.scenes import SceneManager
from ..managers.inputs import InputManager
from ..managers.virtual_camera import VirtualCameraManager
from ..managers.scene_items import SceneItemManager
from ..managers.sources import SourceManager


logger = logging.getLogger(__name__)


class OBSManager:
    """
    OBS 统一管理器
    
    这个类提供了一个统一的接口来访问所有 OBS 功能模块，
    是使用 OBS SDK 的推荐方式。
    """
    
    def __init__(self, config: Optional[OBSConfig] = None, auto_connect: bool = True):
        """
        初始化 OBS 管理器
        
        Args:
            config: 配置对象，如果为 None 则使用默认配置
            auto_connect: 是否自动连接到 OBS
        """
        self.config = config or OBSConfig()
        self.client = OBSClient(self.config)
        
        # 初始化各个功能管理器
        self.recording = RecordingManager(self.client)
        self.streaming = StreamingManager(self.client)
        self.scenes = SceneManager(self.client)
        self.inputs = InputManager(self.client)
        self.virtual_camera = VirtualCameraManager(self.client)
        self.scene_items = SceneItemManager(self.client)
        self.sources = SourceManager(self.client)
        
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        if auto_connect:
            self.connect()
    
    def connect(self) -> bool:
        """
        连接到 OBS
        
        Returns:
            bool: 连接是否成功
        """
        return self.client.connect()
    
    def disconnect(self):
        """断开与 OBS 的连接"""
        self.client.disconnect()
    
    def is_connected(self) -> bool:
        """检查是否已连接到 OBS"""
        return self.client.is_connected()
    
    def get_version(self) -> Dict[str, Any]:
        """获取 OBS 版本信息"""
        return self.client.get_version()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取 OBS 统计信息"""
        return self.client.get_stats()
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取 OBS 完整状态摘要
        
        Returns:
            Dict: 包含所有模块状态的字典
        """
        if not self.is_connected():
            return {"connected": False, "error": "未连接到 OBS"}
        
        try:
            return {
                "connected": True,
                "version": self.get_version(),
                "recording": self.recording.get_info(),
                "streaming": self.streaming.get_info(),
                "scenes": self.scenes.get_info(),
                "inputs": self.inputs.get_info(),
                "virtual_camera": self.virtual_camera.get_info(),
                "sources": self.sources.get_info(),
            }
        except Exception as e:
            self.logger.error(f"获取状态失败: {e}")
            return {"connected": True, "error": str(e)}
    
    def register_event_callback(self, callback, event_type=None):
        """
        注册事件回调
        
        Args:
            callback: 回调函数
            event_type: 事件类型，None 表示监听所有事件
        """
        self.client.register_event_callback(callback, event_type)
    
    def unregister_event_callback(self, callback, event_type=None):
        """
        取消注册事件回调
        
        Args:
            callback: 回调函数
            event_type: 事件类型
        """
        self.client.unregister_event_callback(callback, event_type)
    
    # 便捷方法 - 录制
    def start_recording(self, output_directory: Optional[str] = None, filename: Optional[str] = None) -> bool:
        """开始录制"""
        return self.recording.start(output_directory, filename)

    def stop_recording(self) -> Optional[str]:
        """停止录制"""
        return self.recording.stop()

    def is_recording(self) -> bool:
        """检查是否正在录制"""
        return self.recording.is_recording()

    def toggle_recording(self) -> bool:
        """切换录制状态"""
        return self.recording.toggle()

    def quick_record(self, duration: float, output_directory: Optional[str] = None, filename: Optional[str] = None) -> Optional[str]:
        """快速录制指定时长"""
        return self.recording.quick_record(duration, output_directory, filename)

    def set_recording_directory(self, directory: str) -> bool:
        """设置录制输出目录"""
        return self.recording.set_output_directory(directory)

    def get_recording_directory(self) -> Optional[str]:
        """获取当前录制输出目录"""
        return self.recording.get_output_directory()
    
    # 便捷方法 - 推流
    def start_streaming(self) -> bool:
        """开始推流"""
        return self.streaming.start()
    
    def stop_streaming(self) -> bool:
        """停止推流"""
        return self.streaming.stop()
    
    def is_streaming(self) -> bool:
        """检查是否正在推流"""
        return self.streaming.is_streaming()
    
    def toggle_streaming(self) -> bool:
        """切换推流状态"""
        return self.streaming.toggle()
    
    # 便捷方法 - 场景
    def get_scenes(self) -> list:
        """获取所有场景名称"""
        return self.scenes.get_names()
    
    def get_current_scene(self) -> str:
        """获取当前场景"""
        return self.scenes.get_current_program()
    
    def switch_scene(self, scene_name: str) -> bool:
        """切换场景"""
        return self.scenes.switch_to(scene_name)

    def create_scene(self, scene_name: str) -> bool:
        """创建新场景"""
        return self.scenes.create(scene_name)

    def delete_scene(self, scene_name: str) -> bool:
        """删除场景"""
        return self.scenes.delete(scene_name)

    def enable_studio_mode(self, enabled: bool = True) -> bool:
        """启用/禁用 Studio Mode"""
        return self.scenes.enable_studio_mode(enabled)

    def trigger_transition(self) -> bool:
        """触发 Studio Mode 转场"""
        return self.scenes.trigger_transition()
    
    # 便捷方法 - 输入
    def get_inputs(self) -> list:
        """获取所有输入源名称"""
        return self.inputs.get_names()
    
    def get_audio_inputs(self) -> list:
        """获取音频输入源名称"""
        return self.inputs.get_audio_inputs()

    def get_input_kinds(self, unversioned: bool = False) -> list:
        """获取所有可用的输入类型"""
        return self.inputs.get_input_kinds(unversioned)

    def mute_input(self, input_name: str) -> bool:
        """静音输入源"""
        return self.inputs.mute(input_name)
    
    def unmute_input(self, input_name: str) -> bool:
        """取消静音输入源"""
        return self.inputs.unmute(input_name)
    
    def toggle_input_mute(self, input_name: str) -> bool:
        """切换输入源静音状态"""
        return self.inputs.toggle_mute(input_name)
    
    def is_input_muted(self, input_name: str) -> bool:
        """检查输入源是否静音"""
        return self.inputs.is_muted(input_name)

    def save_input_kinds(self, filepath: str = None) -> str:
        """保存输入类型数据到 JSON 文件"""
        return self.inputs.save_input_kinds_to_json(filepath)
    
    # 便捷方法 - 虚拟摄像头
    def start_virtual_camera(self) -> bool:
        """启动虚拟摄像头"""
        return self.virtual_camera.start()
    
    def stop_virtual_camera(self) -> bool:
        """停止虚拟摄像头"""
        return self.virtual_camera.stop()
    
    def is_virtual_camera_active(self) -> bool:
        """检查虚拟摄像头是否激活"""
        return self.virtual_camera.is_active()
    
    def toggle_virtual_camera(self) -> bool:
        """切换虚拟摄像头状态"""
        return self.virtual_camera.toggle()
    
    # 便捷方法 - 场景项
    def show_scene_item(self, scene_name: str, source_name: str) -> bool:
        """显示场景项"""
        return self.scene_items.show_by_source_name(scene_name, source_name)
    
    def hide_scene_item(self, scene_name: str, source_name: str) -> bool:
        """隐藏场景项"""
        return self.scene_items.hide_by_source_name(scene_name, source_name)
    
    def toggle_scene_item(self, scene_name: str, source_name: str) -> Optional[bool]:
        """切换场景项显示状态"""
        return self.scene_items.toggle_by_source_name(scene_name, source_name)
    
    def get_scene_items(self, scene_name: str) -> list:
        """获取场景中的所有场景项"""
        return self.scene_items.get_list(scene_name)

    # 便捷方法 - 源管理
    def get_sources(self) -> list:
        """获取所有源名称"""
        return self.sources.get_names()

    def source_exists(self, source_name: str) -> bool:
        """检查源是否存在"""
        return self.sources.exists(source_name)

    # 创建源（全局，不添加到场景）
    def create_text_source(self, source_name: str, text: str = "", font_size: int = 32, color: int = 0xFFFFFF) -> bool:
        """创建文本源（全局）"""
        return self.sources.create_text_source(source_name, text, font_size, color)

    def create_image_source(self, source_name: str, file_path: str) -> bool:
        """创建图像源（全局）"""
        return self.sources.create_image_source(source_name, file_path)

    def create_video_source(self, source_name: str, file_path: str, loop: bool = True) -> bool:
        """创建视频源（全局）"""
        return self.sources.create_video_source(source_name, file_path, loop)

    def create_color_source(self, source_name: str, color: int = 0x000000, width: int = 1920, height: int = 1080) -> bool:
        """创建颜色源（全局）"""
        return self.sources.create_color_source(source_name, color, width, height)

    def create_browser_source(self, source_name: str, url: str, width: int = 1920, height: int = 1080) -> bool:
        """创建浏览器源（全局）"""
        return self.sources.create_browser_source(source_name, url, width, height)

    # 创建源并添加到场景（推荐的工作流程）
    def create_text_source_in_scene(self, scene_name: str, source_name: str, text: str = "",
                                   font_size: int = 32, color: int = 0xFFFFFF,
                                   position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """创建文本源并添加到场景"""
        return self.sources.create_text_source_in_scene(scene_name, source_name, text, font_size, color, position, scale)

    def create_image_source_in_scene(self, scene_name: str, source_name: str, file_path: str,
                                   position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """创建图像源并添加到场景"""
        return self.sources.create_image_source_in_scene(scene_name, source_name, file_path, position, scale)

    def create_video_source_in_scene(self, scene_name: str, source_name: str, file_path: str,
                                   loop: bool = True, position: Optional[tuple] = None,
                                   scale: Optional[tuple] = None) -> bool:
        """创建视频源并添加到场景"""
        return self.sources.create_video_source_in_scene(scene_name, source_name, file_path, loop, position, scale)

    def create_color_source_in_scene(self, scene_name: str, source_name: str, color: int = 0x000000,
                                   width: int = 1920, height: int = 1080,
                                   position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """创建颜色源并添加到场景"""
        return self.sources.create_color_source_in_scene(scene_name, source_name, color, width, height, position, scale)

    def create_browser_source_in_scene(self, scene_name: str, source_name: str, url: str,
                                     width: int = 1920, height: int = 1080,
                                     position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """创建浏览器源并添加到场景"""
        return self.sources.create_browser_source_in_scene(scene_name, source_name, url, width, height, position, scale)

    def delete_source(self, source_name: str) -> bool:
        """删除源"""
        return self.sources.delete_source(source_name)

    def set_text_content(self, source_name: str, text: str) -> bool:
        """设置文本源内容"""
        return self.sources.set_text_content(source_name, text)

    def set_image_path(self, source_name: str, file_path: str) -> bool:
        """设置图像源路径"""
        return self.sources.set_image_path(source_name, file_path)

    def set_video_path(self, source_name: str, file_path: str) -> bool:
        """设置视频源路径"""
        return self.sources.set_video_path(source_name, file_path)

    def add_source_to_scene(self, scene_name: str, source_name: str,
                           position: Optional[tuple] = None,
                           scale: Optional[tuple] = None) -> bool:
        """将源添加到场景"""
        return self.sources.add_source_to_scene(scene_name, source_name, position, scale)
    
    # 上下文管理器支持
    def __enter__(self):
        """上下文管理器入口"""
        if not self.is_connected():
            self.connect()
        return self
    
    def __exit__(self, *args):
        """上下文管理器出口"""
        # 忽略异常信息参数
        _ = args
        self.disconnect()
