import pypdf 
from fastapi import APIRouter

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

@router.get("/")
async def get_resume():
    return {
        "message": "Resume endpoint working"
    }

@router.post("/upload")
async def upload_resume():
    return {
        "message": "Resume uploaded successfully"
    }

reader = pypdf.PdfReader("resume.pdf")

for page in reader.pages:
    print(page.extract_text())