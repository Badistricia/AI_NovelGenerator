# novel_generator/agents/reviewer.py
from .base import BaseAgent
from novel_generator.common import invoke_with_cleaning
from .interceptors import HookInterceptor
import logging

class ReviewerAgent(BaseAgent):
    """
    负责执行一致性审查与报错打回的判官 Agent
    """
    def __init__(self, llm_adapter, hook_interceptor: HookInterceptor):
        super().__init__(llm_adapter)
        self.hook = hook_interceptor
        
    def invoke(self, draft: str, chapter_title: str) -> tuple[bool, str]:
        """
        返回: (is_passed: bool, feedback: str)
        """
        rules = self.hook.get_rules()
        if not rules:
            return True, ""
            
        rules_text = "\n".join([f"- {r}" for r in rules])
        prompt = f"""
你现在的身份是冷酷且极其严格的《小说一致性与设定规范审查长》（Reviewer Agent）。
以下是本小说的【雷区/核心限制规则（Hook）】：
{rules_text}

请审查以下刚写出来的【章节草稿: {chapter_title}】：
{draft}

【审查任务与要求】：
1. 请逐字逐句比对草稿中的剧情走势、人物对话、角色心理描写、动机等，是否**触犯了上述任何一条核心限制规则**！
2. 如果没有任何违规，请直接且只输出四个字母: PASS
3. 如果发现哪怕一处违规（比如出现了明令禁止的性格要素、不该出现的降智流向等），请输出详细的报错打回信息。在开头必须包含纯大写字母: VIOLATION。然后以严厉的口吻指出：
   - 违规的具体表现是什么？
   - 违反了规则库中的哪一条？
   - 要求主笔应该如何重写和修正这段剧情？

直接输出你的审查结论：
"""
        logging.info("ReviewerAgent: Reviewing the draft against hook rules...")
        response = invoke_with_cleaning(self.llm_adapter, prompt)
        
        # 判断逻辑
        res_upper = response.upper()
        if "VIOLATION" in res_upper or ("PASS" not in res_upper and "违反" in response):
            logging.warning(f"ReviewerAgent: Found violations:\n{response}")
            return False, response
        else:
            logging.info("ReviewerAgent: Draft PASSED the hook rules.")
            return True, ""
