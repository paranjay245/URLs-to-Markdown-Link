from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import urlparse
from test_titles import get_reddit_title, get_other_title

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Add headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def extract_urls(text):
    url_pattern = r'https?://(?:www\.)?(?:reddit\.com|twitter\.com|x\.com|apps\.apple\.com|t3\.chat)[^\s<>"]+|https?://[^\s<>"]+'
    return re.findall(url_pattern, text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_urls():
    text = request.form.get('urls', '')
    urls = extract_urls(text)
    
    results = []
    for url in urls:
        if 'reddit.com' in url:
            title = get_reddit_title(url)
        else:
            title = get_other_title(url)
        results.append({
            'title': title,
            'url': url,
            'markdown': f"- [{title}]({url})"
        })
    
    return jsonify(results)

@app.route('/health', methods=['GET'])
def health_check():
    try:
        logger.info("Health check requested")
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask server...")
        # Listen on all interfaces with a different port
        app.run(host='0.0.0.0', port=5002, debug=True)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise  