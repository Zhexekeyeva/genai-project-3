from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from llm_api import stream_llm
from logger import save_log, get_stats

import time
import json

app = FastAPI()

# Разрешаем фронтенду подключаться
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/ask")
async def ask_llm(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    start_time = time.time()
    full_answer = ""

    async def token_stream():
        nonlocal full_answer

        async for token in stream_llm(prompt):
            full_answer += token
            yield token

        # логируем после завершения стрима
        duration = time.time() - start_time
        save_log(prompt, full_answer, duration)

    return StreamingResponse(token_stream(), media_type="text/plain")


@app.get("/api/logs")
def get_logs():
    try:
        with open("logs.json", "r", encoding="utf-8") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    return JSONResponse(logs)


@app.get("/api/stats")
def stats():
    return JSONResponse(get_stats())