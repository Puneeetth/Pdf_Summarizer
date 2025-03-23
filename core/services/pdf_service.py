import os
import time
import PyPDF2
from io import BytesIO

class PDFService:
    """Service for handling PDF file operations"""
    
    @staticmethod
    def extract_text(pdf_file):
        """
        Extract text content from a PDF file
        
        Args:
            pdf_file: File object or path to PDF
            
        Returns:
            tuple: (extracted_text, processing_time)
        """
        start_time = time.time()
        
        try:
            # Handle both file paths and file objects
            if isinstance(pdf_file, str):
                reader = PyPDF2.PdfFileReader(open(pdf_file, 'rb'))
            else:
                # If it's a Django uploaded file
                file_bytes = BytesIO(pdf_file.read())
                reader = PyPDF2.PdfReader(file_bytes)
            
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n\n"
                
            end_time = time.time()
            processing_time = end_time - start_time
            
            return text.strip(), processing_time
        
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            raise Exception(f"Error extracting text from PDF: {str(e)}")
