from fastapi import FastAPI
from core.config import settings
from db.base import Base
from db.session import engine
from fastapi.staticfiles import StaticFiles
from apis.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)
    
def include_router(app):
    app.include_router(api_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app

app = start_application()

@app.get('/')
async def main():
    pass

@app.post('/users')
async def create_user():
    pass

@app.post('/jobs/create-job')
async def create_job():
    pass

@app.get('/jobs/get/{id}')
async def read_job(id):
    pass

@app.get('/jobs/all')
async def read_jobs():
    pass

@app.put('/jobs/update/{id}')
async def update_job(id):
    pass

@app.delete('/jobs/delete/{id}')
async def delete_job(id):
    pass