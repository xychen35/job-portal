from fastapi import FastAPI
from core.config import settings
from db.base_class import Base
from db.session import engine
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
# app.mount("/static", StaticFiles(directory="static"), name="static")


Base.metadata.create_all(engine)

@app.get('/')
async def main():
    pass