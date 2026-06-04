import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, Response
import time
from templates import upload_page_html


@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(cleanup_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


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


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@app.post("/upload/{file_id}")
async def upload_file(file_id: str, file: UploadFile):
    if file_id in file_store:
        raise HTTPException(status_code=409, detail="File already uploaded for this ID")

    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPEG files are accepted")

    data = await file.read()

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 10 MB.")

    file_store[file_id] = FileEntry(
        data=data,
        content_type=file.content_type,
        filename=file.filename or "upload.jpg",
        created_at=time.time(),
    )

    return {"status": "ok"}


@app.get("/file/{file_id}")
async def get_file(file_id: str):
    entry = file_store.pop(file_id, None)
    if entry is None:
        raise HTTPException(status_code=404, detail="File not found")

    return Response(
        content=entry.data,
        media_type=entry.content_type,
        headers={"Content-Disposition": f'attachment; filename="{entry.filename}"'},
    )


TTL_SECONDS = 300  # 5 minutes
CLEANUP_INTERVAL = 30  # seconds


def cleanup_expired():
    """Remove file entries older than TTL_SECONDS."""
    now = time.time()
    expired = [fid for fid, entry in file_store.items() if now - entry.created_at > TTL_SECONDS]
    for fid in expired:
        del file_store[fid]


async def cleanup_loop():
    while True:
        await asyncio.sleep(CLEANUP_INTERVAL)
        cleanup_expired()


@app.get("/{file_id}")
async def mobile_page(file_id: str):
    return HTMLResponse(content=upload_page_html(file_id))
