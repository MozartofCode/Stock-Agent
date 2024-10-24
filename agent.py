# @Author: Bertan Berker
# @Language: Python
#

# Import relevant functionality
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import openai
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate

from tools import get_news

#from langsmith import LangSmith

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create the agent
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-3.5-turbo")


prompt_template = PromptTemplate(
    input_variables=["message"],
    template="You are a financial advisor. A client asks you about what stocks to invest in.\
    Use all the resources necessary to provide the best answer.",
)

tools = [
    Tool(
        func=get_news,
        name="Latest_News",
        description="Gets the latest news from WSJ"
    )
]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

print("Agent created")

user_message = "I want to invest in a tech company. What company do you suggest I invest based on the latest news?"

formatted_prompt = prompt_template.format(message=user_message)

ingredient_response = ""
# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=formatted_prompt)]}, config
):
    print(chunk)
    print("----")
