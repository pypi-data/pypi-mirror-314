import os
import inspect
import subprocess
import nest_asyncio
import chainlit as cl
from SwarmPlus.agent import Agent
from SwarmPlus.utils.response_model import Agentoutput

# Ensure that asyncio allows nested loops (important for Jupyter/other environments)
nest_asyncio.apply()

class run_ui_demo:
    def __init__(self, agent: Agent):
        """
        Initializes the UI with the provided agent instance.

        :param agent: The agent instance to be used in the UI.
        :raises ValueError: If the provided agent is not an instance of CollabAgents.agent.Agent.
        """
        
        if not isinstance(agent, Agent):
            raise ValueError(
                "Invalid agent object. The 'agent' parameter must be an instance of 'CollabAgents.agent.Agent'. "
                "Please ensure that you are passing an initialized 'Agent' object from the 'CollabAgents' library. "
                "Example: agent = Agent(...)"
            )
        self.agent = agent
        
        self.setup_chainlit_callbacks()

    def setup_chainlit_callbacks(self):
        """
        Sets up the Chainlit callbacks for chat start, message, and end events.
        """
        @cl.on_chat_start
        async def start_message():
            cl.user_session.set("agent", self.agent)
            cl.user_session.set("messages", [])

        @cl.on_message
        async def on_message(user_input: cl.Message):
            agent = cl.user_session.get("agent")
            messages = cl.user_session.get("messages", [])
            
            # Ensure agent and message session exist to avoid disconnections
            if agent:
                output = agent.run(user_input.content, messages,UI=True)
                if isinstance(output,Agentoutput):
                    cl.user_session.set("messages", output.messages)
                    await cl.Message(output.response,author=output.agent_name).send()
                else:
                    await cl.Message(output).send()

            else:
                await cl.Message("Agent session was disconnected. Please restart the chat.").send()

    def run(self, port=8080):
        """
        Runs the Chainlit UI with the specified port.

        :param port: The port number on which to run the Chainlit app.
        """
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        caller_filename = os.path.basename(caller_file)

        subprocess.run(["chainlit", "run", caller_filename, "--port", str(port)])
