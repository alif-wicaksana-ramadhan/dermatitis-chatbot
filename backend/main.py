from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import uuid

from rag import rag_pipeline

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    ansewr: str


@app.get("/start-session")
async def start_session():
    session_id = str(uuid.uuid4())
    redis_client.set(session_id, "active", ex=3600)  # Auto-expire in 1 hour
    return {"session_id": session_id}


@app.get("/check-session")
async def check_session(session_id: str):
    if not redis_client.get(session_id):
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return {"message": "Session is active"}


@app.get("/end-session")
async def end_session(session_id: str):
    redis_client.delete(session_id)
    return {"message": "Session terminated successfully"}


@app.post("/submit")
def submit_question(question: Question):
    print("Question: ", question.question)
    result = rag_pipeline.run(
        {
            "query_embedder": {"text": question.question},
            "prompt_builder": {"question": question.question},
        }
    )
    return result
