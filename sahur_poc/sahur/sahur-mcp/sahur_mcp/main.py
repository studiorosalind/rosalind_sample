from fastapi import FastAPI
from .dummy_github import get_github_file

app = FastAPI()

@app.get("/github/file")
async def github_file(filename: str):
    return get_github_file(filename)
