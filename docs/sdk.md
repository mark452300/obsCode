# OBS SDK 测试指南

本目录包含 OBS SDK 的测试用例，特别是 `scenes.py` 模块的完整测试套件。

## 测试文件说明

### `test_scenes.py`
场景管理器 (`SceneManager`) 的完整测试套件，包含以下测试类别：

#### 基础功能测试
- **连接状态测试**: 验证与 OBS 的连接和版本信息
- **场景列表操作**: 测试获取所有场景、场景名称列表等
- **当前场景获取**: 测试获取当前节目场景
- **场景存在性检查**: 验证场景是否存在的检查功能

#### 场景管理测试
- **创建和删除场景**: 测试场景的创建、删除操作
- **场景切换**: 测试场景之间的切换功能
- **场景重命名**: 测试场景重命名功能
- **错误处理**: 测试对不存在场景的操作异常处理

#### Studio Mode 测试
- **Studio Mode 启用/禁用**: 测试 Studio Mode 的开关
- **预览场景设置**: 测试预览场景的设置和获取
- **转场触发**: 测试 Studio Mode 下的转场功能
- **状态验证**: 验证 Studio Mode 各种状态的正确性

#### 转场覆盖测试
- **转场覆盖设置**: 测试场景转场覆盖的设置和获取
- **参数验证**: 测试转场持续时间的有效性验证
- **错误处理**: 测试对不存在场景的转场覆盖操作

#### 高级功能测试
- **批量操作**: 测试多个场景的批量创建和切换
- **边界情况**: 测试特殊字符、长名称等边界情况
- **并发操作**: 测试快速连续操作的稳定性
- **信息摘要**: 测试场景信息摘要功能

## 运行测试

### 前置条件

1. **OBS Studio 运行中**
   ```
   确保 OBS Studio 正在运行
   ```

2. **启用 WebSocket 服务器**
   ```
   OBS Studio -> 工具 -> WebSocket 服务器设置
   勾选"启用 WebSocket 服务器"
   设置端口（默认 4455）和密码
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

### 运行方式

#### 方式一：使用测试运行脚本（推荐）

```bash
# 运行所有测试
python run_scene_tests.py

# 详细输出
python run_scene_tests.py -v

# 仅检查连接配置
python run_scene_tests.py -c

# 运行特定测试方法
python run_scene_tests.py -t test_create_and_delete_scene
```

#### 方式二：直接使用 unittest

```bash
# 运行所有场景测试
python -m unittest tests.test_scenes -v

# 运行特定测试类
python -m unittest tests.test_scenes.TestSceneManager -v

# 运行特定测试方法
python -m unittest tests.test_scenes.TestSceneManager.test_create_and_delete_scene -v
```

#### 方式三：直接运行测试文件

```bash
cd tests
python test_scenes.py
```

### 配置说明

测试使用的默认配置：
- **主机**: 127.0.0.1
- **端口**: 4455  
- **密码**: el8peI520f03ZEVK

如需修改配置，可以：

1. **修改环境变量**:
   ```bash
   export OBS_HOST=192.168.1.100
   export OBS_PORT=4455
   export OBS_PASSWORD=your_password
   ```

2. **修改配置文件**: 编辑 `obs_sdk/config.py` 中的默认值

## 测试结果说明

### 成功输出示例
```
test_connection_status (__main__.TestSceneManager) ... ok
test_create_and_delete_scene (__main__.TestSceneManager) ... ok
test_get_all_scenes (__main__.TestSceneManager) ... ok
...

Ran 15 tests in 12.345s

OK
```

### 常见问题

#### 连接失败
```
OBSConnectionError: 无法连接到 OBS
```
**解决方案**:
- 确认 OBS Studio 正在运行
- 检查 WebSocket 服务器是否启用
- 验证连接参数（host, port, password）

#### 场景不存在错误
```
OBSResourceNotFoundError: 场景 'TestScene' 未找到
```
**解决方案**:
- 这通常是正常的测试行为，测试会自动清理
- 如果持续出现，检查 OBS 中是否有残留的测试场景

#### 权限错误
```
Permission denied
```
**解决方案**:
- 确认 OBS WebSocket 密码正确
- 检查防火墙设置

## 测试最佳实践

1. **运行前准备**
   - 关闭其他可能影响 OBS 的程序
   - 确保 OBS 处于稳定状态
   - 备份重要的 OBS 配置

2. **测试环境**
   - 使用专门的测试 OBS 配置文件
   - 避免在生产环境中运行测试

3. **故障排除**
   - 使用 `-v` 参数获取详细日志
   - 检查 OBS 日志文件
   - 逐个运行测试方法定位问题

## 扩展测试

如需添加新的测试用例：

1. 在 `TestSceneManager` 类中添加新的测试方法
2. 方法名以 `test_` 开头
3. 使用 `self.assert*` 方法进行断言
4. 在 `setUp` 和 `tearDown` 中处理测试数据
5. 添加适当的日志和注释

示例：
```python
def test_new_feature(self):
    """测试新功能"""
    # 准备测试数据
    test_scene = "TestScene_NewFeature"
    
    # 执行操作
    result = self.obs.scenes.new_feature(test_scene)
    
    # 验证结果
    self.assertTrue(result, "新功能应该成功")
    
    # 清理
    if self.obs.scenes.exists(test_scene):
        self.obs.scenes.delete(test_scene)
```
