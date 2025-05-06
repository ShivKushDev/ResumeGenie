from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import resume

app = FastAPI(
    title="ResumeGenie API",
    description="API for analyzing and improving resumes",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["resume"])

@app.get("/")
async def root():
    return {"message": "Welcome to ResumeGenie API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
