
from pydantic import BaseModel
from datetime import date,datetime
import uuid
class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

class BookCreateModel(BaseModel):
    title: str
    author: str 
    publisher: str
    published_date: str
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title : str
    author : str 
    publisher : str
    page_count : int
    language : str
from enum import Enum
class Status(Enum):
    Success = "Success",
    Failed = "Failed" 

class GetBookResondModel(BaseModel):
    Status:Status
    Book:Book

class BookResondModel(BaseModel):
    Status:Status
    bookmodel:Book 