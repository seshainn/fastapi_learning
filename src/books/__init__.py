from fastapi import FastAPI
from src.books.routes import router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting ...")
    await init_db()
    yield
    print("server is shutting down ...")

version="v1"

app = FastAPI(
    title="Books API", #helps in swagger docs
    description="A REST API for a book review website",
    version=version,
    lifespan=lifespan
)

app.include_router(router, prefix="/api/{version}/books", tags=["books"])
