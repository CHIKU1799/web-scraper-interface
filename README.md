# Web Scraper Interface

A modern, AI-powered web scraping interface that combines web scraping capabilities with Hugging Face LLM models to extract and structure information from websites.

## Features

- 🕷️ **Dual Scraping Methods**: Static content (requests) and dynamic content (Selenium)
- 🤖 **AI-Powered Analysis**: Uses Hugging Face transformers for content summarization and structuring
- 🎨 **Modern UI**: Beautiful, responsive interface with real-time status updates
- 📊 **Structured Output**: AI-generated summaries and organized data extraction
- 💾 **Export Functionality**: Download scraped data as JSON
- 🔄 **Real-time Monitoring**: Health checks and status indicators

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Web Scraping**: BeautifulSoup4, Selenium, Requests
- **AI/ML**: Hugging Face Transformers, PyTorch
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome

## Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium scraping)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd web_scraper_interface
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the interface**
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Basic Scraping

1. Enter a website URL in the input field
2. Choose scraping method:
   - **Static Content**: Faster, for simple websites
   - **Dynamic Content**: Slower, for JavaScript-heavy sites
3. Click "Scrape & Analyze"
4. View the AI-processed results

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

### Exporting Data

Click the "Export" button to download the complete scraped data as a JSON file, including both raw and structured information.

## Configuration

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
REQUEST_TIMEOUT=10
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

## API Endpoints

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

## Troubleshooting

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

### Performance Optimization

- Use static scraping for simple websites
- Limit text length for faster LLM processing
- Consider using smaller models for faster inference

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Hugging Face for the transformer models
- BeautifulSoup for HTML parsing
- Selenium for dynamic content scraping
- Bootstrap for the UI framework 