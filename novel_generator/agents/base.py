# novel_generator/agents/base.py
import abc

class BaseAgent(abc.ABC):
    """
    Agent 的抽象基类
    """
    def __init__(self, llm_adapter):
        self.llm_adapter = llm_adapter
        
    @abc.abstractmethod
    def invoke(self, *args, **kwargs) -> str:
        """执行Agent的核心动作"""
        pass
