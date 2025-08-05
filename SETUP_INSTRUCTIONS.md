# Setup Instructions for Enhanced Study Buddy App

## 🚀 Enhanced OCR Capabilities!

The app now supports **multiple OCR engines** for maximum accuracy:
- **PaddleOCR** (free, runs locally)
- **EasyOCR** (free, deep learning based)
- **Tesseract** (industry standard)
- **ImageMagick + Tesseract** (enhanced preprocessing)

The system automatically uses the best available engine for each document!

### What You Need:
- ✅ Gemini API key (for AI analysis)
- ✅ At least one OCR engine (multiple recommended for best results)
- ✅ ImageMagick + Ghostscript (for advanced PDF processing)

## Setup Steps

### Step 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated API key
4. Add it to your `.env` file:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 2. Update Your .env File

Your complete `.env` file should now look like this (much simpler!):
```
# Gemini API Key (only API key needed now - PaddleOCR is free and runs locally!)
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

## Installation & Running

### Step 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: On first run, PaddleOCR and EasyOCR will automatically download their language models (~200MB total). This is a one-time download.

### Step 4. Install External Tools (Optional but Recommended)

#### Install Tesseract OCR
**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

#### Install ImageMagick
**Windows:**
1. Download from: https://imagemagick.org/script/download.php#windows
2. Install and add to PATH

**macOS:**
```bash
brew install imagemagick
```

**Linux:**
```bash
sudo apt-get install imagemagick
```

#### Install Ghostscript
**Windows:**
1. Download from: https://www.ghostscript.com/download/gsdnld.html
2. Install and add to PATH

**macOS:**
```bash
brew install ghostscript
```

**Linux:**
```bash
sudo apt-get install ghostscript
```

### Step 5. Verify Setup
```bash
python verify_setup_enhanced.py
```

This will show you which OCR engines are available and working.

### Step 6. Run the App
```bash
streamlit run app.py
```

## Benefits of Enhanced OCR System

✅ **Multiple Engines**: Uses the best OCR engine for each document
✅ **Higher Accuracy**: Combines results from multiple engines
✅ **Image Preprocessing**: ImageMagick enhances images before OCR
✅ **Fallback Support**: If one engine fails, others are used
✅ **Free**: All OCR engines are free and open-source
✅ **Privacy**: All processing happens locally on your machine
✅ **Offline**: Works without internet connection

## OCR Engine Comparison

| Engine | Strengths | Best For |
|--------|-----------|----------|
| **PaddleOCR** | Fast, multilingual | General documents |
| **EasyOCR** | Deep learning, good with complex layouts | Handwritten text, complex layouts |
| **Tesseract** | Industry standard, highly configurable | Clean printed text |
| **ImageMagick+Tesseract** | Advanced preprocessing | Poor quality scans |

## Troubleshooting

### Common Issues
- **"No OCR engines available"**: Install at least one OCR engine (PaddleOCR, EasyOCR, or Tesseract)
- **"ImageMagick not found"**: Make sure ImageMagick is installed and added to PATH
- **"Tesseract not found"**: Install Tesseract OCR and add to PATH
- **"Import error"**: Run `pip install -r requirements.txt` to install all dependencies
- **"Gemini API error"**: Check that your API key is valid and has sufficient quota
- **Low OCR accuracy**: Install more OCR engines for better results

### Performance Tips
- **Install all OCR engines** for maximum accuracy
- **Use high-resolution PDFs** (300 DPI or higher) for better OCR results
- **Ensure good lighting** in scanned documents
- **ImageMagick preprocessing** significantly improves results for poor-quality scans
