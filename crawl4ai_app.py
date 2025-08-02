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
import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variables for LLM model
llm_model = None
tokenizer = None
summarizer = None
content_classifier = None

def initialize_models():
    """Initialize Hugging Face models"""
    global llm_model, tokenizer, summarizer, content_classifier
    
    print("Loading Hugging Face models...")
    
    try:
        # Load a text classification model for content categorization
        model_name = "distilbert-base-uncased"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        llm_model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Load a summarization model
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Load a text classification model for content type detection
        content_classifier = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")
        
        print("Models loaded successfully!")
    except Exception as e:
        print(f"Error loading models: {e}")

class Crawl4AIScraper:
    """Enhanced web scraper with Crawl4AI-inspired features"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_metadata(self, soup, url):
        """Extract comprehensive metadata from the page"""
        metadata = {
            'title': '',
            'description': '',
            'keywords': '',
            'author': '',
            'language': '',
            'robots': '',
            'og_title': '',
            'og_description': '',
            'og_image': '',
            'twitter_card': '',
            'canonical_url': '',
            'structured_data': []
        }
        
        # Basic meta tags
        if soup.title:
            metadata['title'] = soup.title.string.strip()
        
        meta_tags = {
            'description': 'meta[name="description"]',
            'keywords': 'meta[name="keywords"]',
            'author': 'meta[name="author"]',
            'language': 'meta[http-equiv="content-language"]',
            'robots': 'meta[name="robots"]'
        }
        
        for key, selector in meta_tags.items():
            tag = soup.select_one(selector)
            if tag and tag.get('content'):
                metadata[key] = tag['content'].strip()
        
        # Open Graph tags
        og_tags = {
            'og_title': 'meta[property="og:title"]',
            'og_description': 'meta[property="og:description"]',
            'og_image': 'meta[property="og:image"]'
        }
        
        for key, selector in og_tags.items():
            tag = soup.select_one(selector)
            if tag and tag.get('content'):
                metadata[key] = tag['content'].strip()
        
        # Twitter Card
        twitter_card = soup.select_one('meta[name="twitter:card"]')
        if twitter_card and twitter_card.get('content'):
            metadata['twitter_card'] = twitter_card['content'].strip()
        
        # Canonical URL
        canonical = soup.select_one('link[rel="canonical"]')
        if canonical and canonical.get('href'):
            metadata['canonical_url'] = urljoin(url, canonical['href'])
        
        # Structured data (JSON-LD)
        structured_scripts = soup.find_all('script', type='application/ld+json')
        for script in structured_scripts:
            try:
                data = json.loads(script.string)
                metadata['structured_data'].append(data)
            except:
                continue
        
        return metadata
    
    def extract_content_blocks(self, soup):
        """Extract content blocks with semantic meaning"""
        content_blocks = {
            'headings': [],
            'paragraphs': [],
            'lists': [],
            'tables': [],
            'forms': [],
            'navigation': [],
            'footer': []
        }
        
        # Extract headings
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for heading in headings:
                content_blocks['headings'].append({
                    'level': i,
                    'text': heading.get_text().strip(),
                    'id': heading.get('id', ''),
                    'class': heading.get('class', [])
                })
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if text and len(text) > 10:  # Filter out very short paragraphs
                content_blocks['paragraphs'].append({
                    'text': text,
                    'class': p.get('class', [])
                })
        
        # Extract lists
        lists = soup.find_all(['ul', 'ol'])
        for lst in lists:
            items = [li.get_text().strip() for li in lst.find_all('li')]
            content_blocks['lists'].append({
                'type': lst.name,
                'items': items,
                'class': lst.get('class', [])
            })
        
        # Extract tables
        tables = soup.find_all('table')
        for table in tables:
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text().strip() for td in tr.find_all(['td', 'th'])]
                rows.append(cells)
            content_blocks['tables'].append({
                'rows': rows,
                'class': table.get('class', [])
            })
        
        # Extract forms
        forms = soup.find_all('form')
        for form in forms:
            inputs = []
            for input_tag in form.find_all('input'):
                inputs.append({
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name', ''),
                    'placeholder': input_tag.get('placeholder', '')
                })
            content_blocks['forms'].append({
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'inputs': inputs
            })
        
        # Extract navigation
        nav_elements = soup.find_all(['nav', 'header'])
        for nav in nav_elements:
            links = [a.get('href') for a in nav.find_all('a', href=True)]
            content_blocks['navigation'].append({
                'links': links,
                'class': nav.get('class', [])
            })
        
        # Extract footer
        footer = soup.find('footer')
        if footer:
            content_blocks['footer'] = {
                'text': footer.get_text().strip(),
                'links': [a.get('href') for a in footer.find_all('a', href=True)]
            }
        
        return content_blocks
    
    def extract_media(self, soup, base_url):
        """Extract media elements"""
        media = {
            'images': [],
            'videos': [],
            'audio': [],
            'iframes': []
        }
        
        # Extract images
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if src:
                full_url = urljoin(base_url, src)
                media['images'].append({
                    'src': full_url,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', '')
                })
        
        # Extract videos
        videos = soup.find_all(['video', 'source'])
        for video in videos:
            src = video.get('src', '')
            if src:
                full_url = urljoin(base_url, src)
                media['videos'].append({
                    'src': full_url,
                    'type': video.get('type', ''),
                    'poster': video.get('poster', '')
                })
        
        # Extract audio
        audio_elements = soup.find_all('audio')
        for audio in audio_elements:
            src = audio.get('src', '')
            if src:
                full_url = urljoin(base_url, src)
                media['audio'].append({
                    'src': full_url,
                    'controls': audio.get('controls') is not None
                })
        
        # Extract iframes
        iframes = soup.find_all('iframe')
        for iframe in iframes:
            src = iframe.get('src', '')
            if src:
                full_url = urljoin(base_url, src)
                media['iframes'].append({
                    'src': full_url,
                    'title': iframe.get('title', ''),
                    'width': iframe.get('width', ''),
                    'height': iframe.get('height', '')
                })
        
        return media
    
    def extract_links(self, soup, base_url):
        """Extract and categorize links"""
        links = {
            'internal': [],
            'external': [],
            'social': [],
            'navigation': [],
            'footer': []
        }
        
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text().strip()
            
            if not href or href.startswith('#'):
                continue
            
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            
            # Categorize links
            if parsed_url.netloc == urlparse(base_url).netloc:
                links['internal'].append({
                    'url': full_url,
                    'text': text,
                    'title': link.get('title', '')
                })
            else:
                links['external'].append({
                    'url': full_url,
                    'text': text,
                    'title': link.get('title', '')
                })
            
            # Social media links
            social_patterns = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube']
            if any(pattern in full_url.lower() for pattern in social_patterns):
                links['social'].append({
                    'url': full_url,
                    'text': text,
                    'platform': next((p for p in social_patterns if p in full_url.lower()), 'other')
                })
        
        return links
    
    def scrape_with_requests(self, url):
        """Enhanced scraping using requests"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            
            # Extract comprehensive data
            metadata = self.extract_metadata(soup, url)
            content_blocks = self.extract_content_blocks(soup)
            media = self.extract_media(soup, url)
            links = self.extract_links(soup, url)
            
            # Get clean text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'encoding': response.encoding,
                'metadata': metadata,
                'content_blocks': content_blocks,
                'media': media,
                'links': links,
                'text': clean_text,
                'word_count': len(clean_text.split()),
                'character_count': len(clean_text)
            }
            
        except Exception as e:
            return {'error': str(e)}

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

def structure_content_with_llm(content):
    """Enhanced LLM processing with content classification"""
    try:
        if not content or 'text' not in content:
            return {'error': 'No content to process'}
        
        text = content['text']
        
        # Truncate text if too long for model
        if len(text) > 1000:
            text = content['text'][:1000] + "..."
        
        # Generate summary
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        
        # Classify content sentiment (if classifier is available)
        sentiment = "neutral"
        if content_classifier:
            try:
                sentiment_result = content_classifier(text[:512])  # Limit for classification
                sentiment = sentiment_result[0]['label']
            except:
                pass
        
        # Analyze content structure
        content_analysis = {
            'has_headings': len(content.get('content_blocks', {}).get('headings', [])) > 0,
            'has_lists': len(content.get('content_blocks', {}).get('lists', [])) > 0,
            'has_tables': len(content.get('content_blocks', {}).get('tables', [])) > 0,
            'has_forms': len(content.get('content_blocks', {}).get('forms', [])) > 0,
            'has_images': len(content.get('media', {}).get('images', [])) > 0,
            'has_videos': len(content.get('media', {}).get('videos', [])) > 0
        }
        
        # Structure the content
        structured_data = {
            'url': content.get('url', ''),
            'title': content.get('metadata', {}).get('title', ''),
            'description': content.get('metadata', {}).get('description', ''),
            'summary': summary[0]['summary_text'],
            'sentiment': sentiment,
            'content_analysis': content_analysis,
            'statistics': {
                'word_count': content.get('word_count', 0),
                'character_count': content.get('character_count', 0),
                'headings_count': len(content.get('content_blocks', {}).get('headings', [])),
                'paragraphs_count': len(content.get('content_blocks', {}).get('paragraphs', [])),
                'images_count': len(content.get('media', {}).get('images', [])),
                'internal_links_count': len(content.get('links', {}).get('internal', [])),
                'external_links_count': len(content.get('links', {}).get('external', [])),
                'social_links_count': len(content.get('links', {}).get('social', []))
            },
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
        method = data.get('method', 'requests')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Initialize scraper
        scraper = Crawl4AIScraper()
        
        # Scrape the website
        if method == 'selenium':
            # Fallback to selenium for dynamic content
            scraped_data = scrape_with_selenium(url)
        else:
            scraped_data = scraper.scrape_with_requests(url)
        
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
    
    app.run(debug=True, host='0.0.0.0', port=5000) 