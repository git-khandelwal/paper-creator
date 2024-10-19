from fastapi import FastAPI, HTTPException, UploadFile, File
from models import SamplePaper, SamplePaperUpdate
from database import create_paper, fetch_paper, update_paper, delete_paper
from extractor import gemini_extraction

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to PDF Extractor!"}

@app.post("/papers", response_model=dict)
async def create_sample_paper(paper: SamplePaper):
    paper_data = paper.model_dump()
    paper_id = await create_paper(paper_data)
    return {"paper_id": str(paper_id)}

@app.get("/papers/{paper_id}", response_model=dict)
async def get_sample_paper(paper_id: str):
    paper = await fetch_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@app.put("/papers/{paper_id}", response_model=dict)
async def update_sample_paper(paper_id: str, paper_update: SamplePaperUpdate):
    updated_data = paper_update.model_dump(exclude_unset=True)
    modified_count = await update_paper(paper_id, updated_data)
    if not modified_count:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper updated"}

@app.delete("/papers/{paper_id}")
async def delete_sample_paper(paper_id: str):
    deleted_count = await delete_paper(paper_id)
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper deleted"}

# PDF extraction 
@app.post("/extract/pdf", response_model=dict)
async def extract_pdf(file: UploadFile = File(...)):
    paper_data = await gemini_extraction(file)
    return paper_data

