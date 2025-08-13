"""
配置管理

提供 OBS SDK 的配置管理功能。
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class OBSConfig:
    """OBS 连接配置"""
    
    host: str = "127.0.0.1"   
    port: int = 4455
    password: str = "el8peI520f03ZEVK"
    timeout: float = 10.0
    max_retries: int = 3
    auto_connect: bool = True
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls, prefix: str = "OBS_") -> "OBSConfig":
        """从环境变量创建配置"""
        # 创建一个默认实例来获取默认值
        defaults = cls()

        return cls(
            host=os.getenv(f"{prefix}HOST", defaults.host),
            port=int(os.getenv(f"{prefix}PORT", str(defaults.port))),
            password=os.getenv(f"{prefix}PASSWORD", defaults.password),
            timeout=float(os.getenv(f"{prefix}TIMEOUT", str(defaults.timeout))),
            max_retries=int(os.getenv(f"{prefix}MAX_RETRIES", str(defaults.max_retries))),
            auto_connect=os.getenv(f"{prefix}AUTO_CONNECT", str(defaults.auto_connect).lower()).lower() in ("true", "1", "yes"),
            log_level=os.getenv(f"{prefix}LOG_LEVEL", defaults.log_level),
        )
    
    def validate(self):
        """验证配置"""
        if not (1 <= self.port <= 65535):
            raise ValueError(f"端口必须在 1-65535 之间: {self.port}")
        
        if self.timeout <= 0:
            raise ValueError(f"超时时间必须大于 0: {self.timeout}")
        
        if self.max_retries < 0:
            raise ValueError(f"最大重试次数不能为负数: {self.max_retries}")
    
    def get_websocket_url(self) -> str:
        """获取 WebSocket URL"""
        return f"ws://{self.host}:{self.port}"
