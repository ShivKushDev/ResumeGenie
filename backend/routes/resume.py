from fastapi import APIRouter, UploadFile, HTTPException, File, Form
from typing import Optional
from pydantic import BaseModel
import tempfile
import os

router = APIRouter()

class AnalysisResponse(BaseModel):
    success: bool
    analysis: dict
    message: str

@router.post("/upload", response_model=AnalysisResponse)
async def upload_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None)
):
    """
    Upload and analyze a resume file
    - Accepts PDF files
    - Optionally compare against a job description
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Create a temporary file to store the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Here we'll add the resume analysis logic
        analysis_result = {
            "filename": file.filename,
            "size": len(content),
            "job_match": bool(job_description),
            # Add more analysis fields here
        }
        
        return AnalysisResponse(
            success=True,
            analysis=analysis_result,
            message="Resume successfully analyzed"
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up the temporary file
        if 'temp_path' in locals():
            os.unlink(temp_path)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume_text(
    resume_text: str = Form(...),
    job_description: Optional[str] = Form(None)
):
    """
    Analyze resume text directly
    - Accepts plain text input
    - Optionally compare against a job description
    """
    try:
        analysis_result = {
            "word_count": len(resume_text.split()),
            "char_count": len(resume_text),
            "job_match": bool(job_description),
            # Add more analysis fields here
        }
        
        return AnalysisResponse(
            success=True,
            analysis=analysis_result,
            message="Text successfully analyzed"
        )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
