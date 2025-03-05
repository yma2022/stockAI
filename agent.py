import os
import warnings
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import json

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain import hub

_ = load_dotenv(find_dotenv())
warnings.filterwarnings("ignore")

# Initialize these variables at module level so they're only created once
polygon = None
toolkit = None
tools = None
agent_executor = None

def initialize_agent():
    """Initialize the agent and tools if not already done."""
    global polygon, toolkit, tools, agent_executor
    
    if agent_executor is not None:
        return
    
    ''' Set up Polygon Toolkit '''
    polygon = PolygonAPIWrapper()
    toolkit = PolygonToolkit.from_polygon_api_wrapper(polygon)
    tools = toolkit.get_tools()

    ''' Set up OpenAI agent '''
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    instructions = """You are an assistant pulling stock data and providing analysis. 
    Format your analysis using Markdown for better readability. Use headers, bullet points, 
    and other markdown features to make your analysis clear and well-structured."""
    prompt = base_prompt.partial(instructions=instructions)
    agent = create_openai_functions_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
    )

def pull_stock_data_step_by_step(ticker="AAPL"):
    """Pulls news, technical indicators, and financials step-by-step using the agent."""
    
    # Make sure the agent is initialized
    initialize_agent()
    
    steps_output = []
    
    steps_output.append(f"## Analysis for {ticker}\n")
    
    steps_output.append("### Step 1: Latest News")
    news_data = agent_executor.invoke({"input": f"Get latest news for {ticker}"})
    steps_output.append(news_data.get('output', 'No news data available'))
    
    # Calculate date range for the last 20 days
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
    
    steps_output.append("\n### Step 2: Stock Price Data")
    try:
        # Try using the agent first
        aggregates = agent_executor.invoke({
            "input": f"Get stock aggregates for {ticker} from {start_date} to {end_date}"
        })
        steps_output.append(aggregates.get('output', 'No aggregate data available'))
    except ValueError as e:
        error_str = str(e)
        if "API Error:" in error_str:
            json_str = error_str.split("API Error: ", 1)[1]
            try:
                if "{'ticker':" in json_str and "'results':" in json_str:
                    formatted_data = f"**Price data for {ticker}:**\n\n"
                    formatted_data += "| Date | Open | High | Low | Close | Volume |\n"
                    formatted_data += "|------|------|------|-----|-------|--------|\n"
                    
                    # Use ast.literal_eval which is safer for evaluating Python literals
                    import ast
                    data = ast.literal_eval(json_str)
                    
                    for result in data.get('results', []):
                        date = datetime.fromtimestamp(result['t']/1000).strftime('%Y-%m-%d')
                        formatted_data += f"| {date} | ${result['o']} | ${result['h']} | ${result['l']} | ${result['c']} | {result['v']:,.0f} |\n"
                    
                    steps_output.append(formatted_data)
                    
                    if data.get('results'):
                        results = data.get('results')
                        if len(results) > 1:
                            first_price = results[0]['c']
                            last_price = results[-1]['c']
                            price_change = last_price - first_price
                            percent_change = (price_change / first_price) * 100
                            
                            steps_output.append(f"\n**Price Summary:**")
                            steps_output.append(f"* Starting price: ${first_price}")
                            steps_output.append(f"* Current price: ${last_price}")
                            steps_output.append(f"* Change: ${price_change:.2f} ({percent_change:.2f}%)")

                            if percent_change > 0:
                                trend = "upward"
                            elif percent_change < 0:
                                trend = "downward"
                            else:
                                trend = "flat"
                            steps_output.append(f"* Overall trend: {trend}")
                else:
                    data = json.loads(json_str)

            except Exception as parse_err:
                steps_output.append(f"Could not parse API response. Showing raw data:")
                steps_output.append(f"```\n{json_str}\n```")

                import re

                steps_output.append("\n**Extracted Price Data:**\n")
                steps_output.append("| Date | Open | High | Low | Close | Volume |")
                steps_output.append("|------|------|------|-----|-------|--------|")

                result_pattern = r"{'v': ([\d.]+), 'vw': ([\d.]+), 'o': ([\d.]+), 'c': ([\d.]+), 'h': ([\d.]+), 'l': ([\d.]+), 't': (\d+)"
                matches = re.findall(result_pattern, json_str)
                
                for match in matches:
                    volume, _, open_price, close, high, low, timestamp = match
                    try:
                        date = datetime.fromtimestamp(int(timestamp)/1000).strftime('%Y-%m-%d')
                        steps_output.append(f"| {date} | ${open_price} | ${high} | ${low} | ${close} | {float(volume):,.0f} |")
                    except:
                        steps_output.append(f"| {timestamp} | ${open_price} | ${high} | ${low} | ${close} | {float(volume):,.0f} |")
        else:
            steps_output.append(f"Error fetching aggregates: {e}")
    
    steps_output.append("\n### Step 3: Financial Numbers")
    financial_data = agent_executor.invoke({"input": f"Get financial numbers for {ticker}"})
    steps_output.append(financial_data.get('output', 'No financial data available'))
    analysis_prompt = f"""
    Analyze the following stock data for {ticker} and provide insights:
    
    1. Recent news and their potential impact
    2. Price trends from the aggregate data
    3. Key financial metrics and what they indicate
    4. Overall investment outlook
    
    Format your response using Markdown with clear sections, bullet points for key insights, 
    and a summary conclusion.
    """
    
    steps_output.append("\n### Step 4: Analysis and Conclusions")
    analysis_result = agent_executor.invoke({"input": analysis_prompt})
    steps_output.append(analysis_result.get('output', 'No analysis available'))
    
    return {"output": "\n\n".join(steps_output)}


if __name__ == "__main__":
    stock_analysis = pull_stock_data_step_by_step("MRK")
    print("\nFinal Analysis Result:")
    print(stock_analysis.get('output', 'No analysis available'))
