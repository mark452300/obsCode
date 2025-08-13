#!/usr/bin/env python3
"""
简单的删除输入源测试
"""

import sys
import os
import time

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from obs_sdk import OBSManager


def main():
    """简单测试删除功能"""
    print("🧪 简单删除测试")
    print("=" * 40)
    
    try:
        with OBSManager() as obs:
            # 获取场景
            scenes = obs.scenes.get_names()
            if not scenes:
                print("❌ 没有可用的场景")
                return False
            
            test_scene = scenes[0]
            test_name = f"删除测试_{int(time.time())}"
            
            print(f"1. 创建输入源: {test_name}")
            
            # 创建输入源
            result = obs.inputs.create_input(
                input_name=test_name,
                input_kind="text_gdiplus_v3",
                scene_name=test_scene,
                input_settings={"text": "测试删除"}
            )
            
            if not result.get('success'):
                print("❌ 创建失败")
                return False
            
            print(f"✅ 创建成功: {result['input_uuid']}")
            
            # 检查输入源列表
            print(f"\n2. 检查输入源是否存在")
            all_inputs_before = obs.inputs.get_names()
            print(f"删除前输入源数量: {len(all_inputs_before)}")
            
            if test_name in all_inputs_before:
                print(f"✅ 输入源存在于列表中")
            else:
                print(f"❌ 输入源不在列表中")
                return False
            
            # 删除输入源
            print(f"\n3. 删除输入源: {test_name}")
            try:
                success = obs.inputs.remove_input(input_name=test_name)
                print(f"删除操作返回: {success}")
            except Exception as e:
                print(f"❌ 删除时出错: {e}")
                return False
            
            # 等待一下让删除生效
            time.sleep(0.5)
            
            # 再次检查输入源列表
            print(f"\n4. 验证删除结果")
            all_inputs_after = obs.inputs.get_names()
            print(f"删除后输入源数量: {len(all_inputs_after)}")
            
            if test_name not in all_inputs_after:
                print(f"✅ 输入源已从列表中移除")
                print(f"✅ 删除测试成功")
                return True
            else:
                print(f"❌ 输入源仍在列表中")
                print(f"删除前: {all_inputs_before}")
                print(f"删除后: {all_inputs_after}")
                return False
                
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 测试通过！")
    else:
        print("\n💥 测试失败！")
    sys.exit(0 if success else 1)
