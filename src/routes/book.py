from fastapi import APIRouter
import os
from dotenv import load_dotenv
from ..utils.search_books import get_cleaned_books_list

load_dotenv()

book_router = APIRouter()


@book_router.get('/search')
async def list_books(search_term: str | None = None):
    search_url = f'{os.getenv("BOOK_API_SEARCH_URL")}search.json'

    if search_term is not None:
        clean_search_term = search_term.replace(" ", "+")
        url_params = {
            'q': clean_search_term,
            'fields': '*',
            'lang': 'pt-BR',
        }

    books = get_cleaned_books_list(search_url, url_params)

    return {"listed_books": books}
