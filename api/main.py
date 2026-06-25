import uvicorn
from fastapi import FastAPI
from routes import router

app = FastAPI(title="Persona Engine API App Glue", version="1.0.0")

# Mount API components 
app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
