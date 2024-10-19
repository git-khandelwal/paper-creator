import motor.motor_asyncio
from bson import ObjectId
 
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.sample_papers_db

papers_collection = db.get_collection('papers')

async def fetch_paper(paper_id: str):
    paper = await papers_collection.find_one({"_id": ObjectId(paper_id)})
    if paper:
        paper['_id'] = str(paper['_id'])  # Convert ObjectId to string for JSON serialization
    return paper

async def create_paper(paper: dict):
    result = await papers_collection.insert_one(paper)
    return result.inserted_id

async def update_paper(paper_id: str, paper_data: dict):
    result = await papers_collection.update_one({"_id": ObjectId(paper_id)}, {"$set": paper_data})
    return result.modified_count

async def delete_paper(paper_id: str):
    result = await papers_collection.delete_one({"_id": ObjectId(paper_id)})
    return result.deleted_count
