"""
场景管理器

负责 OBS 场景功能的管理。
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


class SceneManager:
    """
    场景管理器

    提供场景相关的所有功能，包括场景切换、Studio Mode 等。
    """

    def __init__(self, client: OBSClient):
        """
        初始化场景管理器

        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_all(self) -> List[Dict[str, Any]]:
        """
        获取所有场景

        Returns:
            List[Dict]: 场景列表
        """
        response = self.client.call(requests.GetSceneList())
        if hasattr(response, 'datain'):
            return response.datain.get('scenes', [])
        return []

    def get_names(self) -> List[str]:
        """
        获取所有场景名称

        Returns:
            List[str]: 场景名称列表
        """
        scenes = self.get_all()
        return [scene.get('sceneName', '') for scene in scenes]

    def get_group_list(self) -> List[str]:
        """
        获取所有组列表

        组在 OBS 中实际上是场景，只是被重命名和修改了。
        在 obs-websocket 中，我们尽可能地将它们视为场景。

        Returns:
            List[str]: 组名称列表
        """
        try:
            response = self.client.call(requests.GetGroupList())
            if hasattr(response, 'datain'):
                return response.datain.get('groups', [])
            return []
        except Exception as e:
            self.logger.error(f"获取组列表失败: {e}")
            return []

    def get_current_program(self) -> str:
        """
        获取当前节目场景

        Returns:
            str: 当前节目场景名称
        """
        response = self.client.call(requests.GetCurrentProgramScene())
        if hasattr(response, 'datain'):
            return response.datain.get('currentProgramSceneName', '')
        return ''

    def get_current_preview(self) -> str:
        """
        获取当前预览场景（Studio Mode）

        Returns:
            str: 当前预览场景名称
        """
        try:
            response = self.client.call(requests.GetCurrentPreviewScene())
            if hasattr(response, 'datain'):
                return response.datain.get('currentPreviewSceneName', '')
        except Exception as e:
            self.logger.debug(f"获取预览场景失败（可能未启用 Studio Mode）: {e}")
        return ''

    def switch_to(self, scene_name: str) -> bool:
        """
        切换到指定场景

        Args:
            scene_name: 场景名称

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 场景不存在
        """
        try:
            # 检查场景是否存在
            available_scenes = self.get_names()
            if scene_name not in available_scenes:
                raise OBSResourceNotFoundError("场景", scene_name, available_scenes)

            self.client.call(requests.SetCurrentProgramScene(sceneName=scene_name))
            self.logger.info(f"已切换到场景: {scene_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"切换场景失败: {e}")
            return False

    def set_preview(self, scene_name: str) -> bool:
        """
        设置预览场景（Studio Mode）

        Args:
            scene_name: 场景名称

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 场景不存在
        """
        try:
            # 检查场景是否存在
            available_scenes = self.get_names()
            if scene_name not in available_scenes:
                raise OBSResourceNotFoundError("场景", scene_name, available_scenes)

            self.client.call(requests.SetCurrentPreviewScene(sceneName=scene_name))
            self.logger.info(f"已设置预览场景: {scene_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"设置预览场景失败: {e}")
            return False

    def is_studio_mode_enabled(self) -> bool:
        """
        检查 Studio Mode 是否启用

        Returns:
            bool: True 表示 Studio Mode 已启用
        """
        try:
            response = self.client.call(requests.GetStudioModeEnabled())
            if hasattr(response, 'datain'):
                return response.datain.get('studioModeEnabled', False)
        except Exception as e:
            self.logger.debug(f"获取 Studio Mode 状态失败: {e}")
        return False

    def enable_studio_mode(self, enabled: bool = True) -> bool:
        """
        启用或禁用 Studio Mode

        Args:
            enabled: True 启用，False 禁用

        Returns:
            bool: 操作是否成功
        """
        try:
            self.client.call(requests.SetStudioModeEnabled(studioModeEnabled=enabled))
            status = "启用" if enabled else "禁用"
            self.logger.info(f"Studio Mode 已{status}")
            return True

        except Exception as e:
            self.logger.error(f"设置 Studio Mode 失败: {e}")
            return False

    def disable_studio_mode(self) -> bool:
        """
        禁用 Studio Mode

        Returns:
            bool: 操作是否成功
        """
        return self.enable_studio_mode(False)

    def trigger_transition(self) -> bool:
        """
        触发 Studio Mode 转场

        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.is_studio_mode_enabled():
                self.logger.warning("Studio Mode 未启用，无法触发转场")
                return False

            self.client.call(requests.TriggerStudioModeTransition())
            self.logger.info("已触发 Studio Mode 转场")
            return True

        except Exception as e:
            self.logger.error(f"触发转场失败: {e}")
            return False

    def exists(self, scene_name: str) -> bool:
        """
        检查场景是否存在

        Args:
            scene_name: 场景名称

        Returns:
            bool: True 表示场景存在
        """
        return scene_name in self.get_names()

    def create(self, scene_name: str) -> bool:
        """
        创建新场景

        Args:
            scene_name: 场景名称

        Returns:
            bool: 操作是否成功
        """
        try:
            # 检查场景是否已存在
            if self.exists(scene_name):
                self.logger.warning(f"场景 '{scene_name}' 已存在")
                return False

            self.client.call(requests.CreateScene(sceneName=scene_name))
            self.logger.info(f"已创建场景: {scene_name}")
            return True

        except Exception as e:
            self.logger.error(f"创建场景失败: {e}")
            return False

    def delete(self, scene_name: str) -> bool:
        """
        删除场景

        Args:
            scene_name: 场景名称

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 场景不存在
        """
        try:
            # 检查场景是否存在
            available_scenes = self.get_names()
            if scene_name not in available_scenes:
                raise OBSResourceNotFoundError("场景", scene_name, available_scenes)

            self.client.call(requests.RemoveScene(sceneName=scene_name))
            self.logger.info(f"已删除场景: {scene_name}")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"删除场景失败: {e}")
            return False

    def get_info(self) -> Dict[str, Any]:
        """
        获取场景信息摘要

        Returns:
            Dict: 场景信息
        """
        return {
            "current_program": self.get_current_program(),
            "current_preview": self.get_current_preview(),
            "studio_mode": self.is_studio_mode_enabled(),
            "total_scenes": len(self.get_names()),
            "scene_names": self.get_names(),
        }

    def rename(self, scene_name: str, new_scene_name: str) -> bool:
        """
        重命名场景

        Args:
            scene_name: 当前场景名称
            new_scene_name: 新的场景名称

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 场景不存在或新名称已存在
        """
        try:
            # 检查场景是否存在
            available_scenes = self.get_names()
            if scene_name not in available_scenes:
                raise OBSResourceNotFoundError("场景", scene_name, available_scenes)

            # 检查新名称是否已存在
            if new_scene_name in available_scenes:
                self.logger.warning(f"场景 '{new_scene_name}' 已存在")
                return False

            self.client.call(requests.SetSceneName(sceneName=scene_name, newSceneName=new_scene_name))
            self.logger.info(f"已将场景 '{scene_name}' 重命名为 '{new_scene_name}'")
            return True

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"重命名场景失败: {e}")
            return False

    def get_scene_transition_override(self, scene_name: str) -> Dict[str, Any]:
        """
        获取场景的转场覆盖设置

        Args:
            scene_name: 场景名称

        Returns:
            Dict: 转场覆盖设置信息
            {
                "transition_name": str,      # 覆盖的转场名称，如果没有则为 None
                "transition_duration": int    # 转场持续时间（毫秒），如果没有则为 None
            }

        Raises:
            OBSResourceNotFoundError: 场景不存在
        """
        try:
            # 检查场景是否存在
            available_scenes = self.get_names()
            if scene_name not in available_scenes:
                raise OBSResourceNotFoundError("场景", scene_name, available_scenes)

            response = self.client.call(requests.GetSceneSceneTransitionOverride(sceneName=scene_name))
            if hasattr(response, 'datain'):
                return {
                    "transition_name": response.datain.get('transitionName'),
                    "transition_duration": response.datain.get('transitionDuration')
                }
            return {}

        except OBSResourceNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"获取场景转场覆盖设置失败: {e}")
            return {}

    def set_scene_transition_override(self, scene_name: str, transition_name: Optional[str] = None,  transition_duration: Optional[int] = None) -> bool:
        """
        设置场景的转场覆盖

        Args:
            scene_name: 场景名称
            transition_name: 要覆盖的转场名称，指定 None 可移除覆盖
            transition_duration: 转场持续时间（毫秒），指定 None 可移除设置，值范围 50-20000

        Returns:
            bool: 操作是否成功

        Raises:
            OBSResourceNotFoundError: 场景不存在
            ValueError: transition_duration 超出有效范围
        """
        try:
            # 检查场景是否存在
            available_scenes = self.get_names()
            if scene_name not in available_scenes:
                raise OBSResourceNotFoundError("场景", scene_name, available_scenes)

            # 验证 transition_duration 范围
            if transition_duration is not None and (transition_duration < 50 or transition_duration > 20000):
                raise ValueError("transition_duration 必须在 50-20000 毫秒范围内")

            self.client.call(requests.SetSceneSceneTransitionOverride(
                sceneName=scene_name,
                transitionName=transition_name,
                transitionDuration=transition_duration
            ))
            self.logger.info(f"已为场景 '{scene_name}' 设置转场覆盖")
            return True

        except OBSResourceNotFoundError:
            raise
        except ValueError:
            raise
        except Exception as e:
            self.logger.error(f"设置场景转场覆盖失败: {e}")
            return False
