from ast import keyword
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR/"templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터"}
    )

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):

    keyword = q
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 1)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["price"],
            image=book["image"],
        )
        book_models.append(book_model)

    await mongodb.engine.save_all(book_models)
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
