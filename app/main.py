from fastapi import FastAPI
from services.resume import router as resume_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Interview Engine",
    description="Backend API for the AI Interview Engine",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(
    title="AI Interview Engine"
)


@app.get("/")
async def root():
    return {
        "message": "AI Interview Engine API is running!"
    }


app.include_router(resume_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }