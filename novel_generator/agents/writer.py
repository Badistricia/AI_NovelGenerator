# novel_generator/agents/writer.py
from .base import BaseAgent
from novel_generator.common import invoke_with_cleaning
import logging

class WriterAgent(BaseAgent):
    """
    负责草稿创作的主笔 Agent
    """
    def invoke(self, base_prompt: str, feedback: str = None) -> str:
        if feedback:
            # 引入反馈闭环，强制重写违规部分
            prompt = (
                f"{base_prompt}\n\n"
                f"【拦截器判官反馈意见】\n"
                f"因为您之前的草稿存在严重的 OOC 与规则违背，请根据以下审校意见重写本章：\n"
                f"{feedback}\n\n"
                f"要求：\n"
                f"1. 请极其严格地遵守上述拦截器意见。\n"
                f"2. 仅仅修正违规及降智的内容，保持其他优秀的设定和环境描写逻辑一致。\n"
                f"3. 请直接输出修改后的完整草稿正文！"
            )
            logging.info("WriterAgent: Received feedback, rewriting draft...")
        else:
            prompt = base_prompt
            logging.info("WriterAgent: Generating initial draft...")
            
        return invoke_with_cleaning(self.llm_adapter, prompt)
