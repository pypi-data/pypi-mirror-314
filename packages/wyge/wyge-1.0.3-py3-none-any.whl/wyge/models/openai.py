import openai
import os
from wyge.memory.basic_memory import ChatMemory
from wyge.tools.base_tool import handle_tool_calls

class ChatOpenAI:
    def __init__(self,
                 api_key=None,
                 model_name='gpt-4o-mini', 
                 memory: bool = False,
                 tools: list = None,
                 temperature=0.2,
                 max_tokens=1500):

        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("API key must be provided either via argument or 'OPENAI_API_KEY' environment variable.")
        
        os.environ['OPENAI_API_KEY'] = self.api_key
        
        self.model_name = model_name
        self.memory = memory
        self.tools = tools
        self.temperature = temperature
        self.max_tokens = max_tokens

        if self.memory:
            self.chat_memory = ChatMemory()

    def run(self, prompt, system_message=None, return_tool_output=False):
        if not self.memory:
            messages=[
                {"role": "system", "content": system_message or "You are a helpful assistant. If needed use appropriate tool wisely."},
                {"role": "user", "content": prompt}
            ]
        else:
            if system_message:
                self.chat_memory.update_system_message(system_message)
            if prompt:
                self.chat_memory.summarize_memory(self.api_key)
                self.chat_memory.add_message('user', prompt)
                
        response=None
        if self.memory:
            messages = self.chat_memory.get_memory()

        # print(messages)
        response = openai.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools= self.tools
        )
        print(response.choices[0])
     
        tool_outputs = None
        if response.choices[0].finish_reason == 'function_call' or response.choices[0].finish_reason=='tool_calls':
            print(response.choices[0].message.tool_calls)
            tool_outputs = handle_tool_calls(response)
            print(tool_outputs)

        if self.memory:
                self.chat_memory.add_response(response, tool_outputs)
                
        if not return_tool_output:
            
            if not self.memory and tool_outputs:
                messages.append(response.choices[0].message)
                import json
                print(tool_outputs)
                messages.append({'role': 'tool', 'content':json.dumps(str(tool_outputs)), 'tool_call_id': response.choices[0].message.tool_calls[0].id})
            if tool_outputs:
                response = openai.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools= self.tools
                )
                print(response.choices[0])

        return tool_outputs or response.choices[0].message.content 

    def clear_memory(self, keep_system_message=True):
        if self.memory and self.chat_memory:
            self.chat_memory.clear_memory(keep_system_message=keep_system_message)

    def search_memory(self, keyword, exact_match=False):
        if self.memory and self.chat_memory:
            return self.chat_memory.search_memory(keyword, exact_match=exact_match)
        return []

    def last_message(self):
        if self.memory and self.chat_memory:
            return self.chat_memory.last_message()
        return None
    
    def update_system_message(self, content):
        self.chat_memory.update_system_message(content)



    def get_config(self):
        masked_api_key = '*' * (len(self.api_key) - 4) + self.api_key[-4:] if self.api_key else None
        return {
            'api_key': masked_api_key,
            'model_name': self.model_name,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
