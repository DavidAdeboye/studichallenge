import os
import subprocess
import tempfile
import logging
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

class TesseractOnlyProcessor:
    def __init__(self):
        """
        Ultra-simple OCR processor using only Tesseract
        """
        # Verify Tesseract is available
        try:
            result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Tesseract command failed")
            logger.info("Tesseract is available")
        except Exception as e:
            raise Exception(f"Tesseract not available: {e}")
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from PDF using pdf2image + Tesseract
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        try:
            # Convert PDF to images using pdf2image (more reliable than ImageMagick in Python)
            logger.info("Converting PDF to images...")
            images = convert_from_path(pdf_path, dpi=200)  # Lower DPI for speed
            logger.info(f"Generated {len(images)} images")
            
            # Extract text from each image
            all_text = []
            for i, image in enumerate(images):
                try:
                    logger.info(f"Processing page {i+1}/{len(images)}")
                    
                    # Save image temporarily
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_image:
                        image.save(temp_image.name, 'PNG')
                        temp_image_path = temp_image.name
                    
                    # Run Tesseract
                    with tempfile.NamedTemporaryFile(suffix='', delete=False) as temp_text:
                        temp_text_path = temp_text.name
                    
                    subprocess.run([
                        'tesseract', temp_image_path, temp_text_path,
                        '--oem', '3',     # Use LSTM OCR Engine Mode
                        '--psm', '6',     # Assume uniform block of text
                        '-l', 'eng'       # English language
                    ], check=True, capture_output=True)
                    
                    # Read extracted text
                    with open(f"{temp_text_path}.txt", 'r', encoding='utf-8') as f:
                        page_text = f.read().strip()
                    
                    if page_text:
                        all_text.append(f"--- Page {i + 1} ---\n{page_text}\n")
                    
                    # Clean up temp files
                    os.unlink(temp_image_path)
                    os.unlink(f"{temp_text_path}.txt")
                    
                except Exception as e:
                    logger.warning(f"Failed to process page {i+1}: {e}")
                    continue
            
            result_text = "\n".join(all_text)
            logger.info(f"Extracted {len(result_text)} characters total")
            return result_text
            
        except Exception as e:
            logger.error(f"OCR processing error: {e}")
            raise Exception(f"OCR processing failed: {e}")
    
    def validate_setup(self):
        """
        Validate that Tesseract is working
        """
        try:
            # Test Tesseract  
            subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
            
            logger.info("Tesseract-only processor validated successfully")
            return True
        except Exception as e:
            raise Exception(f"OCR validation failed: {e}")
