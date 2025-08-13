# OBS SDK 数据保存指南

本指南说明如何保存 OBS 输入类型数据，以及不同格式的选择建议。

## 🎯 推荐方案：JSON 格式

对于 Python 项目，**强烈推荐使用 JSON 格式**，原因如下：

### ✅ JSON 格式优势
- **Python 原生支持** - 无需额外依赖
- **数据结构完整** - 支持嵌套对象和数组
- **跨平台兼容** - 标准格式，易于集成
- **可读性好** - 结构清晰，便于调试
- **API 友好** - Web API 标准格式

## 🚀 快速使用

### 基本用法
```python
from obs_sdk import OBSManager

# 保存到默认位置（download/input_kinds.json）
with OBSManager() as obs:
    saved_file = obs.save_input_kinds()
    print(f"数据已保存到: {saved_file}")
```

### 自定义保存路径
```python
# 保存到 download 目录的子文件夹
with OBSManager() as obs:
    saved_file = obs.save_input_kinds("download/config/obs_config.json")
    print(f"数据已保存到: {saved_file}")
```

## 📊 保存的数据结构

生成的 JSON 文件包含以下信息：

```json
{
  "metadata": {
    "timestamp": "2025-08-12T18:58:00.143393",
    "total_kinds": 14,
    "current_inputs_count": 3
  },
  "input_kinds": {
    "versioned": ["color_source_v3", "text_gdiplus_v3", ...],
    "unversioned": ["color_source", "text_gdiplus", ...],
    "by_category": {
      "audio": ["wasapi_input_capture", ...],
      "video_media": ["image_source", "ffmpeg_source", ...],
      "capture": ["monitor_capture", "window_capture", ...],
      "other": ["slideshow_v2", "dshow_input", ...]
    }
  },
  "current_inputs": ["桌面音频", "麦克风/Aux", "媒体源"],
  "statistics": {
    "audio_types_count": 3,
    "video_types_count": 6,
    "capture_types_count": 3,
    "other_types_count": 2
  }
}
```

## 🎯 实际使用场景

### 1. 配置备份
```python
# 定期备份输入类型配置
with OBSManager() as obs:
    version = obs.get_version().get('obsVersion', 'unknown')
    backup_file = f"download/backup/input_kinds_{version}.json"
    obs.save_input_kinds(backup_file)
```

### 2. 系统兼容性检查
```python
# 生成兼容性报告
with OBSManager() as obs:
    obs.save_input_kinds("download/reports/system_compatibility.json")
```

### 3. 开发环境配置
```python
# 保存开发环境配置
with OBSManager() as obs:
    obs.save_input_kinds("download/dev/dev_input_types.json")
```

### 4. 数据分析
```python
import json

# 加载并分析数据
with open("download/input_kinds.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# 分析音频类型
audio_types = data['input_kinds']['by_category']['audio']
print(f"支持的音频类型: {len(audio_types)} 种")
```

## 📋 其他格式对比

| 格式 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| **JSON** | Python原生支持，结构完整 | 文件稍大 | **API，配置，通用（推荐）** |
| CSV | Excel兼容，简单直观 | 结构限制 | 数据分析，报表 |
| YAML | 人类可读，配置友好 | 需要依赖 | 配置文件，文档 |
| XML | 标准格式，验证支持 | 冗余较多 | 企业集成，标准 |

## 🔧 高级用法

### 直接使用 InputManager
```python
from obs_sdk import OBSManager

with OBSManager() as obs:
    # 直接调用 InputManager 方法
    saved_file = obs.inputs.save_input_kinds_to_json("custom/path.json")
```

### 批量保存
```python
import os
from datetime import datetime

with OBSManager() as obs:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 保存多个副本到 download 目录
    obs.save_input_kinds(f"download/daily/input_kinds_{timestamp}.json")
    obs.save_input_kinds("download/latest/input_kinds_latest.json")
    obs.save_input_kinds("download/archive/input_kinds_archive.json")
```

## 📖 数据读取示例

```python
import json

def load_input_kinds_data(filepath: str):
    """加载输入类型数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_input_types(data):
    """分析输入类型数据"""
    stats = data['statistics']
    
    print("📊 输入类型统计:")
    print(f"  音频类型: {stats['audio_types_count']} 种")
    print(f"  视频类型: {stats['video_types_count']} 种")
    print(f"  捕获类型: {stats['capture_types_count']} 种")
    print(f"  其他类型: {stats['other_types_count']} 种")
    
    return stats

# 使用示例
data = load_input_kinds_data("download/input_kinds.json")
analyze_input_types(data)
```

## 🛠️ 错误处理

```python
try:
    with OBSManager() as obs:
        saved_file = obs.save_input_kinds("download/input_kinds.json")
        print(f"✅ 保存成功: {saved_file}")
except Exception as e:
    print(f"❌ 保存失败: {e}")
```

## 📁 推荐目录结构

```
your_project/
├── download/                # 下载和数据文件目录
│   ├── input_kinds.json     # 默认保存文件
│   ├── backup/              # 备份文件
│   │   └── input_kinds_31.1.2.json
│   ├── config/              # 配置文件
│   │   └── dev_input_types.json
│   ├── daily/               # 按日期保存
│   │   └── 20250812_input_kinds.json
│   ├── versions/            # 按版本保存
│   │   └── obs_31_1_2.json
│   └── reports/             # 报告文件
│       └── system_compatibility.json
```

## 🎉 总结

- **推荐格式**: JSON（Python 项目首选）
- **保存方法**: `obs.save_input_kinds(filepath)` (默认: download/input_kinds.json)
- **数据结构**: 完整的元数据、分类信息、统计数据
- **使用场景**: 配置备份、兼容性检查、数据分析
- **优势**: 原生支持、结构完整、易于集成

**开始使用**: `py -3.11 examples/save_input_data_example.py` 🚀
