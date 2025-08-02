# 🤖 AI-Powered Web Scraper Interface

A modern, AI-powered web scraping interface that combines web scraping capabilities with Hugging Face LLM models to extract and structure information from websites.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🕷️ **Dual Scraping Methods**: Static content (requests) and dynamic content (Selenium)
- 🤖 **AI-Powered Analysis**: Uses Hugging Face transformers for content summarization and structuring
- 🎨 **Modern UI**: Beautiful, responsive interface with real-time status updates
- 📊 **Structured Output**: AI-generated summaries and organized data extraction
- 💾 **Export Functionality**: Download scraped data as JSON
- 🔄 **Real-time Monitoring**: Health checks and status indicators
- 🚀 **Easy Setup**: Automated setup script and comprehensive documentation

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Web Scraping**: BeautifulSoup4, Selenium, Requests
- **AI/ML**: Hugging Face Transformers, PyTorch
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium scraping)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CHIKU1799/web-scraper-interface.git
   cd web-scraper-interface
   ```

2. **Run the setup script**
   ```bash
   ./setup.py
   ```

3. **Start the application**
   ```bash
   ./start.sh
   ```

4. **Access the interface**
   Open your browser and navigate to `http://localhost:5002`

## 📖 Usage

### Web Interface

1. Enter a website URL in the input field
2. Choose scraping method:
   - **Static Content**: Faster, for simple websites
   - **Dynamic Content**: Slower, for JavaScript-heavy sites
3. Click "Scrape & Analyze"
4. View the AI-processed results

### API Usage

#### Scrape a website
```bash
curl -X POST http://localhost:5002/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "method": "requests"
  }'
```

#### Check health
```bash
curl http://localhost:5002/api/health
```

### Understanding the Results

The interface provides four main sections:

1. **AI Analysis**: 
   - URL and title
   - AI-generated summary
   - Content statistics
   - Processing timestamp

2. **Raw Data**: 
   - Text content preview
   - Content length information

3. **Extracted Links**: 
   - All links found on the page
   - Clickable for easy access

4. **Extracted Images**: 
   - Image URLs found on the page
   - Direct links to images

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Model Configuration
MODEL_CACHE_DIR=./models
MAX_TEXT_LENGTH=1000

# Scraping Configuration
REQUEST_TIMEOUT=15
SELENIUM_WAIT_TIME=3
```

### Customizing Models

You can modify the models used in `app.py`:

```python
# Change the summarization model
summarizer = pipeline("summarization", model="your-preferred-model")

# Change the classification model
model_name = "your-preferred-model"
```

## 📁 Project Structure

```
web_scraper_interface/
├── app.py                 # Main Flask application
├── crawl4ai_app.py        # Enhanced version with advanced features
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
├── start.sh              # Quick start script
├── demo.py               # Demo/testing script
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Web interface template
└── static/
    ├── css/
    │   └── style.css     # Custom styling
    └── js/
        └── app.js        # Frontend functionality
```

## 🧪 Testing

Run the demo script to test the application:

```bash
python demo.py
```

This will test multiple websites and show you the scraping capabilities.

## 🔍 API Endpoints

### POST /api/scrape
Scrape a website and analyze content.

**Request Body:**
```json
{
  "url": "https://example.com",
  "method": "requests"  // or "selenium"
}
```

**Response:**
```json
{
  "success": true,
  "raw_data": { ... },
  "structured_data": { ... }
}
```

### GET /api/health
Check application health and model status.

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Ensure Chrome browser is installed
   - The application automatically downloads the appropriate ChromeDriver

2. **Model Loading Issues**
   - Check internet connection for model downloads
   - Ensure sufficient disk space for model caching

3. **Scraping Failures**
   - Try switching between static and dynamic methods
   - Check if the website blocks automated access
   - Verify the URL is accessible

4. **Port Conflicts**
   - The application runs on port 5002 by default
   - Use `./start.sh` to automatically handle port conflicts

### Performance Optimization

- Use static scraping for simple websites
- Limit text length for faster LLM processing
- Consider using smaller models for faster inference

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the transformer models
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Selenium](https://selenium.dev/) for dynamic content scraping
- [Bootstrap](https://getbootstrap.com/) for the UI framework
- [Font Awesome](https://fontawesome.com/) for the icons

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Open an [Issue](https://github.com/CHIKU1799/web-scraper-interface/issues)
3. Create a [Discussion](https://github.com/CHIKU1799/web-scraper-interface/discussions)

---

⭐ **Star this repository if you find it helpful!** 
