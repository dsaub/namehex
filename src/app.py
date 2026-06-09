from fastapi import FastAPI
from .routes import user
app = FastAPI()

@app.get("/")
async def root():
    return {
        "status": "ok"
    }

app.include_router(user.router)