import pdfplumber
from docx import Document
from fastapi import HTTPException
import tempfile
import os

async def extract_text_from_file(file) -> str:
    """
    Extract text content from PDF or DOCX files
    """
    file_extension = file.filename.lower().split('.')[-1]
    
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        if file_extension == 'pdf':
            return extract_from_pdf(temp_path)
        elif file_extension == 'docx':
            return extract_from_docx(temp_path)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a PDF or DOCX file."
            )
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)

def extract_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF file
    """
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing PDF file: {str(e)}"
        )

def extract_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX file
    """
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text).strip()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing DOCX file: {str(e)}"
        )
