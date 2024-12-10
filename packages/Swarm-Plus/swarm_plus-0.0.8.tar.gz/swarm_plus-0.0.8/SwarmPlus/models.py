import sys
sys.dont_write_bytecode =True

import os
import json
import openai
import base64
import requests
from dotenv import load_dotenv
from typing import List,Union,Dict,Any,Union
from pydantic import BaseModel,Field
from SwarmPlus.helper import print_colored
from openai import OpenAI, AsyncOpenAI

class DefaultResponseFormat1(BaseModel):

    thoughts:Union[list,str]
    tool_name:str
    tool_args:Dict[str,Any]


# Chat Model ---------------------------------------------------------------

class OpenaiChatModel:

    def __init__(self,model_name="gpt-4o",api_key=None,temperature=0.5,max_tokens=3000,max_retries=3,verbose=False) -> None:
        

        load_dotenv()

        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature =temperature
        self.max_tokens =max_tokens
        self.max_retries=max_retries
        self.client = OpenAI(api_key=self.api_key)
        self.async_client = AsyncOpenAI(api_key=self.api_key)

        self.verbose =verbose

    async def aget_summary(self,messages):

        total_token_count = 0

        for attempt in range(self.max_retries):

            if self.verbose:
                print_colored("Hitting The API....","brown")

            response = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            response_message = response.choices[0].message.content

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            total_token_count+=response.usage.total_tokens

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                return response_message,{"input_tokens":input_tokens,"output_tokens":output_tokens}
            
            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

                messages.append({"role":"assistant","content":response_message})
                messages.append({"role":"user","content":f"Facing Error, Please check your response: {str(e)}"})
        else:

            return "Sorry I am not able to process your request.",total_token_count


    def get_output(self,messages,agent_response_format=DefaultResponseFormat1):

        total_token_count = 0

        for attempt in range(self.max_retries):

            if self.verbose:

                print_colored("Hitting The API....","brown")

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            response_message = response.choices[0].message.content

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            total_token_count+=response.usage.total_tokens

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                response_message = json.loads(response_message)

                agent_response_format(**response_message)

                return response_message,{"input_tokens":input_tokens,"output_tokens":output_tokens}
    
            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}\n\n{e}","red")

                messages.append({"role":"assistant","content":str(response_message)})

                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})

        else:

            return "Sorry I am not able to process your request.",total_token_count


    async def aget_output(self,messages,agent_response_format=DefaultResponseFormat1):

        total_token_count = 0

        for attempt in range(self.max_retries):

            if self.verbose:
                print_colored("Hitting The API....","brown")

            response = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            response_message = response.choices[0].message.content

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            total_token_count+=response.usage.total_tokens

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                response_message = json.loads(response_message)

                agent_response_format(**response_message)

                return response_message,{"input_tokens":input_tokens,"output_tokens":output_tokens}
    
            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}\n\n{e}","red")

                messages.append({"role":"assistant","content":str(response_message)})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})

        else:

            return "Sorry I am not able to process your request.",total_token_count


# Structed output Model -----------------------------------------------------------

class OpenaiStructedOutputModel:

    def __init__(self,model_name='gpt-4o',api_key=None,temperature=0.5,max_tokens=3000,max_retries=3) -> None:
        
        load_dotenv()
        
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens    
        self.max_retries = max_retries
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=self.api_key)

    def get_output(self,messages,tools=[],agent_response_format=DefaultResponseFormat1):
        
        total_token_count = 0

        for i in range(self.max_retries):

            try:

                if agent_response_format:

                    response = self.client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        response_format=agent_response_format
                    )
                    response_message = response.choices[0].message

                    total_token_count+=response.usage.total_tokens

                    response_dump= response_message.model_dump()['parsed']

                    response_dump['tool_args'] = {i['key']:i['value'] for i in response_dump['tool_args']}

                    return response_dump,total_token_count
                
                if len(tools):

                    response = self.client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        tools=[openai.pydantic_function_tool(i) for i in tools]
                    )
                    response_message = response.choices[0].message

                    input_tokens = response.usage.prompt_tokens
                    output_tokens = response.usage.completion_tokens

                    total_token_count+=response.usage.total_tokens
                    
                    response_dump= response_message.model_dump()['parsed']

                    response_dump['tool_args'] = {i['key']:i['value'] for i in response_dump['tool_args']}

                    return response_dump,{"input_tokens":input_tokens,"output_tokens":output_tokens}
                
            except Exception as e:

                print_colored(f"Facing Error With the Response :\n\n{response_message}.\n\nRetrying.....{i}","red")

                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        else:
            
            return "Sorry I am not able to process your request.",total_token_count


    async def aget_output(self,messages,tools=[],agent_response_format=DefaultResponseFormat1):
        
        total_token_count = 0

        for i in range(self.max_retries):

            try:

                if agent_response_format:

                    response = await self.async_client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        response_format=agent_response_format
                    )
                    response_message = response.choices[0].message

                    input_tokens = response.usage.prompt_tokens
                    output_tokens = response.usage.completion_tokens

                    total_token_count+=response.usage.total_tokens

                    response_dump= response_message.model_dump()['parsed']

                    response_dump['tool_args'] = {i['key']:i['value'] for i in response_dump['tool_args']}

                    return response_dump,total_token_count
                
                if len(tools):

                    response = await self.client.beta.chat.completions.parse(
                        model=self.model_name,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        tools=[openai.pydantic_function_tool(i) for i in tools]
                    )
                    response_message = response.choices[0].message

                    total_token_count+=response.usage.total_tokens
                    
                    response_dump= response_message.model_dump()['parsed']

                    response_dump['tool_args'] = {i['key']:i['value'] for i in response_dump['tool_args']}

                    return response_dump,{"input_tokens":input_tokens,"output_tokens":output_tokens}
                
            except Exception as e:

                print_colored(f"Facing Error With the Response :\n\n{response_message}.\n\nRetrying.....{i}","red")

                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        else:
            
            return "Sorry I am not able to process your request.",total_token_count


# Vission Model -------------------------------------------------------------------

class OpenAIVissionModel:
    def __init__(self,model='gpt-4o',api_key=None,max_tokens=3000):

        load_dotenv()

        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.max_tokens = max_tokens
        self.async_client = AsyncOpenAI(api_key=self.api_key)


    def encode_image(self, image_path):
        """Encodes an image to a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def get_output(self, question,image_path=None,base64_image=None):
        """Analyzes the content of an image using AI."""

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if not base64_image:
            base64_image = self.encode_image(image_path)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": self.max_tokens
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=payload)
        response = response.json()

        return response['choices'][0]['message']['content']
    

# Ollama Models -------------------------------------------------------------------

# import requests

# class OllamaModels:

#     def __init__(self,model_name="llama3.1:8b",ollama_url="http://localhost:11434/api/chat") -> None:
#         self.model = model_name
#         self.ollama_url = ollama_url

#     def get_output(self,messages,tools=[],temperature=0.2,top_p=0.7,max_tokens=1024):

#         options = {
#             "temperature":temperature,
#             "top_p":top_p,
#         }

#         data = {"model":self.model,
#                 "messages":messages,
#                 "tools":tools,
#                 "stream": False,
#                 "options":options}

#         response = requests.post(self.ollama_url,json=data)

#         if response.status_code==200:

#             return response.json()['message']['content']
        
#         else:

#             return response.content
        
# Anthropic Models

import os
from typing import Union
from anthropic import Anthropic,AsyncAnthropic
from typing import List, Dict, Any
from pydantic import BaseModel,Field

class AnthropicResponseFormat(BaseModel):
    thoughts: str = Field(..., description="Always think before taking any action.")  # Required field
    tool_name: str = Field(..., description="Select a tool")  # Required field
    tool_args: Dict[str,Any] = Field(..., description="Provide valid arguments")  # Required field

class AnthropicModel:

    def __init__(self,model_name='claude-3-opus-20240229',api_key=None,temperature=0.5,max_tokens=3000,max_retries=3,async_mode=False) -> None:
        
        load_dotenv()
        
        self.model_name = model_name
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.temperature = temperature
        self.max_tokens = max_tokens    
        self.max_retries = max_retries
        self.client = Anthropic(api_key=api_key)
        self.async_client =AsyncAnthropic(api_key=api_key)

    def generate_tool_schemas(self,models: List[BaseModel]) -> List[Dict[str, Any]]:
        tool_schemas = []

        for model in models:
            schema = model.model_json_schema()
            tool_schema = {
                "name": model.__name__,
                "description": model.__doc__ or "No description provided.",
                "input_schema": {
                    "type": "object",
                    "properties": schema.get("properties", {}),
                    "required": schema.get("required", [])
                }
            }
            tool_schemas.append(tool_schema)
        
        return tool_schemas


    async def aget_summary(self,messages):

        system_prompt = messages[0]["content"]

        messages = messages[1:]
        
        total_token_count = 0

        for i in range(self.max_retries):

            try:

                response = await self.async_client.messages.create(
                    system=system_prompt,
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )

                response_dump = response.content[0].text
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                
                if isinstance(response_dump,str):
                    
                        return response_dump, {"input_tokens":input_tokens,"output_tokens":output_tokens}
                    
                print_colored(f"Facing Error With the Response :\n\nRetrying.....{response_dump}","red")
                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"facing Error,Please check your response: {str(e)}"})
        
            except Exception as e:

                print_colored(f"Facing Error With the Response :\n\nRetrying.....{e}","red")

                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"facing Error,Please check your response: {str(e)}"})
        else:
            
            return "Sorry I am not able to process your request.",total_token_count
        

    def get_output(self,messages,tools=[],agent_response_format=AnthropicResponseFormat):

        system_prompt = messages[0]["content"]

        messages = messages[1:]
        
        total_token_count = 0

        tools = self.generate_tool_schemas([agent_response_format])

        for i in range(self.max_retries):

            try:

                if agent_response_format:

                    response = self.client.messages.create(
                        system=system_prompt,
                        model=self.model_name,
                        messages=messages,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        tools=tools,
                        tool_choice={"type": "tool", "name": "AnthropicResponseFormat"}
                    )

                    response_dump = response.content[0].input
                    response_dump['thoughts'] = [response_dump['thoughts']]
                    input_tokens = response.usage.input_tokens
                    output_tokens = response.usage.output_tokens

                    if isinstance(response_dump,dict):
                    
                        return response_dump, {"input_tokens":input_tokens,"output_tokens":output_tokens}
                    
                    print_colored(f"Facing Error With the Response :\n\nRetrying.....{response_dump}","red")
                    messages.append({"role":"assistant","content":str(response_dump)})
                    messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        
            except Exception as e:

                print_colored(f"Facing Error With the Response :\n\nRetrying.....{e}","red")

                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        
        else:
            
            return "Sorry I am not able to process your request.",total_token_count
        
    async def aget_output(self,messages,tools=[],agent_response_format=AnthropicResponseFormat):

        system_prompt = messages[0]["content"]

        messages = messages[1:]
        
        total_token_count = 0

        tools = self.generate_tool_schemas([agent_response_format])

        for i in range(self.max_retries):

            try:

                response = await self.async_client.messages.create(
                    system=system_prompt,
                    model=self.model_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    tools=tools,
                    tool_choice={"type": "tool", "name": "AnthropicResponseFormat"}
                )

                response_dump = response.content[0].input
                response_dump['thoughts'] = [response_dump['thoughts']]
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                
                if isinstance(response_dump,dict):
                    
                        return response_dump, {"input_tokens":input_tokens,"output_tokens":output_tokens}
                    
                print_colored(f"Facing Error With the Response :\n\nRetrying.....{response_dump}","red")
                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        
            except Exception as e:

                print_colored(f"Facing Error With the Response :\n\nRetrying.....{e}","red")

                messages.append({"role":"assistant","content":str(response_dump)})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        else:
            
            return "Sorry I am not able to process your request.",total_token_count
        


import httpx
import requests
from SwarmPlus.helper import extract_json

class OllamaModels:

    def __init__(self,model_name="llama3.2",ollama_url="http://localhost:11434/api/chat",temperature=0.2,top_p=0.7,max_tokens=1024,number_of_try=3,api_key="",verbose=None) -> None:
        self.model = model_name
        self.ollama_url = ollama_url
        self.max_tokens=max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens=max_tokens
        self.number_of_try = number_of_try
        self.verbose=verbose

    def aget_summary(self,messages,tools=[]):

        options = {
            "temperature":self.temperature,
            "top_p":self.top_p,
        }

        data = {"model":self.model,
                "messages":messages,
                "tools":tools,
                "stream": False,
                "options":options}
        
        total_token_count = 0
        
        for attempt in range(self.number_of_try):

            response = requests.post(self.ollama_url,json=data)

            if response.status_code==200:

                response_result = response.json()['message']['content']

            input_tokens = response.json()['usage']['prompt_tokens']
            output_tokens = response.json()['usage']['completion_tokens']

            total_token_count+=response.json()['usage']['total_tokens']

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                if isinstance(response_result,str):

                        return response_result,{"input_tokens":input_tokens,"output_tokens":output_tokens}
                
                else:

                    print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                    messages.append({"role":"assistant","content":response_result})
                    messages.append({"role":"user","content":f"You should provide a valid json. Please check your response"})

            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                messages.append({"role":"assistant","content":response_result})
                messages.append({"role":"user","content":f"Please check your response: {str(e)}"})
        else:

            return "Sorry I am not able to process your request.",{"input_tokens":0,"output_tokens":0}
            



    def get_output(self,messages,tools=[],agent_response_format=DefaultResponseFormat1):

        options = {
            "temperature":self.temperature,
            "top_p":self.top_p,
        }

        data = {"model":self.model,
                "messages":messages,
                "tools":tools,
                "stream": False,
                "options":options}
        
        for attempt in range(self.number_of_try):

            response = requests.post(self.ollama_url,json=data)

            if response.status_code==200:

                response_result = response.json()['message']['content']

                try:

                    if isinstance(response_result,str):

                        response_message = extract_json(response_result)

                        if isinstance(response_message,dict):

                            final_response = agent_response_format(**response_message)

                            final_response = final_response.model_dump()

                            return final_response,{"input_tokens":111,"output_tokens":111}
                        
                        else:

                            print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                            messages.append({"role":"assistant","content":response_result})
                            messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {response_message}"})

                    elif isinstance(response_result,dict):

                        final_response = agent_response_format(**response_result)

                        final_response = final_response.model_dump()

                        return final_response,{"input_tokens":1111,"output_tokens":1111}
                
                    else:

                        print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                        messages.append({"role":"assistant","content":response_result})
                        messages.append({"role":"user","content":f"You should provide a valid json. Please check your response"})

                except Exception as e:

                    print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

                    messages.append({"role":"assistant","content":response_result})
                    messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
            else:
                print("Error : ",response.content)
                return response.content, {"input_tokens":111,"output_tokens":111}
            
        else:

            return "Sorry I am not able to process your request.",{"input_tokens":0,"output_tokens":0}



    async def aget_output(self,messages,tools=[],agent_response_format=DefaultResponseFormat1):

        options = {
            "temperature":self.temperature,
            "top_p":self.top_p,
        }

        data = {"model":self.model,
                "messages":messages,
                "tools":tools,
                "stream": False,
                "options":options}
        

        async with httpx.AsyncClient() as client:

            for attempt in range(self.number_of_try):

                response = await client.post(self.ollama_url, json=data)

                if response.status_code==200:

                    response_result = response.json()['message']['content']

                    try:

                        if isinstance(response_result,str):

                            response_message = extract_json(response_result)

                            if isinstance(response_message,dict):

                                final_response = agent_response_format(**response_message)

                                final_response = final_response.model_dump()

                                return final_response,{"input_tokens":111,"output_tokens":111}
                            
                            else:

                                print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                                messages.append({"role":"assistant","content":response_result})
                                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {response_message}"})

                        elif isinstance(response_result,dict):

                            final_response = agent_response_format(**response_result)

                            final_response = final_response.model_dump()

                            return final_response,{"input_tokens":1111,"output_tokens":1111}
                    
                        else:

                            print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                            messages.append({"role":"assistant","content":response_result})
                            messages.append({"role":"user","content":f"You should provide a valid json. Please check your response"})

                    except Exception as e:

                        print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

                        messages.append({"role":"assistant","content":response_result})
                        messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
                else:
                    print("Error : ",response.content)
                    return response.content, {"input_tokens":111,"output_tokens":111}
            
            else:

                return "Sorry I am not able to process your request.",{"input_tokens":0,"output_tokens":0}
            
    # --------------------------- Groq ---------------------------------


class GroqModel:

    def __init__(self,model_name="llama-3.1-70b-versatile",api_key=None,temperature=0.5,max_tokens=3000,max_retries=3,verbose=False) -> None:
        
        load_dotenv()

        self.model_name = model_name
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.temperature =temperature
        self.max_tokens =max_tokens
        self.max_retries=max_retries
        self.client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=self.api_key)
        self.async_client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1",api_key=self.api_key)

        self.verbose =verbose
        
    async def aget_summary(self,messages):

        total_token_count = 0

        for attempt in range(self.max_retries):

            if self.verbose:
                print_colored("Hitting The API....","brown")

            response = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            response_result = response.choices[0].message.content

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            total_token_count+=response.usage.total_tokens

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                if isinstance(response_result,str):

                        return response_result,{"input_tokens":input_tokens,"output_tokens":output_tokens}
                
                else:

                    print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                    messages.append({"role":"assistant","content":response_result})
                    messages.append({"role":"user","content":f"You should provide a valid json. Please check your response"})

            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                messages.append({"role":"assistant","content":response_result})
                messages.append({"role":"user","content":f"Please check your response: {str(e)}"})
        else:

            return "Sorry I am not able to process your request.",{"input_tokens":0,"output_tokens":0}
        

    def get_output(self,messages,agent_response_format=DefaultResponseFormat1):

        total_token_count = 0

        for attempt in range(self.max_retries):

            if self.verbose:

                print_colored("Hitting The API....","brown")

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            response_result = response.choices[0].message.content

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            total_token_count+=response.usage.total_tokens

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                if isinstance(response_result,str):

                    response_message = extract_json(response_result)

                    if isinstance(response_message,dict):

                        final_response = agent_response_format(**response_message)

                        final_response = final_response.model_dump()

                        return final_response,{"input_tokens":input_tokens,"output_tokens":output_tokens}
                    
                    else:

                        print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                        messages.append({"role":"assistant","content":response_result})
                        messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {response_message}"})

                elif isinstance(response_result,dict):

                    final_response = agent_response_format(**response_result)

                    final_response = final_response.model_dump()

                    return final_response,{"input_tokens":input_tokens,"output_tokens":output_tokens}
            
                else:

                    print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                    messages.append({"role":"assistant","content":response_result})
                    messages.append({"role":"user","content":f"You should provide a valid json. Please check your response"})

            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

                messages.append({"role":"assistant","content":response_result})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        else:

            return "Sorry I am not able to process your request.",{"input_tokens":0,"output_tokens":0}


    async def aget_output(self,messages,agent_response_format=DefaultResponseFormat1):

        total_token_count = 0

        for attempt in range(self.max_retries):

            if self.verbose:
                print_colored("Hitting The API....","brown")

            response = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            response_result = response.choices[0].message.content

            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            total_token_count+=response.usage.total_tokens

            if self.verbose:
            
                print_colored(f"Total Token Usage {response.usage.total_tokens}","brown")

            try:

                if isinstance(response_result,str):

                    response_message = extract_json(response_result)

                    if isinstance(response_message,dict):

                        final_response = agent_response_format(**response_message)

                        final_response = final_response.model_dump()

                        return final_response,{"input_tokens":input_tokens,"output_tokens":output_tokens}
                    
                    else:

                        print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                        messages.append({"role":"assistant","content":response_result})
                        messages.append({"role":"user","content":f"You should provide a valid json. Please check your response and Here is the error :{response_message}"})

                elif isinstance(response_result,dict):

                    final_response = agent_response_format(**response_result)

                    final_response = final_response.model_dump()

                    return final_response,{"input_tokens":input_tokens,"output_tokens":output_tokens}
            
                else:

                    print_colored(f"Facing Error With the Response :{response_result}.\nRetrying.....{attempt+1}","red")

                    messages.append({"role":"assistant","content":response_result})
                    messages.append({"role":"user","content":f"You should provide a valid json. Please check your response"})

            except Exception as e:

                print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

                messages.append({"role":"assistant","content":response_result})
                messages.append({"role":"user","content":f"You should provide a valid json. Please check your response: {str(e)}"})
        else:

            return "Sorry I am not able to process your request.",{"input_tokens":0,"output_tokens":0}



# ------------------------------------------------------ Gemini Model ---------------------------------------------------------------



# import os
# import json
# from dotenv import load_dotenv
# import google.generativeai as genai
# from SwarmPlus.helper import print_colored

# load_dotenv()

# from typing import  Union
# from typing import Any, List
# from typing_extensions import TypedDict

# class ArgsGemini(TypedDict):
#     key: str
#     value: Any  # This allows for any type, including another TypedDict, making it flexible

# # Define the response format class using Pydantic BaseModel for validation
# class GeminiResponseFormat(BaseModel):
#     thoughts: List[str] = Field(..., description="Always think before taking any action.")  # Required field
#     tool_name: str = Field(..., description="Select a tool")  # Required field
#     tool_args: List[ArgsGemini] = Field(..., description="Provide valid arguments")  # Required field


# class GeminiModel:

#     def __init__(self,model_name="gemini-1.5-pro",api_key=None,temperature=0.5,max_tokens=3000,max_retries=3,verbose=False) -> None:
                
#         self.model_name = model_name
#         self.api_key = api_key or os.getenv("GOOGLE_API_KEY")

#         if not self.api_key:
#             raise ValueError("API key is required to initialize GeminiChatModel.")
        
#         self.max_retries=max_retries
#         self.verbose =verbose
#         self.generation_config = {'temperature': temperature, 'max_output_tokens': max_tokens, 'response_mime_type': "application/json",'response_schema':GeminiResponseFormat}
#         # self.generation_config = {'temperature': temperature, 'max_output_tokens': max_tokens, 'response_mime_type': "application/json"}

#         self.client = genai.GenerativeModel(model_name=self.model_name,generation_config=self.generation_config)
    
#     def process_messages(self,messages):

#         if len(messages)==2:

#             messages.insert(1,{'role': 'assistant', 'content': ['OK I understand. I will do my best!']})
            
#         for message in messages:

#             message["parts"] = [str(message.get("content"))]

#             if 'content' in message.keys():
                
#                 message.pop("content")

#             if message['role'] == "system":
#                 message["role"] = "user"

#             # Change 'model' role to 'assistant'
#             if message["role"] == "assistant":
#                 message["role"] = "model"

#         return messages
        
#     async def aget_output(self,messages):

#         total_token_count = 0

#         messages = self.process_messages(messages=messages)

#         for attempt in range(self.max_retries):

#             if self.verbose:
#                 print_colored("Hitting The API....","brown")

#             chat_session = self.client.start_chat(history=messages[0:-1])

#             response_message = chat_session.send_message(messages[-1]['parts'])

#             if self.verbose:
            
#                 print_colored(f"Total Token Usage {response_message.usage_metadata.total_tokens}","brown")

#             try:

#                 json_response = json.loads(response_message.text)

#                 print("***********************:\n\n",json_response)

#                 return json_response,{"input_tokens":response_message.usage_metadata.prompt_token_count,"output_tokens":response_message.usage_metadata.candidates_token_count}
            
#             except Exception as e:

#                 print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

#                 messages.append({"role":"model","parts":[response_message]})
#                 messages.append({"role":"user","parts":[f"You should provide a valid json. Please check your response: {str(e)}"]})
#         else:

#             return "Sorry I am not able to process your request.",total_token_count
        
#     def get_output(self,messages):

#         total_token_count = 0

#         messages = self.process_messages(messages=messages)

#         for attempt in range(self.max_retries):

#             if self.verbose:
#                 print_colored("Hitting The API....","brown")

#             chat_session = self.client.start_chat(history=messages[0:-1])

#             response_message = chat_session.send_message(messages[-1]['parts'])

#             if self.verbose:
            
#                 print_colored(f"Total Token Usage {response_message.usage_metadata.total_tokens}","brown")

#             try:

#                 json_response = json.loads(response_message.text)

#                 print(f"Output : \n\n{json_response}\n\n")

#                 return json_response,{"input_tokens":response_message.usage_metadata.prompt_token_count,"output_tokens":response_message.usage_metadata.candidates_token_count}
            
#             except Exception as e:

#                 print_colored(f"Facing Error With the Response :{response_message}.\nRetrying.....{attempt+1}","red")

#                 messages.append({"role":"model","parts":[response_message]})
#                 messages.append({"role":"user","parts":[f"You should provide a valid json. Please check your response: {str(e)}"]})
#         else:

#             return "Sorry I am not able to process your request.",total_token_count