"""
源管理器

负责 OBS 源功能的管理，包括创建、删除、配置各种类型的源。
"""

import logging
from typing import List, Dict, Any, Optional, Union

try:
    from obswebsocket import requests
except ImportError:
    raise ImportError("请安装 obs-websocket-py: pip install obs-websocket-py")

from ..core.client import OBSClient
from ..core.exceptions import OBSResourceNotFoundError


logger = logging.getLogger(__name__)


class SourceManager:
    """
    源管理器
    
    提供源相关的所有功能，包括创建、删除、配置各种类型的源。
    """
    
    # 常用源类型定义
    SOURCE_TYPES = {
        'text': 'text_gdiplus_v2',  # 文本源
        'image': 'image_source',    # 图像源
        'video': 'ffmpeg_source',   # 视频源
        'audio': 'ffmpeg_source',   # 音频源
        'window': 'window_capture', # 窗口捕获
        'display': 'monitor_capture', # 显示器捕获
        'camera': 'dshow_input',    # 摄像头
        'browser': 'browser_source', # 浏览器源
        'color': 'color_source',    # 颜色源
    }
    
    def __init__(self, client: OBSClient):
        """
        初始化源管理器
        
        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        获取所有源
        
        Returns:
            List[Dict]: 源列表
        """
        try:
            response = self.client.call(requests.GetInputList())
            if hasattr(response, 'datain'):
                return response.datain.get('inputs', [])
            return []
        except Exception as e:
            self.logger.error(f"获取源列表失败: {e}")
            return []
    
    def get_names(self) -> List[str]:
        """
        获取所有源名称
        
        Returns:
            List[str]: 源名称列表
        """
        sources = self.get_all()
        return [source.get('inputName', '') for source in sources]
    
    def exists(self, source_name: str) -> bool:
        """
        检查源是否存在
        
        Args:
            source_name: 源名称
            
        Returns:
            bool: True 表示源存在
        """
        return source_name in self.get_names()
    
    def get_source_info(self, source_name: str) -> Optional[Dict[str, Any]]:
        """
        获取源的详细信息
        
        Args:
            source_name: 源名称
            
        Returns:
            Dict: 源信息，如果源不存在返回 None
        """
        try:
            if not self.exists(source_name):
                return None
            
            sources = self.get_all()
            for source in sources:
                if source.get('inputName') == source_name:
                    return source
            return None
        except Exception as e:
            self.logger.error(f"获取源信息失败: {e}")
            return None
    
    def create_source(self, source_name: str, source_type: str, settings: Optional[Dict[str, Any]] = None) -> bool:
        """
        创建源
        
        Args:
            source_name: 源名称
            source_type: 源类型
            settings: 源设置
            
        Returns:
            bool: 创建是否成功
        """
        try:
            if self.exists(source_name):
                self.logger.warning(f"源 '{source_name}' 已存在")
                return False
            
            settings = settings or {}
            
            self.client.call(requests.CreateInput(
                inputName=source_name,
                inputKind=source_type,
                inputSettings=settings
            ))
            
            self.logger.info(f"成功创建源: {source_name} (类型: {source_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"创建源失败: {e}")
            return False
    
    def delete_source(self, source_name: str) -> bool:
        """
        删除源
        
        Args:
            source_name: 源名称
            
        Returns:
            bool: 删除是否成功
        """
        try:
            if not self.exists(source_name):
                raise OBSResourceNotFoundError("源", source_name, self.get_names())
            
            self.client.call(requests.RemoveInput(inputName=source_name))
            self.logger.info(f"成功删除源: {source_name}")
            return True
            
        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"删除源失败: {e}")
            return False

    def get_settings(self, source_name: str) -> Dict[str, Any]:
        """
        获取源设置

        Args:
            source_name: 源名称

        Returns:
            Dict: 源设置
        """
        try:
            if not self.exists(source_name):
                raise OBSResourceNotFoundError("源", source_name, self.get_names())

            response = self.client.call(requests.GetInputSettings(inputName=source_name))
            if hasattr(response, 'datain'):
                return response.datain.get('inputSettings', {})
            return {}

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"获取源设置失败: {e}")
            return {}

    def set_settings(self, source_name: str, settings: Dict[str, Any]) -> bool:
        """
        设置源设置

        Args:
            source_name: 源名称
            settings: 设置字典

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.exists(source_name):
                raise OBSResourceNotFoundError("源", source_name, self.get_names())

            self.client.call(requests.SetInputSettings(
                inputName=source_name,
                inputSettings=settings
            ))
            self.logger.info(f"已更新源设置: {source_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"设置源设置失败: {e}")
            return False

    # 便捷方法 - 创建特定类型的源
    def create_text_source(self, source_name: str, text: str = "", font_size: int = 32, color: int = 0xFFFFFF) -> bool:
        """
        创建文本源

        Args:
            source_name: 源名称
            text: 文本内容
            font_size: 字体大小
            color: 文本颜色 (RGB hex)

        Returns:
            bool: 创建是否成功
        """
        settings = {
            'text': text,
            'font': {
                'face': 'Arial',
                'size': font_size,
                'style': ''
            },
            'color': color,
            'opacity': 100,
            'outline': False,
            'drop_shadow': False
        }

        return self.create_source(source_name, self.SOURCE_TYPES['text'], settings)

    def create_image_source(self, source_name: str, file_path: str) -> bool:
        """
        创建图像源

        Args:
            source_name: 源名称
            file_path: 图像文件路径

        Returns:
            bool: 创建是否成功
        """
        settings = {
            'file': file_path,
            'unload': False
        }

        return self.create_source(source_name, self.SOURCE_TYPES['image'], settings)

    def create_video_source(self, source_name: str, file_path: str, loop: bool = True) -> bool:
        """
        创建视频源

        Args:
            source_name: 源名称
            file_path: 视频文件路径
            loop: 是否循环播放

        Returns:
            bool: 创建是否成功
        """
        settings = {
            'local_file': file_path,
            'looping': loop,
            'restart_on_activate': True
        }

        return self.create_source(source_name, self.SOURCE_TYPES['video'], settings)

    def create_color_source(self, source_name: str, color: int = 0x000000, width: int = 1920, height: int = 1080) -> bool:
        """
        创建颜色源

        Args:
            source_name: 源名称
            color: 颜色值 (RGB hex)
            width: 宽度
            height: 高度

        Returns:
            bool: 创建是否成功
        """
        settings = {
            'color': color,
            'width': width,
            'height': height
        }

        return self.create_source(source_name, self.SOURCE_TYPES['color'], settings)

    def create_browser_source(self, source_name: str, url: str, width: int = 1920, height: int = 1080) -> bool:
        """
        创建浏览器源

        Args:
            source_name: 源名称
            url: 网页URL
            width: 宽度
            height: 高度

        Returns:
            bool: 创建是否成功
        """
        settings = {
            'url': url,
            'width': width,
            'height': height,
            'fps': 30,
            'shutdown': False,
            'restart_when_active': False
        }

        return self.create_source(source_name, self.SOURCE_TYPES['browser'], settings)

    # 便捷方法 - 创建源并添加到场景
    def create_text_source_in_scene(self, scene_name: str, source_name: str, text: str = "",
                                   font_size: int = 32, color: int = 0xFFFFFF,
                                   position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """
        创建文本源并添加到场景

        Args:
            scene_name: 场景名称
            source_name: 源名称
            text: 文本内容
            font_size: 字体大小
            color: 文本颜色 (RGB hex)
            position: 位置 (x, y)
            scale: 缩放 (x, y)

        Returns:
            bool: 创建并添加是否成功
        """
        settings = {
            'text': text,
            'font': {
                'face': 'Arial',
                'size': font_size,
                'style': ''
            },
            'color': color,
            'opacity': 100,
            'outline': False,
            'drop_shadow': False
        }

        return self.create_and_add_to_scene(scene_name, source_name, self.SOURCE_TYPES['text'],
                                          settings, position, scale)

    def create_image_source_in_scene(self, scene_name: str, source_name: str, file_path: str,
                                   position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """
        创建图像源并添加到场景

        Args:
            scene_name: 场景名称
            source_name: 源名称
            file_path: 图像文件路径
            position: 位置 (x, y)
            scale: 缩放 (x, y)

        Returns:
            bool: 创建并添加是否成功
        """
        settings = {
            'file': file_path,
            'unload': False
        }

        return self.create_and_add_to_scene(scene_name, source_name, self.SOURCE_TYPES['image'],
                                          settings, position, scale)

    def create_video_source_in_scene(self, scene_name: str, source_name: str, file_path: str,
                                   loop: bool = True, position: Optional[tuple] = None,
                                   scale: Optional[tuple] = None) -> bool:
        """
        创建视频源并添加到场景

        Args:
            scene_name: 场景名称
            source_name: 源名称
            file_path: 视频文件路径
            loop: 是否循环播放
            position: 位置 (x, y)
            scale: 缩放 (x, y)

        Returns:
            bool: 创建并添加是否成功
        """
        settings = {
            'local_file': file_path,
            'looping': loop,
            'restart_on_activate': True
        }

        return self.create_and_add_to_scene(scene_name, source_name, self.SOURCE_TYPES['video'],
                                          settings, position, scale)

    def create_color_source_in_scene(self, scene_name: str, source_name: str, color: int = 0x000000,
                                   width: int = 1920, height: int = 1080,
                                   position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """
        创建颜色源并添加到场景

        Args:
            scene_name: 场景名称
            source_name: 源名称
            color: 颜色值 (RGB hex)
            width: 宽度
            height: 高度
            position: 位置 (x, y)
            scale: 缩放 (x, y)

        Returns:
            bool: 创建并添加是否成功
        """
        settings = {
            'color': color,
            'width': width,
            'height': height
        }

        return self.create_and_add_to_scene(scene_name, source_name, self.SOURCE_TYPES['color'],
                                          settings, position, scale)

    def create_browser_source_in_scene(self, scene_name: str, source_name: str, url: str,
                                     width: int = 1920, height: int = 1080,
                                     position: Optional[tuple] = None, scale: Optional[tuple] = None) -> bool:
        """
        创建浏览器源并添加到场景

        Args:
            scene_name: 场景名称
            source_name: 源名称
            url: 网页URL
            width: 宽度
            height: 高度
            position: 位置 (x, y)
            scale: 缩放 (x, y)

        Returns:
            bool: 创建并添加是否成功
        """
        settings = {
            'url': url,
            'width': width,
            'height': height,
            'fps': 30,
            'shutdown': False,
            'restart_when_active': False
        }

        return self.create_and_add_to_scene(scene_name, source_name, self.SOURCE_TYPES['browser'],
                                          settings, position, scale)

    # 源属性设置的便捷方法
    def set_text_content(self, source_name: str, text: str) -> bool:
        """
        设置文本源内容

        Args:
            source_name: 文本源名称
            text: 新的文本内容

        Returns:
            bool: 设置是否成功
        """
        try:
            current_settings = self.get_settings(source_name)
            current_settings['text'] = text
            return self.set_settings(source_name, current_settings)
        except Exception as e:
            self.logger.error(f"设置文本内容失败: {e}")
            return False

    def set_image_path(self, source_name: str, file_path: str) -> bool:
        """
        设置图像源路径

        Args:
            source_name: 图像源名称
            file_path: 新的图像文件路径

        Returns:
            bool: 设置是否成功
        """
        try:
            current_settings = self.get_settings(source_name)
            current_settings['file'] = file_path
            return self.set_settings(source_name, current_settings)
        except Exception as e:
            self.logger.error(f"设置图像路径失败: {e}")
            return False

    def set_video_path(self, source_name: str, file_path: str) -> bool:
        """
        设置视频源路径

        Args:
            source_name: 视频源名称
            file_path: 新的视频文件路径

        Returns:
            bool: 设置是否成功
        """
        try:
            current_settings = self.get_settings(source_name)
            current_settings['local_file'] = file_path
            return self.set_settings(source_name, current_settings)
        except Exception as e:
            self.logger.error(f"设置视频路径失败: {e}")
            return False

    def create_and_add_to_scene(self, scene_name: str, source_name: str, source_type: str,
                               settings: Optional[Dict[str, Any]] = None,
                               position: Optional[tuple] = None,
                               scale: Optional[tuple] = None) -> bool:
        """
        创建源并添加到场景（推荐的工作流程）

        Args:
            scene_name: 场景名称
            source_name: 源名称
            source_type: 源类型
            settings: 源设置
            position: 位置 (x, y)，默认为 (0, 0)
            scale: 缩放 (x, y)，默认为 (1.0, 1.0)

        Returns:
            bool: 创建并添加是否成功
        """
        try:
            # 首先创建源
            if not self.create_source(source_name, source_type, settings):
                return False

            # 然后添加到场景
            return self.add_source_to_scene(scene_name, source_name, position, scale)

        except Exception as e:
            self.logger.error(f"创建并添加源到场景失败: {e}")
            return False

    def add_source_to_scene(self, scene_name: str, source_name: str,
                           position: Optional[tuple] = None,
                           scale: Optional[tuple] = None) -> bool:
        """
        将已存在的源添加到场景

        Args:
            scene_name: 场景名称
            source_name: 源名称
            position: 位置 (x, y)，默认为 (0, 0)
            scale: 缩放 (x, y)，默认为 (1.0, 1.0)

        Returns:
            bool: 添加是否成功
        """
        try:
            if not self.exists(source_name):
                raise OBSResourceNotFoundError("源", source_name, self.get_names())

            # 添加源到场景
            self.client.call(requests.CreateSceneItem(
                sceneName=scene_name,
                sourceName=source_name
            ))

            # 如果指定了位置或缩放，设置变换
            if position is not None or scale is not None:
                # 获取刚创建的场景项ID
                scene_items_response = self.client.call(requests.GetSceneItemList(sceneName=scene_name))
                if hasattr(scene_items_response, 'datain'):
                    scene_items = scene_items_response.datain.get('sceneItems', [])
                    for item in scene_items:
                        if item.get('sourceName') == source_name:
                            item_id = item.get('sceneItemId')

                            transform = {}
                            if position is not None:
                                transform['positionX'] = position[0]
                                transform['positionY'] = position[1]
                            if scale is not None:
                                transform['scaleX'] = scale[0]
                                transform['scaleY'] = scale[1]

                            if transform:
                                self.client.call(requests.SetSceneItemTransform(
                                    sceneName=scene_name,
                                    sceneItemId=item_id,
                                    sceneItemTransform=transform
                                ))
                            break

            self.logger.info(f"成功将源 '{source_name}' 添加到场景 '{scene_name}'")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"添加源到场景失败: {e}")
            return False

    def get_info(self) -> Dict[str, Any]:
        """
        获取源管理信息摘要

        Returns:
            Dict: 源管理信息
        """
        all_sources = self.get_all()
        source_types = {}

        for source in all_sources:
            source_type = source.get('inputKind', 'unknown')
            source_types[source_type] = source_types.get(source_type, 0) + 1

        return {
            "total_sources": len(all_sources),
            "source_names": self.get_names(),
            "source_types": source_types,
            "available_types": list(self.SOURCE_TYPES.keys())
        }


