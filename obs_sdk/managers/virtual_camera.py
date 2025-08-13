"""
虚拟摄像头管理器

负责 OBS 虚拟摄像头功能的管理。
"""

import logging
from typing import Dict, Any

try:
    from obswebsocket import requests
except ImportError:
    raise ImportError("请安装 obs-websocket-py: pip install obs-websocket-py")

from ..core.client import OBSClient
from ..core.exceptions import OBSOutputRunningError, OBSOutputNotRunningError


logger = logging.getLogger(__name__)


class VirtualCameraManager:
    """
    虚拟摄像头管理器
    
    提供虚拟摄像头相关的所有功能。
    """
    
    def __init__(self, client: OBSClient):
        """
        初始化虚拟摄像头管理器
        
        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取虚拟摄像头状态
        
        Returns:
            Dict: 虚拟摄像头状态信息
        """
        response = self.client.call(requests.GetVirtualCamStatus())
        if hasattr(response, 'datain'):
            return response.datain
        return {}
    
    def is_active(self) -> bool:
        """
        检查虚拟摄像头是否激活
        
        Returns:
            bool: True 表示虚拟摄像头已激活
        """
        status = self.get_status()
        return status.get('outputActive', False)
    
    def start(self) -> bool:
        """
        启动虚拟摄像头
        
        Returns:
            bool: 操作是否成功
            
        Raises:
            OBSOutputRunningError: 虚拟摄像头已在运行中
        """
        try:
            if self.is_active():
                raise OBSOutputRunningError("虚拟摄像头")
            
            self.client.call(requests.StartVirtualCam())
            self.logger.info("虚拟摄像头已启动")
            return True
            
        except OBSOutputRunningError:
            raise
        except Exception as e:
            self.logger.error(f"启动虚拟摄像头失败: {e}")
            return False
    
    def stop(self) -> bool:
        """
        停止虚拟摄像头
        
        Returns:
            bool: 操作是否成功
            
        Raises:
            OBSOutputNotRunningError: 虚拟摄像头未在运行中
        """
        try:
            if not self.is_active():
                raise OBSOutputNotRunningError("虚拟摄像头")
            
            self.client.call(requests.StopVirtualCam())
            self.logger.info("虚拟摄像头已停止")
            return True
            
        except OBSOutputNotRunningError:
            raise
        except Exception as e:
            self.logger.error(f"停止虚拟摄像头失败: {e}")
            return False
    
    def toggle(self) -> bool:
        """
        切换虚拟摄像头状态
        
        Returns:
            bool: 切换后的激活状态（True=激活，False=停止）
        """
        try:
            response = self.client.call(requests.ToggleVirtualCam())
            
            active = False
            if hasattr(response, 'datain'):
                active = response.datain.get('outputActive', False)
            
            status = "启动" if active else "停止"
            self.logger.info(f"虚拟摄像头已{status}")
            return active
            
        except Exception as e:
            self.logger.error(f"切换虚拟摄像头状态失败: {e}")
            return self.is_active()
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取虚拟摄像头信息摘要
        
        Returns:
            Dict: 虚拟摄像头信息
        """
        return {
            "active": self.is_active(),
            "status": self.get_status(),
        }
