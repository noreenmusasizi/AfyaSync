from fastapi import FastAPI

app = FastAPI(
    title="AfyaSync API",
    description="An offline-first healthcare infrastructure prototype.",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "project": "AfyaSync",
        "status": "running",
        "message": "Welcome to the AfyaSync API",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
