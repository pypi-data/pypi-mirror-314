# Create output class
from pydantic import BaseModel
from typing import List,Dict,Any

class AssistantData(BaseModel):
    agent_name:str
    messages :list=[]

class ToolOutput(BaseModel):
    agent_name:str
    response:Any=""
    messages:list=[]
    assistant_agents:List[AssistantData]=[]
    tool_name:str
    tool_args : Dict
    context_variables : Dict

class Agentoutput(BaseModel):
    agent_name:str
    response:Any=""
    messages:list=[]
    assistant_agents:List[AssistantData]=[]
    context_variables : Dict


