from pdf2image import convert_from_path
import tempfile
import os
import subprocess
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class PDFHandler:
    def __init__(self):
        self.conversion_methods = []
        
        # Check pdf2image availability
        try:
            convert_from_path
            self.conversion_methods.append('pdf2image')
            logger.info("pdf2image is available")
        except Exception as e:
            logger.warning(f"pdf2image not available: {e}")
        
        # Check ImageMagick availability
        try:
            subprocess.run(['magick', '--version'], capture_output=True, check=True)
            self.conversion_methods.append('imagemagick')
            logger.info("ImageMagick is available")
        except Exception as e:
            logger.warning(f"ImageMagick not available: {e}")
        
        if not self.conversion_methods:
            raise Exception("No PDF conversion methods available! Please install pdf2image or ImageMagick.")
        
        logger.info(f"Available PDF conversion methods: {', '.join(self.conversion_methods)}")
    
    def convert_pdf_to_images(self, pdf_path):
        """
        Convert PDF pages to images for OCR processing using multiple methods
        """
        # Try pdf2image first (usually faster)
        if 'pdf2image' in self.conversion_methods:
            try:
                logger.info("Converting PDF using pdf2image...")
                images = convert_from_path(pdf_path, dpi=300)
                logger.info(f"Successfully converted {len(images)} pages using pdf2image")
                return images
            except Exception as e:
                logger.warning(f"pdf2image conversion failed: {e}")
        
        # Try ImageMagick as fallback
        if 'imagemagick' in self.conversion_methods:
            try:
                logger.info("Converting PDF using ImageMagick...")
                return self._convert_with_imagemagick(pdf_path)
            except Exception as e:
                logger.error(f"ImageMagick conversion failed: {e}")
        
        raise Exception("All PDF conversion methods failed")
    
    def _convert_with_imagemagick(self, pdf_path):
        """
        Convert PDF to images using ImageMagick
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Convert PDF to images using ImageMagick
            output_pattern = os.path.join(temp_dir, "page_%03d.png")
            
            subprocess.run([
                'magick',
                pdf_path,
                '-density', '300',
                '-quality', '100',
                '-alpha', 'remove',
                '-colorspace', 'RGB',
                output_pattern
            ], check=True, capture_output=True)
            
            # Load images
            images = []
            image_files = sorted([f for f in os.listdir(temp_dir) if f.endswith('.png')])
            
            for image_file in image_files:
                image_path = os.path.join(temp_dir, image_file)
                try:
                    image = Image.open(image_path)
                    # Convert to RGB if necessary
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    images.append(image.copy())  # Copy to avoid issues when temp files are deleted
                except Exception as e:
                    logger.warning(f"Failed to load image {image_file}: {e}")
                    continue
            
            if not images:
                raise Exception("No images were successfully converted")
            
            logger.info(f"Successfully converted {len(images)} pages using ImageMagick")
            return images
    
    def save_images_temporarily(self, images):
        """
        Save images to temporary files and return their paths
        """
        temp_paths = []
        for i, image in enumerate(images):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f'_page_{i}.png')
            image.save(temp_file.name, 'PNG')
            temp_paths.append(temp_file.name)
        return temp_paths
    
    def cleanup_temp_files(self, file_paths):
        """
        Clean up temporary image files
        """
        for file_path in file_paths:
            try:
                os.unlink(file_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file {file_path}: {str(e)}")
    
    def validate_setup(self):
        """
        Validate that at least one PDF conversion method is available
        """
        if not self.conversion_methods:
            raise Exception("No PDF conversion methods available! Please install pdf2image or ImageMagick.")
        
        logger.info(f"PDF handler setup validated. Available methods: {', '.join(self.conversion_methods)}")
        return True
