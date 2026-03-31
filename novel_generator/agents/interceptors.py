# novel_generator/agents/interceptors.py
import re

class HookInterceptor:
    """
    拦截器引擎：负责解析并拦截违背用户核心设定的生成内容
    """
    def __init__(self, user_guidance: str):
        self.user_guidance = user_guidance
        self.rules = self._parse_rules(user_guidance)
        
    def _parse_rules(self, text: str) -> list:
        # 从用户指导中提取包含“禁止”、“严禁”、“必须”、“强制”等字眼的句子作为硬性规则
        rules = []
        if not text:
            return rules
        for line in text.split('\n'):
            line = line.strip()
            if any(keyword in line for keyword in ['禁止', '严禁', '必须', '强制']):
                rules.append(line)
        return rules
        
    def get_rules(self) -> list:
        """回传当前启用的拦截规则"""
        return self.rules
