#!/usr/bin/env python3
"""
Demo script for Web Scraper Interface
Tests the scraping functionality without the web interface
"""

import requests
import json
import time

def test_scraping_api():
    """Test the scraping API endpoint"""
    
    # Test URLs
    test_urls = [
        "https://example.com",
        "https://httpbin.org/html",
        "https://quotes.toscrape.com"
    ]
    
    print("🧪 Testing Web Scraper API")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\n📡 Testing URL: {url}")
        
        try:
            # Test static scraping
            response = requests.post(
                "http://localhost:5002/api/scrape",
                json={
                    "url": url,
                    "method": "requests"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    structured = data['structured_data']
                    print(f"✅ Success!")
                    print(f"   Title: {structured.get('title', 'N/A')}")
                    print(f"   Summary: {structured.get('summary', 'N/A')[:100]}...")
                    print(f"   Word Count: {structured.get('statistics', {}).get('word_count', 0)}")
                    print(f"   Images: {structured.get('statistics', {}).get('images_count', 0)}")
                else:
                    print(f"❌ API returned error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        time.sleep(1)  # Be nice to servers

def test_health_api():
    """Test the health API endpoint"""
    print("\n🏥 Testing Health API")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:5002/api/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status', 'unknown')}")
            print(f"   Models Loaded: {data.get('models_loaded', False)}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def main():
    """Main demo function"""
    print("🚀 Web Scraper Interface Demo")
    print("Make sure the Flask app is running on http://localhost:5002")
    print("=" * 60)
    
    # Test health first
    test_health_api()
    
    # Test scraping
    test_scraping_api()
    
    print("\n" + "=" * 60)
    print("✅ Demo completed!")
    print("\nTo run the full web interface:")
    print("1. python app.py")
    print("2. Open http://localhost:5002 in your browser")

if __name__ == "__main__":
    main() 