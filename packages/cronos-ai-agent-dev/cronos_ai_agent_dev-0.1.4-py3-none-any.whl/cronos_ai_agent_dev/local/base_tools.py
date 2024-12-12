from abc import ABC, abstractmethod
import json
from ..error_handler import ErrorHandler
from ..logger import logger

class BaseTools(ABC):
    def __init__(self):
        self.functions = self.register_functions
        self._function_names = {f.name: f.execute for f in self.functions}
        self._function_specs = [f.spec for f in self.functions]

    @abstractmethod
    def register_functions(self):
        """Register and return a list of function objects."""
        pass

    def execute_function(self, function_name: str, function_arg: dict, message: str, history: list):
        logger.info("Executing function: %s, with arguments: %s", function_name, function_arg)

        if function_name not in self._function_names:
            return json.dumps(
                {
                    "success": False,
                    "response": f"Function {function_name} is not registered",
                }
            )

        try:
            result = self._function_names[function_name](function_arg, message, history)
            return json.dumps(result)
        except Exception as e:
            return json.dumps(ErrorHandler.handle_function_error(e, function_name))

    @property
    def function_specs(self):
        return self._function_specs

    @property
    def function_names(self):
        return list(self._function_names.keys())