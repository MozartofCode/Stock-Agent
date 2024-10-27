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
import requests
from newsapi import NewsApiClient
from flask import Flask, request, jsonify
from flask_cors import CORS

# TODO: Add tools for reddit scanner, Power BI API for data visualization, and yahoo finance API for stock data, Math API for calculations

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

news_api_key = os.getenv('NEWS_API_KEY')
newsapi = NewsApiClient(news_api_key)

politician_api_key = os.getenv('POLITICIAN_API_KEY')

app = Flask(__name__)
CORS(app)


def get_latest_news(company):
    top_headlines = newsapi.get_top_headlines(q=company, language='en', country='us')
    return extract_news_data(top_headlines)


def extract_news_data(top_headlines):
    if top_headlines['status'] == 'ok' and top_headlines['totalResults'] > 0:
        news_summary = []
        for article in top_headlines['articles']:
            news_item = article['description']
            news_summary.append(news_item)
        return news_summary
    else:
        return "No news articles available."
    


def get_balance_sheet(company_ticker):

    finance = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company_ticker}?period=annual&apikey={politician_api_key}"

    response = requests.get(finance)
    data = response.json()

    return data


def scan_reddit(company):
    return




@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('question', '')
    
    # Create the agent
    memory = MemorySaver()
    model = ChatOpenAI(model_name="gpt-3.5-turbo")

    prompt_template = PromptTemplate(
        input_variables=["message"],
        template="You are a world-class financial advisor who uses tools to find the best undervalued stocks that are going to make HUGE profits for your clients \
            BASED ON YOUR CLIENTS INTERESTS provide a detailed analysis of 5 good stocks to buy today"
    )

    api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

    tools = [
        Tool(
            func=get_latest_news,
            name="Latest_News",
            description="Gets the latest news of the day about a specific company",
        ),
        # Tool(
        #     func=get_balance_sheet,
        #     name="Balance_Sheet",
        #     description="Gets the balance sheet of a specific company given its ticker symbol but limits the results to 2000 characters",
        # ),

        #wikipedia_tool,
    ]

    agent_executor = create_react_agent(model, tools, checkpointer=memory)
    formatted_prompt = prompt_template.format(message=user_message)

    recommendation = ""

    # Use the agent
    config = {"configurable": {"thread_id": "abc125"}}
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=formatted_prompt)]}, config
    ):
        if "agent" in chunk:
            recommendation = chunk["agent"]["messages"][0].content

    return jsonify({"answer": recommendation})


if __name__ == '__main__':
    app.run(debug=True)