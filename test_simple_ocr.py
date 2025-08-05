#!/usr/bin/env python3
"""
Test script to verify simple OCR extraction from the notes.pdf
"""
import os
from simple_ocr_processor import SimpleOCRProcessor

def test_simple_ocr_extraction():
    print("🧪 Testing Simple OCR Extraction")
    print("=" * 50)
    
    # Initialize processor
    try:
        ocr_processor = SimpleOCRProcessor()
        
    except Exception as e:
        print(f"❌ Failed to initialize simple OCR processor: {e}")
        return
    
    # Test PDF path
    pdf_path = r"C:\Users\david\Downloads\notes.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return
    
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    
    try:
        # Extract text from PDF
        print("🔄 Extracting text using Simple OCR Processor...")
        extracted_text = ocr_processor.extract_text_from_pdf(pdf_path)
        
        # Show results
        print("\n" + "=" * 50)
        print("📋 EXTRACTED TEXT:")
        print("=" * 50)
        print(extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text)
        
        print(f"\n✅ Total extracted text length: {len(extracted_text)} characters")
        
        # Save to file
        output_file = "simple_extraction_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        
        print(f"✅ Full text saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error during OCR processing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_ocr_extraction()
