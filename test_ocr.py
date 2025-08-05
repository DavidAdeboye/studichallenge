#!/usr/bin/env python3
"""
Test script to verify enhanced OCR extraction from the notes.pdf
"""
import os
from ocr_processor import OCRProcessor
from pdf_handler import PDFHandler

def test_ocr_extraction():
    print("🧪 Testing Enhanced OCR Extraction")
    print("=" * 50)
    
    # Initialize processors
    try:
        pdf_handler = PDFHandler()
        ocr_processor = OCRProcessor()
        
        print(f"✅ OCR Engines Available: {', '.join(ocr_processor.available_engines)}")
        print(f"✅ PDF Methods Available: {', '.join(pdf_handler.conversion_methods)}")
        
    except Exception as e:
        print(f"❌ Failed to initialize processors: {e}")
        return
    
    # Test PDF path
    pdf_path = r"C:\Users\david\Downloads\notes.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    
    try:
        # For testing, let's convert only the first few pages using ImageMagick
        print("🔄 Converting first 3 pages using ImageMagick...")
        
        import subprocess
        import tempfile
        from PIL import Image
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert only first 3 pages
            output_pattern = os.path.join(temp_dir, "page_%d.png")
            
            subprocess.run([
                'magick',
                f"{pdf_path}[0-2]",  # Only first 3 pages
                '-density', '200',  # Lower DPI for faster processing
                '-quality', '90',
                '-alpha', 'remove',
                '-colorspace', 'RGB',
                output_pattern
            ], check=True, capture_output=True)
            
            # Load images
            images = []
            for i in range(3):
                page_file = os.path.join(temp_dir, f"page_{i}.png")
                if os.path.exists(page_file):
                    image = Image.open(page_file)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    images.append(image.copy())
            
            print(f"✅ Successfully loaded {len(images)} pages")
            
            # Extract text
            print("🔄 Extracting text using multiple OCR engines...")
            extracted_text = ocr_processor.extract_text_from_images(images)
        
        # Show results
        print("\n" + "=" * 50)
        print("📋 EXTRACTED TEXT (First 3 pages):")
        print("=" * 50)
        print(extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text)
        
        print(f"\n✅ Total extracted text length: {len(extracted_text)} characters")
        
        # Save to file
        output_file = "test_extraction_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        print(f"✅ Full text saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error during OCR processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ocr_extraction()
