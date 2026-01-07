from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import *
from app.core.database import init_db
from app.api import admin
from app.api import admin_articles
from app.api import articles
from app.api import bot_simple as bot

app = FastAPI(
    title="Namoz Education Backend",
    description="Backend API for Namoz education platform with admin panel",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin.router)
app.include_router(admin_articles.router)
app.include_router(articles.router)
app.include_router(bot.router)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Namoz Education API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)