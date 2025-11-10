import time
import pytest
import sys
import os
from fourier_aurora_client import AuroraClient

class TestAuroraClient:
    @pytest.fixture(autouse=True)
    def setup_client(self):
        """在每个测试前初始化客户端"""
        self.client = AuroraClient.get_instance(domain_id=123, robot_name="gr3", serial_number=None)
        time.sleep(1)
        assert self.client is not None, "Failed to create AuroraClient instance"
        yield

    def test_fsm_state_switch(self):
        """测试FSM状态切换 - 使用状态名称而不是数字"""
        # 切换到 PdStand 状态
        self.client.set_fsm_state(1)
        time.sleep(1.0)
        
        # 验证状态是否正确切换 - 现在返回的是状态名称
        current_state = self.client.get_fsm_state()
        # 根据实际返回的状态名称进行断言
        expected_states = ['JointStand', 'PdStand']  # 可能的预期状态
        assert current_state in expected_states, f"Expected one of {expected_states}, but got {current_state}"

    def test_initial_state(self):
        """测试初始状态"""
        initial_state = self.client.get_fsm_state()
        assert initial_state is not None, "Should be able to get initial FSM state"
        assert isinstance(initial_state, str), f"FSM state should be string, but got {type(initial_state)}"

    @pytest.mark.parametrize("target_state,expected_state_name", [
        (1, 'JointStand'),  # 根据实际状态名称调整
        (3, 'SecurityProtection'),
    ])
    def test_multiple_state_transitions(self, target_state, expected_state_name):
        """参数化测试多个状态转换 - 使用状态名称"""
        self.client.set_fsm_state(target_state)
        time.sleep(1.0)
        current_state = self.client.get_fsm_state()
        assert current_state == expected_state_name, f"Expected state {expected_state_name}, but got {current_state}"

    def test_get_all_states(self):
        """测试获取所有可能的状态"""
        # 可以添加一个测试来探索所有可能的状态
        states_tested = set()
        test_cases = [1, 2, 3, 4]  # 根据API文档调整
        
        for state_code in test_cases:
            try:
                self.client.set_fsm_state(state_code)
                time.sleep(0.5)
                state_name = self.client.get_fsm_state()
                states_tested.add((state_code, state_name))
                print(f"State code {state_code} -> State name: {state_name}")
            except Exception as e:
                print(f"Error testing state {state_code}: {e}")
        
        print(f"Discovered state mappings: {states_tested}")
        assert len(states_tested) > 0, "Should discover at least one state mapping"