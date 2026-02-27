from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from ingest import ingest_pdf
from rag_pipeline import ask_policy

app = FastAPI(title="PolicyAI Backend")


# -------- REQUEST MODEL --------
class QuestionRequest(BaseModel):
    question: str


# -------- UPLOAD PDF --------
@app.post("/upload")
async def upload_policy(file: UploadFile = File(...)):

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_pdf(temp_path)

    os.remove(temp_path)

    return {"message": "Document processed successfully"}
    

# -------- ASK QUESTION --------
@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer, citations = ask_policy(request.question)

    return {
        "answer": answer,
        "citations": citations
    }