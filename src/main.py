from fastapi import FastAPI

from src.routes.book import book_router
from src.routes.token import token_router
from src.routes.user import user_router

app = FastAPI(
    title='BookFlow API',
    version='0.1.0',
)

app.include_router(user_router)
app.include_router(book_router)
app.include_router(token_router)
