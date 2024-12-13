from typing import Any
from wyge.prompts.react_prompt import reAct_prompt

class Agent:
    def __init__(self, llm, tools=None, max_iterations=25, react_prompt=None ) -> None:
        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations

        if react_prompt:
            self.react_prompt = react_prompt
        else:
            self.react_prompt = reAct_prompt

        if self.tools:
            self.llm.tools = self.tools
        
        self.llm.memory = True
        self.llm.update_system_message(self.react_prompt)

    def __call__(self, prompt) -> Any:
        response = self._execute(prompt)
        return response

    def _execute(self, prompt):
        i = 0
        next_prompt = prompt
        while i<self.max_iterations:
            i += 1
            response = self.llm.run(next_prompt, return_tool_output=True)
            print(response)
            print("\n------------------------------------------------------------------------\n")
            next_prompt = None
            if 'Final Answer:' in response:
                return response
                