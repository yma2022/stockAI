from flask import Flask, render_template, request, Markup
import markdown
import re
from agent import pull_stock_data_step_by_step

app = Flask(__name__)

def process_markdown_images(html_content):
    """Add max-width styling to all images in the HTML content."""
    # This regex finds img tags and adds a style attribute to limit width
    return re.sub(
        r'<img(.*?)>',
        r'<img\1 style="max-width:100%; height:auto;">',
        html_content
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis_result = None
    ticker = None
    
    if request.method == 'POST':
        ticker = request.form.get('ticker', 'AAPL')
        if ticker:
            result = pull_stock_data_step_by_step(ticker)
            if 'output' in result:
                md_content = result['output']
                html_content = markdown.markdown(md_content, extensions=['tables'])
                html_content = process_markdown_images(html_content)                
                analysis_result = Markup(html_content)
            else:
                analysis_result = "No analysis results found."
    
    return render_template('index.html', analysis_result=analysis_result, ticker=ticker)

if __name__ == '__main__':
    app.run(debug=True) 