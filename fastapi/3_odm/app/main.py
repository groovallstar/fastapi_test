from ast import keyword
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import mongodb
from app.models.book import BookModel

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR/"templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword="Python", publisher="Public", price=1000, image="python.jpg")
    await mongodb.engine.save(book)
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터"}
    )

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터", "keyword": q}
    )

@app.on_event("startup")
def on_app_start():
    """before app starts"""
    mongodb.connect()

@app.on_event("shutdown")
def on_app_shutdown():
    """after app shutdown"""
    mongodb.close()
