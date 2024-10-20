import getpass
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import fitz  # PyMuPDF for PDF Text Extraction
from fastapi import UploadFile, HTTPException
import json

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Provide your Google API Key: ')

async def extract_text_from_pdf(file: UploadFile) -> str:
    text = ""
    data = file.file.read()
    doc = fitz.open(stream=data, filetype="pdf")
    for page in doc:
        text += page.get_text("text")
    return text

def extract_text_from_txt(file: UploadFile) -> str:
    text = file.file.read().decode("utf-8")
    return text

def process_text(text: str, sample_paper: str):
    prompt_template = """
    Extract questions, answers, and other fields from the following text:

    Text: {text}

    Format the output as JSON for a SamplePaper class. Here is the class structure:
    SamplePaper: {sample_paper}
    """
    
    prompt = PromptTemplate(input_variables=["text", "sample_paper"], template=prompt_template)
    llm = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0)
    chain = LLMChain(prompt=prompt, llm=llm)
    result = chain.run(text=text, sample_paper=sample_paper)
    
    return result

sample_paper = """
class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str, should contain at most 5 words
    reference_id: str
    hint: Optional[str] = None
    params: Optional[dict] = {}

class Section(BaseModel):
    marks_per_question: int
    type: str
    questions: List[Question]

class Params(BaseModel):
    board: str, should be one of the following school boards: CBSE, ICSE, IB, NIOS, AISSCE. Check for any of these words in the text. If none are mentioned, then the default value should be CBSE.
    grade: int
    subject: str

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int, should be in minutes
    marks: int
    params: Params
    tags: List[str], the tags should be based the type of questions provided(eg: If a mathematics question is provided, question: What is the differential of sin(x)? Then the tags should be ["Calculus"]). Look for their types in Questions Class.
    chapters: List[str], the chapters should be the Chapter Name(eg: ["Calculus"] for this question: What is the differential of sin(x)?) in a list based on the type of questions provided. Look for their chapters in Questions Class based on Standard 10 or 12 school books.
    sections: List[Section]
    """

async def gemini_extraction(file):
    filename = file.filename
    file_extension = os.path.splitext(filename)[1].lower()
    
    if file_extension == ".pdf":
        extracted_text = await extract_text_from_pdf(file)
    elif file_extension == ".txt":
        extracted_text = extract_text_from_txt(file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    data = process_text(text=extracted_text, sample_paper=sample_paper)
    data = data.replace("```", "").replace("json", "").strip()
    data = json.loads(data)
    return data
