from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from pathlib import Path

app = FastAPI()

WEBROOT = Path("../webroot").resolve()

app.mount("/", StaticFiles(directory=WEBROOT, html=True), name="static")


@app.middleware("http")
async def check_openpayai(request: Request, call_next):
    rel_path = request.url.path.lstrip("/") or "index.html"
    file_path = (WEBROOT / rel_path).resolve()

    if not str(file_path).startswith(str(WEBROOT)):
        return JSONResponse({"detail": "Forbidden"}, status_code=403)

    dir_path = WEBROOT / rel_path
    if dir_path.exists() and dir_path.is_dir() and not request.url.path.endswith("/"):
        return RedirectResponse(url=request.url.path + "/")

    return await call_next(request)
