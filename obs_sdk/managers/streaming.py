"""
推流管理器

负责 OBS 推流功能的管理。
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


class StreamingManager:
    """
    推流管理器
    
    提供推流相关的所有功能，包括开始、停止推流等。
    """
    
    def __init__(self, client: OBSClient):
        """
        初始化推流管理器
        
        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取推流状态
        
        Returns:
            Dict: 推流状态信息
        """
        response = self.client.call(requests.GetStreamStatus())
        if hasattr(response, 'datain'):
            return response.datain
        return {}
    
    def is_streaming(self) -> bool:
        """
        检查是否正在推流
        
        Returns:
            bool: True 表示正在推流
        """
        status = self.get_status()
        return status.get('outputActive', False)
    
    def is_reconnecting(self) -> bool:
        """
        检查是否正在重连
        
        Returns:
            bool: True 表示正在重连
        """
        status = self.get_status()
        return status.get('outputReconnecting', False)
    
    def get_duration(self) -> int:
        """
        获取推流时长（毫秒）
        
        Returns:
            int: 推流时长
        """
        status = self.get_status()
        return status.get('outputDuration', 0)
    
    def get_timecode(self) -> str:
        """
        获取推流时间码
        
        Returns:
            str: 时间码字符串
        """
        status = self.get_status()
        return status.get('outputTimecode', '00:00:00')
    
    def get_bytes_sent(self) -> int:
        """
        获取已发送字节数
        
        Returns:
            int: 已发送字节数
        """
        status = self.get_status()
        return status.get('outputBytes', 0)
    
    def get_dropped_frames(self) -> int:
        """
        获取丢帧数
        
        Returns:
            int: 丢帧数
        """
        status = self.get_status()
        return status.get('outputSkippedFrames', 0)
    
    def get_total_frames(self) -> int:
        """
        获取总帧数
        
        Returns:
            int: 总帧数
        """
        status = self.get_status()
        return status.get('outputTotalFrames', 0)
    
    def get_congestion(self) -> float:
        """
        获取网络拥塞度
        
        Returns:
            float: 拥塞度 (0.0-1.0)
        """
        status = self.get_status()
        return status.get('outputCongestion', 0.0)
    
    def start(self) -> bool:
        """
        开始推流
        
        Returns:
            bool: 操作是否成功
            
        Raises:
            OBSOutputRunningError: 推流已在进行中
        """
        try:
            if self.is_streaming():
                raise OBSOutputRunningError("推流")
            
            self.client.call(requests.StartStream())
            self.logger.info("推流已开始")
            return True
            
        except OBSOutputRunningError:
            raise
        except Exception as e:
            self.logger.error(f"开始推流失败: {e}")
            return False
    
    def stop(self) -> bool:
        """
        停止推流
        
        Returns:
            bool: 操作是否成功
            
        Raises:
            OBSOutputNotRunningError: 推流未在进行中
        """
        try:
            if not self.is_streaming():
                raise OBSOutputNotRunningError("推流")
            
            self.client.call(requests.StopStream())
            self.logger.info("推流已停止")
            return True
            
        except OBSOutputNotRunningError:
            raise
        except Exception as e:
            self.logger.error(f"停止推流失败: {e}")
            return False
    
    def toggle(self) -> bool:
        """
        切换推流状态
        
        Returns:
            bool: 切换后的推流状态（True=推流中，False=已停止）
        """
        try:
            response = self.client.call(requests.ToggleStream())
            
            active = False
            if hasattr(response, 'datain'):
                active = response.datain.get('outputActive', False)
            
            status = "开始" if active else "停止"
            self.logger.info(f"推流已{status}")
            return active
            
        except Exception as e:
            self.logger.error(f"切换推流状态失败: {e}")
            return self.is_streaming()
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取推流信息摘要
        
        Returns:
            Dict: 推流信息
        """
        status = self.get_status()
        return {
            "streaming": self.is_streaming(),
            "reconnecting": self.is_reconnecting(),
            "duration": self.get_duration(),
            "timecode": self.get_timecode(),
            "bytes_sent": self.get_bytes_sent(),
            "dropped_frames": self.get_dropped_frames(),
            "total_frames": self.get_total_frames(),
            "congestion": self.get_congestion(),
            "drop_rate": (
                self.get_dropped_frames() / max(self.get_total_frames(), 1) * 100
                if self.get_total_frames() > 0 else 0.0
            )
        }
