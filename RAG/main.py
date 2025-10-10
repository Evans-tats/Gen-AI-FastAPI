from fastapi import FastAPI, HTTPException, status,File, UploadFile, BackgroundTasks, Depends, Body
from typing import Annotated
from loguru import logger
from google import generativeai as genai
from dotenv import load_dotenv
import os

from .upload import save_file
from .extractor import pdf_text_extractor
from .utils_service import vector_service
from .dependencies import get_rag_content
from .schema import RAGContentRequest

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

@app.post("/upload")
async def file_upload_controller(file : Annotated[UploadFile, File(description="upload document")], background_tasks: BackgroundTasks):
    if file.content_type != "application/pdf":
        raise HTTPException(
            detail = f"Only uploading PDF documents are supported",
            status_code=status.HTTP_404_NOT_FOUND
        )
    try:
        filepath = await save_file(file)
        background_tasks.add_task(pdf_text_extractor, filepath=filepath)
        background_tasks.add_task(vector_service.store_file_content_in_db,
                                  filepath.replace(".pdf", ".txt"),
                                  512,
                                  "knowledge_base",
                                  768
                                  )

    except Exception as e:
        raise HTTPException(detail=f"An error occured while saving file - Error : {e}",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
    return {"filename" : file.filename, "message" : "File upload successfully"}


@app.post("/generate/text")
async def serve_text_to_text_controller(
    body : RAGContentRequest = Body(...),
    rag_content: str = Depends(get_rag_content)
):
    prompt = body.prompt  + rag_content
    logger.info("Prompt preview (first 500 chars):\n{}", prompt[:500])
    output = model.generate_content(prompt)
    text_output = output.candidates[0].content.parts[0].text
    return text_output