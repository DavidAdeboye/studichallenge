import sys
import os
import subprocess
from dotenv import load_dotenv

def verify_setup():
    print("🔍 Verifying Enhanced Study Buddy setup...\n")
    
    # Load environment variables
    load_dotenv()
    
    success = True
    
    # Check Python packages
    print("📦 Checking Python packages...")
    required_packages = [
        'streamlit',
        'paddlepaddle',
        'paddleocr',
        'opencv-python',
        'numpy',
        'google-generativeai',
        'pdf2image',
        'PIL',
        'python-dotenv',
        'pytesseract',
        'easyocr'
    ]
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'opencv-python':
                import cv2
            elif package == 'python-dotenv':
                import dotenv
            else:
                __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - Not installed")
            success = False
    
    # Check external tools
    print("\n🛠️ Checking external tools...")
    
    # Check Tesseract
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"  ✅ Tesseract (v{version})")
    except Exception as e:
        print(f"  ⚠️ Tesseract - {str(e)}")
        print("    💡 Install from: https://github.com/tesseract-ocr/tesseract")
    
    # Check ImageMagick
    try:
        result = subprocess.run(['magick', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ ImageMagick ({version_line.split()[1]})")
        else:
            raise Exception("Command failed")
    except Exception as e:
        print(f"  ⚠️ ImageMagick - Not available")
        print("    💡 Install from: https://imagemagick.org/")
    
    # Check Ghostscript
    try:
        result = subprocess.run(['gswin64c', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ Ghostscript ({version_line.split()[2]})")
        else:
            raise Exception("Command failed")
    except Exception as e:
        print(f"  ⚠️ Ghostscript - Not available")
        print("    💡 Install from: https://www.ghostscript.com/")
    
    # Check environment variables
    print("\n🔑 Checking environment variables...")
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print("  ✅ GEMINI_API_KEY is set")
    else:
        print("  ❌ GEMINI_API_KEY is not set")
        print("    💡 Get your API key from: https://makersuite.google.com/app/apikey")
        success = False
    
    # Test components
    print("\n🧪 Testing components...")
    
    # Test PDF Handler
    try:
        from pdf_handler import PDFHandler
        pdf = PDFHandler()
        pdf.validate_setup()
        print(f"  ✅ PDF Handler (Methods: {', '.join(pdf.conversion_methods)})")
    except Exception as e:
        print(f"  ❌ PDF Handler - {str(e)}")
        success = False
    
    # Test OCR
    try:
        from ocr_processor import OCRProcessor
        ocr = OCRProcessor()
        ocr.validate_setup()
        print(f"  ✅ OCR Processor (Engines: {', '.join(ocr.available_engines)})")
    except Exception as e:
        print(f"  ❌ OCR Processor - {str(e)}")
        success = False
    
    # Test AI
    try:
        from ai_processor import AIProcessor
        ai = AIProcessor()
        print("  ✅ AI Processor")
    except Exception as e:
        print(f"  ❌ AI Processor - {str(e)}")
        success = False
    
    print("\n" + "="*60)
    if success:
        print("🎉 All components are working correctly!")
        print("📚 Your enhanced Study Buddy is ready to use!")
        print("\n🚀 Run the application with: streamlit run app.py")
    else:
        print("❌ Some components are not working correctly.")
        print("📋 Please install missing dependencies and check your setup.")
        print("\n📖 For installation help, check SETUP_INSTRUCTIONS.md")
    
    return success

if __name__ == "__main__":
    verify_setup()
