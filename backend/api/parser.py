import pdfplumber
import docx
import pytesseract
from PIL import Image

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# Extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


# Extract text from Images
def extract_text_from_image(file):
    try:
        import os
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"OCR Error: Ensure Tesseract is installed correctly. Details: {e}"


# Main function
def extract_resume_text(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    
    elif name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
        
    elif name.endswith((".jpg", ".jpeg", ".png")):
        return extract_text_from_image(uploaded_file)
    
    else:
        return "Unsupported file format"

