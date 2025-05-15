from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.books.routes import book_router
from src.db.main import initdb
version ='v1'


@asynccontextmanager
async def lifespan(app : FastAPI):
    await initdb()
    yield
    print('server is stopping')


app = FastAPI(
    title='Bookly',
    description='A RESTful API for a book review web service',
    version=version,
    lifespan=lifespan

)

# 'postgresql://airflow_user:airflow_pass@postgres:5432/'
app.include_router(book_router,prefix=f"/api/{version}/books",tags=["books"])