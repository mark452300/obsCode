# remove_input 方法文档

## 📋 **概述**

`remove_input` 方法用于删除 OBS 中的输入源，基于 OBS WebSocket API 的 `RemoveInput` 请求实现。

## 🔧 **方法签名**

```python
def remove_input(self, input_name: str = None, input_uuid: str = None) -> bool:
```

## 📝 **参数说明**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `input_name` | `str` | 可选 | 要删除的输入源名称 |
| `input_uuid` | `str` | 可选 | 要删除的输入源 UUID |

**注意**：`input_name` 和 `input_uuid` 必须提供其中一个，但不能同时提供。

## 🎯 **返回值**

- **类型**：`bool`
- **说明**：删除操作是否成功
- **`True`**：删除成功
- **`False`**：删除失败（通常不会发生，失败时会抛出异常）

## ⚠️ **重要注意事项**

1. **级联删除**：删除输入源会自动删除所有使用该输入源的场景项目
2. **不可恢复**：删除操作是不可逆的
3. **参数互斥**：只能提供 `input_name` 或 `input_uuid` 中的一个
4. **静默处理**：删除不存在的输入源不会抛出异常，而是返回 `True`

## 🚨 **异常情况**

| 异常类型 | 触发条件 | 说明 |
|----------|----------|------|
| `ValueError` | 参数验证失败 | 未提供参数或同时提供两个参数 |
| `OBSResourceNotFoundError` | 输入源不存在 | 某些情况下可能抛出 |
| `Exception` | OBS 连接或其他错误 | 网络问题或 OBS 内部错误 |

## 💡 **使用示例**

### 基本使用

```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 使用输入源名称删除
    success = obs.inputs.remove_input(input_name="我的文本源")
    if success:
        print("删除成功")
    
    # 使用输入源 UUID 删除
    success = obs.inputs.remove_input(input_uuid="12345678-1234-1234-1234-123456789abc")
    if success:
        print("删除成功")
```

### 错误处理

```python
try:
    # 删除输入源
    obs.inputs.remove_input(input_name="测试输入源")
    print("删除成功")
    
except ValueError as e:
    print(f"参数错误: {e}")
    
except OBSResourceNotFoundError as e:
    print(f"输入源不存在: {e}")
    
except Exception as e:
    print(f"删除失败: {e}")
```

### 安全删除（检查存在性）

```python
input_name = "要删除的输入源"

# 先检查输入源是否存在
if obs.inputs.exists(input_name):
    success = obs.inputs.remove_input(input_name=input_name)
    if success:
        print(f"成功删除输入源: {input_name}")
else:
    print(f"输入源不存在: {input_name}")
```

### 批量删除

```python
# 删除多个输入源
input_names_to_delete = ["文本1", "文本2", "图像1"]

for name in input_names_to_delete:
    try:
        if obs.inputs.exists(name):
            obs.inputs.remove_input(input_name=name)
            print(f"✅ 删除: {name}")
        else:
            print(f"⚠️ 不存在: {name}")
    except Exception as e:
        print(f"❌ 删除失败 {name}: {e}")
```

## 🧪 **测试覆盖**

我们为 `remove_input` 方法创建了全面的测试：

### 测试用例

1. **基本删除功能**
   - 创建输入源
   - 删除输入源
   - 验证删除结果

2. **使用 UUID 删除**
   - 通过 UUID 删除输入源
   - 验证删除成功

3. **错误处理**
   - 删除不存在的输入源
   - 参数验证错误
   - 异常情况处理

4. **集成测试**
   - 与其他方法的协同工作
   - 批量操作测试
   - 计数验证

### 运行测试

```bash
# 运行专门的删除测试
py -3.11 tests/test_remove_input.py

# 运行简单测试
py -3.11 tests/test_remove_simple.py

# 运行完整的输入管理器测试
py -3.11 tests/test_inputs.py
```

## 🔄 **与其他方法的配合**

### 创建和删除的完整生命周期

```python
with OBSManager() as obs:
    # 1. 创建输入源
    result = obs.inputs.create_input(
        input_name="临时文本",
        input_kind="text_gdiplus_v3",
        scene_name="主场景",
        input_settings={"text": "临时内容"}
    )
    
    if result['success']:
        print(f"创建成功: {result['input_uuid']}")
        
        # 2. 使用输入源...
        # (进行一些操作)
        
        # 3. 删除输入源
        obs.inputs.remove_input(input_name="临时文本")
        print("清理完成")
```

### 输入源管理

```python
def cleanup_test_inputs(obs):
    """清理所有测试输入源"""
    all_inputs = obs.inputs.get_names()
    
    for name in all_inputs:
        if name.startswith("测试_") or name.startswith("Test_"):
            try:
                obs.inputs.remove_input(input_name=name)
                print(f"清理: {name}")
            except Exception as e:
                print(f"清理失败 {name}: {e}")
```

## 📊 **性能考虑**

1. **删除延迟**：删除操作可能需要短暂时间生效，建议在删除后等待 0.5 秒再进行验证
2. **批量操作**：大量删除时建议在每次删除间添加小延迟
3. **错误恢复**：删除操作不可逆，建议在重要操作前备份配置

## 🎯 **最佳实践**

1. **总是进行错误处理**
2. **删除前检查输入源是否存在**
3. **重要输入源删除前进行确认**
4. **批量删除时添加适当延迟**
5. **记录删除操作以便调试**

这个 `remove_input` 方法完善了输入源的生命周期管理，与现有的 `create_input` 方法形成了完整的 CRUD 操作集合。
