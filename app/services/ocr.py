import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text(file_path: str) -> str:
    """
    Main entry point for OCR. 
    Determines the file type (PDF or Image) based on the extension 
    and calls the appropriate helper function.
    
    Args:
        file_path (str): The path to the file to be processed.
    
    Returns:
        str: The full extracted text from the file.
    """
    # Check if the file is a PDF
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    
    # If not PDF, assume it is an image (JPG, PNG, etc.)
    return extract_text_from_image(file_path)

def extract_text_from_image(path: str) -> str:
    """
    Extracts text from a single image file using Tesseract OCR.
    """
    # Open the image file using Pillow (PIL)
    image = Image.open(path)
    
    # Run Tesseract OCR on the loaded image object
    # This converts the visual text in the image into a string
    return pytesseract.image_to_string(image)
    
def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a scanned PDF.
    Since Tesseract cannot read PDFs directly, this function:
    1. Converts PDF pages into images.
    2. Runs OCR on each image page.
    """
    # Convert PDF to a list of images (one image per page)
    # Note: This requires 'Poppler' to be installed on your system
    pages = convert_from_path(path)
    
    text = ""
    
    # Loop through each page image
    for page in pages:
        # Extract text from the current page image and append it
        text += pytesseract.image_to_string(page)
        
    return text