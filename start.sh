#!/bin/bash

echo "🚀 Starting Web Scraper Interface..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the web_scraper_interface directory."
    exit 1
fi

# Kill any existing processes on port 5002
echo "🔄 Checking for existing processes..."
lsof -ti:5002 | xargs kill -9 2>/dev/null || true

# Start the application
echo "🌟 Starting Flask application on port 5002..."
echo "📱 Web Interface: http://localhost:5002"
echo "🔗 Health Check: http://localhost:5002/api/health"
echo ""
echo "Press Ctrl+C to stop the application"
echo "=================================="

python app.py 