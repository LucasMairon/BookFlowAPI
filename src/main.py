from fastapi import FastAPI
from .routes.book import book_router

app = FastAPI()

app.include_router(book_router, prefix='/book', tags=['book'])
