import os
import subprocess
import tempfile
import logging
from PIL import Image

logger = logging.getLogger(__name__)

class SimpleOCRProcessor:
    def __init__(self):
        """
        Simple, reliable OCR processor using ImageMagick + Tesseract
        """
        # Verify ImageMagick is available
        try:
            result = subprocess.run(['magick', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("ImageMagick command failed")
            logger.info("ImageMagick is available")
        except Exception as e:
            raise Exception(f"ImageMagick not available: {e}")
        
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
        Extract text from PDF using ImageMagick + Tesseract method
        """
        logger.info(f"Processing PDF: {pdf_path}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert PDF to images using ImageMagick (process in smaller batches)
                logger.info("Converting PDF to images...")
                image_pattern = os.path.join(temp_dir, "page_%03d.png")
                
                # Convert with the exact same method that worked in terminal
                subprocess.run([
                    'magick',
                    pdf_path,
                    image_pattern
                ], check=True, capture_output=True)
                
                # Find all generated images
                image_files = sorted([f for f in os.listdir(temp_dir) if f.endswith('.png')])
                logger.info(f"Generated {len(image_files)} images")
                
                # Extract text from each image
                all_text = []
                for i, image_file in enumerate(image_files):
                    try:
                        image_path = os.path.join(temp_dir, image_file)
                        text_file = os.path.join(temp_dir, f"page_{i:03d}_text")
                        
                        logger.info(f"Processing page {i+1}/{len(image_files)}")
                        
                        # Run Tesseract with optimized settings
                        subprocess.run([
                            'tesseract', image_path, text_file,
                            '--oem', '3',     # Use LSTM OCR Engine Mode
                            '--psm', '6',     # Assume uniform block of text
                            '-l', 'eng'       # English language
                        ], check=True, capture_output=True)
                        
                        # Read extracted text
                        with open(f"{text_file}.txt", 'r', encoding='utf-8') as f:
                            page_text = f.read().strip()
                        
                        if page_text:
                            all_text.append(f"--- Page {i + 1} ---\n{page_text}\n")
                        
                    except Exception as e:
                        logger.warning(f"Failed to process page {i+1}: {e}")
                        continue
                
                result_text = "\n".join(all_text)
                logger.info(f"Extracted {len(result_text)} characters total")
                return result_text
                
            except subprocess.CalledProcessError as e:
                logger.error(f"Command failed: {e}")
                raise Exception(f"OCR processing failed: {e}")
            except Exception as e:
                logger.error(f"OCR processing error: {e}")
                raise Exception(f"OCR processing failed: {e}")
    
    def extract_text_from_images(self, images):
        """
        Extract text from a list of PIL images
        """
        all_text = []
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, image in enumerate(images):
                try:
                    # Save image temporarily
                    image_path = os.path.join(temp_dir, f"page_{i:03d}.png")
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(image_path, 'PNG')
                    
                    # Extract text directly with Tesseract (no preprocessing)
                    text_file = os.path.join(temp_dir, f"page_{i:03d}_text")
                    subprocess.run([
                        'tesseract', image_path, text_file,
                        '--oem', '3', '--psm', '6', '-l', 'eng'
                    ], check=True, capture_output=True)
                    
                    # Read text
                    with open(f"{text_file}.txt", 'r', encoding='utf-8') as f:
                        page_text = f.read().strip()
                    
                    if page_text:
                        all_text.append(f"--- Page {i + 1} ---\n{page_text}\n")
                        
                except Exception as e:
                    logger.warning(f"Failed to process image {i+1}: {e}")
                    continue
        
        return "\n".join(all_text)
    
    def validate_setup(self):
        """
        Validate that the OCR system is working
        """
        try:
            # Test ImageMagick
            subprocess.run(['magick', '--version'], capture_output=True, check=True)
            
            # Test Tesseract  
            subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
            
            logger.info("Simple OCR processor validated successfully")
            return True
        except Exception as e:
            raise Exception(f"OCR validation failed: {e}")
