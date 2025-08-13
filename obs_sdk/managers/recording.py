"""
录制管理器

负责 OBS 录制功能的管理。
"""

import time
import logging
import os
import shutil
from typing import Optional, Dict, Any

try:
    from obswebsocket import requests
except ImportError:
    raise ImportError("请安装 obs-websocket-py: pip install obs-websocket-py")

from ..core.client import OBSClient
from ..core.exceptions import OBSOutputRunningError, OBSOutputNotRunningError


logger = logging.getLogger(__name__)


class RecordingManager:
    """
    录制管理器
    
    提供录制相关的所有功能，包括开始、停止、暂停、恢复录制等。
    """
    
    def __init__(self, client: OBSClient):
        """
        初始化录制管理器

        Args:
            client: OBS 客户端实例
        """
        self.client = client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._default_output_dir = None
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取录制状态
        
        Returns:
            Dict: 录制状态信息
        """
        response = self.client.call(requests.GetRecordStatus())
        if hasattr(response, 'datain'):
            return response.datain
        return {}
    
    def is_recording(self) -> bool:
        """
        检查是否正在录制
        
        Returns:
            bool: True 表示正在录制
        """
        status = self.get_status()
        return status.get('outputActive', False)
    
    def is_paused(self) -> bool:
        """
        检查录制是否暂停
        
        Returns:
            bool: True 表示录制已暂停
        """
        status = self.get_status()
        return status.get('outputPaused', False)
    
    def get_duration(self) -> Optional[int]:
        """
        获取录制时长（毫秒）
        
        Returns:
            Optional[int]: 录制时长，未录制时返回 None
        """
        status = self.get_status()
        return status.get('outputDuration')
    
    def get_timecode(self) -> Optional[str]:
        """
        获取录制时间码

        Returns:
            Optional[str]: 时间码字符串，未录制时返回 None
        """
        status = self.get_status()
        return status.get('outputTimecode')

    def set_output_directory(self, directory: str) -> bool:
        """
        设置录制输出目录

        Args:
            directory: 输出目录路径

        Returns:
            bool: 设置是否成功
        """
        try:
            # 确保目录存在
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                self.logger.info(f"创建录制目录: {directory}")

            # 获取绝对路径
            abs_directory = os.path.abspath(directory)

            # 尝试通过设置输出设置来改变录制路径
            # 使用 SetOutputSettings 来设置录制输出路径
            try:
                # 获取当前的录制输出设置
                response = self.client.call(requests.GetOutputSettings(outputName="adv_file_output"))
                if hasattr(response, 'datain'):
                    settings = response.datain.get('outputSettings', {})
                    # 更新路径设置
                    settings['path'] = abs_directory
                    # 设置新的输出设置
                    self.client.call(requests.SetOutputSettings(
                        outputName="adv_file_output",
                        outputSettings=settings
                    ))
                    self._default_output_dir = abs_directory
                    self.logger.info(f"录制输出目录已设置为: {abs_directory}")
                    return True
            except Exception as e:
                self.logger.warning(f"使用高级输出设置失败: {e}")

            # 如果高级设置失败，尝试简单录制输出
            try:
                response = self.client.call(requests.GetOutputSettings(outputName="simple_file_output"))
                if hasattr(response, 'datain'):
                    settings = response.datain.get('outputSettings', {})
                    settings['FilePath'] = abs_directory
                    self.client.call(requests.SetOutputSettings(
                        outputName="simple_file_output",
                        outputSettings=settings
                    ))
                    self._default_output_dir = abs_directory
                    self.logger.info(f"录制输出目录已设置为: {abs_directory}")
                    return True
            except Exception as e:
                self.logger.warning(f"使用简单输出设置失败: {e}")

            # 如果都失败了，至少记录目录以供参考
            self._default_output_dir = abs_directory
            self.logger.warning(f"无法通过API设置录制目录，但已记录目标目录: {abs_directory}")
            return False

        except Exception as e:
            self.logger.error(f"设置录制输出目录失败: {e}")
            return False

    def get_output_directory(self) -> Optional[str]:
        """
        获取当前录制输出目录

        Returns:
            Optional[str]: 当前输出目录路径
        """
        try:
            # 尝试从高级输出获取
            try:
                response = self.client.call(requests.GetOutputSettings(outputName="adv_file_output"))
                if hasattr(response, 'datain'):
                    settings = response.datain.get('outputSettings', {})
                    path = settings.get('path')
                    if path:
                        return path
            except:
                pass

            # 尝试从简单输出获取
            try:
                response = self.client.call(requests.GetOutputSettings(outputName="simple_file_output"))
                if hasattr(response, 'datain'):
                    settings = response.datain.get('outputSettings', {})
                    path = settings.get('FilePath')
                    if path:
                        return path
            except:
                pass

            return self._default_output_dir
        except Exception as e:
            self.logger.error(f"获取录制输出目录失败: {e}")
            return self._default_output_dir

    def _move_file_to_directory(self, source_path: str, target_directory: str) -> Optional[str]:
        """
        将文件移动到指定目录

        Args:
            source_path: 源文件路径
            target_directory: 目标目录

        Returns:
            Optional[str]: 新的文件路径，失败时返回 None
        """
        try:
            if not os.path.exists(source_path):
                self.logger.error(f"源文件不存在: {source_path}")
                return None

            # 确保目标目录存在
            if not os.path.exists(target_directory):
                os.makedirs(target_directory, exist_ok=True)
                self.logger.info(f"创建目标目录: {target_directory}")

            # 获取文件名
            filename = os.path.basename(source_path)
            target_path = os.path.join(target_directory, filename)

            # 如果目标文件已存在，添加时间戳
            if os.path.exists(target_path):
                import datetime
                timestamp = datetime.datetime.now().strftime("_%H%M%S")
                name, ext = os.path.splitext(filename)
                filename = f"{name}{timestamp}{ext}"
                target_path = os.path.join(target_directory, filename)

            # 移动文件
            shutil.move(source_path, target_path)
            self.logger.info(f"文件已移动: {source_path} -> {target_path}")
            return target_path

        except Exception as e:
            self.logger.error(f"移动文件失败: {e}")
            return None
    
    def start(self, output_directory: Optional[str] = None, filename: Optional[str] = None) -> bool:
        """
        开始录制

        Args:
            output_directory: 可选的输出目录，如果不指定则使用默认的download目录
            filename: 可选的文件名，如果不指定则使用默认命名

        Returns:
            bool: 操作是否成功

        Raises:
            OBSOutputRunningError: 录制已在进行中
        """
        try:
            if self.is_recording():
                raise OBSOutputRunningError("录制")

            # 如果指定了输出目录，则设置它
            if output_directory:
                self.set_output_directory(output_directory)
            elif self._default_output_dir is None:
                # 如果没有设置过默认目录，则设置为download文件夹
                download_dir = os.path.join(os.getcwd(), "download")
                self.set_output_directory(download_dir)

            # 如果指定了文件名，尝试设置完整路径
            if filename and output_directory:
                try:
                    full_path = os.path.join(output_directory, filename)
                    # 尝试设置录制文件名
                    self.client.call(requests.SetRecordFilename(filename=full_path))
                    self.logger.info(f"设置录制文件路径: {full_path}")
                except Exception as e:
                    self.logger.warning(f"设置录制文件名失败: {e}")

            self.client.call(requests.StartRecord())
            self.logger.info("录制已开始")
            return True

        except OBSOutputRunningError:
            raise
        except Exception as e:
            self.logger.error(f"开始录制失败: {e}")
            return False
    
    def stop(self) -> Optional[str]:
        """
        停止录制
        
        Returns:
            Optional[str]: 录制文件路径，失败时返回 None
            
        Raises:
            OBSOutputNotRunningError: 录制未在进行中
        """
        try:
            if not self.is_recording():
                raise OBSOutputNotRunningError("录制")
            
            response = self.client.call(requests.StopRecord())
            
            output_path = ""
            if hasattr(response, 'datain'):
                output_path = response.datain.get('outputPath', '')
            
            self.logger.info(f"录制已停止，文件保存至: {output_path}")
            return output_path
            
        except OBSOutputNotRunningError:
            raise
        except Exception as e:
            self.logger.error(f"停止录制失败: {e}")
            return None
    
    def toggle(self) -> bool:
        """
        切换录制状态
        
        Returns:
            bool: 切换后的录制状态（True=录制中，False=已停止）
        """
        try:
            response = self.client.call(requests.ToggleRecord())
            
            active = False
            if hasattr(response, 'datain'):
                active = response.datain.get('outputActive', False)
            
            status = "开始" if active else "停止"
            self.logger.info(f"录制已{status}")
            return active
            
        except Exception as e:
            self.logger.error(f"切换录制状态失败: {e}")
            return self.is_recording()
    
    def pause(self) -> bool:
        """
        暂停录制
        
        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.is_recording():
                self.logger.warning("录制未在进行中，无法暂停")
                return False
            
            if self.is_paused():
                self.logger.warning("录制已暂停")
                return True
            
            self.client.call(requests.PauseRecord())
            self.logger.info("录制已暂停")
            return True
            
        except Exception as e:
            self.logger.error(f"暂停录制失败: {e}")
            return False
    
    def resume(self) -> bool:
        """
        恢复录制
        
        Returns:
            bool: 操作是否成功
        """
        try:
            if not self.is_recording():
                self.logger.warning("录制未在进行中，无法恢复")
                return False
            
            if not self.is_paused():
                self.logger.warning("录制未暂停")
                return True
            
            self.client.call(requests.ResumeRecord())
            self.logger.info("录制已恢复")
            return True
            
        except Exception as e:
            self.logger.error(f"恢复录制失败: {e}")
            return False
    
    def quick_record(self, duration: float, output_directory: Optional[str] = None, filename: Optional[str] = None) -> Optional[str]:
        """
        快速录制指定时长

        Args:
            duration: 录制时长（秒）
            output_directory: 可选的输出目录，如果不指定则使用默认的download目录
            filename: 可选的文件名，如果不指定则使用默认命名

        Returns:
            Optional[str]: 录制文件路径，失败时返回 None
        """
        try:
            # 设置默认的download目录
            if not output_directory:
                output_directory = os.path.join(os.getcwd(), "download")

            # 首先尝试设置录制目录
            self.set_output_directory(output_directory)

            if self.start():
                self.logger.info(f"开始录制 {duration} 秒...")
                time.sleep(duration)
                original_path = self.stop()

                if original_path:
                    # 等待一小段时间确保文件完全写入并释放
                    time.sleep(0.5)

                    # 如果录制成功，检查文件是否在正确的目录中
                    original_dir = os.path.dirname(original_path)
                    target_dir = os.path.abspath(output_directory)

                    # 如果文件不在目标目录中，移动它
                    if os.path.normpath(original_dir).lower() != os.path.normpath(target_dir).lower():
                        # 尝试多次移动文件，因为可能被占用
                        for attempt in range(3):
                            moved_path = self._move_file_to_directory(original_path, target_dir)
                            if moved_path:
                                return moved_path
                            else:
                                self.logger.warning(f"文件移动失败，尝试 {attempt + 1}/3")
                                time.sleep(1)  # 等待1秒后重试

                        self.logger.warning(f"文件移动失败，返回原始路径: {original_path}")
                        return original_path
                    else:
                        return original_path

            return None

        except Exception as e:
            self.logger.error(f"快速录制失败: {e}")
            # 尝试停止录制
            try:
                if self.is_recording():
                    self.stop()
            except:
                pass
            return None
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取录制信息摘要
        
        Returns:
            Dict: 录制信息
        """
        status = self.get_status()
        return {
            "recording": self.is_recording(),
            "paused": self.is_paused(),
            "duration": self.get_duration(),
            "timecode": self.get_timecode(),
            "bytes": status.get('outputBytes', 0),
        }
