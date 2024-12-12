from ..prompts import full_prompts
from .base_assistant import BaseAssistant
from .custom_tools import CustomTools

class CustomAssistant(BaseAssistant):
    def __init__(self):
        self.tools = CustomTools()
        super().__init__(tools_instance=self.tools)

    @property
    def prompts(self):
        return full_prompts()
