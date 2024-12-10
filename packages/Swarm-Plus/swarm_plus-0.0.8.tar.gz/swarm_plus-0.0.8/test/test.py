import os
import asyncio
import nest_asyncio
from SwarmPlus.agent import Agent
from SwarmPlus.models import OpenaiChatModel
from SwarmPlus.tools.FileOperationsTool import SaveFile, CreateFolder
from SwarmPlus.memory import ConversationBufferMemory

nest_asyncio.apply()

# Define OpenAI API key
openai_api_key = "OPENAI_API_KEY"

# Shared tools for file and folder operations
tools = [CreateFolder, SaveFile]

# Memory setup for agents
memory = ConversationBufferMemory()

# Step 1: Define the HR Agent
hr_description = "Responsible for handling HR operations, including manpower and staffing queries."
hr_instruction = """
You are the HR manager. Handle all queries related to manpower, hiring, and employee relations. 
Here are some current HR details you can reference:
- Total Employees: 150
- Current Open Positions: 5 (Software Engineer, Data Analyst, HR Specialist, Marketing Coordinator, and Sales Executive)
- Employee Satisfaction Rating: 4.2/5
- Average Tenure: 3 years
- Recent Hires: John Doe (Software Engineer), Sarah Lee (Data Analyst)
- Current Hiring Goals: 3 additional hires for the Sales team, 2 for the Customer Support team
- Upcoming Initiatives: Employee wellness program, leadership training sessions for middle management

Feel free to provide this information in response to queries from the CEO.
"""


hr_model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
hr_agent = Agent(
    model=hr_model,
    agent_name="HR Agent",
    agent_description=hr_description,
    agent_instructions=hr_instruction,
    tools=tools,
    assistant_agents=[],  # This agent doesn't interact with others in this setup
    max_allowed_attempts=15,
    verbose=True,
    memory=ConversationBufferMemory(),  # Separate memory for HR
)

# Step 3: Define the Sales Agent
sales_description = "Handles all queries and tasks related to sales, including revenue targets and client relations."
sales_instruction = """
You are the Sales manager. Handle all queries related to sales performance, targets, and client relations.
Here are some current Sales details you can reference:
- Monthly Sales Target: $500,000
- Current Month-to-Date Sales: $320,000
- Top Clients: Acme Corp, Globex Industries, Initech, Umbrella Corporation
- Recent Deals Closed: $75,000 with Initech, $45,000 with Globex Industries
- Current Opportunities in Pipeline: 8 (2 in final negotiation, 3 in initial discussions, 3 in proposal review)
- Sales Team Size: 10 members (including 3 senior sales executives, 5 mid-level, 2 junior)
- Quarterly Sales Growth: 8%
- Upcoming Initiatives: New CRM implementation, sales training on advanced negotiation techniques

Feel free to provide this information in response to queries from the CEO.
"""


sales_model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
sales_agent = Agent(
    model=sales_model,
    agent_name="Sales Agent",
    agent_description=sales_description,
    agent_instructions=sales_instruction,
    tools=tools,
    assistant_agents=[],  # This agent doesn't interact with others in this setup
    max_allowed_attempts=15,
    verbose=True,
    memory=ConversationBufferMemory(),  # Separate memory for Sales
)

# Step 1: Define the CEO Agent
ceo_description = "CEO responsible for overseeing company operations and interacting with HR and Sales for strategic decisions."
ceo_instruction = "You are the CEO of the company. Communicate with HR for manpower and staffing queries and with Sales for sales strategies and metrics."

ceo_model = OpenaiChatModel(model_name="gpt-4o-mini", api_key=openai_api_key, temperature=0)
ceo_agent = Agent(
    model=ceo_model,
    agent_name="CEO Agent",
    agent_description=ceo_description,
    agent_instructions=ceo_instruction,
    tools=tools,
    assistant_agents=[hr_agent,sales_agent],  # HR and Sales will be added below
    max_allowed_attempts=15,
    verbose=True,
    memory=memory,
)

async def main():

    messages = []

    user_input = input("User: ")

    while user_input!="bye":

        output = await ceo_agent.arun(user_input,messages=messages)

        messages = output.messages

        user_input = input("User: ")

if __name__ == "__main__":

    asyncio.run(main())



    

