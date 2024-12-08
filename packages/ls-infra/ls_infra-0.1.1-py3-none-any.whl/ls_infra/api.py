from fastapi import FastAPI

app = FastAPI(title="LS Infrastructure API")

@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong"} 