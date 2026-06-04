from dataclasses import dataclass
from fastapi import FastAPI
import time

app = FastAPI()


@dataclass
class FileEntry:
    data: bytes
    content_type: str
    filename: str
    created_at: float


file_store: dict[str, FileEntry] = {}


@app.get("/status/{file_id}")
async def get_status(file_id: str):
    ready = file_id in file_store
    return {"ready": ready}
