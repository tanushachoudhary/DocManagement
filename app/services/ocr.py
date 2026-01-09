import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text(file_path:str)->str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    return extract_text_from_image(file_path)

def extract_text_from_image(path:str)->str:
    image=Image.open(path)
    return pytesseract.image_to_string(image)
    
def extract_text_from_pdf(path:str)->str:
    pages=convert_from_path(path)
    text=""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text