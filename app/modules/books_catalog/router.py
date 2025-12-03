from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import BookOut, BookCreate, AddBookOut
from app.core.sessionmaker_fastapi import db_sessions
from .service import BookService


router = APIRouter()


@router.post("/", response_model=AddBookOut)
async def add_book(
    payload: BookCreate,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = BookService(session)    
    book = await svc.add_book(payload)
    return AddBookOut(success=True, book_id=book.id)


@router.get("/", response_model=list[BookOut])
async def get_books(
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = BookService(session)
    books = await svc.list_books()
    return books


@router.get("/{book_id}", response_model=BookOut)
async def get_book(
    book_id: int,
    session: AsyncSession = Depends(db_sessions.get_db_with_commit),
):
    svc = BookService(session)
    book = await svc.get_book(book_id)
    return book