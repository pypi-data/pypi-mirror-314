import os
import json
from abc import ABC, abstractmethod
from openai import OpenAI
from ..memory import Memory
from ..tools import Tools


class BaseAssistant(ABC):
    def __init__(self, memory_instance=None, tools_instance=None, openai_client=None, model="gpt-4o", max_iterations=10):
        self.memory_instance = memory_instance if memory_instance is not None else Memory()
        self.tools_instance = tools_instance if tools_instance is not None else Tools()
        self.openai_client = openai_client if openai_client is not None else OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self.model = model
        self.max_iterations = max_iterations
        self.assistant = self.openai_client.beta.assistants.create(
            name="Base Assistant",
            instructions=self.prompts,
            model=self.model,
            tools=self.tools_instance.function_specs,
        )

    @abstractmethod
    def prompts(self):
        """Return the instructions for the assistant."""
        pass

    async def run_assistant(self, chat_id: int, message: str, history: list):
        try:
            history_formatted = self.memory_instance.format_history_for_openai(history)
            thread = self.openai_client.beta.threads.create()
            for history_item in history_formatted:
                self.openai_client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role=history_item.get("role", "user"),
                    content=history_item.get("content", ""),
                )
            self.openai_client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message,
            )
            run = self.openai_client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=self.assistant.id, timeout=60
            )
            keep_going = True
            n_iterations = 0
            assistant_response = None
            while keep_going and n_iterations < self.max_iterations:
                n_iterations += 1
                if run.status == "completed":
                    messages = self.openai_client.beta.threads.messages.list(thread_id=thread.id)
                    for message in messages:
                        if message.role == "assistant":
                            assistant_response = message.content[0].text.value
                            keep_going = False
                            break
                elif run.status == "requires_action":
                    tool_outputs = self.handle_tool_calls(run, message, history)
                    if tool_outputs:
                        run = self.openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs,
                        )
            if assistant_response is None:
                assistant_response = "Error, please try again."
        except Exception as e:
            assistant_response = f"Error, the conversation has been reset. {e}"
            self.memory_instance.reset_conversation(chat_id)
        return assistant_response

    def handle_tool_calls(self, run, message, history):
        tool_outputs = []
        if run.required_action.submit_tool_outputs:
            tools_calls = run.required_action.submit_tool_outputs.tool_calls
            for call in tools_calls:
                if call.type == "function" and call.function.name in self.tools_instance.function_names:
                    call_function_argument = json.loads(call.function.arguments)
                    tool_output = self.tools_instance.execute_function(
                        function_name=call.function.name,
                        function_arg=call_function_argument,
                        message=message,
                        history=history,
                    )
                    tool_outputs.append({
                        "tool_call_id": call.id,
                        "output": tool_output,
                    })
        return tool_outputs