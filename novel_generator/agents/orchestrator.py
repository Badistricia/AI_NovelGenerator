# novel_generator/agents/orchestrator.py
import logging
from .writer import WriterAgent
from .reviewer import ReviewerAgent
from .interceptors import HookInterceptor

class ChapterOrchestrator:
    """
    多智能体工作流调度中心：负责衔接 Writer 与 Reviewer，处理重试与反馈闭环。
    """
    def __init__(self, llm_adapter, user_guidance: str):
        self.writer = WriterAgent(llm_adapter)
        self.reviewer = ReviewerAgent(llm_adapter, HookInterceptor(user_guidance))
        self.max_retries = 3 # 草稿如果不通过，最多重试3次
        
    def generate(self, base_prompt: str, chapter_title: str) -> str:
        feedback = None
        draft = ""
        
        for attempt in range(1, self.max_retries + 1):
            if attempt > 1:
                logging.info(f"== Orchestrator: Attempt {attempt}/{self.max_retries} for chapter '{chapter_title}' ==")
                
            # 1. 主笔创作
            draft = self.writer.invoke(base_prompt, feedback)
            if not draft.strip():
                logging.warning("Orchestrator: Writer returned empty draft.")
                continue
                
            # 2. 判官审核
            passed, violations = self.reviewer.invoke(draft, chapter_title)
            
            # 3. 判定流向
            if passed:
                logging.info("Orchestrator: SUCCESS! Draft passed all consistency checks.")
                return draft
            else:
                feedback = violations
                
        logging.warning("Orchestrator: WARNING! Max retries reached. Returning the latest drafted version despite possible violations.")
        return draft
