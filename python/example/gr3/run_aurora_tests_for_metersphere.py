#!/usr/bin/env python3
"""
Aurora SDK 测试脚本 - 专为 MeterSphere 集成设计
"""
import time
import sys
import os
import json
import subprocess
from fourier_aurora_client import AuroraClient

def run_pytest_and_generate_report():
    """运行 pytest 并生成报告"""
    # 运行 pytest 生成 JUnit XML 报告（MeterSphere 支持）
    result = subprocess.run([
        'pytest', 
        'test_Aurora_sdk_api.py',
        '--junitxml=test-results.xml',
        '-v'
    ], capture_output=True, text=True)
    
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    return result.returncode

def manual_test_cases():
    """手动测试用例，用于直接集成到 MeterSphere"""
    test_results = []
    
    try:
        # 测试用例 1: 客户端初始化
        client = AuroraClient.get_instance(domain_id=123, robot_name="gr3", serial_number=None)
        time.sleep(1)
        
        if client is not None:
            test_results.append({
                "name": "客户端初始化测试",
                "status": "PASS",
                "message": "Aurora Client 初始化成功"
            })
        else:
            test_results.append({
                "name": "客户端初始化测试", 
                "status": "FAIL",
                "message": "Aurora Client 初始化失败"
            })
            return test_results
        
        # 测试用例 2: 获取初始状态
        initial_state = client.get_fsm_state()
        test_results.append({
            "name": "获取初始状态测试",
            "status": "PASS" if initial_state is not None else "FAIL",
            "message": f"初始状态: {initial_state}" if initial_state else "无法获取初始状态"
        })
        
        # 测试用例 3: 状态切换测试
        client.set_fsm_state(1)
        time.sleep(1.0)
        new_state = client.get_fsm_state()
        
        expected_states = ['JointStand', 'PdStand']
        if new_state in expected_states:
            test_results.append({
                "name": "状态切换测试",
                "status": "PASS", 
                "message": f"状态切换成功: {new_state}"
            })
        else:
            test_results.append({
                "name": "状态切换测试",
                "status": "FAIL",
                "message": f"状态切换失败，期望 {expected_states}，实际: {new_state}"
            })
            
    except Exception as e:
        test_results.append({
            "name": "测试执行",
            "status": "ERROR",
            "message": f"测试执行异常: {str(e)}"
        })
    
    return test_results

if __name__ == "__main__":
    print("开始执行 Aurora SDK 测试...")
    
    # 方式1: 使用 pytest（推荐）
    # exit_code = run_pytest_and_generate_report()
    # sys.exit(exit_code)
    
    # 方式2: 手动测试用例（适合 MeterSphere 直接调用）
    results = manual_test_cases()
    
    # 输出结果给 MeterSphere
    print("\n=== 测试结果汇总 ===")
    for result in results:
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"{status_icon} {result['name']}: {result['status']} - {result['message']}")
    
    # 统计结果
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] in ["FAIL", "ERROR"])
    
    print(f"\n测试统计: 通过 {passed}, 失败 {failed}, 总计 {len(results)}")
    
    # 如果有失败用例，返回非零退出码
    sys.exit(1 if failed > 0 else 0)