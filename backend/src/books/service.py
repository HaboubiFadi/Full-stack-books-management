from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Book
from src.books.schemas import BookCreateModel,BookUpdateModel
from sqlmodel import select,desc
from datetime import datetime

class BookService:
    """
    This class provides methods to create , read , update , and delete books .
    """
    

    async def get_all_books(self , session : AsyncSession):
        """
        Get a list of all books 

        return :
            List : list of books
        
        """
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)

        return result.all()
    
    async def get_book(self,book_uid,session : AsyncSession):
        """Get a book by its UUID.

        Args:
            book_uid (str): the UUID of the book

        Returns:
            Book: the book object
        """
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None
    
    async def create_book(self,book_data: BookCreateModel,session : AsyncSession):
        """
        Add a book  to the books table

        Args :
            BookCreateModel : is the bookmodel injected from the restful api as a body
        
        Returns :
            Book: the new book
        """
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        new_book.published_date = datetime.strptime(book_data_dict['published_date'],"%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        print(new_book)
        
        return new_book
    

    async def update_book(self,book_uid:int,update_data:BookUpdateModel,session : AsyncSession):
        """
        Update a book by using it's Id.
        
        Args :
        book_id:int : the ID of the book we aim to update
        updated_book_data:BookUpdateModel  the data of the new updated book

        return :
            Book : updated book
        
        """

        book_to_update = await self.get_book(book_uid,session)


        if book_to_update is not None:
            update_data_dict = update_data.model_dump()
        
            for key ,value in update_data_dict.items():
                setattr(book_to_update,key,value)
            book_to_update.updated_at=datetime.now()
            await session.commit()
            return book_to_update
        else:
            return None
    

    async def delete_book(self, book_uid:str , session:AsyncSession):
        """Delete a book

        Args:
            book_uid (str): the UUID of the book
        """
        book_to_delete = await self.get_book(book_uid,session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return {}

        else:
            return None
    
    
    