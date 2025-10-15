from fastapi import FastAPI, File, UploadFile, Form, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from google import generativeai as genai
from PIL import Image
import io, os
from dotenv import load_dotenv

from SSE.stream import GeminiChatStream


"middleware"
import csv
import time
from datetime import datetime,timezone
from uuid import uuid4
from typing import Callable, Awaitable


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use a current multimodal model
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

@app.post("/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form("Describe this image")
):
    try:
        img_bytes = await file.read()
        image = Image.open(io.BytesIO(img_bytes))

        response = model.generate_content([prompt, image])
        return JSONResponse({"result": response.text})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
# @app.post("generate/text")
# async def serve_text_to_text_controller(
#     request : Request,
#     body : str,
#     url_content: str = Depends
# )
@app.get("/generate/text/stream")
async def serve_text_to_text_stream_controller(
    prompt : str
):
    return StreamingResponse(
        GeminiChatStream().chat_stream(prompt),media_type="text/event-stream"
    )



csv_header = ["Request ID", "Datetime", "Endpoint Triggered", "Client IP Address",
"Response Time", "Status Code", "Successful"]
@app.middleware("http")
async def monitor_service(req : Request, call_next : Callable[[Request], Awaitable[Response]]) -> Response:
    request_id = uuid4().hex
    request_datetime = datetime.now(timezone.utc).isoformat()
    start_time = time.perf_counter()
    response : Response = await call_next(req)
    response_time = round(time.perf_counter() - start_time, 4)
    response.headers["X_Response-Time"] = str(response_time)
    response.headers["X-API-Request-id"] = request_id

    with open("usage.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(csv_header)
        writer.writerow(
            [
                request_id,
                request_datetime,
                req.url,
                req.client.host,
                response_time,
                response.status_code,
                response.status_code< 400
            ]
        )
    return response
