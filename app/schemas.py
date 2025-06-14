from pydantic import BaseModel

class CreateBook(BaseModel):
    name: str
    author: str
    release_year: int
    ISBN: str | None = None
    stock: int

class CreateReader(BaseModel):
    username: str
    email: str

class CreateLibrarian(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str