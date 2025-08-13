"""
输入管理器

负责 OBS 输入源功能的管理。
"""

import logging
from typing import List, Dict, Any

try:
    from obswebsocket import requests
except ImportError:
    raise ImportError("请安装 obs-websocket-py: pip install obs-websocket-py")

from ..core.client import OBSClient
from ..core.exceptions import OBSResourceNotFoundError
from ..types.input_types import InputTypeHelper, to_chinese, to_english


logger = logging.getLogger(__name__)


class InputManager:
    """
    输入管理器

    提供输入源相关的所有功能，包括静音控制、音量调节等。
    """

    def __init__(self, client: OBSClient):
        """
        初始化输入管理器

        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_all(self) -> List[Dict[str, Any]]:
        """
        获取所有输入源(所有的输入源，不管是哪一个场景)

        Returns:
            List[Dict]: 输入源列表
        """
        response = self.client.call(requests.GetInputList())
        if hasattr(response, 'datain'):
            return response.datain.get('inputs', [])
        return []

    def get_names(self) -> List[str]:
        """
        获取所有输入源名称

        Returns:
            List[str]: 输入源名称列表
        """
        inputs = self.get_all()
        return [inp.get('inputName', '') for inp in inputs]

    def get_input_kinds(self, unversioned: bool = False) -> List[str]:
        """
        获取所有可用的输入类型(这个是系统所支持的输入类型，而不是用户创建的输入源类型)

        Args:
            unversioned: True=返回未版本化的类型，False=返回带版本后缀的类型（如果可用）

        Returns:
            List[str]: 输入类型列表
        """
        try:
            response = self.client.call(requests.GetInputKindList(unversioned=unversioned))
            if hasattr(response, 'datain'):
                return response.datain.get('inputKinds', [])
            return []
        except Exception as e:
            self.logger.error(f"获取输入类型列表失败: {e}")
            return []

    def get_special_inputs(self) -> Dict[str, str]:
        """
        获取特殊输入源名称

        Returns:
            Dict[str, str]: 特殊输入源名称映射
            包括: desktop1, desktop2, mic1, mic2, mic3, mic4
        """
        try:
            response = self.client.call(requests.GetSpecialInputs())
            if hasattr(response, 'datain'):
                return {
                    'desktop1': response.datain.get('desktop1') or '',
                    'desktop2': response.datain.get('desktop2') or '',
                    'mic1': response.datain.get('mic1') or '',
                    'mic2': response.datain.get('mic2') or '',
                    'mic3': response.datain.get('mic3') or '',
                    'mic4': response.datain.get('mic4') or ''
                }
            return {}
        except Exception as e:
            self.logger.error(f"获取特殊输入源失败: {e}")
            return {}

    def get_audio_inputs(self) -> List[str]:
        """
        获取音频输入源名称

        Returns:
            List[str]: 音频输入源名称列表
        """
        inputs = self.get_all()
        audio_inputs = []

        for inp in inputs:
            input_kind = inp.get('inputKind', '').lower()
            input_name = inp.get('inputName', '')

            # 检查是否为音频输入
            if any(keyword in input_kind for keyword in [
                'audio', 'mic', 'wasapi', 'pulse', 'alsa', 'coreaudio'
            ]):
                audio_inputs.append(input_name)

        return audio_inputs

    def exists(self, input_name: str) -> bool:
        """
        检查输入源是否存在

        Args:
            input_name: 输入源名称

        Returns:
            bool: True 表示输入源存在
        """
        return input_name in self.get_names()

    def is_muted(self, input_name: str) -> bool:
        """
        检查输入源是否静音

        Args:
            input_name: 输入源名称

        Returns:
            bool: True 表示已静音

        Raises:
            OBSResourceNotFoundError: 输入源不存在
        """
        try:
            if not self.exists(input_name):
                raise OBSResourceNotFoundError("输入源", input_name, self.get_names())

            response = self.client.call(requests.GetInputMute(inputName=input_name))
            if hasattr(response, 'datain'):
                return response.datain.get('inputMuted', False)
            return False

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"获取输入源静音状态失败: {e}")
            return False

    def mute(self, input_name: str) -> bool:
        """
        静音输入源

        Args:
            input_name: 输入源名称

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 输入源不存在
        """
        try:
            if not self.exists(input_name):
                raise OBSResourceNotFoundError("输入源", input_name, self.get_names())

            self.client.call(requests.SetInputMute(inputName=input_name, inputMuted=True))
            self.logger.info(f"已静音输入源: {input_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"静音输入源失败: {e}")
            return False

    def unmute(self, input_name: str) -> bool:
        """
        取消静音输入源

        Args:
            input_name: 输入源名称

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 输入源不存在
        """
        try:
            if not self.exists(input_name):
                raise OBSResourceNotFoundError("输入源", input_name, self.get_names())

            self.client.call(requests.SetInputMute(inputName=input_name, inputMuted=False))
            self.logger.info(f"已取消静音输入源: {input_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"取消静音输入源失败: {e}")
            return False

    def toggle_mute(self, input_name: str) -> bool:
        """
        切换输入源静音状态

        Args:
            input_name: 输入源名称

        Returns:
            bool: 切换后的静音状态（True=静音，False=未静音）

        Raises:
            OBSResourceNotFoundError: 输入源不存在
        """
        try:
            if not self.exists(input_name):
                raise OBSResourceNotFoundError("输入源", input_name, self.get_names())

            response = self.client.call(requests.ToggleInputMute(inputName=input_name))

            muted = False
            if hasattr(response, 'datain'):
                muted = response.datain.get('inputMuted', False)

            status = "静音" if muted else "取消静音"
            self.logger.info(f"输入源 '{input_name}' 已{status}")
            return muted

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"切换输入源静音状态失败: {e}")
            return self.is_muted(input_name)

    def get_settings(self, input_name: str) -> Dict[str, Any]:
        """
        获取输入源设置

        Args:
            input_name: 输入源名称

        Returns:
            Dict: 输入源设置

        Raises:
            OBSResourceNotFoundError: 输入源不存在
        """
        try:
            if not self.exists(input_name):
                raise OBSResourceNotFoundError("输入源", input_name, self.get_names())

            response = self.client.call(requests.GetInputSettings(inputName=input_name))
            if hasattr(response, 'datain'):
                return response.datain.get('inputSettings', {})
            return {}

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"获取输入源设置失败: {e}")
            return {}

    def set_settings(self, input_name: str, settings: Dict[str, Any]) -> bool:
        """
        设置输入源设置

        Args:
            input_name: 输入源名称
            settings: 设置字典

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 输入源不存在
        """
        try:
            if not self.exists(input_name):
                raise OBSResourceNotFoundError("输入源", input_name, self.get_names())

            self.client.call(requests.SetInputSettings(
                inputName=input_name,
                inputSettings=settings
            ))
            self.logger.info(f"已更新输入源设置: {input_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"设置输入源设置失败: {e}")
            return False

    def get_info(self) -> Dict[str, Any]:
        """
        获取输入源信息摘要

        Returns:
            Dict: 输入源信息
        """
        all_inputs = self.get_all()
        audio_inputs = self.get_audio_inputs()
        input_kinds = self.get_input_kinds()

        # 获取音频输入的静音状态
        audio_status = {}
        for input_name in audio_inputs:
            try:
                audio_status[input_name] = self.is_muted(input_name)
            except:
                audio_status[input_name] = None

        # 统计输入源类型分布
        input_type_count = {}
        for inp in all_inputs:
            input_kind = inp.get('inputKind', 'unknown')
            input_type_count[input_kind] = input_type_count.get(input_kind, 0) + 1

        return {
            "total_inputs": len(all_inputs),
            "audio_inputs": len(audio_inputs),
            "available_input_kinds": len(input_kinds),
            "input_names": self.get_names(),
            "audio_input_names": audio_inputs,
            "audio_mute_status": audio_status,
            "available_kinds": input_kinds,
            "input_type_distribution": input_type_count,
        }

    def save_input_kinds_to_json(self, filepath: str = None) -> str:
        """
        将输入类型数据保存为 JSON 格式

        Args:
            filepath: 保存路径，默认为 download/input_kinds.json

        Returns:
            str: 保存的文件路径
        """
        import json
        import os
        from datetime import datetime

        if filepath is None:
            # 默认保存到 download 目录
            filepath = "download/input_kinds.json"

        try:
            # 获取数据
            input_kinds_versioned = self.get_input_kinds(unversioned=False)
            input_kinds_unversioned = self.get_input_kinds(unversioned=True)
            current_inputs = self.get_names()

            # 按类别分组
            audio_types = []
            video_types = []
            capture_types = []
            other_types = []

            for kind in input_kinds_versioned:
                if 'audio' in kind.lower() or 'wasapi' in kind.lower():
                    audio_types.append(kind)
                elif 'capture' in kind.lower():
                    capture_types.append(kind)
                elif any(x in kind.lower() for x in ['image', 'video', 'ffmpeg', 'text', 'browser', 'color']):
                    video_types.append(kind)
                else:
                    other_types.append(kind)

            # 构建数据结构
            data = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "total_kinds": len(input_kinds_versioned),
                    "current_inputs_count": len(current_inputs)
                },
                "input_kinds": {
                    "versioned": input_kinds_versioned,
                    "unversioned": input_kinds_unversioned,
                    "by_category": {
                        "audio": audio_types,
                        "video_media": video_types,
                        "capture": capture_types,
                        "other": other_types
                    }
                },
                "current_inputs": current_inputs,
                "statistics": {
                    "audio_types_count": len(audio_types),
                    "video_types_count": len(video_types),
                    "capture_types_count": len(capture_types),
                    "other_types_count": len(other_types)
                }
            }

            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"输入类型数据已保存到: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"保存输入类型数据失败: {e}")
            raise

    def create_input(self, input_name: str, input_kind: str, scene_name: str = None,
                     scene_uuid: str = None, input_settings: Dict[str, Any] = None,
                     scene_item_enabled: bool = True, check_duplicates: bool = True) -> Dict[str, Any]:
        """
        创建一个新的输入，并将其作为场景项添加到指定的场景

        Args:
            input_name: 要创建的新输入的名称
            input_kind: 要创建的输入类型
            scene_name: 将输入添加到的场景名称（与 scene_uuid 二选一）
            scene_uuid: 将输入添加到的场景UUID（与 scene_name 二选一）
            input_settings: 用于初始化输入的设置对象
            scene_item_enabled: 是否启用创建的场景项，默认为 True
            check_duplicates: 是否检查重复的输入名称，默认为 True

        Returns:
            Dict[str, Any]: 包含新创建输入的详细信息
            - input_uuid: 新创建的输入的 UUID
            - scene_item_id: 新创建的场景项目的 ID
            - input_name: 输入名称
            - input_kind: 输入类型
            - success: 创建是否成功

        Raises:
            ValueError: 当参数验证失败时
            OBSResourceNotFoundError: 当场景不存在时
            Exception: 当 OBS 调用失败时
        """
        try:
            # 1. 基本参数验证
            if not input_name or not input_name.strip():
                raise ValueError("输入名称不能为空")

            if not input_kind or not input_kind.strip():
                raise ValueError("输入类型不能为空")

            if (scene_name is None) == (scene_uuid is None):
                raise ValueError("必须提供 scene_name 或 scene_uuid，但不能同时提供两者")

            # 2. 检查输入名称是否已存在
            if check_duplicates and self.exists(input_name):
                raise ValueError(f"输入名称 '{input_name}' 已存在")

            # 3. 验证输入类型是否支持
            available_kinds = self.get_input_kinds()
            if available_kinds and input_kind not in available_kinds:
                self.logger.warning(f"输入类型 '{input_kind}' 可能不受支持")

            # 4. 构建请求参数
            request_params = {
                "inputName": input_name.strip(),
                "inputKind": input_kind.strip(),
                "sceneItemEnabled": scene_item_enabled
            }

            if scene_name is not None:
                request_params["sceneName"] = scene_name.strip()
            if scene_uuid is not None:
                request_params["sceneUuid"] = scene_uuid.strip()
            if input_settings is not None:
                request_params["inputSettings"] = input_settings

            # 5. 发送请求
            self.logger.debug(f"创建输入请求参数: {request_params}")
            response = self.client.call(requests.CreateInput(**request_params))

            # 6. 处理响应
            if hasattr(response, 'datain') and response.datain:
                result = response.datain
                input_uuid = result.get('inputUuid', '')
                scene_item_id = result.get('sceneItemId', 0)

                self.logger.info(f"成功创建输入 '{input_name}' (UUID: {input_uuid}, 场景项ID: {scene_item_id})")

                return {
                    'input_uuid': input_uuid,
                    'scene_item_id': scene_item_id,
                    'input_name': input_name,
                    'input_kind': input_kind,
                    'success': True
                }
            else:
                self.logger.warning(f"创建输入 '{input_name}' 的响应为空或无效")
                return {
                    'input_uuid': '',
                    'scene_item_id': 0,
                    'input_name': input_name,
                    'input_kind': input_kind,
                    'success': False
                }

        except ValueError as e:
            self.logger.error(f"参数验证失败: {e}")
            raise
        except Exception as e:
            # 检查是否是特定的 OBS 错误
            error_msg = str(e).lower()
            if 'scene' in error_msg and ('not found' in error_msg or '不存在' in error_msg):
                from ..core.exceptions import OBSResourceNotFoundError
                raise OBSResourceNotFoundError(f"场景不存在: {scene_name or scene_uuid}")
            elif 'input' in error_msg and ('exists' in error_msg or '已存在' in error_msg):
                raise ValueError(f"输入名称 '{input_name}' 已存在")
            else:
                self.logger.error(f"创建输入失败: {e}")
                raise

    def get_input_types_with_chinese(self) -> Dict[str, str]:
        """
        获取输入类型及其中文名称映射

        Returns:
            Dict[str, str]: 英文类型 -> 中文名称的映射
        """
        return InputTypeHelper.get_all_mappings()

    def get_chinese_name(self, input_kind: str) -> str:
        """
        获取输入类型的中文名称

        Args:
            input_kind: 英文输入类型

        Returns:
            str: 中文名称
        """
        return to_chinese(input_kind)

    def get_english_type(self, chinese_name: str) -> str:
        """
        根据中文名称获取英文输入类型

        Args:
            chinese_name: 中文名称

        Returns:
            str: 英文输入类型
        """
        return to_english(chinese_name)

    def remove_input(self, input_name: str = None, input_uuid: str = None) -> bool:
        """
        删除输入源

        注意：将立即删除所有相关的场景项目

        Args:
            input_name: 要删除的输入源名称（与 input_uuid 二选一）
            input_uuid: 要删除的输入源 UUID（与 input_name 二选一）

        Returns:
            bool: 删除是否成功

        Raises:
            ValueError: 当 input_name 和 input_uuid 都未提供或都提供时
            OBSResourceNotFoundError: 当输入源不存在时
        """
        try:
            # 参数验证
            if (input_name is None) == (input_uuid is None):
                raise ValueError("必须提供 input_name 或 input_uuid，但不能同时提供两者")

            # 构建请求参数
            request_params = {}
            if input_name is not None:
                request_params["inputName"] = input_name.strip()
            if input_uuid is not None:
                request_params["inputUuid"] = input_uuid.strip()

            # 发送请求
            self.logger.debug(f"删除输入源请求参数: {request_params}")
            self.client.call(requests.RemoveInput(**request_params))

            # 记录成功信息
            identifier = input_name or input_uuid
            self.logger.info(f"成功删除输入源: {identifier}")
            return True

        except ValueError as e:
            self.logger.error(f"参数验证失败: {e}")
            raise
        except Exception as e:
            # 检查是否是特定的 OBS 错误
            error_msg = str(e).lower()
            if 'input' in error_msg and ('not found' in error_msg or '不存在' in error_msg):
                from ..core.exceptions import OBSResourceNotFoundError
                identifier = input_name or input_uuid
                raise OBSResourceNotFoundError(f"输入源不存在: {identifier}")
            else:
                self.logger.error(f"删除输入源失败: {e}")
                raise

    def rename_input(self, new_input_name: str, input_name: str = None, input_uuid: str = None) -> bool:
        """
        重命名输入源

        Args:
            new_input_name: 新的输入源名称
            input_name: 当前输入源名称（与 input_uuid 二选一）
            input_uuid: 当前输入源 UUID（与 input_name 二选一）

        Returns:
            bool: 重命名是否成功

        Raises:
            ValueError: 当参数验证失败时
            OBSResourceNotFoundError: 当输入源不存在时
        """
        try:
            # 参数验证
            if not new_input_name or not new_input_name.strip():
                raise ValueError("新输入名称不能为空")

            if (input_name is None) == (input_uuid is None):
                raise ValueError("必须提供 input_name 或 input_uuid，但不能同时提供两者")

            # 检查新名称是否已存在
            if self.exists(new_input_name.strip()):
                raise ValueError(f"输入名称 '{new_input_name.strip()}' 已存在")

            # 构建请求参数
            request_params = {
                "newInputName": new_input_name.strip()
            }

            if input_name is not None:
                request_params["inputName"] = input_name.strip()
            if input_uuid is not None:
                request_params["inputUuid"] = input_uuid.strip()

            # 发送请求
            self.logger.debug(f"重命名输入源请求参数: {request_params}")
            self.client.call(requests.SetInputName(**request_params))

            # 记录成功信息
            old_identifier = input_name or input_uuid
            self.logger.info(f"成功重命名输入源: {old_identifier} -> {new_input_name}")
            return True

        except ValueError as e:
            self.logger.error(f"参数验证失败: {e}")
            raise
        except Exception as e:
            # 检查是否是特定的 OBS 错误
            error_msg = str(e).lower()
            if 'input' in error_msg and ('not found' in error_msg or '不存在' in error_msg):
                from ..core.exceptions import OBSResourceNotFoundError
                identifier = input_name or input_uuid
                raise OBSResourceNotFoundError(f"输入源不存在: {identifier}")
            else:
                self.logger.error(f"重命名输入源失败: {e}")
                raise

    def get_input_default_settings(self, input_kind: str) -> Dict[str, Any]:
        """
        获取输入类型的默认设置

        Args:
            input_kind: 输入类型名称

        Returns:
            Dict[str, Any]: 输入类型的默认设置对象

        Raises:
            ValueError: 当输入类型为空时
            OBSResourceNotFoundError: 当输入类型不存在时
        """
        try:
            # 参数验证
            if not input_kind or not input_kind.strip():
                raise ValueError("输入类型不能为空")

            # 发送请求
            self.logger.debug(f"获取输入类型默认设置: {input_kind}")
            response = self.client.call(requests.GetInputDefaultSettings(inputKind=input_kind.strip()))

            # 处理响应
            if hasattr(response, 'datain') and response.datain:
                default_settings = response.datain.get('defaultInputSettings', {})
                self.logger.info(f"成功获取输入类型 '{input_kind}' 的默认设置")
                return default_settings
            else:
                self.logger.warning(f"获取输入类型 '{input_kind}' 默认设置的响应为空")
                return {}

        except ValueError as e:
            self.logger.error(f"参数验证失败: {e}")
            raise
        except Exception as e:
            # 检查是否是特定的 OBS 错误
            error_msg = str(e).lower()
            if 'kind' in error_msg and ('not found' in error_msg or '不存在' in error_msg or 'invalid' in error_msg):
                from ..core.exceptions import OBSResourceNotFoundError
                raise OBSResourceNotFoundError(f"输入类型不存在: {input_kind}")
            else:
                self.logger.error(f"获取输入类型默认设置失败: {e}")
                raise

