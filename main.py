from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from models import SamplePaper, SamplePaperUpdate
from database import create_paper, fetch_paper, update_paper, delete_paper
from langchain_llm import gemini_extraction
from redis import asyncio as aioredis
import json
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from contextlib import asynccontextmanager

redis_client = None

async def get_redis_client() -> aioredis.Redis:
    global redis_client
    if redis_client is None:
        redis_client = await aioredis.from_url("redis://localhost", decode_responses=True)
    return redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    global redis_client
    redis_client = await get_redis_client()
    await FastAPILimiter.init(redis_client)
    yield
    # Shutdown logic
    if redis_client:
        await redis_client.close()

app = FastAPI(lifespan=lifespan)

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
    cached_paper = await redis_client.get(paper_id)
    if cached_paper:
        return json.loads(cached_paper)
    
    paper = await fetch_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    await redis_client.set(paper_id, json.dumps(paper), ex=60 * 60)
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

# PDF extraction using LangChain and Gemini
@app.post("/extract/pdf", response_model=dict, dependencies=[Depends(RateLimiter(times=2, seconds=60))])
async def extract_pdf(file: UploadFile = File(...)):
    paper_data = await gemini_extraction(file)
    return paper_data
