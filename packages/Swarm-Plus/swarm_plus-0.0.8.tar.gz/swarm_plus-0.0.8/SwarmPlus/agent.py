# -------------------------------- Structured Agent -------------------------------------

import json
import asyncio
import nest_asyncio
import chainlit as cl
from enum import Enum
from typing import List,Type,Union,Dict, Any
from SwarmPlus.helper import print_colored
from pydantic import BaseModel,Field
from SwarmPlus.utils.response_model import Agentoutput,AssistantData,ToolOutput
from SwarmPlus.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory

# Apply the patch
nest_asyncio.apply()

class Agent:

    def __init__(self,model,agent_name,agent_description,agent_instructions,tools=[],return_tool_output=[],assistant_agents=[],max_allowed_attempts=10,verbose=True,memory: Union[ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory]=ConversationBufferMemory()) -> None:
        self.model = model 
        self.agent_name = agent_name
        self.agent_description = agent_description
        self.agent_instructions=agent_instructions
        self.tools = tools
        self.assistant_agents = assistant_agents
        self.tool_names = []
        self.messages = []
        self.max_allowed_attempts= max_allowed_attempts
        self.attempts_made = 0
        self.verbose = verbose
        self.input_tokens = 0
        self.output_tokens = 0
        self.memory = memory
        self.return_tool_output = return_tool_output
        self.agent_response_format = None

        if not isinstance(memory, (ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory)):

            raise TypeError("memory must be an instance of one of the following: ConversationBufferMemory, ConversationBufferWindowMemory,ConversationSummaryMemory, ConversationSummaryBufferMemory")

        if len(self.assistant_agents):

            self.prepare_prompt()
            self.agents_as_tools = {agent.agent_name:agent for agent in assistant_agents}
            self.assistants_names = []

        self.response_format = self.prepare_Default_tools()

        if len(self.tools):

            self.tool_objects = {i:j for i,j in zip(self.tool_names,tools)}

            tool_schemas = self.prepare_schema_from_tool(self.tools)
            self.agent_instructions+="""\n## Available Tools:\n"""
            self.agent_instructions+=f"""\nYou have access to the following tools:\n{tool_schemas}\nYou must use one of these tools to answer the user's question.\n\n"""
            self.agent_instructions+=f"""IMPORTANT!: You must provide your response in the below json format.
{{
"thoughts":["Always you should think before taking any action"],
"tool_name":"Name of the tool. It must be either one of these: {self.tool_names}",
"tool_args":{{"arg_name":"arg_value"}}
}}
"""
    def prepare_Default_tools(self):

        # Prepare final answer tool
        class FinalAnswer(BaseModel):
            """
            Use this tool for interacting with the user, including asking clarifying questions or delivering final responses.  
            This tool facilitates seamless communication to gather necessary information or provide a well-formulated answer that addresses the user's query comprehensively.  
            Ensure all messages are clear, concise, and contextually relevant to maintain an effective dialogue.
            """
            final_answer: str = Field(
                description="The message to communicate with the user. This can be a question for clarification or the final answer to their query."
            )
            def run(self):
                return self.final_answer
    
        self.tools.append(FinalAnswer)

        # Prepare Assign Task tool
        if len(self.assistant_agents):

            self.assistants_names = [i.agent_name for i in self.assistant_agents]

            recipients = Enum("recipient", {name: name for name in self.assistants_names})

            assistant_description = f"Choose the right agent to assign the task: {self.assistants_names}\n\n"

            for assistant in self.assistant_agents:

                assistant_description+=assistant.agent_name+" : "+assistant.agent_description+"\n"

            class AssignTask(BaseModel):

                """Use this tool to facilitate direct, synchronous communication between specialized agents within your agency. When you send a message using this tool, you receive a response exclusively from the designated recipient agent. To continue the dialogue, invoke this tool again with the desired recipient agent and your follow-up message. Remember, communication here is synchronous; the recipient agent won't perform any tasks post-response. You are responsible for relaying the recipient agent's responses back to the user, as the user does not have direct access to these replies. Keep engaging with the tool for continuous interaction until the task is fully resolved. Do not send more than 1 task at a time."""

                my_primary_instructions: str = Field(...,
                                                    description="Please repeat your primary instructions step-by-step, including both completed "
                                                                "and the following next steps that you need to perform. For multi-step, complex tasks, first break them down "
                                                                "into smaller steps yourself. Then, issue each step individually to the "
                                                                "recipient agent via the task_details parameter. Each identified step should be "
                                                                "sent in separate task_details. Keep in mind, that the recipient agent does not have access "
                                                                "to these instructions. You must include recipient agent-specific instructions "
                                                                "in the task_details or additional_instructions parameters.")
                
                recipient: recipients = Field(..., description=assistant_description,examples=self.assistants_names)

                task_details: str = Field(...,
                                    description="Specify the task required for the recipient agent to complete. Focus on "
                                                "clarifying what the task entails, rather than providing exact "
                                                "instructions.")

                additional_instructions: str = Field(description="Any additional instructions or clarifications that you would like to provide to the recipient agent.")

            self.tools.append(AssignTask)
                
        self.tool_names = [i.__name__ for i in self.tools]

        tool_names = Enum("tools_names", {name: name for name in self.tool_names})

        if self.model.client.__module__=='openai':

            class DefaultResponseFormat(BaseModel):

                thoughts:Union[list,str] = Field(..., description="Always think before taking any action.")
                tool_name: tool_names = Field(..., description="Select a tool")  # Required field
                tool_args: Dict[str,Any] = Field(..., description="Provide valid arguments")  # Required field

            self.agent_response_format = DefaultResponseFormat

        elif self.model.client.__module__=='anthropic':

            class AnthropicResponseFormat(BaseModel):
                thoughts: str = Field(..., description="Always think before taking any action.")  # Required field
                tool_name: tool_names = Field(..., description="Select a tool")  # Required field
                tool_args: Dict[str,Any] = Field(..., description="Provide valid arguments")  # Required field

            self.agent_response_format = AnthropicResponseFormat

        else:

            self.agent_response_format = DefaultResponseFormat

        # class ToolChoices(BaseModel):
        #     thoughts: List[str] = Field(description="Your Thoughts")
        #     tool_name : Literal[*self.tool_names] = Field(description=f"Select an appropriate tools from : {self.tool_names}",examples=self.tool_names)
        #     tool_args : Union[*self.tools]

        # return ToolChoices

    def prepare_schema_from_tool(self,Tools: List[Type[BaseModel]]) -> List[dict]:
        schemas = ""
        for tool in Tools:
            schema = tool.model_json_schema()
            schemas+="\n"
            schemas += f""""Tool Name": {tool.__name__},
"Tool Description": {tool.__doc__},
"Tool Parameters": 
    "Properties": {schema["properties"]},
    "Required": {schema["required"]},
    "Type": {schema["type"]}\n"""
            schemas+="\n"
            
        return schemas

    def prepare_prompt(self):

        if len(self.assistant_agents):

            self.agent_instructions+="\n**Task Assignment**: You can assign tasks to the following agents, who are here to help you achieve your goal.\n"

            self.agent_instructions+="-----------------------------------------------\n"

            for agent in self.assistant_agents:

                self.agent_instructions+="- **Agent Name**: "+agent.agent_name+"\n"
                self.agent_instructions+="- **Agent Description**:"+agent.agent_description+"\n"

            self.agent_instructions+="\n-----------------------------------------------\n"
                
    def prepare_messages(self,content,role=None,messages=[]):

        if not len(messages):

            messages = [
                {"role":"system","content":self.agent_instructions},
                {"role":"user","content":content}
            ]

        else:

            messages.append({"role":role,"content":content})

        return messages


    def update_system_prompt(self,agent_instructions,messages,summary):

        messages[0]['content'] = (
        f"{agent_instructions}\n\n"
        "Summary of previous interactions:\n"
        f"{'-'*40}\n"
        f"{summary}\n"
        f"{'-'*40}")

        return messages[:1]
    
    async def process_memory(self,messages):

        if len(messages):

            conversation_messages = messages[1:]

            if isinstance(self.memory,ConversationBufferMemory):

                return messages
            
            elif isinstance(self.memory,ConversationBufferWindowMemory):

                return self.memory.prepare_memory(messages)
            
            elif isinstance(self.memory,ConversationSummaryMemory):

                output = await self.memory.prepare_memory(self.model,conversation_messages)

                summary = output['summary']

                if summary:

                    return self.update_system_prompt(self.agent_instructions,messages[:1],summary)
                else:
                    return messages

            elif isinstance(self.memory,ConversationSummaryBufferMemory):

                output = await self.memory.prepare_memory(self.model,conversation_messages)

                summary = output['summary']

                if summary:

                    new_messages = output["messages"]

                    return self.update_system_prompt(self.agent_instructions,messages[:1],summary) + new_messages
                else:
                    return messages
        else:
            return messages
    
    async def aexecute_tool(self,messages,tool_details,context_variables={}):

        assistant_content=str(tool_details)

        tool_details['tool_args'].update({"context_variables":context_variables})

        if tool_details['tool_name'] in self.tool_names :

            context_variables = tool_details['tool_args'].get("context_variables","")

            if tool_details['tool_name'] == 'AssignTask':

                try:

                    arguments = tool_details['tool_args']

                    task_details =arguments.get('task_details',"")

                    additional_instructions =arguments.get('additional_instructions',"")

                    if self.verbose:

                        print_colored(f"{self.agent_name} assigned a task to {arguments['recipient']}","orange")

                    assistant_agent = self.agents_as_tools[arguments['recipient']]

                    user_input = task_details + "\n" + additional_instructions

                    if self.verbose:
                    
                        print_colored("Task Details: "+user_input,"cyan")

                    tool_content = await assistant_agent.arun(user_input,context_variables=context_variables)

                    tool_content = f"Response from the {arguments['recipient']} : "+str(tool_content.response)
                    
                except Exception as e:

                    if self.verbose:
                    
                        print_colored("Error Tool: "+str(e),"red")

                    tool_content = f"Error while assigning task to {arguments['recipient']}. Please provide the correct agent name. Here is the list of available agents: {[i.agent_name for i in self.assistant_agents]}"

            else:

                try:
                    if self.verbose:

                        print_colored(f"{self.agent_name} : Calling Tool {tool_details['tool_name']}","yellow")

                    if not context_variables:

                        tool_output = self.tool_objects[tool_details['tool_name']](**tool_details['tool_args']).run()

                        if asyncio.iscoroutine(tool_output):

                            tool_output = asyncio.run(tool_output)

                    else:

                        output = self.tool_objects[tool_details['tool_name']](**tool_details['tool_args']).run()

                        if asyncio.iscoroutine(output):

                            tool_output,context_variables = asyncio.run(output)

                        else:

                            tool_output,context_variables = output

                    if self.verbose:

                        print_colored(f"{tool_details['tool_name']} Output : {tool_output}","blue")

                    tool_content=f"Output From {tool_details['tool_name']} Tool: {str(tool_output)}"

                except Exception as e:

                    if self.verbose:
                    
                        print_colored("Error Tool: "+str(e),"red")

                    tool_content = "Error while executing tool. Please check the tool name or provide valid arguments to the tool: " + str(e)

        else:

            tool_content= "There is no such a tool available. Here are the available tools : "+str(self.tool_names)

        messages.append({"role":"assistant","content":assistant_content.strip()})
        messages.append({"role":"user","content":tool_content.strip()})

        self.messages = messages

        return messages,context_variables
        
    async def arun(self,user_input=None,messages=[],context_variables={}):

        if self.attempts_made<=self.max_allowed_attempts:

            if self.verbose:
            
                print_colored(f"Attempt Number : {self.attempts_made}/{self.max_allowed_attempts}","pink")

            self.attempts_made+=1

            messages = await self.process_memory(messages)

            if user_input:

                messages = self.prepare_messages(user_input,role="user",messages=messages)

            tool_details,token_usage = await self.model.aget_output(messages,agent_response_format=self.agent_response_format)

            self.messages = messages

            self.input_tokens=token_usage['input_tokens']
            self.output_tokens=token_usage['output_tokens']

            # print("Tool Details : \n\n",tool_details)

            if not isinstance(tool_details,dict):
            
                agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

                return Agentoutput(agent_name=self.agent_name,response="I am not able to process your request",messages=messages,assistant_agents=agent_data,context_variables=context_variables)

            # tool_details = json.loads(tool_details)

            if tool_details['tool_name'] in self.return_tool_output:

                thoughts = tool_details.get('thoughts','')

                if isinstance(thoughts,list):

                    thoughts = '\n'.join(thoughts)

                messages.append({"role":"assistant","content":str(tool_details)})

                agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

                return ToolOutput(agent_name=self.agent_name,response=thoughts,messages=messages,assistant_agents=agent_data,tool_name=tool_details['tool_name'],tool_args=tool_details['tool_args'],context_variables=context_variables)

            if tool_details['tool_name']=='FinalAnswer':

                if self.verbose:

                    thoughts = tool_details.get('thoughts','')

                    if isinstance(thoughts,list):

                        thoughts = '\n'.join(thoughts)
                
                    print_colored(f"Thoughts: {thoughts}","magenta")

                    print_colored(f"{self.agent_name} : {tool_details['tool_args']['final_answer']}","green")

                messages.append({"role":"assistant","content":tool_details['tool_args']['final_answer']})

                self.attempts_made = 0

                self.messages = messages

                agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

                return Agentoutput(agent_name=self.agent_name,response=tool_details['tool_args']['final_answer'],messages=messages,assistant_agents=agent_data,context_variables=context_variables)

            else:

                if self.verbose:
                
                    thoughts = tool_details.get('thoughts','')

                    if isinstance(thoughts,list):

                        thoughts = '\n'.join(thoughts)
                
                    print_colored(f"Thoughts: {thoughts}","magenta")

                messages,context_variables = await self.aexecute_tool(messages,tool_details,context_variables=context_variables)

                self.messages = messages

                return await self.arun(messages=messages,context_variables=context_variables)

        else:
            if self.verbose:
            
                print_colored(f"{self.agent_name} : Sorry! Max Attempt Exceeded, I can't take anymore tasks: {self.attempts_made}","red")
        
            agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

            return Agentoutput(agent_name=self.agent_name,response="Sorry! Max Attempt Exceeded, I can't take anymore tasks",messages=messages,assistant_agents=agent_data,context_variables=context_variables)


    def execute_tool(self,messages,tool_details,UI=False,context_variables={}):

        assistant_content=str(tool_details)

        tool_details['tool_args'].update({"context_variables":context_variables})

        if tool_details['tool_name'] in self.tool_names :

            elements = []
            
            if tool_details['tool_name'] == 'AssignTask':

                try:

                    arguments = tool_details['tool_args']

                    task_details =arguments.get('task_details',"")

                    additional_instructions =arguments.get('additional_instructions',"")

                    if self.verbose:

                        print_colored(f"{self.agent_name} assigned a task to {arguments['recipient']}","orange")

                    assistant_agent = self.agents_as_tools[arguments['recipient']]

                    user_input = task_details + "\n" + additional_instructions

                    if UI:

                        elements.append(cl.Text(name=f"🤖 {self.agent_name} assigned a task to 👨‍💻 {arguments['recipient']}:",content=user_input,display="inline"))

                        asyncio.run(cl.Message("",author=self.agent_name,elements=elements).send())

                    if self.verbose:
                    
                        print_colored("Task Details: "+user_input,"cyan")

                    tool_content = assistant_agent.run(user_input,context_variables=context_variables)

                    if UI:

                        # asyncio.run(chat_messages.remove())

                        elements.append(cl.Text(name=f"👨‍💻 {arguments['recipient']} Response:",content=str(tool_content.response),display="inline"))

                        chat_messages = asyncio.run(cl.Message("",author=self.agent_name,elements=elements).send())

                    tool_content = f"Response from the {arguments['recipient']} : \n\n "+str(tool_content.response) + "\n\n"

                except Exception as e:

                    if self.verbose:
                    
                        print_colored("Error Tool: "+str(e),"red")

                    tool_content = f"Error while assigning task to {arguments['recipient']}. Please provide the correct agent name. Here is the list of available agents: {[i.agent_name for i in self.assistant_agents]}"

            else:

                try:
                    if self.verbose:

                        print_colored(f"{self.agent_name} : Calling Tool 🛠️{tool_details['tool_name']}","yellow")

                    if UI:

                        try:

                            elements.append(cl.Text(name=f"🤖 {self.agent_name} is using 🛠️`{tool_details['tool_name']}` Tool",content=" ",display="inline"))

                            chat_messages2 = asyncio.run(cl.Message("",author=self.agent_name,elements=elements).send())

                        except Exception as e:
                            print("Error: ",e)

                    if not context_variables:
                                
                        tool_output = self.tool_objects[tool_details['tool_name']](**tool_details['tool_args']).run()

                        if asyncio.iscoroutine(tool_output):

                            tool_output = asyncio.run(tool_output) 

                    else:

                        output = self.tool_objects[tool_details['tool_name']](**tool_details['tool_args']).run()

                        if asyncio.iscoroutine(output):

                            tool_output,context_variables = asyncio.run(output) 

                        else:

                            tool_output,context_variables = output 

                    if self.verbose:

                        print_colored(f"{tool_details['tool_name']} Output : {tool_output}","blue")

                    if UI:

                        # chat_messages2.remove()

                        elements.append(cl.Text(name=f"🛠️{tool_details['tool_name']} Output:",content=str(tool_output),display="inline"))

                        chat_messages2 = asyncio.run(cl.Message(content="",author=self.agent_name,elements=elements).send())

                    tool_content=f"Output From {tool_details['tool_name']} Tool: {str(tool_output)}"

                except Exception as e:

                    if self.verbose:
                    
                        print_colored("Error Tool: "+str(e),"red")

                    tool_content = "Error while executing tool. Please check the tool name or provide a valid arguments to the tool: "+str(e)

        else:

            tool_content = "There is no such tool available. Here are the available tools: " + str(self.tool_names)

        messages.append({"role":"assistant","content":assistant_content.strip()})
        messages.append({"role":"user","content":tool_content.strip()})

        self.messages = messages

        return messages,context_variables
            
    def run(self,user_input=None,messages=[],UI=False,context_variables={}):

        if self.attempts_made<=self.max_allowed_attempts:

            if self.verbose:
            
                print_colored(f"Attempt Number : {self.attempts_made}/{self.max_allowed_attempts}","pink")

            self.attempts_made+=1

            messages = asyncio.run(self.process_memory(messages))

            if user_input:

                messages = self.prepare_messages(user_input,role="user",messages=messages)

            tool_details,token_usage = self.model.get_output(messages,agent_response_format=self.agent_response_format)

            self.messages = messages

            self.input_tokens=token_usage['input_tokens']
            self.output_tokens=token_usage['output_tokens']

            tool_name = tool_details.get('tool_name','')

            # print("Tool Details : \n\n",tool_details)

            if not isinstance(tool_details,dict):
        
                agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

                return Agentoutput(agent_name=self.agent_name,response="I am not able to process your request",messages=messages,assistant_agents=agent_data,context_variables=context_variables)

            # tool_details = json.loads(tool_details)

            if tool_name in self.return_tool_output:

                thoughts = tool_details.get('thoughts','')

                if isinstance(thoughts,list):

                    thoughts = '\n'.join(thoughts)

                messages.append({"role":"assistant","content":str(tool_details)})

                agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

                return ToolOutput(agent_name=self.agent_name,response=thoughts,messages=messages,assistant_agents=agent_data,tool_name=tool_details['tool_name'],tool_args=tool_details['tool_args'],context_variables=context_variables)

            if tool_name=='FinalAnswer':

                if self.verbose:
                
                    thoughts = tool_details.get('thoughts','')

                    if isinstance(thoughts,list):

                        thoughts = '\n'.join(thoughts)

                    print_colored(f"Thoughts: {thoughts}","magenta")

                    print_colored(f"{self.agent_name} : {tool_details['tool_args']['final_answer']}","green")

                messages.append({"role":"assistant","content":tool_details['tool_args']['final_answer']})

                self.attempts_made = 0

                agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

                print("context_variables: ",context_variables)

                return Agentoutput(agent_name=self.agent_name,response=tool_details['tool_args']['final_answer'],messages=messages,assistant_agents=agent_data,context_variables=context_variables)
            
            else:

                if self.verbose:
                
                    thoughts = tool_details.get('thoughts','')

                    if isinstance(thoughts,list):

                        thoughts = '\n'.join(thoughts)
                
                    print_colored(f"Thoughts: {thoughts}","magenta")

                messages,context_variables = self.execute_tool(messages,tool_details,UI=UI,context_variables=context_variables)

                self.messages = messages

                return self.run(messages=messages,context_variables=context_variables)

        else:
            if self.verbose:
            
                print_colored(f"{self.agent_name} : Sorry! Max Attempt Exceeded, I can't take anymore tasks: {self.attempts_made}","red")
            
            agent_data = [AssistantData(agent_name=assistant.agent_name,messages=assistant.messages) for assistant in self.assistant_agents]

            return Agentoutput(agent_name=self.agent_name,response="Sorry! Max Attempt Exceeded, I can't take anymore tasks",messages=messages,assistant_agents=agent_data,context_variables=context_variables)

