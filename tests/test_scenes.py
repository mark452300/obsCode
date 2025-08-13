"""
测试场景管理器 (SceneManager)

这个测试文件使用真实的 OBS 连接来测试场景管理功能。
运行测试前请确保：
1. OBS Studio 正在运行
2. WebSocket 服务器已启用（工具 -> WebSocket 服务器设置）
3. 配置正确的连接参数（host, port, password）
"""

import unittest
import time
import logging

from obs_sdk import OBSManager, OBSConfig
from obs_sdk.exceptions import OBSResourceNotFoundError


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestSceneManager(unittest.TestCase):
    """场景管理器测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化 - 建立 OBS 连接"""
        cls.config = OBSConfig()
        cls.obs = OBSManager(cls.config, auto_connect=False)

        # 尝试连接到 OBS
        if not cls.obs.connect():
            raise unittest.SkipTest("无法连接到 OBS Studio，请确保 OBS 正在运行且 WebSocket 服务器已启用")

        logger.info("已连接到 OBS Studio")

        # 保存初始状态
        cls.initial_scenes = cls.obs.scenes.get_names()
        cls.initial_current_scene = cls.obs.scenes.get_current_program()
        cls.initial_studio_mode = cls.obs.scenes.is_studio_mode_enabled()

        logger.info(f"初始场景列表: {cls.initial_scenes}")
        logger.info(f"初始当前场景: {cls.initial_current_scene}")
        logger.info(f"初始 Studio Mode 状态: {cls.initial_studio_mode}")

    @classmethod
    def tearDownClass(cls):
        """测试类清理 - 恢复初始状态并断开连接"""
        if hasattr(cls, 'obs') and cls.obs.is_connected():
            try:
                # 恢复 Studio Mode 状态
                if cls.initial_studio_mode != cls.obs.scenes.is_studio_mode_enabled():
                    cls.obs.scenes.enable_studio_mode(cls.initial_studio_mode)

                # 清理测试创建的场景
                current_scenes = cls.obs.scenes.get_names()
                for scene in current_scenes:
                    if scene.startswith("TestScene_") and scene not in cls.initial_scenes:
                        try:
                            cls.obs.scenes.delete(scene)
                            logger.info(f"清理测试场景: {scene}")
                        except Exception as e:
                            logger.warning(f"清理场景 {scene} 失败: {e}")

                # 恢复初始场景
                if cls.initial_current_scene and cls.obs.scenes.exists(cls.initial_current_scene):
                    cls.obs.scenes.switch_to(cls.initial_current_scene)

                logger.info("已恢复初始状态")
            except Exception as e:
                logger.error(f"恢复初始状态失败: {e}")
            finally:
                cls.obs.disconnect()
                logger.info("已断开 OBS 连接")

    def setUp(self):
        """每个测试方法的初始化"""
        if not self.obs.is_connected():
            self.skipTest("OBS 连接已断开")

    def test_connection_status(self):
        """测试连接状态"""
        self.assertTrue(self.obs.is_connected(), "应该已连接到 OBS")

        # 测试版本信息
        version_info = self.obs.get_version()
        self.assertIsInstance(version_info, dict, "版本信息应该是字典")
        self.assertIn('obsVersion', version_info, "版本信息应包含 OBS 版本")

        logger.info(f"OBS 版本信息: {version_info}")

    def test_get_all_scenes(self):
        """测试获取所有场景"""
        scenes = self.obs.scenes.get_all()
        self.assertIsInstance(scenes, list, "场景列表应该是列表")

        if scenes:
            # 检查场景数据结构
            scene = scenes[0]
            self.assertIsInstance(scene, dict, "场景应该是字典")
            self.assertIn('sceneName', scene, "场景应包含名称字段")

        logger.info(f"获取到 {len(scenes)} 个场景")

    def test_get_scene_names(self):
        """测试获取场景名称列表"""
        scene_names = self.obs.scenes.get_names()
        self.assertIsInstance(scene_names, list, "场景名称列表应该是列表")

        for name in scene_names:
            self.assertIsInstance(name, str, "场景名称应该是字符串")
            self.assertTrue(len(name) > 0, "场景名称不应为空")

        logger.info(f"场景名称: {scene_names}")

    def test_get_current_program_scene(self):
        """测试获取当前节目场景"""
        current_scene = self.obs.scenes.get_current_program()
        self.assertIsInstance(current_scene, str, "当前场景应该是字符串")

        if current_scene:
            # 验证当前场景在场景列表中
            scene_names = self.obs.scenes.get_names()
            self.assertIn(current_scene, scene_names, "当前场景应在场景列表中")

        logger.info(f"当前节目场景: {current_scene}")

    def test_scene_exists(self):
        """测试场景存在性检查"""
        scene_names = self.obs.scenes.get_names()

        if scene_names:
            # 测试存在的场景
            existing_scene = scene_names[0]
            self.assertTrue(self.obs.scenes.exists(existing_scene), f"场景 {existing_scene} 应该存在")

        # 测试不存在的场景
        non_existent_scene = "NonExistentScene_12345"
        self.assertFalse(self.obs.scenes.exists(non_existent_scene), f"场景 {non_existent_scene} 不应该存在")

    def test_create_and_delete_scene(self):
        """测试创建和删除场景"""
        test_scene_name = "TestScene_CreateDelete"

        # 确保测试场景不存在
        if self.obs.scenes.exists(test_scene_name):
            self.obs.scenes.delete(test_scene_name)

        # 测试创建场景
        result = self.obs.scenes.create(test_scene_name)
        self.assertTrue(result, "创建场景应该成功")
        self.assertTrue(self.obs.scenes.exists(test_scene_name), "创建的场景应该存在")

        # 验证场景在列表中
        scene_names = self.obs.scenes.get_names()
        self.assertIn(test_scene_name, scene_names, "创建的场景应在场景列表中")

        logger.info(f"成功创建场景: {test_scene_name}")

        # 测试重复创建（应该失败）
        result = self.obs.scenes.create(test_scene_name)
        self.assertFalse(result, "重复创建场景应该失败")

        # 测试删除场景
        result = self.obs.scenes.delete(test_scene_name)
        self.assertTrue(result, "删除场景应该成功")

        # 等待删除操作完成
        time.sleep(0.5)

        self.assertFalse(self.obs.scenes.exists(test_scene_name), "删除的场景不应该存在")

        logger.info(f"成功删除场景: {test_scene_name}")

    def test_delete_nonexistent_scene(self):
        """测试删除不存在的场景"""
        non_existent_scene = "NonExistentScene_Delete"

        # 确保场景不存在
        self.assertFalse(self.obs.scenes.exists(non_existent_scene))

        # 测试删除不存在的场景应该抛出异常
        with self.assertRaises(OBSResourceNotFoundError):
            self.obs.scenes.delete(non_existent_scene)

    def test_switch_scene(self):
        """测试场景切换"""
        scene_names = self.obs.scenes.get_names()

        if len(scene_names) < 2:
            # 创建测试场景
            test_scene = "TestScene_Switch"
            self.obs.scenes.create(test_scene)
            scene_names = self.obs.scenes.get_names()

        # 获取当前场景
        current_scene = self.obs.scenes.get_current_program()

        # 选择一个不同的场景进行切换
        target_scene = None
        for scene in scene_names:
            if scene != current_scene:
                target_scene = scene
                break

        if target_scene:
            # 测试切换场景
            result = self.obs.scenes.switch_to(target_scene)
            self.assertTrue(result, f"切换到场景 {target_scene} 应该成功")

            # 等待一小段时间让切换生效
            time.sleep(0.5)

            # 验证切换结果
            new_current_scene = self.obs.scenes.get_current_program()
            self.assertEqual(new_current_scene, target_scene, f"当前场景应该是 {target_scene}")

            logger.info(f"成功切换场景: {current_scene} -> {target_scene}")

            # 切换回原场景
            if current_scene:
                self.obs.scenes.switch_to(current_scene)
        else:
            self.skipTest("需要至少两个场景来测试场景切换")

    def test_switch_to_nonexistent_scene(self):
        """测试切换到不存在的场景"""
        non_existent_scene = "NonExistentScene_Switch"

        # 确保场景不存在
        self.assertFalse(self.obs.scenes.exists(non_existent_scene))

        # 测试切换到不存在的场景应该抛出异常
        with self.assertRaises(OBSResourceNotFoundError):
            self.obs.scenes.switch_to(non_existent_scene)

    def test_rename_scene(self):
        """测试重命名场景"""
        original_name = "TestScene_Rename_Original"
        new_name = "TestScene_Rename_New"

        # 清理可能存在的测试场景
        for name in [original_name, new_name]:
            if self.obs.scenes.exists(name):
                self.obs.scenes.delete(name)

        # 创建测试场景
        self.assertTrue(self.obs.scenes.create(original_name), "创建测试场景应该成功")

        # 测试重命名
        result = self.obs.scenes.rename(original_name, new_name)
        self.assertTrue(result, "重命名场景应该成功")

        # 验证重命名结果
        self.assertFalse(self.obs.scenes.exists(original_name), "原场景名不应该存在")
        self.assertTrue(self.obs.scenes.exists(new_name), "新场景名应该存在")

        logger.info(f"成功重命名场景: {original_name} -> {new_name}")

        # 清理测试场景
        self.obs.scenes.delete(new_name)

    def test_rename_nonexistent_scene(self):
        """测试重命名不存在的场景"""
        non_existent_scene = "NonExistentScene_Rename"
        new_name = "TestScene_NewName"

        # 确保场景不存在
        self.assertFalse(self.obs.scenes.exists(non_existent_scene))

        # 测试重命名不存在的场景应该抛出异常
        with self.assertRaises(OBSResourceNotFoundError):
            self.obs.scenes.rename(non_existent_scene, new_name)

    def test_studio_mode_operations(self):
        """测试 Studio Mode 相关操作"""
        # 保存初始状态
        initial_studio_mode = self.obs.scenes.is_studio_mode_enabled()

        try:
            # 测试启用 Studio Mode
            result = self.obs.scenes.enable_studio_mode(True)
            self.assertTrue(result, "启用 Studio Mode 应该成功")

            # 等待状态更新
            time.sleep(0.5)

            # 验证 Studio Mode 已启用
            self.assertTrue(self.obs.scenes.is_studio_mode_enabled(), "Studio Mode 应该已启用")

            logger.info("成功启用 Studio Mode")

            # 测试获取预览场景
            preview_scene = self.obs.scenes.get_current_preview()
            self.assertIsInstance(preview_scene, str, "预览场景应该是字符串")

            if preview_scene:
                logger.info(f"当前预览场景: {preview_scene}")

            # 测试设置预览场景
            scene_names = self.obs.scenes.get_names()
            current_program = self.obs.scenes.get_current_program()

            # 找一个不同的场景作为预览
            target_preview = None
            for scene in scene_names:
                if scene != current_program:
                    target_preview = scene
                    break

            if target_preview:
                result = self.obs.scenes.set_preview(target_preview)
                self.assertTrue(result, f"设置预览场景 {target_preview} 应该成功")

                # 等待状态更新
                time.sleep(0.5)

                # 验证预览场景设置
                new_preview = self.obs.scenes.get_current_preview()
                self.assertEqual(new_preview, target_preview, f"预览场景应该是 {target_preview}")

                logger.info(f"成功设置预览场景: {target_preview}")

                # 测试触发转场
                result = self.obs.scenes.trigger_transition()
                self.assertTrue(result, "触发转场应该成功")

                # 等待转场完成
                time.sleep(1.0)

                # 验证转场结果（预览场景应该变成节目场景）
                new_program = self.obs.scenes.get_current_program()
                self.assertEqual(new_program, target_preview, f"转场后节目场景应该是 {target_preview}")

                logger.info(f"成功触发转场: {target_preview} 现在是节目场景")

            # 测试禁用 Studio Mode
            result = self.obs.scenes.disable_studio_mode()
            self.assertTrue(result, "禁用 Studio Mode 应该成功")

            # 等待状态更新
            time.sleep(0.5)

            # 验证 Studio Mode 已禁用
            self.assertFalse(self.obs.scenes.is_studio_mode_enabled(), "Studio Mode 应该已禁用")

            logger.info("成功禁用 Studio Mode")

        finally:
            # 恢复初始状态
            if initial_studio_mode != self.obs.scenes.is_studio_mode_enabled():
                self.obs.scenes.enable_studio_mode(initial_studio_mode)
                time.sleep(0.5)

    def test_studio_mode_without_enable(self):
        """测试在未启用 Studio Mode 时的操作"""
        # 确保 Studio Mode 未启用
        if self.obs.scenes.is_studio_mode_enabled():
            self.obs.scenes.disable_studio_mode()
            time.sleep(0.5)

        # 测试在未启用 Studio Mode 时触发转场
        result = self.obs.scenes.trigger_transition()
        self.assertFalse(result, "在未启用 Studio Mode 时触发转场应该失败")

        # 测试获取预览场景（可能返回空字符串）
        preview_scene = self.obs.scenes.get_current_preview()
        self.assertIsInstance(preview_scene, str, "预览场景应该是字符串")

    def test_set_preview_nonexistent_scene(self):
        """测试设置不存在的预览场景"""
        # 启用 Studio Mode
        initial_studio_mode = self.obs.scenes.is_studio_mode_enabled()
        if not initial_studio_mode:
            self.obs.scenes.enable_studio_mode(True)
            time.sleep(0.5)

        try:
            non_existent_scene = "NonExistentScene_Preview"

            # 确保场景不存在
            self.assertFalse(self.obs.scenes.exists(non_existent_scene))

            # 测试设置不存在的预览场景应该抛出异常
            with self.assertRaises(OBSResourceNotFoundError):
                self.obs.scenes.set_preview(non_existent_scene)

        finally:
            # 恢复初始状态
            if not initial_studio_mode:
                self.obs.scenes.disable_studio_mode()
                time.sleep(0.5)

    def test_get_group_list(self):
        """测试获取组列表"""
        groups = self.obs.scenes.get_group_list()
        self.assertIsInstance(groups, list, "组列表应该是列表")

        for group in groups:
            self.assertIsInstance(group, str, "组名应该是字符串")

        logger.info(f"获取到 {len(groups)} 个组: {groups}")

    def test_get_scene_info(self):
        """测试获取场景信息摘要"""
        info = self.obs.scenes.get_info()
        self.assertIsInstance(info, dict, "场景信息应该是字典")

        # 检查必要的字段
        required_fields = ["current_program", "current_preview", "studio_mode", "total_scenes", "scene_names"]
        for field in required_fields:
            self.assertIn(field, info, f"场景信息应包含 {field} 字段")

        # 验证数据类型
        self.assertIsInstance(info["current_program"], str, "当前节目场景应该是字符串")
        self.assertIsInstance(info["current_preview"], str, "当前预览场景应该是字符串")
        self.assertIsInstance(info["studio_mode"], bool, "Studio Mode 状态应该是布尔值")
        self.assertIsInstance(info["total_scenes"], int, "场景总数应该是整数")
        self.assertIsInstance(info["scene_names"], list, "场景名称列表应该是列表")

        # 验证数据一致性
        self.assertEqual(info["total_scenes"], len(info["scene_names"]), "场景总数应该与场景名称列表长度一致")

        if info["current_program"]:
            self.assertIn(info["current_program"], info["scene_names"], "当前节目场景应在场景列表中")

        logger.info(f"场景信息摘要: {info}")

    def test_scene_transition_override(self):
        """测试场景转场覆盖设置"""
        test_scene_name = "TestScene_TransitionOverride"

        # 创建测试场景
        if not self.obs.scenes.exists(test_scene_name):
            self.assertTrue(self.obs.scenes.create(test_scene_name), "创建测试场景应该成功")

        try:
            # 测试获取转场覆盖设置（初始应该为空）
            override_info = self.obs.scenes.get_scene_transition_override(test_scene_name)
            self.assertIsInstance(override_info, dict, "转场覆盖信息应该是字典")

            logger.info(f"初始转场覆盖设置: {override_info}")

            # 测试设置转场覆盖
            test_duration = 1000  # 1秒
            result = self.obs.scenes.set_scene_transition_override(
                test_scene_name,
                transition_name=None,  # 使用默认转场
                transition_duration=test_duration
            )
            self.assertTrue(result, "设置转场覆盖应该成功")

            # 验证设置结果
            override_info = self.obs.scenes.get_scene_transition_override(test_scene_name)
            if 'transition_duration' in override_info and override_info['transition_duration'] is not None:
                self.assertEqual(override_info['transition_duration'], test_duration,
                               f"转场持续时间应该是 {test_duration}")

            logger.info(f"设置转场覆盖后: {override_info}")

            # 测试移除转场覆盖
            result = self.obs.scenes.set_scene_transition_override(
                test_scene_name,
                transition_name=None,
                transition_duration=None
            )
            self.assertTrue(result, "移除转场覆盖应该成功")

            logger.info("成功测试转场覆盖设置")

        finally:
            # 清理测试场景
            if self.obs.scenes.exists(test_scene_name):
                self.obs.scenes.delete(test_scene_name)

    def test_scene_transition_override_invalid_duration(self):
        """测试无效的转场持续时间"""
        test_scene_name = "TestScene_InvalidDuration"

        # 创建测试场景
        if not self.obs.scenes.exists(test_scene_name):
            self.assertTrue(self.obs.scenes.create(test_scene_name), "创建测试场景应该成功")

        try:
            # 测试过小的持续时间
            with self.assertRaises(ValueError):
                self.obs.scenes.set_scene_transition_override(test_scene_name, transition_duration=10)

            # 测试过大的持续时间
            with self.assertRaises(ValueError):
                self.obs.scenes.set_scene_transition_override(test_scene_name, transition_duration=25000)

            logger.info("成功测试无效转场持续时间的验证")

        finally:
            # 清理测试场景
            if self.obs.scenes.exists(test_scene_name):
                self.obs.scenes.delete(test_scene_name)

    def test_scene_transition_override_nonexistent_scene(self):
        """测试对不存在场景的转场覆盖操作"""
        non_existent_scene = "NonExistentScene_TransitionOverride"

        # 确保场景不存在
        self.assertFalse(self.obs.scenes.exists(non_existent_scene))

        # 测试获取不存在场景的转场覆盖设置
        with self.assertRaises(OBSResourceNotFoundError):
            self.obs.scenes.get_scene_transition_override(non_existent_scene)

        # 测试设置不存在场景的转场覆盖
        with self.assertRaises(OBSResourceNotFoundError):
            self.obs.scenes.set_scene_transition_override(non_existent_scene, transition_duration=1000)

    def test_multiple_scene_operations(self):
        """测试多个场景的批量操作"""
        test_scenes = ["TestScene_Multi_1", "TestScene_Multi_2", "TestScene_Multi_3"]

        try:
            # 批量创建场景
            for scene_name in test_scenes:
                if self.obs.scenes.exists(scene_name):
                    self.obs.scenes.delete(scene_name)

                result = self.obs.scenes.create(scene_name)
                self.assertTrue(result, f"创建场景 {scene_name} 应该成功")
                self.assertTrue(self.obs.scenes.exists(scene_name), f"场景 {scene_name} 应该存在")

            logger.info(f"成功创建 {len(test_scenes)} 个测试场景")

            # 测试在多个场景间切换
            original_scene = self.obs.scenes.get_current_program()

            for scene_name in test_scenes:
                result = self.obs.scenes.switch_to(scene_name)
                self.assertTrue(result, f"切换到场景 {scene_name} 应该成功")

                time.sleep(0.3)  # 短暂等待

                current_scene = self.obs.scenes.get_current_program()
                self.assertEqual(current_scene, scene_name, f"当前场景应该是 {scene_name}")

            logger.info("成功测试多场景切换")

            # 恢复原始场景
            if original_scene and self.obs.scenes.exists(original_scene):
                self.obs.scenes.switch_to(original_scene)

        finally:
            # 清理测试场景
            for scene_name in test_scenes:
                if self.obs.scenes.exists(scene_name):
                    self.obs.scenes.delete(scene_name)

    def test_scene_name_edge_cases(self):
        """测试场景名称的边界情况"""
        edge_case_names = [
            "TestScene_空格 测试",
            "TestScene_特殊字符!@#$%",
            "TestScene_数字123",
            "TestScene_很长的场景名称_" + "x" * 50,
        ]

        created_scenes = []

        try:
            for scene_name in edge_case_names:
                # 清理可能存在的场景
                if self.obs.scenes.exists(scene_name):
                    self.obs.scenes.delete(scene_name)

                # 尝试创建场景
                result = self.obs.scenes.create(scene_name)
                if result:
                    created_scenes.append(scene_name)
                    self.assertTrue(self.obs.scenes.exists(scene_name), f"场景 {scene_name} 应该存在")
                    logger.info(f"成功创建边界情况场景: {scene_name}")
                else:
                    logger.warning(f"创建场景失败: {scene_name}")

        finally:
            # 清理创建的场景
            for scene_name in created_scenes:
                if self.obs.scenes.exists(scene_name):
                    self.obs.scenes.delete(scene_name)

    def test_concurrent_operations(self):
        """测试并发操作的稳定性"""
        test_scene_name = "TestScene_Concurrent"

        # 创建测试场景
        if not self.obs.scenes.exists(test_scene_name):
            self.assertTrue(self.obs.scenes.create(test_scene_name), "创建测试场景应该成功")

        try:
            # 快速连续执行多个操作
            operations_count = 5

            for i in range(operations_count):
                # 获取场景信息
                info = self.obs.scenes.get_info()
                self.assertIsInstance(info, dict, f"第 {i+1} 次获取场景信息应该成功")

                # 检查场景存在性
                exists = self.obs.scenes.exists(test_scene_name)
                self.assertTrue(exists, f"第 {i+1} 次检查场景存在性应该成功")

                # 获取场景列表
                scenes = self.obs.scenes.get_names()
                self.assertIsInstance(scenes, list, f"第 {i+1} 次获取场景列表应该成功")
                self.assertIn(test_scene_name, scenes, f"测试场景应该在第 {i+1} 次获取的列表中")

                # 短暂等待
                time.sleep(0.1)

            logger.info(f"成功完成 {operations_count} 次并发操作测试")

        finally:
            # 清理测试场景
            if self.obs.scenes.exists(test_scene_name):
                self.obs.scenes.delete(test_scene_name)


if __name__ == '__main__':
    # 配置更详细的日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 运行测试
    unittest.main(verbosity=2)