from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_email
from pydantic import BaseModel
from database import save_analysis, get_analyses

class Email(BaseModel):
    sender: str
    subject: str
    body: str

class Analysis(BaseModel):
    id: int
    sender: str
    subject: str
    score: int
    risk: str
    created_at: str | None

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
def analyze(email: Email):
    result = analyze_email(
        email.sender,
        email.subject,
        email.body
    )

    save_analysis(
        email.sender,
        email.subject,
        result["score"],
        result["risk"]
    )

    return result


@app.get("/analyses", response_model=list[Analysis])
def get_history():
    analyses = get_analyses()

    return [
        {
            "id": analysis[0],
            "sender": analysis[1],
            "subject": analysis[2],
            "score": analysis[3],
            "risk": analysis[4],
            "created_at": analysis[5]
        }
        for analysis in analyses
    ]


@app.get("/")
def home():
    return {
        "message": "PhishLens API is running"
    }