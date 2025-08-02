#!/usr/bin/env python3
"""
Setup script for Web Scraper Interface
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_chrome():
    """Check if Chrome browser is available"""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium"
        ]
    elif system == "linux":
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium"
        ]
    elif system == "windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
    else:
        print("⚠️  Unknown operating system")
        return False
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            return True
    
    print("⚠️  Chrome browser not found. Selenium scraping may not work.")
    print("Please install Google Chrome or Chromium browser.")
    return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("📝 Creating .env file...")
        env_content = """# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Model Configuration
MODEL_CACHE_DIR=./models
MAX_TEXT_LENGTH=1000

# Scraping Configuration
REQUEST_TIMEOUT=15
SELENIUM_WAIT_TIME=3

# Optional: Hugging Face API Token (for private models)
# HUGGINGFACE_TOKEN=your_token_here
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_modules = [
        'flask',
        'requests',
        'bs4',
        'transformers',
        'torch',
        'selenium'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All imports successful")
    return True

def main():
    """Main setup function"""
    print("🚀 Web Scraper Interface Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check Chrome
    check_chrome()
    
    # Create .env file
    create_env_file()
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\nTo run the application:")
    print("1. python app.py")
    print("2. Open http://localhost:5000 in your browser")
    print("\nFor enhanced features, use:")
    print("python crawl4ai_app.py")

if __name__ == "__main__":
    main() 