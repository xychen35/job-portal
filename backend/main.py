from fastapi import FastAPI
from core.config import Settings

app = FastAPI(title=Settings.TITLE, version=Settings.VERSION)

@app.get('/')
async def main():
    pass