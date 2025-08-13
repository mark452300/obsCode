"""
异常定义

定义 OBS SDK 使用的所有异常类。
"""


class OBSError(Exception):
    """OBS SDK 基础异常"""
    pass


class OBSConnectionError(OBSError):
    """连接错误"""
    pass


class OBSAuthenticationError(OBSError):
    """认证错误"""
    pass


class OBSRequestError(OBSError):
    """请求错误"""
    pass


class OBSResourceNotFoundError(OBSRequestError):
    """资源未找到错误"""
    
    def __init__(self, resource_type: str, resource_name: str, available_resources: list = None):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.available_resources = available_resources or []
        
        message = f"{resource_type} '{resource_name}' 未找到"
        if available_resources:
            message += f"。可用的{resource_type}: {', '.join(available_resources)}"
        
        super().__init__(message)


class OBSNotReadyError(OBSRequestError):
    """OBS 未就绪错误"""
    pass


class OBSOutputRunningError(OBSRequestError):
    """输出已在运行错误"""
    
    def __init__(self, output_type: str):
        self.output_type = output_type
        super().__init__(f"{output_type}已在运行中")


class OBSOutputNotRunningError(OBSRequestError):
    """输出未运行错误"""
    
    def __init__(self, output_type: str):
        self.output_type = output_type
        super().__init__(f"{output_type}未在运行")
