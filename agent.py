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
from langchain_community.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools.google_search.tool import GoogleSearchResults
import requests


#from langsmith import LangSmith

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
google_api_key = "YGOOGLE_API_KEY"
search_engine_id = "SEARCH_ENGINE_ID"
api_key = "YOUR_NEWSAPI_KEY"
url = f"https://newsapi.org/v2/everything?sources=techcrunch&apiKey={api_key}"



def get_news_WSJ(prompt):
    return "The latest news is Apple is releasing a new iPhone"


def get_news_TechCrunch(prompt):
    return "The latest news is Apple is releasing a new iPhone"



# Create the agent
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-3.5-turbo")


prompt_template = PromptTemplate(
    input_variables=["message"],
    template="You are a financial advisor. A client asks you about what stocks to invest in.\
    Use all the resources necessary to provide the best answer.",
)


# Get latest news with an API call & Wikipedia Integration (Built in tool)
# Google Search API
# API request API (for yahoo api)

# Initialize the Google Search tool with API credentials
google_search_tool = GoogleSearchResults(
    api_key=google_api_key,
    search_engine_id=search_engine_id
)


api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

tools = [
    Tool(
        func=get_news_WSJ,
        name="Latest_News",
        description="Gets the latest news of the day from WSJ, these are any news"
    ),
    
    wikipedia_tool,

    google_search_tool
]

agent_executor = create_react_agent(model, tools, checkpointer=memory)

print("Agent created")

user_message = input("Welcome to Finance Agent. What's your prompt?: ")

formatted_prompt = prompt_template.format(message=user_message)

recommendation = ""

# Use the agent
config = {"configurable": {"thread_id": "abc124"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=formatted_prompt)]}, config
):
    if "agent" in chunk:
        recommendation = chunk["agent"]["messages"][0].content
    
    print(chunk)
    print("----")


print(recommendation)