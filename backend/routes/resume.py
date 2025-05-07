from fastapi import APIRouter, UploadFile, HTTPException, File, Form
from typing import Optional
from pydantic import BaseModel
from backend.utils.file_handler import extract_text_from_file

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
    - Accepts PDF and DOCX files
    - Optionally compare against a job description
    """
    try:
        # Extract text from the uploaded file
        resume_text = await extract_text_from_file(file)
        
        # Analyze the extracted text
        analysis_result = await analyze_resume_content(resume_text, job_description)
        
        return AnalysisResponse(
            success=True,
            analysis=analysis_result,
            message="Resume successfully analyzed"
        )
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def analyze_resume_content(resume_text: str, job_description: Optional[str] = None) -> dict:
    """
    Analyze the content of a resume
    """
    analysis = {
        "word_count": len(resume_text.split()),
        "char_count": len(resume_text),
        "sections_found": identify_resume_sections(resume_text),
    }

    if job_description:
        analysis["job_match"] = compare_with_job_description(resume_text, job_description)

    return analysis

def identify_resume_sections(text: str) -> dict:
    """
    Identify common resume sections from the text
    """
    sections = {
        "has_education": any(keyword in text.lower() for keyword in ["education", "degree", "university", "college"]),
        "has_experience": any(keyword in text.lower() for keyword in ["experience", "work", "employment", "job"]),
        "has_skills": any(keyword in text.lower() for keyword in ["skills", "technologies", "tools", "programming"]),
        "has_projects": any(keyword in text.lower() for keyword in ["project", "portfolio", "development"]),
        "has_contact": any(keyword in text.lower() for keyword in ["email", "phone", "contact", "linkedin"])
    }
    return sections

def compare_with_job_description(resume: str, job_desc: str) -> dict:
    """
    Compare resume content with job description
    """
    resume_lower = resume.lower()
    job_desc_lower = job_desc.lower()
    
    # Extract keywords from job description (simple implementation)
    job_words = set(job_desc_lower.split())
    resume_words = set(resume_lower.split())
    
    matching_keywords = job_words.intersection(resume_words)
    
    return {
        "matching_keywords": list(matching_keywords),
        "keyword_match_count": len(matching_keywords),
        "match_percentage": round(len(matching_keywords) / len(job_words) * 100, 2)
    }

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
        analysis_result = await analyze_resume_content(resume_text, job_description)
        return AnalysisResponse(
            success=True,
            analysis=analysis_result,
            message="Text successfully analyzed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
