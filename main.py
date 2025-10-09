from fastapi import FastAPI
from app.models import *

app = FastAPI(
    title="Namoz Education Backend",
    description="Backend API for Namoz education platform",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Namoz Education API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)