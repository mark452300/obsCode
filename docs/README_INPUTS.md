# 输入管理测试说明

本目录包含了 OBS SDK 输入管理功能的完整测试套件。

## 测试文件说明

### 1. `test_inputs.py`
功能演示测试，展示输入管理的各种功能：
- 获取输入源列表
- 检查输入源存在性
- 静音/取消静音操作
- 切换静音状态
- 获取和设置输入源设置
- 错误处理测试

**特点：**
- 需要实际的 OBS 连接
- 会实际操作 OBS 输入源
- 包含详细的操作说明和结果展示

### 2. `test_inputs_unittest.py`
标准单元测试，使用 unittest 框架：
- 使用模拟对象，不需要实际 OBS 连接
- 测试所有公共方法的正常和异常情况
- 包含集成测试（可选，需要环境变量）

**特点：**
- 快速执行，不依赖外部服务
- 全面的边界条件测试
- 标准的测试报告格式

### 3. `run_input_tests.py`
测试运行器，提供多种运行选项：
- `--unit`: 运行单元测试
- `--integration`: 运行集成测试
- `--demo`: 运行功能演示测试
- `--all`: 运行所有测试

## 运行测试

### 前置条件

1. **安装依赖：**
   ```bash
   pip install obs-websocket-py
   ```

2. **OBS 设置（仅集成测试和演示测试需要）：**
   - OBS Studio 正在运行
   - obs-websocket 插件已启用
   - WebSocket 端口设置正确（默认 4455）
   - 配置正确的密码（如果有）

### 运行方式

#### 1. 运行单元测试（推荐开始）
```bash
# 使用测试运行器
python tests/run_input_tests.py --unit

# 或直接运行
python -m unittest tests.test_inputs_unittest -v
```

#### 2. 运行功能演示测试
```bash
# 使用测试运行器
python tests/run_input_tests.py --demo

# 或直接运行
python tests/test_inputs.py
```

#### 3. 运行集成测试
```bash
# 使用测试运行器
python tests/run_input_tests.py --integration

# 或设置环境变量后运行
set OBS_INTEGRATION_TEST=1
python -m unittest tests.test_inputs_unittest.TestInputManagerIntegration -v
```

#### 4. 运行所有测试
```bash
python tests/run_input_tests.py --all
```

#### 5. 使用主测试运行器
```bash
python tests/run_tests.py
```

## 测试覆盖的功能

### 输入源管理
- ✅ 获取所有输入源 (`get_all()`)
- ✅ 获取输入源名称列表 (`get_names()`)
- ✅ 获取音频输入源 (`get_audio_inputs()`)
- ✅ 获取输入类型列表 (`get_input_kinds()`)
- ✅ 检查输入源存在性 (`exists()`)

### 静音控制
- ✅ 检查静音状态 (`is_muted()`)
- ✅ 静音输入源 (`mute()`)
- ✅ 取消静音 (`unmute()`)
- ✅ 切换静音状态 (`toggle_mute()`)

### 设置管理
- ✅ 获取输入源设置 (`get_settings()`)
- ✅ 设置输入源设置 (`set_settings()`)

### 信息获取
- ✅ 获取输入源信息摘要 (`get_info()`)

### 错误处理
- ✅ 不存在的输入源异常处理
- ✅ 连接错误处理
- ✅ 请求失败处理

## 注意事项

1. **单元测试 vs 集成测试：**
   - 单元测试使用模拟对象，执行快速，不需要 OBS
   - 集成测试需要实际的 OBS 连接，测试真实功能

2. **演示测试的影响：**
   - 演示测试会实际操作 OBS 输入源
   - 可能会临时改变输入源的静音状态
   - 测试结束后会尝试恢复原始状态

3. **配置要求：**
   - 确保 `obs_sdk/config.py` 中的连接配置正确
   - 如果 OBS 设置了 WebSocket 密码，需要在配置中指定

4. **故障排除：**
   - 如果连接失败，检查 OBS 是否运行且 WebSocket 插件已启用
   - 如果测试超时，检查防火墙设置
   - 如果找不到输入源，确保 OBS 中至少有一个输入源

## 扩展测试

如果需要添加新的测试用例：

1. **单元测试：** 在 `test_inputs_unittest.py` 中添加新的测试方法
2. **功能测试：** 在 `test_inputs.py` 中添加新的测试函数
3. **运行器：** 如果需要新的运行选项，修改 `run_input_tests.py`

测试方法命名规范：
- 单元测试：`test_<功能>_<场景>()`
- 功能测试：`test_<功能描述>()`
