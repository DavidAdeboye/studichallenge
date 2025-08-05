from paddleocr import PaddleOCR
import pytesseract
import easyocr
import numpy as np
import cv2
import os
import tempfile
import subprocess
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self):
        """
        Initialize multiple OCR engines for better accuracy
        """
        self.engines = {}
        self.available_engines = []
        
        # Initialize PaddleOCR
        try:
            self.engines['paddle'] = PaddleOCR(use_textline_orientation=True, lang='en')
            self.available_engines.append('paddle')
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.warning(f"PaddleOCR initialization failed: {e}")
        
        # Initialize EasyOCR
        try:
            self.engines['easy'] = easyocr.Reader(['en'])
            self.available_engines.append('easy')
            logger.info("EasyOCR initialized successfully")
        except Exception as e:
            logger.warning(f"EasyOCR initialization failed: {e}")
        
        # Check Tesseract availability
        try:
            pytesseract.get_tesseract_version()
            self.available_engines.append('tesseract')
            logger.info("Tesseract is available")
        except Exception as e:
            logger.warning(f"Tesseract not available: {e}")
        
        # Check ImageMagick + Tesseract availability
        try:
            subprocess.run(['magick', '--version'], capture_output=True, check=True)
            self.available_engines.append('imagemagick_tesseract')
            logger.info("ImageMagick + Tesseract is available")
        except Exception as e:
            logger.warning(f"ImageMagick + Tesseract not available: {e}")
        
        if not self.available_engines:
            raise Exception("No OCR engines available! Please install at least one OCR engine.")
        
        logger.info(f"Available OCR engines: {', '.join(self.available_engines)}")
    
    def extract_text_from_images(self, images):
        """
        Extract text from a list of PIL images using multiple OCR engines for better accuracy
        """
        all_text = []
        
        for i, image in enumerate(images):
            try:
                logger.info(f"Processing page {i + 1}/{len(images)}")
                
                # Preprocess image for better OCR
                enhanced_image = self._preprocess_image(image)
                
                # Extract text using multiple engines and combine results
                page_text = self._extract_with_multiple_engines(enhanced_image)
                
                if page_text.strip():
                    all_text.append(f"--- Page {i + 1} ---\n{page_text}\n")
                else:
                    logger.warning(f"No text extracted from page {i + 1}")
                    
            except Exception as e:
                logger.error(f"Error processing image {i + 1}: {str(e)}")
                continue
        
        return "\n".join(all_text)
    
    def extract_text_from_image_file(self, image_path):
        """
        Extract text from a single image file
        """
        try:
            image = Image.open(image_path)
            enhanced_image = self._preprocess_image(image)
            return self._extract_with_multiple_engines(enhanced_image)
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def _preprocess_image(self, image):
        """
        Preprocess image to improve OCR accuracy
        """
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply slight denoising
            image = image.filter(ImageFilter.MedianFilter(size=3))
            
            return image
        except Exception as e:
            logger.warning(f"Image preprocessing failed: {e}")
            return image
    
    def _extract_with_multiple_engines(self, image):
        """
        Extract text using multiple OCR engines and combine results
        """
        results = {}
        
        # Try PaddleOCR
        if 'paddle' in self.available_engines:
            try:
                results['paddle'] = self._extract_with_paddle(image)
            except Exception as e:
                logger.warning(f"PaddleOCR failed: {e}")
        
        # Try EasyOCR
        if 'easy' in self.available_engines:
            try:
                results['easy'] = self._extract_with_easyocr(image)
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}")
        
        # Try Tesseract
        if 'tesseract' in self.available_engines:
            try:
                results['tesseract'] = self._extract_with_tesseract(image)
            except Exception as e:
                logger.warning(f"Tesseract failed: {e}")
        
        # Try ImageMagick + Tesseract
        if 'imagemagick_tesseract' in self.available_engines:
            try:
                results['imagemagick_tesseract'] = self._extract_with_imagemagick_tesseract(image)
            except Exception as e:
                logger.warning(f"ImageMagick + Tesseract failed: {e}")
        
        # Combine results - choose the longest text as it's likely more complete
        if results:
            best_result = max(results.values(), key=len)
            return best_result
        else:
            return ""
    
    def _extract_with_paddle(self, image):
        """
        Extract text using PaddleOCR
        """
        image_array = np.array(image)
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        result = self.engines['paddle'].ocr(image_array, cls=True)
        return self._parse_paddle_result(result)
    
    def _extract_with_easyocr(self, image):
        """
        Extract text using EasyOCR
        """
        image_array = np.array(image)
        result = self.engines['easy'].readtext(image_array)
        
        text_lines = []
        for detection in result:
            if len(detection) >= 2:
                text = detection[1]
                confidence = detection[2] if len(detection) > 2 else 1.0
                if confidence > 0.5:  # Only include high-confidence results
                    text_lines.append(text)
        
        return "\n".join(text_lines)
    
    def _extract_with_tesseract(self, image):
        """
        Extract text using Tesseract directly
        """
        # Configure Tesseract for better accuracy
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz !"#$%&\'()*+,-./:;?<=>?@[\]^_`{|}~'
        text = pytesseract.image_to_string(image, config=custom_config)
        return text.strip()
    
    def _extract_with_imagemagick_tesseract(self, image):
        """
        Extract text using ImageMagick preprocessing + Tesseract
        """
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            try:
                # Save image temporarily
                image.save(temp_file.name, 'PNG')
                
                # Use ImageMagick to preprocess
                processed_file = temp_file.name.replace('.png', '_processed.png')
                subprocess.run([
                    'magick', temp_file.name,
                    '-density', '300',
                    '-quality', '100',
                    '-sharpen', '0x1',
                    '-contrast-stretch', '0.15x0.05%',
                    processed_file
                ], check=True, capture_output=True)
                
                # Run Tesseract on processed image
                text_file = processed_file.replace('.png', '')
                subprocess.run([
                    'tesseract', processed_file, text_file,
                    '--oem', '3', '--psm', '6'
                ], check=True, capture_output=True)
                
                # Read extracted text
                with open(f"{text_file}.txt", 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                
                # Cleanup
                os.unlink(processed_file)
                os.unlink(f"{text_file}.txt")
                
                return text
                
            finally:
                # Cleanup original temp file
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
    
    def _parse_paddle_result(self, result):
        """
        Parse PaddleOCR result and extract text
        """
        if not result or not result[0]:
            return ""
        
        text_lines = []
        for line in result[0]:
            if len(line) >= 2:
                text = line[1][0] if isinstance(line[1], list) else str(line[1])
                confidence = line[1][1] if isinstance(line[1], list) and len(line[1]) > 1 else 1.0
                if confidence > 0.5:  # Only include high-confidence results
                    text_lines.append(text)
        
        return "\n".join(text_lines)
    
    def validate_setup(self):
        """
        Validate that at least one OCR engine is properly set up
        """
        if not self.available_engines:
            raise Exception("No OCR engines available! Please install at least one OCR engine.")
        
        logger.info(f"OCR setup validated. Available engines: {', '.join(self.available_engines)}")
        return True
