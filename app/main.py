from app.routers import auth, book, reader, borrow
from fastapi import FastAPI



app = FastAPI()


app.include_router(auth.router)
app.include_router(book.router)
app.include_router(reader.router)
app.include_router(borrow.router)