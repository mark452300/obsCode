"""
场景项管理器

负责 OBS 场景项功能的管理。
"""

import logging
from typing import List, Dict, Any, Optional

try:
    from obswebsocket import requests
except ImportError:
    raise ImportError("请安装 obs-websocket-py: pip install obs-websocket-py")

from ..core.client import OBSClient
from ..core.exceptions import OBSResourceNotFoundError


logger = logging.getLogger(__name__)


class SceneItemManager:
    """
    场景项管理器
    
    提供场景项相关的所有功能，包括显示/隐藏、变换等。
    """
    
    def __init__(self, client: OBSClient):
        """
        初始化场景项管理器
        
        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def get_list(self, scene_name: str) -> List[Dict[str, Any]]:
        """
        获取场景中的所有场景项
        
        Args:
            scene_name: 场景名称
            
        Returns:
            List[Dict]: 场景项列表
        """
        try:
            response = self.client.call(requests.GetSceneItemList(sceneName=scene_name))
            if hasattr(response, 'datain'):
                return response.datain.get('sceneItems', [])
            return []
        except Exception as e:
            self.logger.error(f"获取场景项列表失败: {e}")
            return []
    
    def get_id(self, scene_name: str, source_name: str) -> Optional[int]:
        """
        根据源名称获取场景项 ID
        
        Args:
            scene_name: 场景名称
            source_name: 源名称
            
        Returns:
            Optional[int]: 场景项 ID，未找到时返回 None
        """
        try:
            response = self.client.call(requests.GetSceneItemId(
                sceneName=scene_name,
                sourceName=source_name
            ))
            if hasattr(response, 'datain'):
                return response.datain.get('sceneItemId')
            return None
        except Exception as e:
            self.logger.error(f"获取场景项 ID 失败: {e}")
            return None
    
    def is_enabled(self, scene_name: str, item_id: int) -> bool:
        """
        检查场景项是否启用（可见）
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            
        Returns:
            bool: True 表示场景项已启用
        """
        try:
            response = self.client.call(requests.GetSceneItemEnabled(
                sceneName=scene_name,
                sceneItemId=item_id
            ))
            if hasattr(response, 'datain'):
                return response.datain.get('sceneItemEnabled', False)
            return False
        except Exception as e:
            self.logger.error(f"获取场景项启用状态失败: {e}")
            return False
    
    def set_enabled(self, scene_name: str, item_id: int, enabled: bool) -> bool:
        """
        设置场景项启用状态
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            enabled: True 启用，False 禁用
            
        Returns:
            bool: 操作是否成功
        """
        try:
            self.client.call(requests.SetSceneItemEnabled(
                sceneName=scene_name,
                sceneItemId=item_id,
                sceneItemEnabled=enabled
            ))
            status = "启用" if enabled else "禁用"
            self.logger.info(f"场景项 {item_id} 已{status}")
            return True
        except Exception as e:
            self.logger.error(f"设置场景项启用状态失败: {e}")
            return False
    
    def show(self, scene_name: str, item_id: int) -> bool:
        """
        显示场景项
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            
        Returns:
            bool: 操作是否成功
        """
        return self.set_enabled(scene_name, item_id, True)
    
    def hide(self, scene_name: str, item_id: int) -> bool:
        """
        隐藏场景项
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            
        Returns:
            bool: 操作是否成功
        """
        return self.set_enabled(scene_name, item_id, False)
    
    def toggle(self, scene_name: str, item_id: int) -> bool:
        """
        切换场景项显示状态
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            
        Returns:
            bool: 切换后的启用状态（True=显示，False=隐藏）
        """
        current_enabled = self.is_enabled(scene_name, item_id)
        new_enabled = not current_enabled
        
        if self.set_enabled(scene_name, item_id, new_enabled):
            return new_enabled
        else:
            return current_enabled
    
    def show_by_source_name(self, scene_name: str, source_name: str) -> bool:
        """
        根据源名称显示场景项
        
        Args:
            scene_name: 场景名称
            source_name: 源名称
            
        Returns:
            bool: 操作是否成功
        """
        item_id = self.get_id(scene_name, source_name)
        if item_id is not None:
            return self.show(scene_name, item_id)
        else:
            self.logger.error(f"未找到源 '{source_name}' 在场景 '{scene_name}' 中")
            return False
    
    def hide_by_source_name(self, scene_name: str, source_name: str) -> bool:
        """
        根据源名称隐藏场景项
        
        Args:
            scene_name: 场景名称
            source_name: 源名称
            
        Returns:
            bool: 操作是否成功
        """
        item_id = self.get_id(scene_name, source_name)
        if item_id is not None:
            return self.hide(scene_name, item_id)
        else:
            self.logger.error(f"未找到源 '{source_name}' 在场景 '{scene_name}' 中")
            return False
    
    def toggle_by_source_name(self, scene_name: str, source_name: str) -> Optional[bool]:
        """
        根据源名称切换场景项显示状态
        
        Args:
            scene_name: 场景名称
            source_name: 源名称
            
        Returns:
            Optional[bool]: 切换后的启用状态，失败时返回 None
        """
        item_id = self.get_id(scene_name, source_name)
        if item_id is not None:
            return self.toggle(scene_name, item_id)
        else:
            self.logger.error(f"未找到源 '{source_name}' 在场景 '{scene_name}' 中")
            return None
    
    def get_transform(self, scene_name: str, item_id: int) -> Dict[str, Any]:
        """
        获取场景项变换信息
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            
        Returns:
            Dict: 变换信息
        """
        try:
            response = self.client.call(requests.GetSceneItemTransform(
                sceneName=scene_name,
                sceneItemId=item_id
            ))
            if hasattr(response, 'datain'):
                return response.datain.get('sceneItemTransform', {})
            return {}
        except Exception as e:
            self.logger.error(f"获取场景项变换信息失败: {e}")
            return {}
    
    def set_transform(self, scene_name: str, item_id: int, transform: Dict[str, Any]) -> bool:
        """
        设置场景项变换信息
        
        Args:
            scene_name: 场景名称
            item_id: 场景项 ID
            transform: 变换信息字典
            
        Returns:
            bool: 操作是否成功
        """
        try:
            self.client.call(requests.SetSceneItemTransform(
                sceneName=scene_name,
                sceneItemId=item_id,
                sceneItemTransform=transform
            ))
            self.logger.info(f"已设置场景项 {item_id} 的变换信息")
            return True
        except Exception as e:
            self.logger.error(f"设置场景项变换信息失败: {e}")
            return False
    
    def get_info(self, scene_name: str) -> Dict[str, Any]:
        """
        获取场景项信息摘要
        
        Args:
            scene_name: 场景名称
            
        Returns:
            Dict: 场景项信息
        """
        items = self.get_list(scene_name)
        
        enabled_count = 0
        disabled_count = 0
        
        for item in items:
            if item.get('sceneItemEnabled', False):
                enabled_count += 1
            else:
                disabled_count += 1
        
        return {
            "scene_name": scene_name,
            "total_items": len(items),
            "enabled_items": enabled_count,
            "disabled_items": disabled_count,
            "items": [
                {
                    "id": item.get('sceneItemId'),
                    "source_name": item.get('sourceName'),
                    "enabled": item.get('sceneItemEnabled', False),
                }
                for item in items
            ]
        }
