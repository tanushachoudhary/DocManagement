# OCR (Optical Character Recognition) service module
# Handles text extraction from images and PDF documents using Tesseract OCR

import pytesseract
# Tesseract wrapper: performs OCR to extract text from images
from pdf2image import convert_from_path
# Converts PDF files into image objects (one per page)
from PIL import Image
# Python Imaging Library: opens and manipulates image files
import os
# Standard library: used for file path operations and validation

def extract_text(file_path: str) -> str:
    """
    Main entry point for text extraction - routes to appropriate handler based on file type.
    Args:
        file_path (str): Absolute or relative path to the document file 
    Returns:
        str: Extracted text content from the document
    Raises:
        ValueError: If file_path is empty or None
        FileNotFoundError: If file does not exist
        
    Supported formats: PDF, PNG, JPG, JPEG, BMP, GIF
    """
    # Input validation
    if not file_path:
        raise ValueError("file_path cannot be empty or None")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Route to appropriate extraction method based on file extension
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)  
    return extract_text_from_image(file_path)

def extract_text_from_image(path: str) -> str:
    """
    Extracts text from image files using Tesseract OCR.
    Args:
        path (str): Absolute or relative path to image file
    Returns:
        str: Extracted text content from the image
    Raises:
        FileNotFoundError: If image file does not exist
        ValueError: If path is empty
        Exception: If OCR processing fails
        
    Supported formats: PNG, JPG, JPEG, BMP, GIF, TIFF
    """
    # Input validation
    if not path:
        raise ValueError("Image path cannot be empty or None")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image file not found: {path}")
    
    try:
        # Open image file using PIL
        image = Image.open(path)
        
        # Extract text using Tesseract OCR
        extracted_text = pytesseract.image_to_string(image)
        
        # Return extracted text (may be empty if no text detected)
        return extracted_text.strip()  # Remove leading/trailing whitespace
        
    except Exception as e:
        raise Exception(f"Error extracting text from image '{path}': {str(e)}")


def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from PDF files by converting pages to images and applying OCR.    
    Args:
        path (str): Absolute or relative path to PDF file       
    Returns:
        str: Concatenated extracted text from all PDF pages       
    Raises:
        FileNotFoundError: If PDF file does not exist
        ValueError: If path is empty or not a valid PDF
        Exception: If PDF conversion or OCR processing fails
        
    Note: Processing time depends on PDF size and page count
    """
    # Input validation
    if not path:
        raise ValueError("PDF path cannot be empty or None")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF file not found: {path}")
    
    if not path.lower().endswith(".pdf"):
        raise ValueError(f"File is not a PDF: {path}")
    
    try:
        # Convert all PDF pages to PIL Image objects
        pages = convert_from_path(path)
        
        if not pages:
            raise ValueError(f"PDF file is empty or cannot be read: {path}")
        
        # Initialize text accumulator
        text = ""
        
        # Process each page sequentially
        for page_num, page in enumerate(pages, 1):
            try:
                # Extract text from current page using OCR
                page_text = pytesseract.image_to_string(page)
                
                # Add page text with page separator
                text += page_text
                
            except Exception as e:
                # Log page-specific error but continue processing
                print(f"Warning: Error processing page {page_num}: {str(e)}")
                continue
        
        # Return combined text from all pages (remove trailing whitespace)
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF '{path}': {str(e)}")