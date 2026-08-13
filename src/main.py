from fastapi import FastAPI
from .routes.book import book_router

app = FastAPI(
    title="BookFlow API",
    version="0.1.0",
)

app.include_router(book_router)
