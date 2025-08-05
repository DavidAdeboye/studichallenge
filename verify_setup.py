"""
Verification script to test Google Cloud Vision and Gemini API setup
"""
import os
from dotenv import load_dotenv
import json
from pathlib import Path

def verify_setup():
    print("🔍 Verifying Study Buddy App Setup")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Create a .env file based on .env.example")
        return False
    else:
        print("✅ .env file found")
    
    # PaddleOCR doesn't require credentials - it's free and runs locally!
    print("✅ No OCR credentials needed - PaddleOCR runs locally for free!")
    
    # Check Gemini API key
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key:
        print("❌ GEMINI_API_KEY not set in .env")
        return False
    elif gemini_key == "your_gemini_api_key_here":
        print("❌ GEMINI_API_KEY still contains placeholder value")
        print("   Get your API key from: https://aistudio.google.com/app/apikey")
        return False
    else:
        print("✅ Gemini API key found")
    
    # Test PaddleOCR
    print("\n🧪 Testing PaddleOCR...")
    try:
        from paddleocr import PaddleOCR
        # Test initialization (this will download models on first run)
        ocr = PaddleOCR(use_textline_orientation=True, lang='en')
        print("✅ PaddleOCR initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing PaddleOCR: {e}")
        print("   Make sure you've installed paddlepaddle and paddleocr")
        return False
    
    # Test Gemini API
    print("\n🧪 Testing Gemini API...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Gemini API configured successfully")
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {e}")
        return False
    
    print("\n🎉 All checks passed! Your setup is ready.")
    print("\nYou can now run the app with:")
    print("   streamlit run app.py")
    
    return True

if __name__ == "__main__":
    verify_setup()
