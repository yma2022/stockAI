# Stock Analysis Tool

This project is a web-based stock analysis tool that provides comprehensive insights for any publicly traded company. It fetches real-time stock data, news, financial metrics, and generates AI-powered analysis to help users make informed investment decisions.

![Stock Analysis Tool Screenshot](https://github.com/user-attachments/assets/f82d3809-1193-43d7-bbb8-bd0ab22eff91)


## Features

- **Real-time Stock Data**: Fetches current price, volume, and historical data for the past 20 days
- **Latest News**: Retrieves and summarizes recent news articles about the company
- **Financial Metrics**: Provides key financial indicators and ratios
- **AI-Powered Analysis**: Generates comprehensive analysis with insights on trends and outlook
- **Responsive Web Interface**: Clean, user-friendly interface with proper markdown rendering

## Technology Stack

- **Backend**: Python with Flask web framework
- **Data Source**: Polygon.io API for stock data and financial information
- **AI Analysis**: OpenAI's GPT models via LangChain
- **Frontend**: HTML, CSS, Bootstrap for responsive design
- **Data Processing**: Markdown rendering with proper image handling

## Installation

### Prerequisites

- Python 3.8 or higher
- API keys for:
  - OpenAI
  - Polygon.io

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-analysis-tool.git
   cd stock-analysis-tool
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   POLYGON_API_KEY=your_polygon_api_key
   ```

## Running the Application

1. Start the Flask web server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter a stock ticker (e.g., AAPL, MSFT, GOOGL) and click "Analyze Stock"

## Project Structure
```
root/
├── agent.py # Core logic for fetching and analyzing stock data
├── app.py # Flask web application
├── requirements.txt # Python dependencies
├── templates/ # HTML templates
│ └── index.html # Main web interface
└── .env # Environment variables (not in repo)
```



## How It Works

1. The user enters a stock ticker in the web interface
2. The application fetches data in a step-by-step process:
   - Latest news about the company
   - Stock price data for the last 20 days
   - Financial metrics and indicators
3. The AI agent analyzes all the collected data
4. Results are formatted in Markdown and displayed in the web interface

## Troubleshooting

- **API Rate Limits**: If you encounter errors related to API rate limits, consider implementing caching or reducing the frequency of requests
- **Image Sizing Issues**: The application includes CSS to constrain image sizes, but some news images might still cause layout issues
- **Missing Data**: Some stocks might have limited financial data available through the API

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Polygon.io](https://polygon.io/) for providing stock market data
- [OpenAI](https://openai.com/) for the AI models
- [LangChain](https://langchain.com/) for the AI agent framework
- [Flask](https://flask.palletsprojects.com/) for the web framework
