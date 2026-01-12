import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text(file_path: str) -> str:
    """
    Main entry point for text extraction.
    Auto-detects file type (PDF vs Image) and routes to the correct helper function.
    """
    # Check file extension to determine how to process it
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    
    # If not a PDF, we assume it's an image (JPG, PNG, etc.)
    return extract_text_from_image(file_path)

def extract_text_from_image(path: str) -> str:
    """
    Extracts text from a single image file.
    """
    # Load the image into memory using Pillow (PIL)
    image = Image.open(path)
    
    # Tesseract scans the image pixel-by-pixel to identify characters
    return pytesseract.image_to_string(image)
    
def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a scanned PDF.
    Since Tesseract cannot read PDFs directly, we convert pages to images first.
    """
    # Convert PDF pages into a list of PIL Image objects.
    # Requires 'Poppler' installed on the OS.
    pages = convert_from_path(path)
    
    text = ""
    
    # Iterate through every page of the PDF
    for page in pages:
        # Extract text from the current page image and append it to our result
        text += pytesseract.image_to_string(page)
        
    return text