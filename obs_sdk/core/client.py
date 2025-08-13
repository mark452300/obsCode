"""
OBS WebSocket 客户端

负责与 OBS 的底层通信，提供连接管理和基础请求功能。
"""

import logging
from typing import Optional, Any, Callable, Dict, List
from threading import Lock

try:
    from obswebsocket import obsws, requests, events
except ImportError:
    raise ImportError("请安装 obs-websocket-py: pip install obs-websocket-py")

from .config import OBSConfig
from .exceptions import OBSConnectionError, OBSAuthenticationError, OBSRequestError


logger = logging.getLogger(__name__)


class OBSClient:
    """
    OBS WebSocket 客户端
    
    负责管理与 OBS 的连接和基础通信功能。
    """
    
    def __init__(self, config: Optional[OBSConfig] = None):
        """
        初始化客户端
        
        Args:
            config: 配置对象，如果为 None 则使用默认配置
        """
        self.config = config or OBSConfig()
        self._ws: Optional[obsws] = None
        self._connected = False
        self._connection_lock = Lock()
        
        # 事件回调
        self._event_callbacks: Dict[str, List[Callable]] = {}
        self._global_callbacks: List[Callable] = []
        
        # 设置日志
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def connect(self) -> bool:
        """
        连接到 OBS
        
        Returns:
            bool: 连接是否成功
        """
        with self._connection_lock:
            if self._connected:
                return True
            
            try:
                self._ws = obsws(
                    host=self.config.host,
                    port=self.config.port,
                    password=self.config.password,
                    timeout=self.config.timeout,
                    legacy=False
                )
                self._ws.connect()
                self._connected = True
                self.logger.info(f"已连接到 OBS ({self.config.host}:{self.config.port})")
                return True
                
            except Exception as e:
                self._connected = False
                error_msg = f"连接 OBS 失败: {str(e)}"
                self.logger.error(error_msg)
                
                if "authentication failed" in str(e).lower():
                    raise OBSAuthenticationError(error_msg)
                else:
                    raise OBSConnectionError(error_msg)
    
    def disconnect(self):
        """断开与 OBS 的连接"""
        with self._connection_lock:
            if not self._connected or not self._ws:
                return
            
            try:
                self._ws.disconnect()
                self._connected = False
                self._ws = None
                self.logger.info("已断开 OBS 连接")
            except Exception as e:
                self.logger.error(f"断开连接时出错: {e}")
                self._connected = False
                self._ws = None
    
    def is_connected(self) -> bool:
        """检查是否已连接到 OBS"""
        return self._connected and self._ws is not None
    
    def call(self, request, max_retries: int = 3) -> Any:
        """
        执行 OBS 请求
        
        Args:
            request: OBS 请求对象
            max_retries: 最大重试次数
            
        Returns:
            OBS 响应对象
            
        Raises:
            OBSConnectionError: 未连接到 OBS
            OBSRequestError: 请求失败
        """
        if not self.is_connected():
            raise OBSConnectionError("未连接到 OBS，请先调用 connect()")
        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                response = self._ws.call(request)
                return response
                
            except Exception as e:
                last_exception = e
                self.logger.warning(f"请求失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}")
                
                if attempt < max_retries:
                    import time
                    time.sleep(0.5 * (2 ** attempt))  # 指数退避
                else:
                    break
        
        # 所有重试都失败了
        error_msg = f"请求失败: {str(last_exception)}"
        self.logger.error(error_msg)
        raise OBSRequestError(error_msg)
    
    def register_event_callback(self, callback: Callable, event_type: Optional[str] = None):
        """
        注册事件回调
        
        Args:
            callback: 回调函数
            event_type: 事件类型，None 表示监听所有事件
        """
        if event_type is None:
            self._global_callbacks.append(callback)
        else:
            if event_type not in self._event_callbacks:
                self._event_callbacks[event_type] = []
            self._event_callbacks[event_type].append(callback)
        
        # 注册到底层 WebSocket 客户端
        if self._ws:
            try:
                if event_type:
                    event_class = getattr(events, event_type, None)
                    if event_class:
                        self._ws.register(self._event_dispatcher, event_class)
                else:
                    self._ws.register(self._event_dispatcher)
            except Exception as e:
                self.logger.warning(f"注册事件回调失败: {e}")
    
    def unregister_event_callback(self, callback: Callable, event_type: Optional[str] = None):
        """
        取消注册事件回调
        
        Args:
            callback: 回调函数
            event_type: 事件类型
        """
        try:
            if event_type is None:
                self._global_callbacks.remove(callback)
            else:
                if event_type in self._event_callbacks:
                    self._event_callbacks[event_type].remove(callback)
                    if not self._event_callbacks[event_type]:
                        del self._event_callbacks[event_type]
        except ValueError:
            self.logger.warning(f"回调函数未找到: {event_type}")
    
    def _event_dispatcher(self, message):
        """内部事件分发器"""
        try:
            event_type = getattr(message, '__class__', type(message)).__name__
            
            # 调用全局回调
            for callback in self._global_callbacks:
                try:
                    callback(message)
                except Exception as e:
                    self.logger.error(f"全局事件回调错误: {e}")
            
            # 调用特定事件回调
            if event_type in self._event_callbacks:
                for callback in self._event_callbacks[event_type]:
                    try:
                        callback(message)
                    except Exception as e:
                        self.logger.error(f"事件回调错误 ({event_type}): {e}")
        
        except Exception as e:
            self.logger.error(f"事件分发器错误: {e}")
    
    def get_version(self) -> Dict[str, Any]:
        """获取 OBS 版本信息"""
        response = self.call(requests.GetVersion())
        if hasattr(response, 'datain'):
            return response.datain
        return {}
    
    def get_stats(self) -> Dict[str, Any]:
        """获取 OBS 统计信息"""
        response = self.call(requests.GetStats())
        if hasattr(response, 'datain'):
            return response.datain
        return {}
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()
