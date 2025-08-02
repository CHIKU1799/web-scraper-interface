from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
import requests
from bs4 import BeautifulSoup
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from dotenv import load_dotenv
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variables for LLM model
llm_model = None
tokenizer = None
summarizer = None

def initialize_models():
    """Initialize Hugging Face models"""
    global llm_model, tokenizer, summarizer
    
    print("Loading Hugging Face models...")
    
    # Load a text classification model for content categorization
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    llm_model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    # Load a summarization model
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    print("Models loaded successfully!")

def scrape_with_selenium(url):
    """Scrape website using Selenium for dynamic content"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Get page source
        page_source = driver.page_source
        
        # Extract text content
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        driver.quit()
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else 'No title',
            'text': text,
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'images': [img.get('src') for img in soup.find_all('img', src=True)]
        }
        
    except Exception as e:
        return {'error': str(e)}

def scrape_with_requests(url):
    """Scrape website using requests for static content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else 'No title',
            'text': text,
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'images': [img.get('src') for img in soup.find_all('img', src=True)]
        }
        
    except Exception as e:
        return {'error': str(e)}

def structure_content_with_llm(content):
    """Use Hugging Face LLM to structure the scraped content"""
    try:
        if not content or 'text' not in content:
            return {'error': 'No content to process'}
        
        text = content['text']
        
        # Truncate text if too long for model
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        # Generate summary
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        
        # Structure the content
        structured_data = {
            'url': content.get('url', ''),
            'title': content.get('title', ''),
            'summary': summary[0]['summary_text'],
            'main_content': text[:500] + "..." if len(text) > 500 else text,
            'links_count': len(content.get('links', [])),
            'images_count': len(content.get('images', [])),
            'extracted_links': content.get('links', [])[:10],  # First 10 links
            'extracted_images': content.get('images', [])[:5],  # First 5 images
            'processing_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return structured_data
        
    except Exception as e:
        return {'error': f'LLM processing error: {str(e)}'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        url = data.get('url')
        method = data.get('method', 'requests')  # 'requests' or 'selenium'
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Scrape the website
        if method == 'selenium':
            scraped_data = scrape_with_selenium(url)
        else:
            scraped_data = scrape_with_requests(url)
        
        if 'error' in scraped_data:
            return jsonify(scraped_data), 400
        
        # Structure the content with LLM
        structured_data = structure_content_with_llm(scraped_data)
        
        return jsonify({
            'success': True,
            'raw_data': scraped_data,
            'structured_data': structured_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'models_loaded': llm_model is not None})

if __name__ == '__main__':
    # Initialize models in a separate thread to avoid blocking
    model_thread = threading.Thread(target=initialize_models)
    model_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5002) 