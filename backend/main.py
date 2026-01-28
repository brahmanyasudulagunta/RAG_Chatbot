from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import tutor, quiz

app = FastAPI(title="SecureBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tutor.router, prefix="/api/tutor", tags=["Tutor"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])


@app.get("/")
def root():
    return {"message": "SecureBot API is running", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
