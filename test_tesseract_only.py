#!/usr/bin/env python3
"""
Test script to verify Tesseract-only OCR extraction
"""
import os
from tesseract_only_processor import TesseractOnlyProcessor

def test_tesseract_only():
    print("🧪 Testing Tesseract-Only OCR Extraction")
    print("=" * 50)
    
    # Initialize processor
    try:
        ocr_processor = TesseractOnlyProcessor()
        
    except Exception as e:
        print(f"❌ Failed to initialize Tesseract-only processor: {e}")
        return
    
    # Test PDF path
    pdf_path = r"C:\Users\david\Downloads\notes.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    
    try:
        # Extract text from PDF (just first few pages to test)
        print("🔄 Extracting text using Tesseract-Only Processor...")
        
        # For testing, let's process just first 3 pages
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, dpi=200, first_page=1, last_page=3)
        print(f"Processing first 3 pages...")
        
        all_text = []
        for i, image in enumerate(images):
            import tempfile
            import subprocess
            
            # Save image temporarily
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image:
                image.save(temp_image.name, 'PNG')
                temp_image_path = temp_image.name
            
            # Run Tesseract
            with tempfile.NamedTemporaryFile(suffix='', delete=False) as temp_text:
                temp_text_path = temp_text.name
            
            subprocess.run([
                'tesseract', temp_image_path, temp_text_path,
                '--oem', '3', '--psm', '6', '-l', 'eng'
            ], check=True, capture_output=True)
            
            # Read extracted text
            with open(f"{temp_text_path}.txt", 'r', encoding='utf-8') as f:
                page_text = f.read().strip()
            
            if page_text:
                all_text.append(f"--- Page {i + 1} ---\n{page_text}\n")
            
            # Clean up temp files
            os.unlink(temp_image_path)
            os.unlink(f"{temp_text_path}.txt")
        
        extracted_text = "\n".join(all_text)
        
        # Show results
        print("\n" + "=" * 50)
        print("📋 EXTRACTED TEXT (First 3 pages):")
        print("=" * 50)
        print(extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text)
        
        print(f"\n✅ Total extracted text length: {len(extracted_text)} characters")
        
        # Save to file
        output_file = "tesseract_only_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        print(f"✅ Full text saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error during OCR processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tesseract_only()
