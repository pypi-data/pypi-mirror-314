from abc import ABC, abstractmethod
from typing import Dict, List
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()


class BaseFunction(ABC):
    @classmethod
    def register(cls) -> "BaseFunction":
        """Register function instance"""
        return cls()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def spec(self) -> Dict:
        pass

    # wait_exponential(multiplier=1, min=4, max=10):
    # This specifies an exponential backoff strategy for waiting between retries.
    # The wait time will start at 4 seconds and can grow up to 10 seconds.
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @abstractmethod
    def execute(self, function_arg: Dict, message: str, history: List) -> Dict:
        pass
