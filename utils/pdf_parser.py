import pdfplumber
import fitz  # PyMuPDF
from typing import Optional
import io

def extract_text_with_pdfplumber(file_content: bytes) -> str:
    """Extract text from PDF using pdfplumber"""
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error with pdfplumber: {e}")
        return ""

def extract_text_with_pymupdf(file_content: bytes) -> str:
    """Extract text from PDF using PyMuPDF (fallback method)"""
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Error with PyMuPDF: {e}")
        return ""

def parse_pdf(file_content: bytes) -> str:
    """
    Parse PDF and extract text using multiple methods for reliability
    
    Args:
        file_content: PDF file content as bytes
        
    Returns:
        Extracted text from PDF
        
    Raises:
        ValueError: If PDF cannot be parsed or contains no readable text
    """
    # Validate input
    if not file_content or len(file_content) == 0:
        raise ValueError("Empty PDF file provided")
    
    # Try pdfplumber first
    text = extract_text_with_pdfplumber(file_content)
    
    # If pdfplumber fails or returns empty, try PyMuPDF
    if not text or len(text) < 50:
        text = extract_text_with_pymupdf(file_content)
    
    if not text:
        raise ValueError("Could not extract text from PDF. Please ensure the PDF contains readable text.")
    
    return text

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text
    Removes potentially dangerous characters while preserving important formatting
    """
    import re
    
    # Validate input
    if not text or not isinstance(text, str):
        return ""
    
    # Remove null bytes and other control characters
    text = text.replace('\x00', ' ').replace('\r', ' ')
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    # Remove special characters but keep important punctuation
    # Keep: letters, numbers, spaces, periods, commas, hyphens, parentheses
    text = re.sub(r'[^\w\s.,\-()#+/@]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Limit length to prevent DoS (max 1MB of text)
    if len(text) > 1_000_000:
        text = text[:1_000_000]
    
    return text.strip()
